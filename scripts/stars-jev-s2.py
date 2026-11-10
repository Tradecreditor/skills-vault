#!/usr/bin/env python3
"""stars-jev-s2.py - github-stars-sync step 5b, J2: ask Jev (S2 `summary_from_readme`) which star notes have a 摘要 that only
rewords the repo description, so the routine can pick them for backfill.

    stars-jev-s2.py [--today YYYY-MM-DD] [--cap N] [--budget-seconds S] [--stars-dir DIR] [--log FILE]
                    [--reference FILE] [--config FILE] [--fixtures DIR]

What it does: on a Monday (UTC) it asks about every wiki/stars/*.md, on other days only about the notes step 5b's CJK filter
does not flag (a 摘要 with at least 20 CJK characters; the flagged ones are candidates already), oldest captured_at first, one
`jev_ask.py ask --state <file> --act-min 0.80 --defer-min 0.50` call per note. The state holds exactly the fields the reference
names for S2 (skills/judging-with-jev/references/vault-routine-questions.md): goal, vault_scope (the `scope:` string of
wiki/hot-list/_config.yaml), full_name, description (GitHub API), summary (the note's ## 摘要) and readme_head (the first 100
README lines). The question JSON is read from that reference, not kept here. Nothing in the vault is written: the state files go
to a fresh temp folder outside the repository.

stdout, in this order (the detail of an unexpected error goes to stderr):
    fallback exit=<n> <note> (<reason>)       one per ask that failed (jev_ask.py exit 3 or 4), as it happens; counted below
    state files: <folder>/<owner>--<repo>.json   the state sent for each note asked
    no    p=0.22 <note>[  recaptured <date>]  p < 0.50; lowest p first
    defer p=0.62 <note>[  recaptured <date>]  0.50 <= p < 0.80. A note with p >= 0.80 (act) is counted, not listed.
                                              `recaptured` = wiki/log.md has a recapture line for it from the last 30 days
    not asked, README or description unreadable: <n> (<notes>)
    not asked, past the cap of <cap> asks / <s> s: <n>
    jev: summary_from_readme <asked>/<act>/<defer>/<no>; fallbacks <n>
  or, in place of that last line and also as the last line:
    jev: off (<reason>)                       Jev is off for the whole run: an ask exited 2 (no accepted key, host not reachable,
                                              kill switch), nothing could be asked, the reference / config / log is unreadable,
                                              or an unexpected error. <reason> is one line without ", backtick or $.
<note> is printed the way the CJK filter prints it: wiki/stars/<owner>--<repo>.md.

Exit codes:
    0  always, once the command line is accepted: the routine never fails because of Jev and branches on the last line
    2  bad command line

Network (the system boundary): the README from raw.githubusercontent.com (HEAD, then main, then master); the repo description
from api.github.com directly, then through scripts/read-url.sh --json (Jina relay). --fixtures DIR replaces both.
Credentials: none here. jev_ask.py reads TYPESAFE_API_KEY itself; JEV_FAKE=<file> makes it answer from canned values with no key
and no network. Python 3.9+, stdlib only.
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JEV_ASK = ROOT / "skills/judging-with-jev/scripts/jev_ask.py"
STARS, LOG = "wiki/stars", "wiki/log.md"    # defaults are relative to the repo root, whatever the working directory
REFERENCE = "skills/judging-with-jev/references/vault-routine-questions.md"
CONFIG = "wiki/hot-list/_config.yaml"
S2_ACT_MIN, S2_DEFER_MIN = "0.80", "0.50"   # the reference's default thresholds for S2 (vault-routine-questions.md, S2)
CAP, BUDGET_SECONDS = 60, 480               # most asks per run; seconds before it stops asking
README_LINES = 100                          # S2's readme_head
RECAPTURE_DAYS = 30                         # a note step 5b rewrote this recently is marked, so the routine skips it
GOAL = "decide whether this star note's summary was written from the README or only rewords the repo description"
CJK = re.compile("[%s-%s]" % (chr(0x4E00), chr(0x9FFF)))   # the same range as step 5b's CJK filter
RECAPTURE = re.compile(r"^## \[(\d{4}-\d\d-\d\d)\] recapture \|.*\| stars/(\S+)", re.M)   # the line step 5b logs per rewrite
SUMMARY = re.compile(r"##\s*摘要\s*\n+(.+?)(?=\n##|\Z)", re.S)
QUESTION = re.compile(r'```json\n(\{\s*"summary_from_readme".+?\n\})\n```', re.S)


class Off(Exception):
    """Jev is off for the whole run; str() is the reason for the jev line."""


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def need(path, label):
    try:
        return read(path)
    except OSError:
        raise Off("cannot read %s" % label)


def front(text, key):
    m = re.search(r'^%s:\s*"?([^"\n]+)' % key, text, re.M)
    return m.group(1).strip() if m else ""


def one_line(reason):
    """A reason the routine can copy into `git commit -m "..."`: one line, ' for a double quote or backtick, no dollar sign, at
    most 160 characters."""
    return " ".join(str(reason).replace('"', "'").replace("`", "'").replace("$", "").split())[:160]


def run(cmd, timeout):
    """(exit code, stdout) of a command; (127, "") when it cannot be started or does not finish in time."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return r.returncode, r.stdout


def fixture(folder, name):
    try:
        return read(os.path.join(folder, name))
    except OSError:
        return ""


def read_readme(full, fixtures):
    """The repo's README, "" when it cannot be read. Network: raw.githubusercontent.com, HEAD then main then master."""
    if fixtures:
        return fixture(fixtures, full.replace("/", "--") + ".readme.md")
    for branch in ("HEAD", "main", "master"):
        text = run(["curl", "-sfL", "-m", "30", "https://raw.githubusercontent.com/%s/%s/README.md" % (full, branch)], 45)[1]
        if text.strip():
            return text
    return ""


def read_repo(full, fixtures):
    """The repo's GitHub API object (description, full_name), None when it cannot be read. Network: api.github.com direct
    (works locally), then scripts/read-url.sh --json (Jina relay: the cloud proxy blocks api.github.com), whose JSON carries
    the API object as a string in .data.content."""
    url = "https://api.github.com/repos/" + full
    if fixtures:
        bodies = (fixture(fixtures, full.replace("/", "--") + ".json"),)
    else:
        bodies = (run(cmd, limit)[1] for cmd, limit in ((["curl", "-sf", "-m", "20", url], 30),
                                                         (["bash", str(ROOT / "scripts/read-url.sh"), "--json", url], 200)))
    for body in bodies:
        try:
            d = json.loads(body)
            if isinstance(d.get("data"), dict):
                d = json.loads(d["data"]["content"])
            if d.get("full_name"):
                return d
        except (ValueError, KeyError, TypeError, AttributeError):
            pass
    return None


def ask(state_file):
    """(exit code of jev_ask.py, the JSON object it printed; {} when it printed none)."""
    code, stdout = run([sys.executable, str(JEV_ASK), "ask", "--state", state_file, "--act-min", S2_ACT_MIN,
                        "--defer-min", S2_DEFER_MIN], 60)
    try:
        out = json.loads(stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {}
    return code, out if isinstance(out, dict) else {}


def sync(args):
    try:
        questions = json.loads(QUESTION.search(need(args.reference or ROOT / REFERENCE, args.reference or REFERENCE)).group(1))
    except (AttributeError, ValueError):
        raise Off("no summary_from_readme question block in %s" % (args.reference or REFERENCE))
    scope = re.search(r'^scope:\s*"(.+?)"', need(args.config or ROOT / CONFIG, args.config or CONFIG), re.M)
    if not scope:
        raise Off("no scope in %s" % (args.config or CONFIG))
    today = args.today or datetime.datetime.now(datetime.timezone.utc).date()
    recent = {m.group(2): m.group(1) for m in RECAPTURE.finditer(need(args.log or ROOT / LOG, args.log or LOG))
              if (today - datetime.date.fromisoformat(m.group(1))).days <= RECAPTURE_DAYS}
    notes = []
    for file in glob.glob(os.path.join(args.stars_dir or ROOT / STARS, "*.md")):
        text = read(file)
        m = SUMMARY.search(text)
        flagged = not m or len(CJK.findall(m.group(1))) < 20   # the note step 5b's CJK filter prints: a candidate already
        if flagged and today.isoweekday() != 1:                # Monday (UTC) asks about every note
            continue
        path = "%s/%s" % ((args.stars_dir or STARS).rstrip("/"), os.path.basename(file))   # as the CJK filter prints it
        notes.append((front(text, "captured_at"), path, file, front(text, "canonical_id").replace("github:", ""),
                      m.group(1).strip() if m else ""))

    out_dir = tempfile.mkdtemp(prefix="jev-s2-")               # outside the repo, so `git add -A` never sees a state file
    t0, asked, fallbacks, left, unread, rows = time.monotonic(), 0, 0, 0, [], []
    bands = {"act": 0, "defer": 0, "no": 0}
    for _, path, file, full, summary in sorted(notes):         # oldest capture first: the thin notes date from the early runs
        if asked >= args.cap or time.monotonic() - t0 >= args.budget_seconds:
            left += 1
            continue
        readme = read_readme(full, args.fixtures)
        meta = read_repo(full, args.fixtures) if readme.strip() else None
        if not meta:
            unread.append(path)
            continue
        slug = os.path.basename(file)[:-3]
        state = {"goal": GOAL, "vault_scope": scope.group(1), "full_name": full, "description": meta.get("description") or "",
                 "summary": summary, "readme_head": "\n".join(readme.splitlines()[:README_LINES])}
        state_file = os.path.join(out_dir, slug + ".json")
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump({"state": state, "questions": questions}, f, ensure_ascii=False)
        code, out = ask(state_file)
        if code == 2:                                          # jev_ask.py: Jev is off for the whole run
            raise Off(out.get("reason", "no reason printed"))
        asked += 1
        if code != 0 or not out.get("ok"):
            fallbacks += 1
            print("fallback exit=%d %s (%s)" % (code, path, one_line(out.get("reason", "no reason printed"))))
            continue
        answer = out["answers"]["summary_from_readme"]
        bands[answer["band"]] += 1
        rows.append((answer["value"], answer["band"], path, slug))

    print("state files: %s/<owner>--<repo>.json" % out_dir)
    for p, band, path, slug in sorted(rows):
        if band != "act":
            print("%-5s p=%.2f %s%s" % (band, p, path, "  recaptured %s" % recent[slug] if slug in recent else ""))
    if unread:
        print("not asked, README or description unreadable: %d (%s)" % (len(unread), ", ".join(unread)))
    if left:
        print("not asked, past the cap of %d asks / %d s: %d" % (args.cap, args.budget_seconds, left))
    if not asked:
        raise Off("nothing asked: %d notes unreadable" % len(unread))
    print("jev: summary_from_readme %d/%d/%d/%d; fallbacks %d" % (asked, bands["act"], bands["defer"], bands["no"], fallbacks))


def main(argv=None):
    p = argparse.ArgumentParser(description="Ask Jev S2 summary_from_readme about the star notes (github-stars-sync step 5b). "
                                            "Exits 0 whenever the command line is accepted; the last stdout line starts with 'jev:'. "
                                            "See the module docstring.")
    p.add_argument("--today", type=datetime.date.fromisoformat, metavar="YYYY-MM-DD",
                   help="override today's date (tests): a Monday asks about every note, and the 30-day recapture rule counts "
                        "from it (default: today, UTC)")
    p.add_argument("--cap", type=int, default=CAP, metavar="N", help="most asks per run (default %d)" % CAP)
    p.add_argument("--budget-seconds", type=int, default=BUDGET_SECONDS, metavar="S",
                   help="stop asking after this many seconds (default %d)" % BUDGET_SECONDS)
    p.add_argument("--stars-dir", metavar="DIR", help="folder of star notes (default: %s at the repo root)" % STARS)
    p.add_argument("--log", metavar="FILE", help="log read for recapture lines (default: %s at the repo root)" % LOG)
    p.add_argument("--reference", metavar="FILE", help="file holding the S2 question JSON (default: %s)" % REFERENCE)
    p.add_argument("--config", metavar="FILE", help="file holding the scope: line (default: %s)" % CONFIG)
    p.add_argument("--fixtures", metavar="DIR",
                   help="for tests and dry runs: read <owner>--<repo>.readme.md and <owner>--<repo>.json from DIR instead of "
                        "the network; a missing file means unreadable")
    args = p.parse_args(argv)
    try:
        sync(args)
    except Off as e:
        print("jev: off (%s)" % one_line(e))
    except Exception as e:                                     # never fail the routine: an unforeseen error is Jev off too
        print("stars-jev-s2: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        print("jev: off (internal error: %s)" % type(e).__name__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
