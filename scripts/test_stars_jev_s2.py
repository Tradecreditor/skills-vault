#!/usr/bin/env python3
"""Tests for stars-jev-s2.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py' -v

Every test runs the real script as a subprocess against a temp folder of star notes, with --fixtures for the README and
repo-description reads and JEV_FAKE for the answers. The child environment holds only PATH, TMPDIR (the test's own folder, so
the state files are cleaned up with it), JEV_BASE_URL (a closed loopback port) and, unless the test is about Jev being off,
JEV_FAKE: no network, no key.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "stars-jev-s2.py"
TUESDAY, MONDAY = "2026-11-10", "2026-11-09"
SUMMARY_ZH = "呢個工具將一段文字轉成簡報，安裝方法係一行指令，支援三種輸出格式，仲附帶十二個範例模板。"
SUMMARY_EN = "A tool that turns text into slides."
README_WITH_TOKEN = "# leaky\n\nCall it: `curl -H 'X-Auth: Bearer EXAMPLE-TOKEN-NOT-REAL' https://example.com`\n"


def state_folder(lines):
    """The folder named by the output line `state files: <folder>/<owner>--<repo>.json`."""
    line = next(ln for ln in lines if ln.startswith("state files: "))
    return line[len("state files: "):].rsplit("/", 1)[0]


class Vault:
    """A temp folder with stars/, fixtures/ and log.md, removed when the test ends."""

    def __init__(self, test):
        self.dir = Path(tempfile.mkdtemp(prefix="stars-jev-s2-test-"))
        test.addCleanup(shutil.rmtree, self.dir, True)
        self.stars, self.fixtures, self.log = self.dir / "stars", self.dir / "fixtures", self.dir / "log.md"
        self.stars.mkdir()
        self.fixtures.mkdir()
        self.log.write_text("# Log\n\n## [2026-09-19] star | acme/first | stars/acme--first\n", encoding="utf-8")

    def path(self, full):
        return "%s/%s.md" % (self.stars, full.replace("/", "--"))

    def note(self, full, summary=SUMMARY_ZH, captured="2026-09-19T11:09:28Z", readme="# tool\n\nInstall: `npx tool`\n",
             description="A tool."):
        slug = full.replace("/", "--")
        (self.stars / (slug + ".md")).write_text(
            '---\ntitle: "%s"\nslug: %s\ntype: repo\nstatus: draft\ncaptured_at: "%s"\ncanonical_id: "github:%s"\n---\n'
            "## 摘要\n\n%s\n\n## Key facts\n\n- **Language**: Python\n" % (full, slug, captured, full, summary), encoding="utf-8")
        if readme is not None:
            (self.fixtures / (slug + ".readme.md")).write_text(readme, encoding="utf-8")
        if description is not None:
            (self.fixtures / (slug + ".json")).write_text(json.dumps({"full_name": full, "description": description}),
                                                         encoding="utf-8")
        return self.path(full)

    def recapture(self, date, full):
        with open(self.log, "a", encoding="utf-8") as f:
            f.write("## [%s] recapture | %s | stars/%s\n" % (date, full, full.replace("/", "--")))

    def run(self, *args, fake=0.22, today=TUESDAY, vault_paths=True):
        env = {"PATH": os.environ["PATH"], "TMPDIR": str(self.dir), "JEV_BASE_URL": "http://127.0.0.1:9"}
        if fake is not None:
            (self.dir / "fake.json").write_text(json.dumps({"summary_from_readme": fake}), encoding="utf-8")
            env["JEV_FAKE"] = str(self.dir / "fake.json")
        paths = ["--stars-dir", str(self.stars), "--log", str(self.log)] if vault_paths else []
        cmd = [sys.executable, str(SCRIPT), *paths, "--fixtures", str(self.fixtures), "--today", today, *args]
        r = subprocess.run(cmd, env=env, cwd=self.dir, capture_output=True, text=True, encoding="utf-8", timeout=120)
        r.lines = r.stdout.splitlines()
        r.last = r.lines[-1] if r.lines else ""
        r.report = [ln for ln in r.lines if not ln.startswith("state files: ")]   # that line names a fresh temp folder
        r.state = lambda slug: json.loads(Path(state_folder(r.lines), slug + ".json").read_text(encoding="utf-8"))
        return r


class Bands(unittest.TestCase):
    def test_a_low_probability_is_counted_as_no(self):
        v = Vault(self)
        v.note("acme/thin")
        self.assertEqual(v.run(fake=0.22).last, "jev: summary_from_readme 1/0/0/1; fallbacks 0")

    def test_a_low_probability_note_is_listed_as_no(self):
        v = Vault(self)
        path = v.note("acme/thin")
        self.assertIn("no    p=0.22 " + path, v.run(fake=0.22).lines)

    def test_a_middle_probability_note_is_listed_as_defer(self):
        v = Vault(self)
        path = v.note("acme/maybe")
        self.assertIn("defer p=0.62 " + path, v.run(fake=0.62).lines)

    def test_a_high_probability_note_is_counted_as_act_and_not_listed(self):
        v = Vault(self)
        v.note("acme/fine")
        self.assertEqual(v.run(fake=0.91).report, ["jev: summary_from_readme 1/1/0/0; fallbacks 0"])


class WhichNotesAreAsked(unittest.TestCase):
    def test_a_note_the_cjk_filter_flags_is_not_asked_on_a_tuesday(self):
        v = Vault(self)
        v.note("acme/english", summary=SUMMARY_EN)
        v.note("acme/fine")
        self.assertEqual(v.run(fake=0.91, today=TUESDAY).last, "jev: summary_from_readme 1/1/0/0; fallbacks 0")

    def test_a_note_the_cjk_filter_flags_is_asked_on_a_monday(self):
        v = Vault(self)
        v.note("acme/english", summary=SUMMARY_EN)
        v.note("acme/fine")
        self.assertEqual(v.run(fake=0.91, today=MONDAY).last, "jev: summary_from_readme 2/2/0/0; fallbacks 0")

    def test_without_path_options_it_reads_the_vault_and_prints_paths_as_the_cjk_filter_does(self):
        v = Vault(self)   # empty fixtures: every real star note is unreadable, so nothing is asked and all are listed
        r = v.run(today=MONDAY, vault_paths=False)   # run from another folder: the defaults do not depend on the cwd
        self.assertRegex(r.stdout, r"(?m)^not asked, README or description unreadable: \d+ \(wiki/stars/[^/, ]+\.md[,)]")


class RecaptureGuard(unittest.TestCase):
    def test_a_note_recaptured_21_days_ago_is_marked(self):
        v = Vault(self)
        path = v.note("acme/thin")
        v.recapture("2026-10-20", "acme/thin")
        self.assertIn("no    p=0.22 %s  recaptured 2026-10-20" % path, v.run(fake=0.22, today="2026-11-10").lines)

    def test_a_note_recaptured_40_days_ago_is_not_marked(self):
        v = Vault(self)
        path = v.note("acme/thin")
        v.recapture("2026-10-01", "acme/thin")
        self.assertIn("no    p=0.22 " + path, v.run(fake=0.22, today="2026-11-10").lines)


class CostGuard(unittest.TestCase):
    def test_notes_past_the_cap_are_reported_as_not_asked(self):
        v = Vault(self)
        v.note("acme/one")
        v.note("acme/two")
        self.assertIn("not asked, past the cap of 1 asks / 480 s: 1", v.run("--cap", "1").lines)

    def test_the_oldest_capture_is_asked_first(self):
        v = Vault(self)
        v.note("acme/newer", captured="2026-10-01T08:00:00Z")
        older = v.note("zeta/older", captured="2026-09-01T08:00:00Z")
        self.assertIn("no    p=0.22 " + older, v.run("--cap", "1", fake=0.22).lines)

    def test_notes_past_the_time_budget_are_reported_as_not_asked(self):
        v = Vault(self)
        v.note("acme/one")
        self.assertIn("not asked, past the cap of 60 asks / 0 s: 1", v.run("--budget-seconds", "0").lines)


class Failures(unittest.TestCase):
    def test_a_readme_showing_a_bearer_token_is_counted_as_a_fallback_and_the_run_completes(self):
        v = Vault(self)
        v.note("acme/leaky", captured="2026-09-01T08:00:00Z", readme=README_WITH_TOKEN)
        v.note("acme/fine", captured="2026-09-02T08:00:00Z")
        self.assertEqual(v.run(fake=0.91).last, "jev: summary_from_readme 2/1/0/0; fallbacks 1")

    def test_a_refused_state_prints_a_fallback_line_with_the_exit_code_and_reason(self):
        v = Vault(self)
        path = v.note("acme/leaky", readme=README_WITH_TOKEN)
        self.assertIn("fallback exit=4 %s (state refused: Bearer token found in the state; send data fields only)" % path,
                      v.run(fake=0.91).lines)

    def test_a_reason_is_printed_without_the_characters_that_break_a_quoted_shell_argument(self):
        v = Vault(self)   # the routine copies reasons into git commit -m "...": no double quote, backtick or dollar sign
        path = v.note("acme/thin")
        (v.dir / "reference.md").write_text(
            '```json\n{"summary_from_readme": {"type": "noul", "instructions": "x"},\n'
            ' "$(id)`a`\\"b\\"": {"type": "noul", "instructions": "y"}\n}\n```\n', encoding="utf-8")
        r = v.run("--reference", str(v.dir / "reference.md"))
        self.assertIn("fallback exit=4 %s (JEV_FAKE has no canned answer for question '(id)'a''b'')" % path, r.lines)

    def test_a_note_whose_readme_cannot_be_read_is_not_a_fallback(self):
        v = Vault(self)
        v.note("acme/gone", readme=None)
        v.note("acme/fine")
        self.assertEqual(v.run(fake=0.91).last, "jev: summary_from_readme 1/1/0/0; fallbacks 0")

    def test_a_note_whose_readme_cannot_be_read_is_reported_as_not_asked(self):
        v = Vault(self)
        path = v.note("acme/gone", readme=None)
        v.note("acme/fine")
        self.assertIn("not asked, README or description unreadable: 1 (%s)" % path, v.run(fake=0.91).lines)

    def test_a_note_whose_repo_description_cannot_be_read_is_reported_as_not_asked(self):
        v = Vault(self)
        path = v.note("acme/nodesc", description=None)
        v.note("acme/fine")
        self.assertIn("not asked, README or description unreadable: 1 (%s)" % path, v.run(fake=0.91).lines)


class JevOff(unittest.TestCase):
    def test_an_unreachable_jev_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        r = v.run(fake=None)   # no JEV_FAKE, JEV_BASE_URL on a closed loopback port: jev_ask.py exits 2
        self.assertEqual((r.returncode, r.last[:33]), (0, "jev: off (cannot reach 127.0.0.1 "))

    def test_a_missing_reference_file_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        r = v.run("--reference", str(v.dir / "no-such-reference.md"))
        self.assertEqual((r.returncode, r.last[:10]), (0, "jev: off ("))

    def test_a_reference_file_without_the_s2_question_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        (v.dir / "reference.md").write_text("# Questions\n\n```json\n{\"summary_from_readme\": {\"type\": \"noul\",\n```\n",
                                            encoding="utf-8")
        r = v.run("--reference", str(v.dir / "reference.md"))
        self.assertEqual((r.returncode, r.last[:10]), (0, "jev: off ("))

    def test_a_run_that_could_ask_nothing_is_reported_as_off(self):
        v = Vault(self)
        v.note("acme/gone", readme=None)
        self.assertEqual(v.run().last, "jev: off (nothing asked: 1 notes unreadable)")

    def test_a_missing_scope_config_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        r = v.run("--config", str(v.dir / "no-such-config.yaml"))
        self.assertEqual((r.returncode, r.last[:10]), (0, "jev: off ("))

    def test_a_config_without_a_scope_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        (v.dir / "config.yaml").write_text("week_start: monday\n", encoding="utf-8")
        r = v.run("--config", str(v.dir / "config.yaml"))
        self.assertEqual((r.returncode, r.last[:10]), (0, "jev: off ("))

    def test_a_missing_log_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        v.log.unlink()   # without the log the 30-day recapture guard cannot work, so nothing is asked
        r = v.run()
        self.assertEqual((r.returncode, r.last[:10]), (0, "jev: off ("))

    def test_an_unexpected_error_ends_in_a_jev_off_line_and_exit_0(self):
        v = Vault(self)
        v.note("acme/thin")
        (v.stars / "acme--binary.md").write_bytes(b"\xff\xfe not utf-8")
        r = v.run()
        self.assertEqual((r.returncode, r.last), (0, "jev: off (internal error: UnicodeDecodeError)"))


class StateSent(unittest.TestCase):
    def test_the_state_file_holds_exactly_the_s2_fields(self):
        v = Vault(self)
        v.note("acme/thin", summary=SUMMARY_ZH, readme="# thin\n\nInstall: `npx thin`", description="A thin tool.")
        (v.dir / "config.yaml").write_text('week_start: monday\nscope: "agents and skills"\n', encoding="utf-8")
        r = v.run("--config", str(v.dir / "config.yaml"))
        self.assertEqual(r.state("acme--thin")["state"], {
            "goal": "decide whether this star note's summary was written from the README or only rewords the repo description",
            "vault_scope": "agents and skills", "full_name": "acme/thin", "description": "A thin tool.",
            "summary": SUMMARY_ZH, "readme_head": "# thin\n\nInstall: `npx thin`"})

    def test_only_the_first_100_readme_lines_are_sent(self):
        v = Vault(self)
        v.note("acme/long", readme="".join("line %d\n" % n for n in range(1, 151)))
        self.assertEqual(v.run().state("acme--long")["state"]["readme_head"].splitlines()[-1], "line 100")

    def test_the_question_sent_is_the_one_in_the_reference_file(self):
        v = Vault(self)
        v.note("acme/thin")
        (v.dir / "reference.md").write_text(
            '### S2\n\n```json\n{\n  "summary_from_readme": {\n    "type": "noul",\n    "instructions": "A test instruction."\n'
            "  }\n}\n```\n", encoding="utf-8")
        r = v.run("--reference", str(v.dir / "reference.md"))
        self.assertEqual(r.state("acme--thin")["questions"],
                         {"summary_from_readme": {"type": "noul", "instructions": "A test instruction."}})


if __name__ == "__main__":
    unittest.main()
