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


HEADER7 = "| Workstream | Status | Priority | Owner | State | Next step | Detail |"


def table(rows, header="| Workstream | State | Next step | Detail |"):
    sep = "|" + "---|" * (header.count("|") - 1)
    lines = ["# handoff", "", "Last updated: 2026-10-05 08:27 UTC by someone.", "", "## In flight", header, sep]
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
            ("Done on branch", "Jeff: merge it", "Waiting on Jeff", "Jeff"),
            ("Blocked by CI", "Fix tests", "Blocked", "Claude Code"),
            ("Live", "Blocked: waiting for a key", "Blocked", "Claude Code"),
            ("Not started; due 2026-12-01", "Start it", "Backlog", "Claude Code"),
            ("Live", "Jeff merges PR #7", "Waiting on Jeff", "Jeff"),
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
        rows = parse([("Skill review (Jeff's ask 2026-10-04: x (nested) y)", "s", "n", ""),
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
                      ("pr", "s", "Jeff merges PR #5", "—"),
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
                      ("E", "Notion-Version 2026-03-11", "none", ""), ("F", "data conversion 2026-10-03", "n", ""),
                      ("G", "subversion-2026-10-02", "n", "")])
        self.assertEqual([r["last_update"] for r in rows],
                         ["2026-10-01", "2026-10-05", "2026-10-05", "2026-10-02", "2026-10-05", "2026-10-03", "2026-10-02"])

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

    # ---- v2: explicit Status / Priority / Owner columns

    def parse7(self, rows):
        return ns.parse_handoff(table(rows, HEADER7), TODAY, REPO_URL)[1]

    def test_explicit_columns_are_parsed_and_override_the_rules(self):
        rows = self.parse7([("A", "in PROGRESS", "p1", "routine", "Live", "Jeff merges PR #7", ""),
                            ("B", "Waiting", "P0", "Claude Code", "Live", "Run it", ""),
                            ("C", "Backlog", "p3", "Jeff", "Live", "none", ""),
                            ("D", "Done", "P2", "Claude Code", "All good. More.", "—", ""),
                            ("E", "Dropped", "P3", "Jeff", "Not wanted. Later.", "none", ""),
                            ("F", "Blocked", "", "", "Live", "Run it", ""),
                            ("G", "", "P1", "", "Live", "Jeff merges it", "")])
        got = [(r["status"], r["priority"], r["owner"]) for r in rows]
        self.assertEqual(got, [("In progress", "P1", "Routine"), ("Waiting on Jeff", "P0", "Claude Code"),
                               ("Backlog", "P3", "Jeff"), ("Done", "P2", "Claude Code"), ("Dropped", "P3", "Jeff"),
                               ("Blocked", None, "Claude Code"), ("Waiting on Jeff", "P1", "Jeff")])
        self.assertEqual(rows[3]["next_step"], "Done — All good.")
        self.assertEqual(rows[4]["next_step"], "Dropped: Not wanted.")      # policy: Dropped: <reason>
        self.assertEqual(rows[2]["next_step"], "none")                  # a Backlog row keeps its Next step as written

    def test_invalid_explicit_values_warn_and_fall_back(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = self.parse7([("A", "Doing", "P9", "Bob", "Live", "Jeff merges it", "")])
        self.assertEqual((rows[0]["status"], rows[0]["priority"], rows[0]["owner"]), ("Waiting on Jeff", None, "Jeff"))
        for text in ("warn: row 'A': unknown Status 'Doing'; using the rule-based status",
                     "warn: row 'A': unknown Owner 'Bob'; using the rule-based owner",
                     "warn: row 'A': unknown Priority 'P9'"):
            self.assertIn(text, err.getvalue())

    def test_current_person_status_and_owner_parse(self):
        # the names derive from the one PERSON constant ...
        self.assertEqual((ns.PERSON, ns.WAITING), ("Jeff", "Waiting on Jeff"))
        self.assertIn("Waiting on Jeff", ns.STATUSES)
        self.assertEqual(ns.OWNERS[0], "Jeff")
        self.assertIn("Jeff", ns.WIP_LIMITS)
        # ... and a handoff row that uses them is read as written: valid, no warning, explicit columns win over the rules
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = self.parse7([("A", "Waiting on Jeff", "P1", "Jeff", "Live", "Run it", "")])
        self.assertEqual((rows[0]["status"], rows[0]["priority"], rows[0]["owner"]), ("Waiting on Jeff", "P1", "Jeff"))
        self.assertEqual(err.getvalue(), "")

    def test_previous_person_name_is_unknown_not_silently_mapped(self):
        old = "Jos" + "ep"            # the previous name, assembled so that it does not appear in the repository text
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = self.parse7([("A", f"Waiting on {old}", "P1", old, "Live", "Run it", ""),
                                ("B", "Backlog", "P2", "Claude Code", "Live", f"{old}: merge it", "")])
        # explicit values: unknown, warned, rules used (Next step "Run it" -> In progress / Claude Code)
        self.assertEqual((rows[0]["status"], rows[0]["owner"]), ("In progress", "Claude Code"))
        self.assertIn(f"warn: row 'A': unknown Status 'Waiting on {old}'; using the rule-based status", err.getvalue())
        self.assertIn(f"warn: row 'A': unknown Owner '{old}'; using the rule-based owner", err.getvalue())
        # a Next step that starts with the old name no longer addresses the board owner (rule e / owner rule)
        self.assertEqual(ns.classify("Live", f"{old}: merge it"), "In progress")
        self.assertEqual(ns.owner_of(f"{old}: merge it"), "Claude Code")
        self.assertEqual(rows[1]["owner"], "Claude Code")
        self.assertNotIn(f"Waiting on {old}", ns.STATUSES)
        self.assertNotIn("waiting on " + old.lower(), ns.STATUS_WORDS)
        self.assertNotIn(old.lower(), ns.OWNER_WORDS)

    def test_old_four_column_format_parses_identically(self):
        old = [("Alpha (first)", "Live", "Run the thing", "`scripts/a.py`"), ("Beta", "Waiting", "Jeff merges PR #7", "—"),
               ("Gamma", "Done and merged", "none", "`docs/`")]
        new = [(w, "", "", "", st, nx, d) for w, st, nx, d in old]
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows7 = self.parse7(new)
        rows4 = parse(old)
        self.assertEqual(err.getvalue(), "")
        self.assertEqual([dict(r, priority=None) for r in rows4], rows7)
        self.assertTrue(all("priority" in r and r["priority"] is None for r in rows4))

    def test_real_handoff_has_explicit_status_priority_owner_on_every_row(self):
        path = SCRIPT.parent.parent / "handoff.md"
        text = path.read_text(encoding="utf-8")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            _, rows = ns.parse_handoff(text, TODAY, REPO_URL)
        self.assertEqual(err.getvalue(), "")                            # no warning: every explicit value is valid
        start = text.index("## In flight")
        lines = [ln for ln in text[start:].split("\n\n")[0].splitlines()[1:] if ln.startswith("|")]
        header = [ns.clean(c).lower() for c in ns.split_row(lines[0])]
        for col in ("status", "priority", "owner"):
            self.assertIn(col, header)
        body = [ns.split_row(ln) for ln in lines[2:]]
        self.assertEqual(len(body), len(rows))
        for cells, r in zip(body, rows):
            for col, key, allowed in (("status", "status", ns.STATUSES), ("priority", "priority", ns.PRIORITIES),
                                      ("owner", "owner", ns.OWNERS)):
                raw = ns.clean(cells[header.index(col)])
                self.assertTrue(raw, (col, r["project"]))
                self.assertIn(r[key], allowed)
                self.assertEqual(r[key], {"status": ns.STATUS_WORDS, "priority": ns.PRIORITY_WORDS, "owner": ns.OWNER_WORDS}[col][raw.lower()])


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


OPTIONS = {"Status": ["Backlog", "In progress", "Waiting on Jeff", "Blocked", "Done", "Dropped"],
           "Priority": ["P0", "P1", "P2", "P3"], "Owner": ["Jeff", "Claude Code", "Routine"], "Area": ["test"], "Source": ["test/handoff.md"]}


class FakeNotion:
    def __init__(self, token=TOKEN, page_size=100, schema=None, options=None, target_date=True):
        self.token, self.page_size, self.inject, self.requests = token, page_size, [], []
        self.pages, self.reject_titles, self.ignore_filter = {}, set(), False
        self.schema = schema or dict(ns.SCHEMA, **({"Target date": "date"} if target_date else {}))
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

    def seed(self, project, source, status="In progress", created=None, props=None):
        pid = "page-%d" % (len(self.pages) + 1)
        self.pages[pid] = {"id": pid, "url": "https://www.notion.so/" + pid, "created_time": created or self.stamp(),
                           "properties": normalise(dict({
            "Project": {"title": [{"type": "text", "text": {"content": project}}]}, "Source": {"select": {"name": source}},
            "Status": {"select": {"name": status}}, "Next step": {"rich_text": [{"type": "text", "text": {"content": "manual"}}]}},
            **(props or {})))}
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
            flt = body.get("filter")
            parts = (flt.get("and") or [flt]) if flt else []
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
        ("Beta", "Waiting", "Jeff merges PR #7", "—"),
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
        self.assertEqual(props["Status"], {"select": {"name": "Waiting on Jeff"}})
        self.assertEqual(props["Owner"], {"select": {"name": "Jeff"}})
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
                         "Duplicate card; the live card is https://www.notion.so/%s." % old)
        self.assertEqual(props["Last update"], {"date": {"start": "2026-10-05"}})            # a move updates Last update
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
        for prop, value in (("Area", "test"), ("Source", "test/handoff.md"), ("Owner", "Jeff"), ("Status", "Waiting on Jeff")):
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
        self.assertIn("Status option 'Waiting on Jeff' missing in Notion", out)
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

    # ---- v2: Priority, Dropped, Target date

    def sync7(self, rows, *extra, **kw):
        Path(self.handoff).write_text(table(rows, HEADER7), encoding="utf-8")
        return self.sync(*extra, **kw)

    def props(self, project, fake=None):
        return next(p["properties"] for p in (fake or self.fake).pages.values()
                    if p["properties"]["Project"]["title"][0]["plain_text"] == project)

    def test_priority_is_written_on_create_compared_on_update_and_omitted_when_empty(self):
        rows = [("Alpha", "In progress", "P1", "Claude Code", "Live", "Run it", ""), ("Beta", "In progress", "", "Claude Code", "Live", "Run it", "")]
        code, out, _ = self.sync7(rows)
        self.assertEqual(code, 0)
        self.summary(out, created=2)
        self.assertEqual(self.props("Alpha")["Priority"], {"select": {"name": "P1"}})
        creates = {r[2]["properties"]["Project"]["title"][0]["text"]["content"]: r[2] for r in self.fake.requests if r[1] == "/v1/pages"}
        self.assertEqual(creates["Beta"]["properties"]["Priority"], {"select": {"name": "P2"}})    # policy default, on create only
        self.assertEqual(self.sync7(rows)[1].split("unchanged=")[1][:1], "2")            # second run: nothing to do
        rows[0] = ("Alpha", "In progress", "p0", "Claude Code", "Live", "Run it", "")    # only Priority changes
        before = len(self.fake.writes())
        code, out, _ = self.sync7(rows)
        self.summary(out, updated=1, unchanged=1)
        (method, path, body, _), = self.fake.writes()[before:]
        self.assertEqual((method, list(body["properties"])), ("PATCH", ["Priority"]))
        self.assertEqual(body["properties"]["Priority"], {"select": {"name": "P0"}})
        self.assertEqual(self.props("Beta")["Priority"], {"select": {"name": "P2"}})
        self.fake.pages[next(k for k, pg in self.fake.pages.items() if pg["properties"]["Project"]["title"][0]["plain_text"] == "Beta")][
            "properties"]["Priority"] = {"select": {"name": "P3"}}
        before = len(self.fake.writes())
        self.summary(self.sync7(rows)[1], unchanged=2)                                   # empty Priority: Notion's value stays
        self.assertEqual(len(self.fake.writes()), before)
        self.assertEqual(self.props("Beta")["Priority"], {"select": {"name": "P3"}})

    def test_priority_option_must_exist(self):
        options = dict(OPTIONS, Priority=["P2"])
        fake = FakeNotion(options=options)
        self.addCleanup(fake.close)
        code, out, _ = self.sync7([("A", "In progress", "P1", "Claude Code", "Live", "Run it", "")], fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Priority option 'P1' missing in Notion", out)
        self.assertEqual(fake.writes(), [])

    def test_missing_priority_property_is_off_but_missing_target_date_is_fine(self):
        schema = dict(ns.SCHEMA)
        del schema["Priority"]
        fake = FakeNotion(schema=schema)
        self.addCleanup(fake.close)
        code, out, _ = self.sync(fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Priority (select)", out)
        self.assertEqual(fake.writes(), [])
        schema = dict(ns.SCHEMA, Priority="rich_text")
        fake = FakeNotion(schema=schema)
        self.addCleanup(fake.close)
        self.assertEqual(self.sync(fake=fake)[0], 2)
        for target_date in (False, True):
            fake = FakeNotion(target_date=target_date)
            self.addCleanup(fake.close)
            self.assertEqual(self.sync(fake=fake)[0], 0)
            self.assertEqual(len(fake.pages), 3)
            self.assertTrue(all("Target date" not in pg["properties"] for pg in fake.pages.values()))   # never written

    def test_dropped_row_is_synced_and_dropped_cards_are_left_alone(self):
        rows = [("Gone", "Dropped", "P3", "Jeff", "No longer wanted. Really.", "none", ""),
                ("Kept", "In progress", "P2", "Claude Code", "Live", "Run it", "")]
        self.assertEqual(self.sync7(rows)[0], 0)
        props = self.props("Gone")
        self.assertEqual(props["Status"], {"select": {"name": "Dropped"}})
        self.assertEqual(props["Next step"]["rich_text"][0]["plain_text"], "Dropped: No longer wanted.")
        self.assertEqual(props["Priority"], {"select": {"name": "P3"}})
        before = len(self.fake.writes())
        self.assertEqual(self.sync7(rows)[0], 0)
        self.assertEqual(len(self.fake.writes()), before)
        # a Dropped card whose row left In flight is not closed; a Dropped extra is not re-closed
        dropped = self.fake.seed("Old idea", "test/handoff.md", status="Dropped")
        extra_dropped = self.fake.seed("Kept", "test/handoff.md", status="Dropped", created="2032-01-01T00:00:00.000Z")
        snapshot = json.dumps({k: self.fake.pages[k] for k in (dropped, extra_dropped)}, sort_keys=True)
        code, out, _ = self.sync7(rows, "--json")
        res = json.loads(out)
        self.assertEqual((code, res["counts"]["closed"], res["counts"]["duplicates"], res["counts"]["failed"]), (0, 0, 0, 0))
        self.assertEqual(len(self.fake.writes()), before)
        self.assertEqual(snapshot, json.dumps({k: self.fake.pages[k] for k in (dropped, extra_dropped)}, sort_keys=True))

    def test_dropped_option_must_exist(self):
        fake = FakeNotion(options=dict(OPTIONS, Status=[o for o in OPTIONS["Status"] if o != "Dropped"]))
        self.addCleanup(fake.close)
        code, out, _ = self.sync7([("A", "Dropped", "P3", "Jeff", "x", "none", "")], fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Status option 'Dropped' missing in Notion", out)

    def test_old_format_rows_create_cards_with_the_policy_default_priority(self):
        self.assertEqual(self.sync("--json")[0], 0)                       # the 4-column ROWS carry no Priority at all
        for p in self.fake.pages.values():
            self.assertEqual(p["properties"]["Priority"], {"select": {"name": "P2"}})
        before = len(self.fake.writes())
        self.summary(self.sync()[1], unchanged=3)
        self.assertEqual(len(self.fake.writes()), before)

    def test_status_change_updates_last_update_even_when_the_row_date_is_older(self):
        pid = self.fake.seed("Z", "test/handoff.md", status="Backlog", props={
            "Area": {"select": {"name": "test"}}, "Owner": {"select": {"name": "Claude Code"}}, "Priority": {"select": {"name": "P2"}},
            "Link": {"url": REPO_URL + "/blob/main/handoff.md"}, "Last update": {"date": {"start": "2026-09-01"}}})
        self.fake.pages[pid]["properties"]["Next step"] = {"rich_text": [{"type": "text", "text": {"content": "Run it"}, "plain_text": "Run it"}]}
        rows = [("Z", "In progress", "P2", "Claude Code", "PR merged 2026-09-01", "Run it", "")]
        before = len(self.fake.writes())
        self.summary(self.sync7(rows)[1], updated=1)
        (method, path, body, _), = self.fake.writes()[before:]
        self.assertEqual(sorted(body["properties"]), ["Last update", "Status"])
        self.assertEqual(body["properties"]["Last update"], {"date": {"start": "2026-10-05"}})   # the handoff's date
        self.summary(self.sync7(rows)[1], unchanged=1)                     # and the row's older date does not undo it
        self.assertEqual(len(self.fake.writes()), before + 1)

    def test_a_closed_card_is_not_reopened_but_same_status_updates_still_apply(self):
        done = self.fake.seed("Re", "test/handoff.md", status="Done", props={"Link": {"url": "https://x/pr/1"}})
        dropped = self.fake.seed("Dr", "test/handoff.md", status="Dropped")
        snapshot = json.dumps({k: self.fake.pages[k] for k in (done, dropped)}, sort_keys=True)
        rows = [("Re", "In progress", "P2", "Claude Code", "Live", "Run it", ""), ("Dr", "Backlog", "P2", "Jeff", "Live", "Start", "")]
        code, out, err = self.sync7(rows, "--json")
        self.assertEqual((code, json.loads(out)["counts"]["updated"], json.loads(out)["counts"]["created"]), (0, 0, 0))
        self.assertIn("card 'Re' is Done in Notion but its row says In progress; not reopened", err)
        self.assertIn("card 'Dr' is Dropped in Notion but its row says Backlog; not reopened", err)
        self.assertEqual(snapshot, json.dumps({k: self.fake.pages[k] for k in (done, dropped)}, sort_keys=True))
        self.assertEqual(self.fake.writes(), [])
        rows = [("Re", "Done", "P2", "Claude Code", "Shipped 2026-10-05", "none", "https://x/pr/2")]   # still Done: the Link may improve
        self.sync7(rows)
        self.assertEqual(self.fake.pages[done]["properties"]["Link"], {"url": "https://x/pr/2"})
        self.assertEqual(self.fake.pages[done]["properties"]["Status"], {"select": {"name": "Done"}})

    def test_dropped_without_a_reason_warns(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = ns.parse_handoff(table([("A", "Dropped", "P3", "Jeff", "", "", ""), ("B", "Dropped", "P3", "Jeff", "Why not. Ok.", "", ""),
                                           ("C", "Dropped", "P3", "Jeff", "x", "Dropped: because", "")], HEADER7), TODAY, REPO_URL)[1]
        self.assertEqual([r["next_step"] for r in rows], ["Dropped", "Dropped: Why not.", "Dropped: because"])
        self.assertIn("warn: row 'A': Dropped without a reason", err.getvalue())
        self.assertEqual(err.getvalue().count("Dropped without a reason"), 1)         # only row A

    # ---- v2: --audit

    def card(self, project="Card", source="test/handoff.md", status="In progress", owner="Claude Code", priority="P2", area="test",
             nxt="Run it", link="https://x.example/e", last="2026-10-05", target=None, fake=None, created=None):
        def sel(v):
            return {"select": {"name": v}} if v else {"select": None}
        props = {"Owner": sel(owner), "Priority": sel(priority), "Area": sel(area),
                 "Next step": {"rich_text": [{"type": "text", "text": {"content": nxt}}] if nxt else []},
                 "Link": {"url": link or None}, "Last update": {"date": {"start": last} if last else None}}
        if target:
            props["Target date"] = {"date": {"start": target}}
        return (fake or self.fake).seed(project, source, status=status, props=props, created=created)

    def audit(self, *extra, fake=None, env=None):
        code, out, err = self.sync("--audit", *extra, fake=fake, env=env)
        self.assertEqual(code, 0, out + err)
        return out, err

    def counts_of(self, out):
        line = out.splitlines()[0]
        self.assertTrue(line.startswith("notion-audit: "), line)
        return dict(kv.split("=") for kv in line[len("notion-audit: "):].split())

    def rule_count(self, rule, make, **fake_kw):
        fake = FakeNotion(**fake_kw)
        self.addCleanup(fake.close)
        make(fake)
        out, _ = self.audit("--json", fake=fake)
        res = json.loads(out)
        return res["counts"][rule], res

    def test_audit_compliant_card_has_no_violation_and_output_shape(self):
        self.card("Fine")
        out, err = self.audit()
        self.assertEqual(err, "")
        self.assertEqual(out, "notion-audit: cards=1 open=1 violations=0 wip=0 p0=0 missing=0 stale=0 waiting=0 blocked=0 "
                              "target=0 overdue=0 evidence=0 dropped=0 dup=0\n")
        res = json.loads(self.audit("--json")[0])
        self.assertEqual(res, {"ok": True, "audit": True, "counts": res["counts"], "violations": [], "other_source_violations": 0,
                               "data_source": "11111111", "exit": 0})

    def test_audit_wip_is_per_owner(self):
        def make(owner, n):
            return lambda f: [self.card("c%d" % i, owner=owner, fake=f) for i in range(n)]
        for owner, n, want in (("Jeff", 3, 0), ("Jeff", 4, 1), ("Claude Code", 5, 0), ("Claude Code", 6, 1), ("Routine", 20, 0)):
            with self.subTest(owner=owner, n=n):
                self.assertEqual(self.rule_count("wip", make(owner, n))[0], want)

        def both(f):
            for i in range(4):
                self.card("j%d" % i, owner="Jeff", fake=f)
            for i in range(5):
                self.card("c%d" % i, owner="Claude Code", fake=f)
        count, res = self.rule_count("wip", both)
        self.assertEqual((count, [v["detail"] for v in res["violations"]]), (1, ["Jeff: 4 In progress > 3"]))
        self.assertIsNone(res["violations"][0]["card"])

    def test_audit_p0_one_open_per_owner(self):
        cases = [("two for one owner", lambda f: [self.card("a", priority="P0", owner="Jeff", status="Backlog", fake=f),
                                                  self.card("b", priority="P0", owner="Jeff", status="Backlog", fake=f)], 1),
                 ("one each", lambda f: [self.card("a", priority="P0", owner="Jeff", fake=f),
                                         self.card("b", priority="P0", owner="Claude Code", fake=f)], 0),
                 ("second is Done", lambda f: [self.card("a", priority="P0", owner="Jeff", fake=f),
                                               self.card("b", priority="P0", owner="Jeff", status="Done", fake=f)], 0)]
        for name, make, want in cases:
            with self.subTest(name):
                self.assertEqual(self.rule_count("p0", make)[0], want)
        res = self.rule_count("p0", cases[0][1])[1]
        self.assertEqual(res["violations"][0]["detail"], "Jeff: 2 open P0 > 1")

    def test_audit_missing_fields_on_open_cards_only(self):
        count, res = self.rule_count("missing", lambda f: [
            self.card("bad", owner=None, nxt="", priority=None, area=None, fake=f),
            self.card("bad2", nxt="", fake=f), self.card("fine", fake=f),
            self.card("done", status="Done", owner=None, nxt="", priority=None, area=None, fake=f),
            self.card("dropped", status="Dropped", owner=None, nxt="Dropped: x", fake=f)])
        self.assertEqual(count, 2)
        self.assertEqual([(v["card"], v["detail"]) for v in res["violations"]],
                         [("bad", "missing Owner, Next step, Priority, Area"), ("bad2", "missing Next step")])

    def test_audit_stale(self):
        cases = [("In progress", "2026-09-22", 0), ("In progress", "2026-09-21", 1), ("Blocked", "2026-09-21", 1),
                 ("Blocked", "2026-09-22", 0), ("Waiting on Jeff", "2026-09-29", 0), ("Waiting on Jeff", "2026-09-28", 1),
                 ("In progress", None, 1), ("Backlog", "2026-01-01", 0), ("Done", "2026-01-01", 0)]
        for status, last, want in cases:
            with self.subTest(status=status, last=last):
                nxt = "Jeff: decide" if status == "Waiting on Jeff" else "Run it"
                count, res = self.rule_count("stale", lambda f: self.card("s", status=status, last=last, nxt=nxt, fake=f))
                self.assertEqual(count, want)
        res = self.rule_count("stale", lambda f: self.card("Old", last="2026-09-01", fake=f))[1]
        self.assertEqual(res["violations"], [{"rule": "stale", "card": "Old", "detail": "In progress, last update 2026-09-01 (35 days)"}])

    def test_audit_waiting_blocked_evidence_dropped(self):
        cases = [("waiting", lambda f: self.card("w", status="Waiting on Jeff", nxt="Merge it", fake=f), 1),
                 ("waiting", lambda f: self.card("w", status="Waiting on Jeff", nxt="JEFF: merge it", fake=f), 0),
                 ("blocked", lambda f: self.card("b", status="Blocked", nxt="", fake=f), 1),
                 ("blocked", lambda f: self.card("b", status="Blocked", nxt="Vendor ships on 2026-11-01", fake=f), 0),
                 ("evidence", lambda f: self.card("d", status="Done", link=None, fake=f), 1),
                 ("evidence", lambda f: self.card("d", status="Done", fake=f), 0),
                 ("evidence", lambda f: self.card("d", status="In progress", link=None, fake=f), 0),
                 ("dropped", lambda f: self.card("x", status="Dropped", nxt="Not wanted", fake=f), 1),
                 ("dropped", lambda f: self.card("x", status="Dropped", nxt="Dropped: not wanted", fake=f), 0)]
        for rule, make, want in cases:
            with self.subTest(rule=rule, want=want):
                self.assertEqual(self.rule_count(rule, make)[0], want)

    def test_audit_evidence_rejects_the_handoff_fallback_and_cards_closed_by_leaving(self):
        cases = [("no link", dict(link=None), 1),
                 ("fallback link", dict(link=REPO_URL + "/blob/main/handoff.md"), 1),
                 ("fallback with anchor", dict(link=REPO_URL + "/blob/main/handoff.md#x"), 1),
                 ("left in flight", dict(nxt="Left test/handoff.md In flight; last seen 2026-10-05."), 1),
                 ("pull request", dict(link=REPO_URL + "/pull/5"), 0),
                 ("a file", dict(link=REPO_URL + "/blob/main/outputs/health/x.md"), 0),
                 ("other handoff file", dict(link=REPO_URL + "/blob/main/docs/handoff.md.bak"), 0)]
        for name, kw, want in cases:
            with self.subTest(name):
                count, res = self.rule_count("evidence", lambda f: self.card("d", status="Done", **dict({"fake": f}, **kw)))
                self.assertEqual(count, want)

    def test_audit_missing_covers_status_project_and_last_update(self):
        count, res = self.rule_count("missing", lambda f: [
            self.card("odd status", status="Not started", fake=f), self.card("", fake=f),
            self.card("no date", status="Backlog", last=None, fake=f),
            self.card("stale only", status="In progress", last=None, fake=f),       # reported once, by the stale rule
            self.card("fine", fake=f)])
        self.assertEqual(sorted((v["card"], v["detail"]) for v in res["violations"] if v["rule"] == "missing"),
                         [("(untitled)", "missing Project"), ("no date", "missing Last update"), ("odd status", "missing Status")])
        self.assertEqual(count, 3)
        self.assertEqual(res["counts"]["stale"], 1)
        fake = FakeNotion()
        self.addCleanup(fake.close)
        self.card("x", status=None, fake=fake)                                      # an empty Status is open and not a policy column
        self.assertEqual(json.loads(self.audit("--json", fake=fake)[0])["counts"]["missing"], 1)

    def test_audit_waiting_and_dropped_need_the_prefix_with_a_colon_and_text(self):
        for rule, status, nxt, want in (("waiting", "Waiting on Jeff", "Jeffrey sends the file", 1),
                                        ("waiting", "Waiting on Jeff", "Jeff merges PR #7", 1),
                                        ("waiting", "Waiting on Jeff", "Jeff:", 1),
                                        ("waiting", "Waiting on Jeff", "jeff: merge PR #7", 0),
                                        ("dropped", "Dropped", "dropped it, lol", 1),
                                        ("dropped", "Dropped", "Dropped", 1),
                                        ("dropped", "Dropped", "Dropped:   ", 1),
                                        ("dropped", "Dropped", "Dropped: no longer wanted", 0)):
            with self.subTest(status=status, nxt=nxt):
                self.assertEqual(self.rule_count(rule, lambda f: self.card("c", status=status, nxt=nxt, fake=f))[0], want)

    def test_audit_text_survives_a_stdout_that_cannot_encode_the_em_dash(self):
        self.card("Mine stale", last="2026-08-01")
        environ = {k: v for k, v in os.environ.items() if not k.startswith("NOTION_")}
        environ.update({"NOTION_TOKEN": TOKEN, "NOTION_API_BASE": self.fake.base, "PYTHONIOENCODING": "ascii"})
        for extra in ([], ["--json"]):
            r = subprocess.run([sys.executable, str(SCRIPT), "--audit", "--source", "test/handoff.md", "--today", TODAY, *extra],
                               env=environ, capture_output=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotIn(b"internal error", r.stdout + r.stderr)
            out = r.stdout.decode("ascii")                                          # everything is ASCII, nothing half-printed
            if not extra:
                self.assertEqual(len(out.splitlines()), 2)
                self.assertIn("[stale] Mine stale \\u2014 In progress, last update 2026-08-01", out)
            else:
                self.assertEqual(json.loads(out)["counts"]["stale"], 1)

    def test_emit_never_raises_on_a_narrow_stream(self):
        raw = io.BytesIO()
        stream = io.TextIOWrapper(raw, encoding="ascii")
        ns.emit("a \u2014 b \u00e9\n", stream)
        stream.flush()
        self.assertEqual(raw.getvalue(), b"a \\u2014 b \\xe9\n")
        out = io.StringIO()
        ns.emit("a \u2014 b\n", out)
        self.assertEqual(out.getvalue(), "a \u2014 b\n")                              # a capable stream is untouched

    def test_audit_target_and_overdue(self):
        def make(f):
            self.card("p1 no target", priority="P1", fake=f)
            self.card("p0 no target", priority="P0", status="Backlog", fake=f)
            self.card("p2 no target", priority="P2", fake=f)
            self.card("p1 with target", priority="P1", target="2026-11-01", fake=f)
            self.card("overdue", priority="P2", target="2026-10-05", fake=f)
            self.card("due today", priority="P2", target="2026-10-06", fake=f)
            self.card("done and late", priority="P1", status="Done", target="2026-01-01", fake=f)
        count, res = self.rule_count("target", make)        # policy: Target date is required for P0 only
        self.assertEqual(count, 1)
        self.assertEqual(res["counts"]["overdue"], 1)
        self.assertEqual({v["card"] for v in res["violations"] if v["rule"] == "target"}, {"p0 no target"})

    def test_audit_target_and_overdue_are_na_without_the_property(self):
        fake = FakeNotion(target_date=False)
        self.addCleanup(fake.close)
        self.card("p1", priority="P1", fake=fake)
        out, _ = self.audit(fake=fake)
        self.assertIn(" target=n/a overdue=n/a ", out)
        self.assertEqual(self.counts_of(out)["violations"], "0")
        res = json.loads(self.audit("--json", fake=fake)[0])
        self.assertEqual((res["counts"]["target"], res["counts"]["overdue"]), (None, None))
        self.assertEqual(res["violations"], [])

    def test_audit_duplicates_count_once_per_extra_open_card(self):
        def make(f):
            self.card("Twin", created="2026-01-01T00:00:00.000Z", fake=f)
            self.card("Twin", created="2026-01-02T00:00:00.000Z", fake=f)
            self.card("Twin", created="2026-01-03T00:00:00.000Z", status="Backlog", fake=f)
            self.card("Twin", created="2026-01-04T00:00:00.000Z", status="Done", fake=f)
            self.card("Twin", source="manual", fake=f)                 # another Source: not a duplicate
            self.card("Solo", fake=f)
        count, res = self.rule_count("dup", make)
        self.assertEqual(count, 2)
        self.assertEqual([v["card"] for v in res["violations"]], ["Twin", "Twin"])

    def test_audit_paginates_skips_trash_and_never_writes(self):
        self.fake.page_size = 2
        for i in range(5):
            self.card("c%d" % i, owner="Routine")
        trashed = self.card("trashed", owner="Routine")
        self.fake.pages[trashed]["in_trash"] = True
        out, _ = self.audit()
        self.assertEqual(self.counts_of(out)["cards"], "5")
        queries = [r for r in self.fake.requests if r[1].endswith("/query")]
        self.assertEqual(len(queries), 3)                                # 5 live + 1 trashed = 6 rows = 3 pages of 2
        self.assertEqual([q[2].get("start_cursor") for q in queries], [None, "2", "4"])
        for q in queries:
            self.assertNotIn("filter", q[2])
            self.assertEqual(q[2]["page_size"], 100)
        self.assertEqual(self.fake.writes(), [])
        self.assertEqual({(m, p.split("?")[0]) for m, p, _, _ in self.fake.requests if m != "GET"},
                         {("POST", "/v1/search"), ("POST", "/v1/data_sources/%s/query" % DS)})
        self.assertEqual(self.fake.count("PATCH", ""), 0)

    def test_audit_never_prints_titles_or_details_of_other_sources(self):
        secret = self.card("SECRET-PROJECT-XYZ", source="manual", status="Waiting on Jeff", owner="Jeff", priority="P0",
                           area="SECRET-AREA", nxt="SECRET-NEXT", link=None, last=None, target="2026-01-01",
                           created="2026-01-01T00:00:00.000Z")
        self.card("SECRET-PROJECT-XYZ", source="manual", status="Backlog", priority="P3", area="SECRET-AREA", nxt="SECRET-NEXT",
                  link="https://secret.example/SECRET-LINK", created="2026-01-02T00:00:00.000Z")
        self.card("Mine stale", last="2026-08-01")
        self.card("Mine P0", owner="Jeff", priority="P0", target="2026-12-01")
        for _ in range(2):
            for extra in ([], ["--json"]):
                out, err = self.audit(*extra)
                self.assertNotRegex(out + err, r"SECRET|secret")
        out, err = self.audit()
        lines = out.splitlines()
        self.assertEqual(err, "")
        # secret card: waiting + stale + overdue (3); its twin: dup (1); p0 fires on Jeff (2 open P0) and names only the owner
        self.assertIn("- 4 more violation(s) on cards from other sources; details only in Notion (this repository is public).", lines)
        self.assertIn("- [p0] Jeff: 2 open P0 > 1", lines)
        self.assertTrue(any(ln.startswith("- [stale] Mine stale — In progress, last update 2026-08-01") for ln in lines))
        self.assertEqual(self.counts_of(out)["violations"], "6")
        res = json.loads(self.audit("--json")[0])
        self.assertEqual(res["other_source_violations"], 4)
        self.assertEqual(sorted(v["rule"] for v in res["violations"]), ["p0", "stale"])
        self.assertIn(secret, self.fake.pages)

    def test_audit_without_other_source_violations_has_no_more_line(self):
        self.card("Mine stale", last="2026-08-01")
        self.assertNotIn("more violation", self.audit()[0])

    def test_audit_source_defaults_and_flag(self):
        self.card("Elsewhere stale", source="other/handoff.md", last="2026-08-01")
        out, _ = self.audit("--source", "other/handoff.md")        # the later --source wins in argparse
        self.assertIn("[stale] Elsewhere stale", out)

    def test_audit_ignores_handoff_and_refuses_dry_run_and_needs_a_token(self):
        os.remove(self.handoff)                                     # --handoff points at a missing file: never read
        self.card("Fine")
        self.assertEqual(self.sync("--audit")[0], 0)
        self.fake.requests.clear()
        code, out, err = self.sync("--audit", "--dry-run")
        self.assertEqual(code, 4)
        self.assertEqual(self.fake.requests, [])
        code, out, err = self.sync("--audit", env={"NOTION_TOKEN": ""})
        self.assertEqual((code, out), (2, "notion-sync: off (NOTION_TOKEN not set)\n"))
        code, out, _ = self.sync("--audit", "--json", env={"NOTION_TOKEN": ""})
        self.assertEqual((code, json.loads(out)["off"]), (2, True))
        self.assertEqual(self.fake.requests, [])

    def test_audit_schema_failure_and_bad_token_are_off(self):
        schema = dict(ns.SCHEMA)
        del schema["Priority"]
        fake = FakeNotion(schema=schema)
        self.addCleanup(fake.close)
        code, out, _ = self.sync("--audit", fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Priority (select)", out)
        bad = FakeNotion(token="other")
        self.addCleanup(bad.close)
        code, out, err = self.sync("--audit", fake=bad)
        self.assertEqual(code, 2)
        self.assertNotIn(TOKEN, out + err)
        self.assertEqual(self.sync("--audit", env={"NOTION_TOKEN": "a b"})[0], 2)
        self.assertEqual(self.sync("--audit", "--today", "nope")[0], 4)
        self.assertEqual(self.sync("--audit", env={"NOTION_API_BASE": "https://evil.example"})[0], 4)


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
