#!/usr/bin/env python3
"""Tests for skills/judging-with-jev/scripts/jev_ask.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py' -v

Every test runs the real script as a subprocess with a minimal environment: no TYPESAFE_API_KEY, no proxy variables,
and JEV_BASE_URL on a closed 127.0.0.1 port, so api.typesafe.ai is never contacted even when a test fails.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "judging-with-jev" / "scripts" / "jev_ask.py"
FAKE = ROOT / "skills" / "judging-with-jev" / "references" / "jev-fake.example.json"
NOWHERE = "http://127.0.0.1:9"          # discard port, nothing listens: a request that slips through is refused locally
ITEM = json.dumps({                     # a valid `ask` input; the example fake file answers `topical` with 0.91
    "state": {"goal": "decide whether this repo is topical", "full_name": "kepano/obsidian-skills",
              "description": "Agent Skills for Obsidian", "topics": ["agent-skills", "obsidian"]},
    "questions": {"topical": {"type": "noul", "instructions": "The repository is an agent skill or tooling built for agents."}},
})


def jev(args, env=None, stdin=None):
    """Run jev_ask.py; return (exit code, stdout parsed as JSON, or {"unparsed": stdout})."""
    full = {"PATH": os.environ.get("PATH", os.defpath), "JEV_BASE_URL": NOWHERE}
    full.update(env or {})
    p = subprocess.run([sys.executable, str(SCRIPT), *args], env=full, input=stdin, capture_output=True, text=True, timeout=30)
    try:
        return p.returncode, json.loads(p.stdout)
    except ValueError:
        return p.returncode, {"unparsed": p.stdout, "stderr": p.stderr}


class KillSwitch(unittest.TestCase):
    def assert_off_by_kill_switch(self, result):
        code, out = result
        seen = (code, out.get("ok"), out.get("off"), "JEV_DISABLED" in str(out.get("reason")))
        self.assertEqual(seen, (2, False, True, True), out)

    def test_probe_is_off_when_disabled_even_with_canned_answers(self):
        self.assert_off_by_kill_switch(jev(["probe"], {"JEV_DISABLED": "1", "JEV_FAKE": str(FAKE)}))

    def test_ask_is_off_when_disabled_even_with_canned_answers(self):
        self.assert_off_by_kill_switch(jev(["ask", "--state", "-"], {"JEV_DISABLED": "1", "JEV_FAKE": str(FAKE)}, ITEM))

    def test_disabled_is_the_reason_given_without_key_or_canned_answers(self):
        self.assert_off_by_kill_switch(jev(["probe"], {"JEV_DISABLED": "1"}))

    def test_disabled_wins_over_an_input_the_script_would_refuse(self):
        self.assert_off_by_kill_switch(jev(["ask", "--state", "-"], {"JEV_DISABLED": "1"}, "not json"))


class NotDisabled(unittest.TestCase):
    """Without the switch (unset, empty or 0) the script answers as before; 0.5 and 0.91 are the example file's values."""

    def assert_probe_answered(self, result):
        code, out = result
        self.assertEqual((code, out.get("ok"), out.get("probe")), (0, True, 0.5), out)

    def test_probe_answers_from_canned_values(self):
        self.assert_probe_answered(jev(["probe"], {"JEV_FAKE": str(FAKE)}))

    def test_zero_does_not_disable(self):
        self.assert_probe_answered(jev(["probe"], {"JEV_DISABLED": "0", "JEV_FAKE": str(FAKE)}))

    def test_empty_does_not_disable(self):
        self.assert_probe_answered(jev(["probe"], {"JEV_DISABLED": "", "JEV_FAKE": str(FAKE)}))

    def test_ask_answers_from_canned_values(self):
        code, out = jev(["ask", "--state", "-"], {"JEV_FAKE": str(FAKE)}, ITEM)
        self.assertEqual((code, out.get("ok"), out.get("answers", {}).get("topical", {}).get("value")), (0, True, 0.91), out)


if __name__ == "__main__":
    unittest.main()
