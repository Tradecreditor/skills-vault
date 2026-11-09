#!/usr/bin/env python3
"""Tests for skills-inventory.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py' -v

Everything runs against a fake Notion server on 127.0.0.1 (NOTION_API_BASE override); api.notion.com is never contacted.
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent / "skills-inventory.py"
spec = importlib.util.spec_from_file_location("skills_inventory", SCRIPT)
si = importlib.util.module_from_spec(spec)
spec.loader.exec_module(si)

TOKEN = "ntn_SECRETTOKEN123"
DS = "11111111-2222-3333-4444-555555555555"
TODAY = "2026-11-09"
SOURCE = "proj/skills-lock.json"
OPTIONS = {"Project": ["proj"], "Scope": ["project", "global"], "Kind": ["skills-cli", "claude-plugin", "folder"],
           "Status": ["Installed", "Removed"], "Vault status": ["draft", "reviewer-approved", "verified", "deprecated", "unknown"],
           "Source": [SOURCE], "Agents": list(si.AGENT_OPTIONS)}


def normalise(props):
    out = {}
    for k, v in props.items():
        v = json.loads(json.dumps(v))
        for key in ("title", "rich_text"):
            if key in v:
                v[key] = [dict(x, plain_text=x["text"]["content"]) for x in v[key]]
        out[k] = v
    return out


class FakeNotion:
    def __init__(self, token=TOKEN, schema=None, options=None):
        self.token, self.inject, self.requests, self.pages = token, [], [], {}
        self.schema = schema or dict(si.SCHEMA)
        self.options = OPTIONS if options is None else options
        self.clock = 0
        self.search_results = [{"object": "data_source", "id": DS, "title": [{"plain_text": "Skill Installs"}]}]
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler())
        self.server.daemon_threads = True
        self.base = "http://127.0.0.1:%d" % self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def stamp(self):
        self.clock += 1
        return "2026-01-01T%02d:%02d:%02d.000Z" % (self.clock // 3600, self.clock // 60 % 60, self.clock % 60)

    def seed(self, skill, source, status="Installed", vault=False, vault_status=None, last_seen="2026-10-01", project="proj"):
        pid = "page-%d" % (len(self.pages) + 1)
        props = {"Skill": {"title": [{"type": "text", "text": {"content": skill}}]}, "Source": {"select": {"name": source}},
                 "Status": {"select": {"name": status}}, "Project": {"select": {"name": project}},
                 "Vault skill": {"checkbox": vault}, "Last seen": {"date": {"start": last_seen}},
                 "Installed": {"date": {"start": "2026-09-01"}}}
        if vault_status:
            props["Vault status"] = {"select": {"name": vault_status}}
        self.pages[pid] = {"id": pid, "url": "https://www.notion.so/" + pid, "created_time": self.stamp(),
                           "properties": normalise(props)}
        return pid

    def prop(self, pid, name):
        return self.pages[pid]["properties"].get(name)

    def writes(self):
        return [r for r in self.requests if r[0] in ("POST", "PATCH") and r[1].startswith("/v1/pages")]

    @staticmethod
    def matches(page, f):
        p = page["properties"]
        if "select" in f:
            return ((p.get(f["property"]) or {}).get("select") or {}).get("name") == f["select"]["equals"]
        if "checkbox" in f:
            return bool((p.get(f["property"]) or {}).get("checkbox")) == f["checkbox"]["equals"]
        return "".join(x["plain_text"] for x in p[f["property"]]["title"]) == f["title"]["equals"]

    def route(self, method, path, body):
        if method == "POST" and path == "/v1/search":
            return 200, {"results": self.search_results, "has_more": False}
        if method == "GET" and path == "/v1/data_sources/" + DS:
            return 200, {"object": "data_source", "id": DS, "properties": {
                n: dict({"type": t}, **({t: {"options": [{"name": o} for o in self.options.get(n, [])]}}
                                        if t in ("select", "multi_select") else {})) for n, t in self.schema.items()}}
        if method == "POST" and path == "/v1/data_sources/%s/query" % DS:
            flt = body.get("filter")
            parts = (flt.get("and") or [flt]) if flt else []
            for f in parts:
                if "select" in f and f["select"]["equals"] not in self.options.get(f["property"], []):
                    return 400, {"object": "error", "status": 400, "code": "validation_error", "message":
                                 'select option "%s" not found for property "%s".' % (f["select"]["equals"], f["property"])}
            rows = [p for p in self.pages.values() if all(self.matches(p, f) for f in parts)]
            return 200, {"results": rows, "has_more": False, "next_cursor": None}
        if method == "POST" and path == "/v1/pages":
            if body["parent"] != {"type": "data_source_id", "data_source_id": DS}:
                return 400, {"object": "error", "status": 400, "code": "validation_error", "message": "bad parent"}
            pid = "page-%d" % (len(self.pages) + 1)
            self.pages[pid] = {"id": pid, "url": "https://www.notion.so/" + pid, "created_time": self.stamp(),
                               "properties": normalise(body["properties"])}
            for name, v in body["properties"].items():
                if "select" in v and v["select"]["name"] not in self.options.get(name, []):
                    self.options = dict(self.options, **{name: self.options.get(name, []) + [v["select"]["name"]]})
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
                for i, (method, prefix, status, obj) in enumerate(fake.inject):
                    if method == self.command and self.path.startswith(prefix):
                        del fake.inject[i]
                        return self.send(status, obj)
                if headers.get("authorization") != "Bearer " + fake.token:
                    sent = headers.get("authorization", "").replace("Bearer ", "")
                    return self.send(401, {"object": "error", "status": 401, "code": "unauthorized",
                                           "message": "API token is invalid: " + sent})
                self.send(*fake.route(self.command, self.path, body))

            def send(self, status, obj):
                raw = json.dumps(obj).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            do_GET = do_POST = do_PATCH = handle_any
        return Handler


def make_skill(base, rel, name):
    d = Path(base) / rel / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text("---\nname: %s\ndescription: x. Use when y.\n---\n" % name, encoding="utf-8")
    return d


LOCK = {"version": 1, "skills": {
    "keeping-handoff-docs": {"source": "Tradecreditor/skills-vault", "sourceType": "github", "computedHash": "aaa"},
    "tdd": {"source": "mattpocock/skills", "sourceType": "github", "computedHash": "bbb", "installMode": "copy"},
    "weird": "not a dict"}}


class CollectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_skill_copy_is_identical(self):
        copy = SCRIPT.parent.parent / "skills" / "tracking-skill-installs-in-notion" / "scripts" / "skills-inventory.py"
        self.assertEqual(copy.read_bytes(), SCRIPT.read_bytes(), "edit both copies of skills-inventory.py together")

    def test_lockfile_folders_and_plugins(self):
        (self.root / "skills-lock.json").write_text(json.dumps(LOCK), encoding="utf-8")
        make_skill(self.root, ".claude/skills", "keeping-handoff-docs")
        make_skill(self.root, ".agents/skills", "keeping-handoff-docs")
        make_skill(self.root, ".claude/skills", "local-only")          # folder with no lock entry
        make_skill(self.root, "skills", "openclaw-thing")
        (self.root / ".claude" / "skills" / "not-a-skill").mkdir()      # no SKILL.md: ignored
        (self.root / ".claude").mkdir(exist_ok=True)
        (self.root / ".claude" / "settings.json").write_text(json.dumps(
            {"enabledPlugins": {"skills-vault@tradecreditor-vault": True, "off@x": False}}), encoding="utf-8")
        (self.root / ".claude" / "settings.local.json").write_text(json.dumps(
            {"enabledPlugins": {"off@x": True, "skills-vault@tradecreditor-vault": False}}), encoding="utf-8")
        rows = {r["skill"]: r for r in si.collect_project(self.root, False)}
        self.assertEqual(sorted(rows), ["keeping-handoff-docs", "local-only", "off@x", "openclaw-thing", "tdd"])
        k = rows["keeping-handoff-docs"]
        self.assertEqual((k["kind"], k["agents"], k["vault"], k["hash"]), ("skills-cli", ["claude-code", "codex"], True, "aaa"))
        self.assertEqual(k["link"], "https://github.com/Tradecreditor/skills-vault/tree/main/skills/keeping-handoff-docs")
        self.assertEqual((rows["tdd"]["agents"], rows["tdd"]["vault"]), ([], False))
        self.assertEqual((rows["local-only"]["kind"], rows["local-only"]["source_repo"]), ("folder", ""))
        self.assertEqual(rows["openclaw-thing"]["agents"], ["openclaw"])
        self.assertEqual((rows["off@x"]["kind"], rows["off@x"]["scope"]), ("claude-plugin", "project"))   # local overrides project

    def test_vault_root_skips_its_own_library_and_marks_local_source_as_vault(self):
        (self.root / "skills-lock.json").write_text(json.dumps({"version": 1, "skills": {
            "scanning-agent-skills": {"source": ".", "sourceType": "local", "computedHash": "c"}}}), encoding="utf-8")
        make_skill(self.root, "skills", "vault-capture")
        make_skill(self.root, ".claude/skills", "scanning-agent-skills")
        rows = si.collect_project(self.root, True)
        self.assertEqual([r["skill"] for r in rows], ["scanning-agent-skills"])
        self.assertTrue(rows[0]["vault"])
        self.assertIsNone(rows[0]["link"])
        self.assertFalse(si.collect_project(self.root, False)[0]["vault"])   # "." outside the vault is not a vault skill

    def test_global_scan(self):
        home = self.root
        make_skill(home, ".claude/skills", "security-audit")
        make_skill(home, ".gemini/skills", "security-audit")
        make_skill(home, ".cursor/skills", "other-one")
        (home / ".claude" / "plugins").mkdir(parents=True)
        (home / ".claude" / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
            "skills-vault@tradecreditor-vault": [{"version": "abc123def456", "scope": "user"}],
            "flat@m": {"version": "1.0.0"}}}), encoding="utf-8")
        (home / ".claude" / "plugins" / "known_marketplaces.json").write_text(json.dumps({
            "tradecreditor-vault": {"source": {"source": "github", "repo": "Tradecreditor/skills-vault"}}}), encoding="utf-8")
        (home / ".claude" / "settings.json").write_text(json.dumps({"enabledPlugins": {"flat@m": True}}), encoding="utf-8")
        rows = {r["skill"]: r for r in si.collect_global(home)}
        self.assertEqual(sorted(rows), ["flat@m", "other-one", "security-audit", "skills-vault@tradecreditor-vault"])
        self.assertEqual(rows["security-audit"]["agents"], ["claude-code", "gemini-cli"])
        self.assertEqual(rows["other-one"]["agents"], ["cursor"])
        p = rows["skills-vault@tradecreditor-vault"]
        self.assertEqual((p["kind"], p["scope"], p["hash"], p["vault"], p["source_repo"]),
                         ("claude-plugin", "global", "abc123def456", False, "Tradecreditor/skills-vault"))   # provenance only
        self.assertEqual(rows["flat@m"]["hash"], "1.0.0")

    def test_bad_lockfile_is_exit_3_and_missing_lockfile_is_fine(self):
        (self.root / "skills-lock.json").write_text("{not json", encoding="utf-8")
        with self.assertRaises(si.Stop) as cm:
            si.collect_project(self.root, False)
        self.assertEqual(cm.exception.code, 3)
        (self.root / "skills-lock.json").unlink()
        self.assertEqual(si.collect_project(self.root, False), [])

    def test_github_source_shapes(self):
        for src, want in (("Tradecreditor/skills-vault", "Tradecreditor/skills-vault"),
                          ("https://github.com/o/r.git", "o/r"), ("https://github.com/o/r/tree/main/skills/x", "o/r"),
                          (".", None), ("./local", None), ("https://example.com/a/b", None), ("", None)):
            self.assertEqual(si.github_repo(src), want, src)
        self.assertTrue(si.is_vault("https://github.com/tradecreditor/skills-vault", False))

    def test_vault_statuses_from_readme(self):
        readme = SCRIPT.parent.parent / "skills" / "README.md"
        statuses = si.vault_statuses(SCRIPT.parent.parent)
        self.assertIn("vault-capture", statuses)
        self.assertEqual(statuses["vault-capture"], "verified")
        folders = {p.name for p in (SCRIPT.parent.parent / "skills").iterdir() if (p / "SKILL.md").is_file()}
        self.assertTrue(folders <= set(statuses) | {"tracking-skill-installs-in-notion"}, folders - set(statuses))
        self.assertTrue(readme.is_file())


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fake = FakeNotion()
        self.addCleanup(self.fake.close)
        for name, val in (("MIN_INTERVAL", 0), ("BACKOFF", (0, 0, 0))):
            patcher = mock.patch.object(si, name, val)
            patcher.start()
            self.addCleanup(patcher.stop)
        (self.root / "skills-lock.json").write_text(json.dumps(LOCK), encoding="utf-8")
        make_skill(self.root, ".claude/skills", "keeping-handoff-docs")

    def run_cli(self, *extra, env=None, fake=None, base_args=True):
        fake = fake or self.fake
        environ = {k: v for k, v in os.environ.items() if not k.startswith("NOTION_")}
        environ.update({"NOTION_TOKEN": TOKEN, "NOTION_API_BASE": fake.base}, **(env or {}))
        argv = (["--root", str(self.root), "--project", "proj", "--source", SOURCE, "--today", TODAY] if base_args else []) + list(extra)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, environ, clear=True), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = si.main(argv)
        return code, out.getvalue(), err.getvalue()

    def summary(self, out, **counts):
        want = dict(created=0, updated=0, removed=0, unchanged=0, failed=0)
        want.update(counts)
        self.assertEqual(out, "skills-inventory: created={created} updated={updated} removed={removed} unchanged={unchanged} "
                              "failed={failed} source=proj/skills-lock.json data_source=11111111\n".format(**want))

    def test_first_run_creates_then_second_is_idempotent_then_removal_and_return(self):
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.summary(out, created=2)
        page = next(p for p in self.fake.pages.values() if p["properties"]["Skill"]["title"][0]["plain_text"] == "keeping-handoff-docs")
        props = page["properties"]
        self.assertEqual(props["Installed"]["date"]["start"], TODAY)
        self.assertEqual(props["Vault skill"]["checkbox"], True)
        self.assertEqual([o["name"] for o in props["Agents"]["multi_select"]], ["claude-code"])
        self.assertEqual(props["Source"]["select"]["name"], SOURCE)
        self.assertNotIn("Vault status", props)                      # never written by a project run
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.summary(out, unchanged=2)
        # the skill leaves the lockfile and the folder: Removed, never deleted; Installed date kept
        (self.root / "skills-lock.json").write_text(json.dumps({"version": 1, "skills": {"tdd": LOCK["skills"]["tdd"]}}), encoding="utf-8")
        shutil.rmtree(self.root / ".claude" / "skills" / "keeping-handoff-docs")
        code, out, _ = self.run_cli("--today", "2026-11-10")
        self.summary(out, removed=1, unchanged=0, updated=1)         # tdd's Last seen moved forward
        self.assertEqual(props["Status"]["select"]["name"], "Removed")
        self.assertEqual(props["Installed"]["date"]["start"], TODAY)
        self.assertEqual(len(self.fake.pages), 2)
        # it comes back: same row goes back to Installed
        (self.root / "skills-lock.json").write_text(json.dumps(LOCK), encoding="utf-8")
        code, out, _ = self.run_cli("--today", "2026-11-11")
        self.summary(out, updated=2)
        self.assertEqual(props["Status"]["select"]["name"], "Installed")
        self.assertEqual(props["Last seen"]["date"]["start"], "2026-11-11")

    def test_last_seen_only_moves_forward_and_other_sources_untouched(self):
        other = self.fake.seed("keeping-handoff-docs", "other/skills-lock.json", project="other")
        self.fake.seed("keeping-handoff-docs", SOURCE, last_seen="2026-12-01")
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.prop(other, "Status")["select"]["name"], "Installed")
        self.assertEqual(self.fake.prop("page-2", "Last seen")["date"]["start"], "2026-12-01")
        self.assertTrue(all("page-1" not in r[1] for r in self.fake.writes()))

    def test_dry_run_reads_but_never_writes(self):
        code, out, err = self.run_cli("--dry-run")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("skills-inventory: dry-run rows=2 created=2"), out)
        self.assertEqual(self.fake.writes(), [])
        self.assertIn("dry-run create 'tdd'", err)

    def test_missing_fixed_option_is_off_but_new_project_option_is_fine(self):
        fake = FakeNotion(options=dict(OPTIONS, Status=["Installed"], Project=[]))
        self.addCleanup(fake.close)
        self.fake.seed("gone", SOURCE)
        code, out, _ = self.run_cli(fake=fake)
        self.assertEqual((code, out), (0, "skills-inventory: created=2 updated=0 removed=0 unchanged=0 failed=0 "
                                           "source=proj/skills-lock.json data_source=11111111\n"))
        fake2 = FakeNotion(options=dict(OPTIONS, Kind=["folder"]))
        self.addCleanup(fake2.close)
        code, out, _ = self.run_cli(fake=fake2)
        self.assertEqual(code, 2)
        self.assertIn("Kind option 'skills-cli' missing", out)
        self.assertEqual(fake2.writes(), [])

    def test_401_is_off_and_never_leaks_the_token(self):
        fake = FakeNotion(token="ntn_OTHER")
        self.addCleanup(fake.close)
        code, out, err = self.run_cli(fake=fake)
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("skills-inventory: off (HTTP 401"), out)
        self.assertNotIn(TOKEN, out + err)
        self.assertIn("***", out)

    def test_schema_mismatch_and_not_found_are_off(self):
        fake = FakeNotion(schema={k: v for k, v in si.SCHEMA.items() if k != "Vault skill"})
        self.addCleanup(fake.close)
        code, out, _ = self.run_cli(fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("Vault skill (checkbox)", out)
        fake.search_results = []
        fake.schema = dict(si.SCHEMA)
        code, out, _ = self.run_cli(fake=fake)
        self.assertEqual(code, 2)
        self.assertIn("not found", out)

    def test_partial_failure_exits_1(self):
        self.fake.inject.append(("POST", "/v1/pages", 400, {"object": "error", "status": 400, "code": "validation_error", "message": "no"}))
        code, out, _ = self.run_cli()
        self.assertEqual(code, 1)
        self.summary(out, created=1, failed=1)

    def test_bad_flags_exit_4_and_foreign_base_refused(self):
        self.assertEqual(self.run_cli("--audit", "--dry-run")[0], 4)
        self.assertEqual(self.run_cli("--audit", "--enrich")[0], 4)
        self.assertEqual(self.run_cli("--today", "2026-13-01")[0], 4)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(si.main(["--nope"]), 4)
        code, _, err = self.run_cli(env={"NOTION_API_BASE": "https://evil.example"})
        self.assertEqual(code, 4)
        self.assertIn("NOTION_API_BASE", err)

    def test_bad_lockfile_is_exit_3(self):
        (self.root / "skills-lock.json").write_text("{", encoding="utf-8")
        code, _, err = self.run_cli()
        self.assertEqual(code, 3)
        self.assertIn("skills-lock.json", err)

    def test_json_output(self):
        code, out, _ = self.run_cli("--json")
        res = json.loads(out)
        self.assertEqual((code, res["ok"], res["exit"], res["counts"]["created"]), (0, True, 0, 2))
        self.assertEqual(res["plan"]["create"], ["keeping-handoff-docs", "tdd"])

    def test_default_source_follows_project_label(self):
        class A:
            global_scope, project, source, root = False, None, None, str(self.root)
        self.assertEqual(si.default_labels(A), (self.root.name, f"{self.root.name}/skills-lock.json"))
        A.project = "alice-app"
        self.assertEqual(si.default_labels(A), ("alice-app", "alice-app/skills-lock.json"))
        A.source = "custom"
        self.assertEqual(si.default_labels(A), ("alice-app", "custom"))

    def test_global_run_labels(self):
        # "global:laptop" is not yet a Source option: Notion would 400 on a filter for it, so the first run must not query by it
        home = self.root / "home"
        make_skill(home, ".claude/skills", "security-audit")
        code, out, err = self.run_cli("--global", "--home", str(home), "--project", "global:laptop", "--today", TODAY, base_args=False)
        self.assertEqual((code, out.startswith("skills-inventory: created=1 ")), (0, True), out + err)
        self.assertIn("Source option 'global:laptop' is new", err)
        self.assertIn("source=global:laptop", out)
        code, out, _ = self.run_cli("--global", "--home", str(home), "--project", "global:laptop", "--today", TODAY, base_args=False)
        self.assertTrue(out.startswith("skills-inventory: created=0 updated=0 removed=0 unchanged=1"), out)   # option exists now
        page = next(iter(self.fake.pages.values()))["properties"]
        self.assertEqual((page["Project"]["select"]["name"], page["Scope"]["select"]["name"]), ("global:laptop", "global"))

    def test_enrich_sets_vault_status_across_sources_only_for_vault_rows(self):
        vault = self.root / "vault"
        (vault / "skills").mkdir(parents=True)
        (vault / "skills" / "README.md").write_text(
            "| name | vault_status | origin_type | what |\n|---|---|---|---|\n| a-skill | verified | x | y |\n"
            "| b-skill | draft | x | y |\n", encoding="utf-8")
        a = self.fake.seed("a-skill", SOURCE, vault=True)
        b = self.fake.seed("b-skill", "other/skills-lock.json", vault=True, vault_status="draft")
        c = self.fake.seed("c-skill", "other/skills-lock.json", vault=True)
        d = self.fake.seed("tdd", SOURCE, vault=False)
        # bare folders: a vault name with no source is recognised, a foreign name or a known source is not
        e = self.fake.seed("b-skill", "global:pc", vault=False)
        self.fake.pages[e]["properties"]["Kind"] = {"select": {"name": "folder"}}
        f = self.fake.seed("b-skill", "global:other", vault=False)
        self.fake.pages[f]["properties"]["Kind"] = {"select": {"name": "folder"}}
        self.fake.pages[f]["properties"]["Source repo"] = normalise({"x": {"rich_text": [{"type": "text", "text": {"content": "someone/else"}}]}})["x"]
        g = self.fake.seed("frontend-design", "global:pc", vault=False)
        self.fake.pages[g]["properties"]["Kind"] = {"select": {"name": "folder"}}
        code, out, _ = self.run_cli("--enrich", "--vault", str(vault), base_args=False)
        self.assertEqual(code, 0)
        self.assertEqual(out, "skills-inventory: enriched=3 unchanged=1 failed=0 vault_skills=2 data_source=11111111\n")
        self.assertEqual((self.fake.prop(e, "Vault skill")["checkbox"], self.fake.prop(e, "Vault status")["select"]["name"]), (True, "draft"))
        self.assertFalse(self.fake.prop(f, "Vault skill")["checkbox"])
        self.assertFalse(self.fake.prop(g, "Vault skill")["checkbox"])
        self.assertEqual(self.fake.prop(a, "Vault status")["select"]["name"], "verified")
        self.assertEqual(self.fake.prop(b, "Vault status")["select"]["name"], "draft")
        self.assertEqual(self.fake.prop(c, "Vault status")["select"]["name"], "unknown")
        self.assertIsNone(self.fake.prop(d, "Vault status"))
        code, out, _ = self.run_cli("--enrich", "--vault", str(vault), "--dry-run", base_args=False)
        self.assertEqual(out, "skills-inventory: dry-run enriched=0 unchanged=4 failed=0 vault_skills=2 data_source=11111111\n")
        code, out, _ = self.run_cli("--enrich", "--vault", str(self.root / "nowhere"), base_args=False)
        self.assertEqual(code, 3)

    def test_audit_names_only_this_sources_rows(self):
        self.fake.seed("draft-one", SOURCE, vault=True, vault_status="draft", last_seen=TODAY)
        self.fake.seed("old-one", SOURCE, last_seen="2026-09-01")
        self.fake.seed("fine", SOURCE, vault=True, vault_status="verified", last_seen=TODAY)
        self.fake.seed("no-status", "other/skills-lock.json", vault=True, last_seen=TODAY, project="other")
        self.fake.seed("gone", SOURCE, status="Removed")
        code, out, _ = self.run_cli("--audit")
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(lines[0], "skills-audit: rows=5 installed=4 projects=2 violations=4 draft-installed=2 stale=1 "
                                   "unknown-vault=1 removed=1")
        self.assertIn("- [draft-installed] draft-one @ proj — vault skill with status draft is installed", lines)
        self.assertIn("- [stale] old-one @ proj — last seen 2026-09-01 (69 days): run the inventory in that project", lines)
        self.assertFalse(any("no-status" in ln for ln in lines))
        self.assertEqual(lines[-1], "- 2 more violation(s) on rows from other projects; details only in Notion (this repository is public).")
        self.assertEqual(self.fake.writes(), [])

    def test_if_changed_skips_offline_until_state_changes_or_ages(self):
        state = str(self.root / "state")
        code, out, _ = self.run_cli("--if-changed", env={"SKILLS_INVENTORY_STATE": state})
        self.assertEqual(code, 0)
        self.summary(out, created=2)
        n = len(self.fake.requests)
        code, out, _ = self.run_cli("--if-changed", env={"SKILLS_INVENTORY_STATE": state})
        self.assertEqual((code, out), (0, "skills-inventory: unchanged since the last run (--if-changed) rows=2 source=proj/skills-lock.json\n"))
        self.assertEqual(len(self.fake.requests), n)                        # no network at all
        make_skill(self.root, ".agents/skills", "tdd")                      # a change: runs again
        code, out, _ = self.run_cli("--if-changed", env={"SKILLS_INVENTORY_STATE": state})
        self.summary(out, updated=1, unchanged=1)
        stamp = next((self.root / "state").iterdir())
        st = json.loads(stamp.read_text(encoding="utf-8"))
        st["ran_at"] -= si.IF_CHANGED_MAX_AGE + 1                           # too old: runs again even if unchanged
        stamp.write_text(json.dumps(st), encoding="utf-8")
        code, out, _ = self.run_cli("--if-changed", env={"SKILLS_INVENTORY_STATE": state})
        self.summary(out, unchanged=2)
        code, out, _ = self.run_cli("--if-changed", "--dry-run", env={"SKILLS_INVENTORY_STATE": state})
        self.assertTrue(out.startswith("skills-inventory: dry-run rows=2"), out)   # dry-run never skips, never stamps
        bad = FakeNotion(token="ntn_OTHER")
        self.addCleanup(bad.close)
        (self.root / "skills-lock.json").write_text("{}", encoding="utf-8")
        code, out, _ = self.run_cli("--if-changed", env={"SKILLS_INVENTORY_STATE": state}, fake=bad)
        self.assertEqual(code, 2)                                           # a failed run leaves no stamp
        code, out, _ = self.run_cli("--if-changed", env={"SKILLS_INVENTORY_STATE": state})
        self.assertTrue(out.startswith("skills-inventory: created=0 updated=2 removed=0"), out)   # both became bare folders

    def test_global_label_from_environment(self):
        class A:
            global_scope, project, source, root = True, None, None, None
        with mock.patch.dict(os.environ, {"SKILLS_INVENTORY_GLOBAL_LABEL": "global:jeff-pc"}):
            self.assertEqual(si.default_labels(A), ("global:jeff-pc", "global:jeff-pc"))
        with mock.patch.dict(os.environ, {"SKILLS_INVENTORY_GLOBAL_LABEL": ""}):
            self.assertTrue(si.default_labels(A)[0].startswith("global:"))

    def test_unexpected_exception_is_one_scrubbed_line(self):
        with mock.patch.object(si, "collect_project", side_effect=RuntimeError("boom " + TOKEN)):
            code, out, err = self.run_cli()
        self.assertEqual(code, 2)
        self.assertEqual(out, "skills-inventory: off (internal error: RuntimeError: boom ***)\n")
        self.assertNotIn(TOKEN, out + err)


if __name__ == "__main__":
    unittest.main()
