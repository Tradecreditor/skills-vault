#!/usr/bin/env python3
"""Tests for skills/auditing-agent-skills/scripts/static_scan.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py' -v

Every test runs the real script as a subprocess on a temporary skill folder and reads its exit code and JSON report;
nothing is imported from the script. Invisible characters are built with chr(), so this file stays ASCII.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "auditing-agent-skills" / "scripts" / "static_scan.py"
SKILL_MD = """---
name: demo-skill
description: Prints a greeting for a named person. Use when a greeting is wanted.
metadata:
  vault_status: "draft"
---

# demo-skill

%s
"""
BODY_LINE = 10  # the line of SKILL.md that %s lands on


class StaticScanCli(unittest.TestCase):
    def scan(self, body_line):
        """Exit code and parsed report of the scanner run on a skill folder whose SKILL.md body is body_line."""
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "demo-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(SKILL_MD % body_line, encoding="utf-8")
            p = subprocess.run([sys.executable, str(SCRIPT), str(skill)], capture_output=True, timeout=60)
        return p.returncode, json.loads(p.stdout.decode("utf-8"))

    def b1_verdict(self, body_line):
        code, report = self.scan(body_line)
        return code, report["floor"], [(f["rule"], f["file"], f["line"]) for f in report["block"]]

    def test_clean_folder_has_no_block_finding(self):
        self.assertEqual(self.b1_verdict("Say hello to the person by name."), (0, "NEEDS_REVIEW", []))

    def test_zero_width_space_is_a_b1_block_finding(self):
        self.assertEqual(self.b1_verdict("Say hel" + chr(0x200B) + "lo to the person."),
                         (1, "REJECT", [("B1", "SKILL.md", BODY_LINE)]))

    def test_hangul_filler_is_a_b1_block_finding(self):
        self.assertEqual(self.b1_verdict("Say hel" + chr(0x3164) + "lo to the person."),
                         (1, "REJECT", [("B1", "SKILL.md", BODY_LINE)]))

    def test_arabic_letter_mark_is_a_b1_block_finding(self):
        self.assertEqual(self.b1_verdict("Say hel" + chr(0x061C) + "lo to the person."),
                         (1, "REJECT", [("B1", "SKILL.md", BODY_LINE)]))

    def test_mongolian_vowel_separator_is_a_b1_block_finding(self):
        self.assertEqual(self.b1_verdict("Say hel" + chr(0x180E) + "lo to the person."),
                         (1, "REJECT", [("B1", "SKILL.md", BODY_LINE)]))

    def test_b1_excerpt_shows_the_three_characters_escaped(self):
        _, report = self.scan("pay" + chr(0x3164) + "lo" + chr(0x061C) + "ad" + chr(0x180E) + "here")
        self.assertEqual([f["excerpt"] for f in report["block"]], ["pay\\u3164lo\\u061cad\\u180ehere"])


if __name__ == "__main__":
    unittest.main()
