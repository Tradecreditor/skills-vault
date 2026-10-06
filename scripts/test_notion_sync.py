#!/usr/bin/env python3
"""Tests for notion-sync.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py' -v

Everything runs against a fake Notion server on 127.0.0.1 (NOTION_API_BASE override); api.notion.com is never contacted.
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent / "notion-sync.py"
spec = importlib.util.spec_from_file_location("notion_sync", SCRIPT)
ns = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ns)

TOKEN = "ntn_SECRETTOKEN123"
DS = "11111111-2222-3333-4444-555555555555"
REPO_URL = "https://github.com/o/r"
TODAY = "2026-10-06"


def table(rows, header="| Workstream | State | Next step | Detail |"):
    lines = ["# handoff", "", "Last updated: 2026-10-05 08:27 UTC by someone.", "", "## In flight", header, "|---|---|---|---|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines + ["", "## Open loops", "| not | a | table |"]) + "\n"


def parse(rows, repo_url=REPO_URL):
    return ns.parse_handoff(table(rows), TODAY, repo_url)[1]


class ParseTests(unittest.TestCase):
    def test_split_row_protects_backtick_pipes_and_escapes(self):
        cells = ns.split_row("| a | `[[../pages/<slug>|…]]` | b \\| c | d |")
        self.assertEqual([c.strip() for c in cells], ["a", "`[[../pages/<slug>|…]]`", "b | c", "d"])
        self.assertEqual(ns.split_row("a | b"), ["a ", " b"])
        self.assertEqual([c.strip() for c in ns.split_row("| a | `open | b |")], ["a", "`open", "b"])  # stray backtick

    def test_clean(self):
        self.assertEqual(ns.clean("**Bold** `code`<br>[txt](http://x) [[a/b|alias]] [[solo]]  __x__"), "Bold code txt alias solo x")

    def test_real_handoff_parses(self):
        path = SCRIPT.parent.parent / "handoff.md"
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(err):
            date, rows = ns.parse_handoff(path.read_text(encoding="utf-8"), TODAY, REPO_URL)
        self.assertEqual((out.getvalue(), err.getvalue()), ("", ""))
        self.assertTrue(rows)
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")
        for r in rows:
            for key in ("project", "status", "owner", "last_update"):
                self.assertTrue(r[key], (key, r))
            self.assertNotIn("**", r["project"])
            self.assertNotIn("`", r["project"])
            self.assertLessEqual(r["last_update"], date)

    def test_status_and_owner_rules(self):
        cases = [  # (state, next, status, owner)
            ("Live", "—", "Done", "Claude Code"),
            ("Live", "none", "Done", "Claude Code"),
            ("Live", "Done: merged", "Done", "Claude Code"),
            ("Live", "Fixed (PR #3)", "Done", "Claude Code"),
            ("Done and merged", "Watch metrics", "Done", "Claude Code"),
            ("Finished", "Watch it", "Done", "Claude Code"),
            ("Done on branch", "Josep: merge it", "Waiting on Josep", "Josep"),
            ("Blocked by CI", "Fix tests", "Blocked", "Claude Code"),
            ("Live", "Blocked: waiting for a key", "Blocked", "Claude Code"),
            ("Not started; due 2026-12-01", "Start it", "Backlog", "Claude Code"),
            ("Live", "Josep merges PR #7", "Waiting on Josep", "Josep"),
            ("Live", "Run the thing", "In progress", "Claude Code"),
            ("Live", "Routine reads it Monday", "In progress", "Routine"),
            ("Live", "Next scheduled run Mon", "In progress", "Routine"),
        ]
        rows = parse([(f"P{i}", s, n, "") for i, (s, n, _, _) in enumerate(cases)])
        self.assertEqual(len(rows), len(cases))
        for r, (s, n, status, owner) in zip(rows, cases):
            self.assertEqual((r["status"], r["owner"]), (status, owner), (s, n))

    def test_done_row_next_step_uses_first_sentence_of_state(self):
        rows = parse([("Gone", "Gone (not seen). Second sentence.", "none", "—"), ("Fixed", "x", "Fixed (PR #1). Later", "")])
        self.assertEqual(rows[0]["next_step"], "Done — Gone (not seen).")
        self.assertEqual(rows[1]["next_step"], "Fixed (PR #1). Later")

    def test_project_trimming(self):
        rows = parse([("Skill review (Josep's ask 2026-10-04: x (nested) y)", "s", "n", ""),
                      ('DEV trigger "x (y)"', "s", "n", ""),
                      ("**Jev pilot 1 —** (H1)", "s", "n", ""),
                      ("Jev pilot 1 — `weekly-hot-list` prefilter (H1, H2)", "s", "n", ""),
                      ("(only parens)", "s", "n", ""),
                      ("Unbalanced (x))", "s", "n", "")])
        self.assertEqual([r["project"] for r in rows], ["Skill review", 'DEV trigger "x (y)"', "Jev pilot 1",
                                                        "Jev pilot 1 — weekly-hot-list prefilter", "(only parens)", "Unbalanced (x))"])

    def test_last_update_ignores_future_dates(self):
        rows = parse([("A", "since 2026-10-01 and 2026-10-03", "plan 2026-12-01", ""),
                      ("B", "only 2026-12-01", "n", ""), ("C", "no date", "n", "2026-13-45"),
                      ("D", "same day 2026-10-05", "n", "")])
        self.assertEqual([r["last_update"] for r in rows], ["2026-10-03", "2026-10-05", "2026-10-05", "2026-10-05"])

    def test_last_updated_falls_back_to_today(self):
        date, _ = ns.parse_handoff("## In flight\n| Workstream |\n|---|\n| A |\n", TODAY, None)
        self.assertEqual(date, TODAY)

    def test_link_resolution(self):
        rows = parse([("url", "s", "n", "see https://example.com/x. and `a/b.md`"),
                      ("path", "s", "n", "`scripts/a.py:12` then `b/c.md`"),
                      ("anchor", "s", "n", "`wiki/x.md#sec`"),
                      ("dir", "s", "n", "`outputs/health/`"),
                      ("skip", "s", "n", "`jev.in_scope.act_min` `two words.md` `[[../p/<s>|x]]` `x.md`"),
                      ("pr", "s", "Josep merges PR #5", "—"),
                      ("fallback", "s", "n", "—")])
        got = {r["project"]: r["link"] for r in rows}
        self.assertEqual(got["url"], "https://example.com/x")
        self.assertEqual(got["path"], REPO_URL + "/blob/main/scripts/a.py")
        self.assertEqual(got["anchor"], REPO_URL + "/blob/main/wiki/x.md")
        self.assertEqual(got["dir"], REPO_URL + "/tree/main/outputs/health/")
        self.assertEqual(got["skip"], REPO_URL + "/blob/main/x.md")
        self.assertEqual(got["pr"], REPO_URL + "/pull/5")
        self.assertEqual(got["fallback"], REPO_URL + "/blob/main/handoff.md")
        self.assertIsNone(parse([("p", "s", "n", "`a/b.md` PR #5")], repo_url=None)[0]["link"])

    def test_link_urls_markdown_balanced_bare_exclusions_and_length(self):
        long_url = "https://example.com/" + "a" * 2000
        rows = parse([("md", "s", "n", "[wiki](https://en.wikipedia.org/wiki/Foo_(bar)) and https://other.example"),
                      ("md2", "s", "n", "[x](https://a.example/p_(q_(r))) tail"),
                      ("br", "s", "n", "https://a.example/x<br>second line"),
                      ("br2", "s", "n", "see<BR />https://b.example/y<br/>"),
                      ("bold", "s", "n", "**https://c.example/z**"),
                      ("quote", "s", "n", 'say "https://d.example/q" or \'https://e.example\''),
                      ("pipe", "s", "n", "https://f.example/a|b"),
                      ("trail", "s", "n", "https://g.example/t_;:"),
                      ("long", "s", "n", long_url + " `scripts/a.py`"),
                      ("long2", "s", "n", long_url + " then https://h.example/ok")])
        got = {r["project"]: r["link"] for r in rows}
        self.assertEqual(got["md"], "https://en.wikipedia.org/wiki/Foo_(bar)")
        self.assertEqual(got["md2"], "https://a.example/p_(q_(r))")
        self.assertEqual(got["br"], "https://a.example/x")
        self.assertEqual(got["br2"], "https://b.example/y")
        self.assertEqual(got["bold"], "https://c.example/z")
        self.assertEqual(got["quote"], "https://d.example/q")
        self.assertEqual(got["pipe"], "https://f.example/a")
        self.assertEqual(got["trail"], "https://g.example/t")
        self.assertEqual(got["long"], REPO_URL + "/blob/main/scripts/a.py")      # over 2000 chars: next rule
        self.assertEqual(got["long2"], "https://h.example/ok")
        self.assertLessEqual(max(len(r["link"]) for r in rows), 2000)

    def test_last_update_ignores_version_dates(self):
        rows = parse([("A", "s", "Notion-Version 2026-03-11 and 2026-10-01", ""), ("B", "v2026-10-04 only", "n", ""),
                      ("C", "version 2026-10-03, VERSION-2026-10-02", "n", ""), ("D", "rev 2026-10-02 fixed", "n", ""),
                      ("E", "Notion-Version 2026-03-11", "none", "")])
        self.assertEqual([r["last_update"] for r in rows], ["2026-10-01", "2026-10-05", "2026-10-05", "2026-10-02", "2026-10-05"])

    def test_title_trim_needs_whitespace_before_the_parenthesis(self):
        rows = parse([("f(x)", "s", "n", ""), ("Tool(v2)", "s", "n", ""), ("Tool (v2)", "s", "n", ""), ("a(b) (c)", "s", "n", "")])
        self.assertEqual([r["project"] for r in rows], ["f(x)", "Tool(v2)", "Tool", "a(b)"])

    def test_duplicates_keep_first(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = parse([("Same", "s", "first", ""), ("Same (again)", "s", "second", "")])
        self.assertEqual([r["next_step"] for r in rows], ["first"])
        self.assertIn("duplicate", err.getvalue())

    def test_missing_columns_and_errors(self):
        rows = parse([("A", "s", "n", "d")])
        self.assertEqual(rows[0]["project"], "A")
        only_ws = ns.parse_handoff("## In flight\n| workstream |\n|---|\n| A |\n", TODAY, None)[1]
        self.assertEqual(only_ws[0]["status"], "Done")      # no Next step column -> empty -> Done
        for text, why in [("# x\n", "no section"), ("## In flight\nnothing\n", "no table"),
                          ("## In flight\n| A | B |\n|---|---|\n| 1 | 2 |\n", "no Workstream")]:
            with self.assertRaises(ns.Stop, msg=why) as cm:
                ns.parse_handoff(text, TODAY, None)
            self.assertEqual(cm.exception.code, 3)


# ---------------------------------------------------------------- fake Notion

def normalise(props):
    out = {}
    for k, v in props.items():
        v = json.loads(json.dumps(v))
        for key in ("title", "rich_text"):
            if key in v:
                v[key] = [dict(x, plain_text=x["text"]["content"]) for x in v[key]]
        out[k] = v
    return out


OPTIONS = {"Status": ["Backlog", "In progress", "Waiting on Josep", "Blocked", "Done"],
           "Owner": ["Josep", "Claude Code", "Routine"], "Area": ["test"], "Source": ["test/handoff.md"]}


class FakeNotion:
    def __init__(self, token=TOKEN, page_size=100, schema=None, options=None):
        self.token, self.page_size, self.inject, self.requests = token, page_size, [], []
        self.pages, self.reject_titles, self.ignore_filter = {}, set(), False
        self.schema = schema or dict(ns.SCHEMA)
        self.options = OPTIONS if options is None else options
        self.databases = {}                 # database id -> [data source ids]
        self.after_commit = []              # (status or None, delay): a create lands, then the answer is lost / delayed
        self.clock = 0
        self.search_results = [{"object": "data_source", "id": DS, "title": [{"plain_text": "Project Status"}]}]
        handler = self._handler()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.server.daemon_threads = True
        self.base = "http://127.0.0.1:%d" % self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def stamp(self):
        self.clock += 1
        return "2026-01-01T%02d:%02d:%02d.000Z" % (self.clock // 3600, self.clock // 60 % 60, self.clock % 60)

    def seed(self, project, source, status="In progress", created=None):
        pid = "page-%d" % (len(self.pages) + 1)
        self.pages[pid] = {"id": pid, "url": "https://www.notion.so/" + pid, "created_time": created or self.stamp(),
                           "properties": normalise({
            "Project": {"title": [{"type": "text", "text": {"content": project}}]}, "Source": {"select": {"name": source}},
            "Status": {"select": {"name": status}}, "Next step": {"rich_text": [{"type": "text", "text": {"content": "manual"}}]}})}
        return pid

    def writes(self):
        return [r for r in self.requests if r[0] in ("POST", "PATCH") and r[1].startswith("/v1/pages")]

    def count(self, method, prefix):
        return len([r for r in self.requests if r[0] == method and r[1].startswith(prefix)])

    @staticmethod
    def matches(page, f):
        if "select" in f:
            return page["properties"][f["property"]]["select"]["name"] == f["select"]["equals"]
        return "".join(x["plain_text"] for x in page["properties"][f["property"]]["title"]) == f["title"]["equals"]

    def route(self, method, path, body):
        if method == "POST" and path == "/v1/search":
            return 200, {"results": self.search_results, "has_more": False}
        if method == "GET" and path == "/v1/data_sources/" + DS:
            return 200, {"object": "data_source", "id": DS, "properties": {
                n: dict({"type": t}, **({"select": {"options": [{"name": o} for o in self.options.get(n, [])]}} if t == "select" else {}))
                for n, t in self.schema.items()}}
        m = re.fullmatch(r"/v1/databases/([^/]+)", path)
        if method == "GET" and m and m.group(1) in self.databases:
            return 200, {"object": "database", "id": m.group(1), "data_sources": [{"id": d, "name": "Project Status"} for d in self.databases[m.group(1)]]}
        if method == "POST" and path == "/v1/data_sources/%s/query" % DS:
            parts = body["filter"].get("and") or [body["filter"]]
            rows = [p for p in self.pages.values() if self.ignore_filter or all(self.matches(p, f) for f in parts)]
            off = int(body.get("start_cursor") or 0)
            more = off + self.page_size < len(rows)
            return 200, {"results": rows[off:off + self.page_size], "has_more": more, "next_cursor": str(off + self.page_size) if more else None}
        if method == "POST" and path == "/v1/pages":
            title = body["properties"]["Project"]["title"][0]["text"]["content"]
            if title in self.reject_titles or body["parent"] != {"type": "data_source_id", "data_source_id": DS}:
                return 400, {"object": "error", "status": 400, "code": "validation_error", "message": "rejected " + title}
            pid = "page-%d" % (len(self.pages) + 1)
            self.pages[pid] = {"id": pid, "url": "https://www.notion.so/" + pid, "created_time": self.stamp(),
                               "properties": normalise(body["properties"])}
            if self.after_commit:
                status, delay = self.after_commit.pop(0)
                time.sleep(delay)
                if status:
                    return status, {"object": "error", "status": status, "code": "lost", "message": "answer lost"}
            return 200, self.pages[pid]
        m = re.fullmatch(r"/v1/pages/([^/]+)", path)
        if method == "PATCH" and m and m.group(1) in self.pages:
            self.pages[m.group(1)]["properties"].update(normalise(body["properties"]))
            return 200, self.pages[m.group(1)]
        return 404, {"object": "error", "status": 404, "code": "object_not_found", "message": "no such thing"}

    def _handler(self):
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def handle_any(self):
                n = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(n)) if n else None
                headers = {k.lower(): v for k, v in self.headers.items()}
                fake.requests.append((self.command, self.path, body, headers))
                for i, (method, prefix, status, extra, obj) in enumerate(fake.inject):
                    if method == self.command and self.path.startswith(prefix):
                        del fake.inject[i]
                        return self.send(status, obj, extra)
                if headers.get("authorization") != "Bearer " + fake.token:
                    sent = headers.get("authorization", "").replace("Bearer ", "")
                    return self.send(401, {"object": "error", "status": 401, "code": "unauthorized",
                                           "message": "API token is invalid: " + sent})
                self.send(*fake.route(self.command, self.path, body))

            def send(self, status, obj, extra=None):
                raw = json.dumps(obj).encode()
                try:
                    self.send_response(status)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(raw)))
                    for k, v in (extra or {}).items():
                        self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(raw)
                except OSError:                     # the client gave up (timeout test)
                    pass
            do_GET = do_POST = do_PATCH = handle_any
        return Handler


ROWS = [("Alpha (first)", "Live", "Run the thing", "`scripts/a.py`"),
        ("Beta", "Waiting", "Josep merges PR #7", "—"),
        ("Gamma", "Not started", "Start it", "`docs/`")]


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.handoff = os.path.join(self.tmp.name, "handoff.md")
        self.fake = FakeNotion()
        self.addCleanup(self.fake.close)
        for name, val in (("MIN_INTERVAL", 0), ("BACKOFF", (0, 0, 0))):
            patcher = mock.patch.object(ns, name, val)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.write(ROWS)

    def write(self, rows):
        Path(self.handoff).write_text(table(rows), encoding="utf-8")

    def sync(self, *extra, env=None, fake=None):
        fake = fake or self.fake
        environ = {k: v for k, v in os.environ.items() if not k.startswith("NOTION_")}
        environ.update({"NOTION_TOKEN": TOKEN, "NOTION_API_BASE": fake.base}, **(env or {}))
        argv = ["--handoff", self.handoff, "--source", "test/handoff.md", "--area", "test", "--repo-url", REPO_URL,
                "--today", TODAY, *extra]
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, environ, clear=True), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ns.main(argv)
        return code, out.getvalue(), err.getvalue()

    def summary(self, out, **counts):
        want = "notion-sync: created={created} updated={updated} closed={closed} unchanged={unchanged} failed={failed} " \
               "source=test/handoff.md data_source=11111111\n".format(**dict(dict(created=0, updated=0, closed=0, unchanged=0, failed=0), **counts))
        self.assertEqual(out, want)

    def test_first_run_creates_then_second_run_is_idempotent(self):
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, created=3)
        self.assertEqual(len(self.fake.pages), 3)
        page = next(p for p in self.fake.pages.values() if p["properties"]["Project"]["title"][0]["plain_text"] == "Beta")
        props = page["properties"]
        self.assertEqual(props["Status"], {"select": {"name": "Waiting on Josep"}})
        self.assertEqual(props["Owner"], {"select": {"name": "Josep"}})
        self.assertEqual(props["Source"], {"select": {"name": "test/handoff.md"}})
        self.assertEqual(props["Area"], {"select": {"name": "test"}})
        self.assertEqual(props["Link"], {"url": REPO_URL + "/pull/7"})
        self.assertEqual(props["Last update"], {"date": {"start": "2026-10-05"}})
        before = len(self.fake.writes())
        self.fake.page_size = 2
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, unchanged=3)
        self.assertEqual(len(self.fake.writes()), before)
        self.assertEqual(self.fake.count("POST", "/v1/data_sources/%s/query" % DS), 3)  # 1 page in run 1, 2 pages in run 2
        self.assertEqual(self.fake.count("POST", "/v1/search"), 2)
        search = next(r for r in self.fake.requests if r[1] == "/v1/search")[2]
        self.assertEqual(search, {"query": "Project Status", "filter": {"property": "object", "value": "data_source"}, "page_size": 100})

    def test_headers_and_no_destructive_fields(self):
        self.sync()
        self.sync("--data-source", DS)
        for _, _, body, headers in self.fake.requests:
            self.assertEqual(headers["authorization"], "Bearer " + TOKEN)
            self.assertEqual(headers["notion-version"], "2026-03-11")
            self.assertEqual(headers["content-type"], "application/json")
            self.assertNotRegex(json.dumps(body), r"archived|in_trash")
        self.assertEqual({m for m, _, _, _ in self.fake.requests}, {"GET", "POST"})
        self.sync(env={"NOTION_VERSION": "2099-01-01"})
        self.assertEqual(self.fake.requests[-1][3]["notion-version"], "2099-01-01")

    def test_edited_next_step_updates_only_that_property(self):
        self.sync()
        self.write([("Alpha (first)", "Live", "Run the other thing", "`scripts/a.py`")] + list(ROWS[1:]))
        before = len(self.fake.writes())
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, updated=1, unchanged=2)
        writes = self.fake.writes()[before:]
        self.assertEqual(len(writes), 1)
        method, path, body, _ = writes[0]
        self.assertEqual(method, "PATCH")
        self.assertEqual(list(body["properties"]), ["Next step"])
        self.assertEqual(body["properties"]["Next step"]["rich_text"][0]["text"]["content"], "Run the other thing")

    def test_long_next_step_is_chunked(self):
        self.write([("Long", "Live", "x" * 4500, "")])
        self.sync()
        body = next(r[2] for r in self.fake.requests if r[1] == "/v1/pages")
        chunks = body["properties"]["Next step"]["rich_text"]
        self.assertEqual([len(c["text"]["content"]) for c in chunks], [1900])  # truncated to 1900 first, then chunked at 2000

    def test_removed_row_is_closed_once_and_manual_rows_untouched(self):
        manual = self.fake.seed("Manual thing", "manual")
        other_same_title = self.fake.seed("Gamma", "someone-else/handoff.md")
        self.sync()
        snapshot = json.dumps({k: self.fake.pages[k] for k in (manual, other_same_title)}, sort_keys=True)
        self.write(ROWS[:2])
        before = len(self.fake.writes())
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, closed=1, unchanged=2)
        (method, path, body, _), = self.fake.writes()[before:]
        gamma = next(k for k, p in self.fake.pages.items() if k not in (manual, other_same_title)
                     and p["properties"]["Project"]["title"][0]["plain_text"] == "Gamma")
        self.assertEqual((method, path), ("PATCH", "/v1/pages/" + gamma))
        self.assertEqual(body["properties"]["Status"], {"select": {"name": "Done"}})
        self.assertEqual(body["properties"]["Next step"]["rich_text"][0]["text"]["content"],
                         "Left test/handoff.md In flight; last seen 2026-10-05.")
        self.assertEqual(body["properties"]["Last update"], {"date": {"start": "2026-10-05"}})
        self.assertEqual(snapshot, json.dumps({k: self.fake.pages[k] for k in (manual, other_same_title)}, sort_keys=True))
        before = len(self.fake.writes())
        code, out, _ = self.sync()                      # already Done: nothing more to do
        self.summary(out, unchanged=2)
        self.assertEqual(len(self.fake.writes()), before)

    def test_server_ignoring_the_source_filter_still_cannot_touch_other_sources(self):
        manual = self.fake.seed("Manual thing", "manual")
        self.fake.ignore_filter = True
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, created=3)
        self.assertNotIn(manual, [r[1].rsplit("/", 1)[1] for r in self.fake.writes() if r[0] == "PATCH"])

    def test_retry_after_429_then_success(self):
        self.fake.inject.append(("POST", "/v1/pages", 429, {"Retry-After": "0"},
                                 {"object": "error", "status": 429, "code": "rate_limited", "message": "slow down"}))
        self.fake.inject.append(("POST", "/v1/pages", 503, {}, {"object": "error", "status": 503, "code": "service_unavailable", "message": "x"}))
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, created=3)
        self.assertEqual(self.fake.count("POST", "/v1/pages"), 5)       # 429 is "not processed": retried without a query
        self.assertEqual(self.fake.count("POST", "/v1/data_sources/%s/query" % DS), 2)   # the 503 triggered one look-up

    def test_partial_failure_exits_1(self):
        self.fake.reject_titles.add("Beta")
        code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.summary(out, created=2, failed=1)
        self.assertIn("FAILED created 'Beta'", err)
        self.assertEqual(self.fake.count("POST", "/v1/pages"), 3)       # a 400 is not retried

    def test_create_gives_up_after_one_retry_and_patch_after_three(self):
        for _ in range(4):
            self.fake.inject.append(("POST", "/v1/pages", 500, {}, {"object": "error", "status": 500, "code": "internal_server_error", "message": "x"}))
        code, out, _ = self.sync()
        self.assertEqual(code, 1)
        self.summary(out, created=1, failed=2)                          # Alpha and Beta: POST, look-up, POST, give up
        self.assertEqual(self.fake.count("POST", "/v1/pages"), 5)
        self.write([("Alpha (first)", "Live", "Changed", "`scripts/a.py`")])
        for _ in range(4):
            self.fake.inject.append(("PATCH", "/v1/pages", 500, {}, {"object": "error", "status": 500, "code": "x", "message": "x"}))
        code, out, _ = self.sync()
        self.assertEqual(code, 1)
        self.assertEqual(self.fake.count("PATCH", "/v1/pages"), 4)      # an idempotent PATCH keeps the 3 retries

    def test_401_is_off_and_never_leaks_the_token(self):
        fake = FakeNotion(token="something-else")
        self.addCleanup(fake.close)
        for extra in ([], ["--json"], ["--dry-run"]):
            code, out, err = self.sync(*extra, fake=fake)
            self.assertEqual(code, 2)
            self.assertNotIn(TOKEN, out + err)
            self.assertIn("401", out)
        self.assertEqual(self.sync(fake=fake)[1].split(" (")[0], "notion-sync: off")
        self.assertEqual(fake.writes(), [])

    def test_missing_or_mistyped_schema_property_is_off(self):
        schema = dict(ns.SCHEMA)
        del schema["Owner"]
        schema["Link"] = "rich_text"
        fake = FakeNotion(schema=schema)
        self.addCleanup(fake.close)
        code, out, _ = self.sync(fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Owner (select)", out)
        self.assertIn("Link (url)", out)
        self.assertEqual(fake.writes(), [])

    def test_data_source_not_found_ambiguous_trashed_and_404(self):
        self.fake.search_results = []
        self.assertEqual(self.sync()[0], 2)
        self.assertIn("not found", self.sync()[1])
        two = self.fake.search_results = [{"object": "data_source", "id": DS, "name": "Project Status"},
                                          {"object": "data_source", "id": "other", "title": [{"plain_text": "Project Status"}]}]
        code, out, _ = self.sync()
        self.assertEqual(code, 2)
        self.assertIn("NOTION_PROJECTS_DS", out)
        two[1]["in_trash"] = True                       # a trashed duplicate does not count
        self.assertEqual(self.sync()[0], 0)
        code, out, _ = self.sync("--data-source", "nope")
        self.assertEqual(code, 2)
        self.assertIn("404", out)
        self.assertEqual(self.sync(env={"NOTION_PROJECTS_DS": DS})[0], 0)   # env id skips the search

    def test_dry_run_with_token_reads_but_never_writes(self):
        self.sync()
        self.fake.requests.clear()
        self.write(ROWS[:2] + [("New", "Live", "Do it", "")])
        code, out, err = self.sync("--dry-run", "--json")
        self.assertEqual(code, 0)
        res = json.loads(out)
        self.assertEqual(res["plan"], {"create": ["New"], "update": [], "close": ["Gamma"], "unchanged": ["Alpha", "Beta"]})
        self.assertEqual(res["counts"]["duplicates"], 0)
        self.assertEqual(res["counts"]["created"], 1)
        self.assertEqual(self.fake.writes(), [])
        code, out, _ = self.sync("--dry-run")
        self.assertRegex(out, r"^notion-sync: dry-run rows=3 created=1 updated=0 closed=1 unchanged=2 failed=0 source=test/handoff.md data_source=11111111\n$")

    def test_unreachable_host_is_off(self):
        fake = FakeNotion()
        base = fake.base
        fake.close()
        code, out, _ = self.sync(env={"NOTION_API_BASE": base})
        self.assertEqual(code, 2)
        self.assertIn("cannot reach", out)

    # ---- F1: creates are never blindly retried

    def titles(self, fake=None):
        return sorted(p["properties"]["Project"]["title"][0]["plain_text"] for p in (fake or self.fake).pages.values())

    def test_create_that_landed_despite_a_5xx_is_not_posted_again(self):
        for status in (502, 409, 500):
            with self.subTest(status=status):
                fake = FakeNotion()
                self.addCleanup(fake.close)
                fake.after_commit.append((status, 0))
                code, out, _ = self.sync(fake=fake)
                self.assertEqual(code, 0)
                self.summary(out, created=3)
                self.assertEqual(self.titles(fake), ["Alpha", "Beta", "Gamma"])      # no second Alpha
                self.assertEqual(fake.count("POST", "/v1/pages"), 3)
                query = [r[2] for r in fake.requests if r[1].endswith("/query")][1]
                self.assertEqual(query["filter"], {"and": [{"property": "Source", "select": {"equals": "test/handoff.md"}},
                                                           {"property": "Project", "title": {"equals": "Alpha"}}]})

    def test_create_that_landed_despite_a_timeout_is_not_posted_again(self):
        with mock.patch.object(ns, "TIMEOUT", 0.2):
            self.fake.after_commit.append((None, 0.5))
            self.write(ROWS[:1])
            code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, created=1)
        self.assertEqual(self.fake.count("POST", "/v1/pages"), 1)
        self.assertEqual(self.titles(), ["Alpha"])

    def test_create_that_did_not_land_is_retried_exactly_once(self):
        self.fake.inject.append(("POST", "/v1/pages", 503, {}, {"object": "error", "status": 503, "code": "service_unavailable", "message": "x"}))
        self.write(ROWS[:1])
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.summary(out, created=1)
        self.assertEqual(self.fake.count("POST", "/v1/pages"), 2)
        self.assertEqual(self.titles(), ["Alpha"])
        fake = FakeNotion()                                   # a non-JSON 200 may have landed too
        self.addCleanup(fake.close)
        fake.inject.append(("POST", "/v1/pages", 200, {}, "not an object"))
        self.assertEqual(self.sync(fake=fake)[0], 0)

    def test_a_400_on_create_is_neither_looked_up_nor_retried(self):
        self.fake.reject_titles.add("Alpha")
        self.write(ROWS[:1])
        self.assertEqual(self.sync()[0], 1)
        self.assertEqual((self.fake.count("POST", "/v1/pages"), self.fake.count("POST", "/v1/data_sources")), (1, 1))

    def test_duplicate_cards_are_set_to_done_pointing_at_the_oldest(self):
        old = self.fake.seed("Alpha", "test/handoff.md", created="2026-01-01T00:00:01.000Z")
        self.fake.seed("Beta", "test/handoff.md")
        copy1 = self.fake.seed("Alpha", "test/handoff.md", created="2026-01-02T00:00:00.000Z")
        copy2 = self.fake.seed("Alpha", "test/handoff.md", status="Done", created="2026-01-03T00:00:00.000Z")
        foreign = self.fake.seed("Alpha", "other/handoff.md")
        self.write(ROWS[:2])
        snapshot = json.dumps({k: self.fake.pages[k] for k in (copy2, foreign)}, sort_keys=True)
        code, out, err = self.sync("--json")
        self.assertEqual(code, 0)
        counts = json.loads(out)["counts"]
        self.assertEqual((counts["duplicates"], counts["updated"], counts["created"], counts["failed"]), (1, 2, 0, 0))
        props = self.fake.pages[copy1]["properties"]
        self.assertEqual(props["Status"], {"select": {"name": "Done"}})
        self.assertEqual(props["Next step"]["rich_text"][0]["text"]["content"],
                         "Duplicate card; the live card is https://www.notion.so/%s. Safe to delete by hand." % old)
        self.assertEqual(self.fake.pages[old]["properties"]["Status"], {"select": {"name": "In progress"}})   # the live card stays
        self.assertEqual(snapshot, json.dumps({k: self.fake.pages[k] for k in (copy2, foreign)}, sort_keys=True))
        patched = [r[1].rsplit("/", 1)[1] for r in self.fake.writes() if r[0] == "PATCH"]
        self.assertNotIn(copy2, patched)
        self.assertNotIn(foreign, patched)
        code, out, _ = self.sync()                            # second run: nothing left to do, no duplicates= in the line
        self.assertEqual(code, 0)
        self.summary(out, unchanged=2)

    def test_duplicates_in_summary_line_and_dry_run(self):
        self.sync()
        self.fake.seed("Beta", "test/handoff.md", created="2030-01-01T00:00:00.000Z")
        before = len(self.fake.writes())
        code, out, _ = self.sync("--dry-run")
        self.assertRegex(out, r"created=0 updated=0 closed=0 unchanged=3 failed=0 duplicates=1 source=test/handoff.md data_source=11111111\n$")
        self.assertEqual(len(self.fake.writes()), before)
        code, out, _ = self.sync()
        self.assertEqual(out, "notion-sync: created=0 updated=0 closed=0 unchanged=3 failed=0 duplicates=1 "
                              "source=test/handoff.md data_source=11111111\n")
        self.assertEqual(self.fake.count("PATCH", "/v1/pages"), 1)

    # ---- F2 / F3: token, version, unexpected errors, scrubbing

    def test_malformed_token_is_off_without_a_request_or_an_echo(self):
        for bad in ("QQQsecret\nZZZtail", "QQQsecret ZZZtail", "QQQsec\u00e9ret", "QQQsecret\tZZZtail"):
            with self.subTest(token=bad):
                self.fake.requests.clear()
                for extra in ([], ["--dry-run"], ["--json"]):
                    code, out, err = self.sync(*extra, env={"NOTION_TOKEN": bad})
                    self.assertEqual(code, 2)
                    self.assertIn("NOTION_TOKEN contains invalid characters", out)
                    self.assertNotIn("QQQ", out + err)
                    self.assertNotIn("ZZZ", out + err)
                self.assertEqual(self.fake.requests, [])
        self.assertEqual(self.sync(env={"NOTION_TOKEN": "  " + TOKEN + "\n"})[0], 0)     # outer whitespace is just stripped

    def test_bad_notion_version_is_refused_before_any_request(self):
        for bad in ("2026-3-11", "latest", "2026-03-11\nX: y", "\u0662026-03-11", "2026-03-11x"):
            with self.subTest(version=bad):
                code, out, err = self.sync(env={"NOTION_VERSION": bad})
                self.assertEqual(code, 4)
                self.assertEqual(self.fake.requests, [])
        self.assertEqual(self.sync(env={"NOTION_VERSION": "2026-03-11"})[0], 0)

    def test_unexpected_exception_is_one_scrubbed_line_and_exit_2(self):
        def boom(args):
            raise RuntimeError("kaboom with " + TOKEN + " inside\nsecond line")
        for extra in ([], ["--json"]):
            with mock.patch.object(ns, "run", boom):
                code, out, err = self.sync(*extra)
            self.assertEqual(code, 2)
            self.assertNotIn(TOKEN, out + err)
            self.assertNotIn("Traceback", out + err)
            self.assertEqual(len(out.splitlines()), 1)
            self.assertIn("internal error: RuntimeError: kaboom with *** inside second line", out)
        self.assertEqual(json.loads(out)["exit"], 2)

    def test_call_turns_a_value_error_into_unreachable(self):
        cfg = {"token": "a\nb", "version": "2026-03-11", "base": self.fake.base, "opener": ns.urllib.request.build_opener(ns.NoRedirect)}
        with self.assertRaises(ns.Unreachable) as cm:
            ns.call(cfg, "GET", "/v1/data_sources/" + DS)
        self.assertNotIn("a\nb", str(cm.exception))
        self.assertEqual(self.fake.requests, [])

    def test_scrub_happens_before_truncation(self):
        with mock.patch.dict(os.environ, {"NOTION_TOKEN": TOKEN}):
            prefix = "HTTP 401 unauthorized: "
            for pad in (300 - len(prefix) - 8, 300 - len(prefix) - 1, 300 - len(prefix)):
                msg = str(ns.ApiError(401, "unauthorized", "x" * pad + TOKEN + " tail"))
                self.assertNotIn(TOKEN[:5], msg)
                self.assertLessEqual(len(msg), 300)
        fake = FakeNotion(token="other")
        self.addCleanup(fake.close)
        pad = "x" * (300 - len("HTTP 401 unauthorized: ") - 8)
        fake.inject.append(("POST", "/v1/search", 401, {}, {"object": "error", "code": "unauthorized", "message": pad + TOKEN}))
        code, out, err = self.sync(fake=fake)
        self.assertEqual(code, 2)
        self.assertNotIn(TOKEN[:8], out + err)

    # ---- F4: 401 / 403 on a write stops the run

    def test_401_or_403_on_a_write_stops_the_run_at_once(self):
        for status in (401, 403):
            with self.subTest(status=status):
                fake = FakeNotion()
                self.addCleanup(fake.close)
                orig = fake.route

                def route(method, path, body, orig=orig, status=status):
                    if method == "POST" and path == "/v1/pages" and body["properties"]["Project"]["title"][0]["text"]["content"] == "Beta":
                        return status, {"object": "error", "status": status, "code": "restricted_resource", "message": "no " + TOKEN}
                    return orig(method, path, body)
                fake.route = route
                code, out, err = self.sync(fake=fake)
                self.assertEqual(code, 2)
                self.assertEqual(out, "notion-sync: off (HTTP %d during writes; 1 writes done before it)\n" % status)
                self.assertNotIn(TOKEN, out + err)
                self.assertEqual(fake.count("POST", "/v1/pages"), 2)               # Alpha ok, Beta refused, Gamma never tried
                self.assertEqual(self.titles(fake), ["Alpha"])
        fake = FakeNotion()
        self.addCleanup(fake.close)
        self.sync(fake=fake)
        self.write([("Alpha (first)", "Live", "Changed", "`scripts/a.py`")] + list(ROWS[1:2]))
        fake.inject.append(("PATCH", "/v1/pages", 403, {}, {"object": "error", "status": 403, "code": "restricted_resource", "message": "no"}))
        code, out, _ = self.sync("--json", fake=fake)
        self.assertEqual((code, json.loads(out)["exit"], json.loads(out)["off"]), (2, 2, True))
        self.assertEqual(fake.count("PATCH", "/v1/pages"), 1)

    # ---- F5: the schema is never changed

    def test_missing_select_option_is_off_and_names_the_property(self):
        for prop, value in (("Area", "test"), ("Source", "test/handoff.md"), ("Owner", "Josep"), ("Status", "Waiting on Josep")):
            with self.subTest(prop=prop):
                options = {k: [o for o in v if o != value] for k, v in OPTIONS.items()}
                fake = FakeNotion(options=options)
                self.addCleanup(fake.close)
                for extra in ([], ["--dry-run"]):
                    code, out, _ = self.sync(*extra, fake=fake)
                    self.assertEqual(code, 2)
                    self.assertIn(f"{prop} option '{value}' missing in Notion; add it by hand", out)
                self.assertEqual(fake.writes(), [])
        fake = FakeNotion(options={"Status": [], "Owner": [], "Area": [], "Source": []})
        self.addCleanup(fake.close)
        code, out, _ = self.sync(fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Status option 'Waiting on Josep' missing in Notion", out)
        self.assertIn("Area option 'test' missing in Notion", out)
        self.assertIn("; add them by hand", out)

    def test_unused_missing_option_does_not_block_an_unchanged_run(self):
        self.sync()
        fake = FakeNotion(options={"Status": [], "Owner": [], "Area": [], "Source": []})
        self.addCleanup(fake.close)
        fake.pages = self.fake.pages
        code, out, _ = self.sync(fake=fake)
        self.assertEqual(code, 0)
        self.summary(out, unchanged=3)

    # ---- F7: --json carries ok and exit

    def test_json_has_ok_and_exit(self):
        res = json.loads(self.sync("--json")[1])
        self.assertEqual((res["ok"], res["exit"], res["counts"]["failed"]), (True, 0, 0))
        self.fake.reject_titles.add("New")
        self.write(ROWS[:2] + [("New", "Live", "Do it", "")])
        code, out, _ = self.sync("--json")
        res = json.loads(out)
        self.assertEqual((code, res["ok"], res["exit"], res["counts"]["failed"]), (1, False, 1, 1))
        code, out, _ = self.sync("--json", "--dry-run")
        self.assertEqual((json.loads(out)["ok"], json.loads(out)["exit"]), (True, 0))

    # ---- F8: a database id instead of a data source id

    def test_database_id_resolves_to_its_only_data_source(self):
        dbid = "aaaaaaaa-db00-0000-0000-000000000000"
        self.fake.databases[dbid] = [DS]
        for extra, env in (([], {"NOTION_PROJECTS_DS": dbid}), (["--data-source", dbid], None)):
            code, out, err = self.sync(*extra, env=env)
            self.assertEqual(code, 0, err)
            self.assertIn("note: aaaaaaaa is a database id; using its data source 11111111. Set NOTION_PROJECTS_DS to that.", err)
            self.assertTrue(out.endswith("data_source=11111111\n"))
        self.assertEqual(len(self.fake.pages), 3)

    def test_database_id_with_zero_or_two_data_sources_keeps_exit_2(self):
        for sources in ([], [DS, "22222222-0000-0000-0000-000000000000"]):
            self.fake.databases["db"] = sources
            code, out, err = self.sync("--data-source", "db")
            self.assertEqual(code, 2)
            self.assertIn("404", out)
            self.assertIn("share the page with the integration, or use the data source id, not the database id", out)
            self.assertNotIn("note:", err)
        code, out, _ = self.sync("--data-source", "nothing-here")
        self.assertEqual(code, 2)
        self.assertIn("not the database id", out)
        self.assertEqual(self.fake.writes(), [])


class RefusalTests(unittest.TestCase):
    def run_cli(self, *argv, env=None):
        environ = {k: v for k, v in os.environ.items() if not k.startswith("NOTION_")}
        environ.update(env or {})
        return subprocess.run([sys.executable, str(SCRIPT), *argv], env=environ, capture_output=True, text=True, timeout=60)

    def test_foreign_api_base_is_refused_before_any_request(self):
        for base in ("https://evil.example", "http://127.0.0.1.evil.example:80", "http://127.0.0.1", "https://api.notion.com"):
            r = self.run_cli("--dry-run", "--today", TODAY, env={"NOTION_TOKEN": TOKEN, "NOTION_API_BASE": base})
            self.assertEqual(r.returncode, 4, base)
            self.assertNotIn(TOKEN, r.stdout + r.stderr)

    def test_no_request_is_sent_on_refusal(self):
        fake = FakeNotion()
        self.addCleanup(fake.close)
        r = self.run_cli("--today", "not-a-date", env={"NOTION_TOKEN": TOKEN, "NOTION_API_BASE": fake.base})
        self.assertEqual(r.returncode, 4)
        self.assertEqual(fake.requests, [])

    def test_bad_command_line_is_4_not_2(self):
        self.assertEqual(self.run_cli("--nope").returncode, 4)

    def test_no_token_without_dry_run_is_off(self):
        r = self.run_cli("--today", TODAY)
        self.assertEqual((r.returncode, r.stdout), (2, "notion-sync: off (NOTION_TOKEN not set)\n"))

    def test_no_token_dry_run_prints_parsed_rows(self):
        r = self.run_cli("--dry-run", "--json", "--today", TODAY)
        self.assertEqual(r.returncode, 0, r.stderr)
        res = json.loads(r.stdout)
        self.assertIsNone(res["plan"])
        self.assertTrue(res["rows"])
        r = self.run_cli("--dry-run", "--today", TODAY)
        self.assertRegex(r.stdout, r"^notion-sync: dry-run rows=\d+ source=\S+/handoff\.md\n$")

    def test_handoff_errors_exit_3(self):
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "h.md")
            Path(bad).write_text("# nothing here\n", encoding="utf-8")
            for path in (bad, os.path.join(d, "missing.md")):
                self.assertEqual(self.run_cli("--dry-run", "--handoff", path).returncode, 3)


if __name__ == "__main__":
    unittest.main()
