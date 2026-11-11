#!/usr/bin/env python3
"""stars-jev-s2.py - github-stars-sync step 5b: ask Jev (S2 `summary_from_readme`) which star notes have a 摘要 that only
rewords the repo description, so the routine can pick them for backfill.

    stars-jev-s2.py [--today YYYY-MM-DD] [--cap N] [--budget-seconds S] [--stars-dir DIR] [--log FILE]
                    [--reference FILE] [--config FILE] [--fixtures DIR]

What it does: first `jev_ask.py probe`; unless that exits 0, Jev is off for the run and nothing is asked. Then, on a Monday
(UTC) it asks about every wiki/stars/*.md, on other days only about the notes step 5b's CJK filter does not flag (a 摘要 with
at least 20 CJK characters; the flagged ones are candidates already), oldest captured_at first, one
`jev_ask.py ask --state <file> --act-min 0.80 --defer-min 0.50` call per note. The oldest-first order starts further on each
day and wraps round (today's day number x a stride, modulo the number of notes; the stride is about one run's worth of notes
and shares no factor with their number), so whatever stops a run early, the cap or the time budget, successive runs reach
every note. The state holds exactly the fields the reference names for S2
(skills/judging-with-jev/references/vault-routine-questions.md): goal, vault_scope (the `scope:` string of
wiki/hot-list/_config.yaml), full_name, description (GitHub API), summary (the note's ## 摘要) and readme_head (the first 100
README lines). The question JSON is read from that reference, not kept here. Nothing in the vault is written: the state files go
to a fresh temp folder outside the repository.

Model and host: `jev.base_url` and `jev.model` of wiki/hot-list/_config.yaml go to jev_ask.py as --base-url / --model, for the
probe and every ask. A key the file does not have leaves jev_ask.py's default; JEV_BASE_URL / JEV_MODEL in the environment,
when set, win over the file. `jev.enabled` is not read: that key governs the hot list only.

stdout, in this order (the detail of an unexpected error goes to stderr):
    fallback exit=<n> <note> (<reason>)       one per ask that failed (jev_ask.py exit 3 or 4, 127 = it did not run or
                                              finish), as it happens; counted below
    state files: <folder>/<owner>--<repo>.json   the state sent for each note asked (not printed when none was)
    no    p=0.22 <note>[  recaptured <date>]  p < 0.50; lowest p first
    defer p=0.62 <note>[  recaptured <date>]  0.50 <= p < 0.80. A note with p >= 0.80 (act) is counted, not listed.
                                              `recaptured` = wiki/log.md has a recapture line for it from the last 30 days
    not asked, README or description unreadable: <n> (<notes>)
    not asked, past the cap of <cap> asks / <s> s: <n>
    jev: summary_from_readme <asked>/<act>/<defer>/<no>; fallbacks <n>
                                              `0/0/0/0; fallbacks 0` when there was nothing to ask: no notes, every note
                                              flagged on a non-Monday, or a cap or budget of 0
  or, in place of that last line and also as the last line:
    jev: off (<reason>)                       Jev is off for the whole run: the probe did not exit 0 or an ask exited 2
                                              (jev_ask.py's reason, whatever it is), every note it tried was unreadable
                                              (`nothing asked <n> notes unreadable`), the reference / config / log is
                                              unreadable, or an unexpected error.
<note> is printed the way the CJK filter prints it: wiki/stars/<owner>--<repo>.md.
Every line is ASCII. Text that is not one of this script's constants (a reason, a path, an option) is printed through a
whitelist: letters, digits, space and . , : / ( ) - _ = [ ] % stay, any other character becomes a space, runs of spaces
collapse, a reason is cut at 160 characters. So a `jev:` line never holds a quote, $, backtick, backslash, | & < > or a
newline, and its only ; is the fixed one before `fallbacks`: the routine can copy it between single or double quotes as it
is. A file in the stars folder whose name has a character outside A-Z a-z 0-9 . _ - is not read: it is listed as unreadable.

Exit codes:
    0  whenever the command line is accepted and stdout can be written: the routine never fails because of Jev and branches
       on the last line. (A reader that closes the pipe early ends the script like any other: BrokenPipeError, not exit 0.)
    2  bad command line

Time: the routine gives the command 600 s. No note is started after --budget-seconds (480, counted from the start, probe
included), and one note takes at most 100 s: README 3 x 10 (HEAD, main, master), description 10 (api.github.com) + 45
(read-url.sh relay), ask 15. So the worst case ends near 480 + 100 = 580 s. The probe is cut at 15 s.

Network (the system boundary): the README from raw.githubusercontent.com (HEAD, then main, then master); the repo description
from api.github.com directly, then through scripts/read-url.sh --json (Jina relay). --fixtures DIR replaces both.
Credentials: none here. jev_ask.py reads TYPESAFE_API_KEY itself; JEV_FAKE=<file> makes it answer from canned values (the file
needs a `probe` value too) with no key and no network. Python 3.9+, stdlib only.
"""
import argparse
import datetime
import glob
import math
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
CAP, BUDGET_SECONDS = 60, 480               # most asks per run; seconds from the start after which no note is started
README_SECONDS, API_SECONDS, RELAY_SECONDS, JEV_SECONDS = 10, 10, 45, 15   # hard limit per call; 3 README tries per note, so
                                            # one note <= 30 + 10 + 45 + 15 = 100 s and a run <= 480 + 100 s (docstring, Time)
README_LINES = 100                          # S2's readme_head
RECAPTURE_DAYS = 30                         # a note step 5b rewrote this recently is marked, so the routine skips it
GOAL = "decide whether this star note's summary was written from the README or only rewords the repo description"
CJK = re.compile("[%s-%s]" % (chr(0x4E00), chr(0x9FFF)))   # the same range as step 5b's CJK filter
RECAPTURE = re.compile(r"^## \[(\d{4}-\d\d-\d\d)\] recapture \|.*\| stars/(\S+)", re.M)   # the line step 5b logs per rewrite
SUMMARY = re.compile(r"##\s*摘要\s*\n+(.+?)(?=\n##|\Z)", re.S)
UNSAFE = re.compile(r"[^A-Za-z0-9 .,:/()\-_=\[\]%]")    # clean(): no quote, $, backtick, backslash, ; | & < >, newline, non-ASCII
NOTE_NAME = re.compile(r"[A-Za-z0-9._-]+\.md\Z")         # the characters GitHub allows in an owner or repo name
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


def clean(text, limit=160):
    """Text from outside this script (a reason, an option, a file name) made safe to print on one line and to copy into a
    shell command in any quoting: every character outside UNSAFE's whitelist becomes a space, runs of spaces collapse, and
    the result is cut at `limit` characters."""
    return " ".join(UNSAFE.sub(" ", str(text)).split())[:limit]


def say(line, stream=None):
    """Write one line, never raising on a stream whose encoding cannot hold a character (it comes out as \\uXXXX): the same
    way scripts/notion-sync.py writes."""
    stream = stream or sys.stdout
    enc = getattr(stream, "encoding", None) or "utf-8"
    try:
        line = line.encode(enc, "backslashreplace").decode(enc)
    except (LookupError, UnicodeError):
        line = line.encode("ascii", "backslashreplace").decode("ascii")
    stream.write(line + "\n")


def run(cmd, timeout):
    """(exit code, stdout) of a command; (127, "") when it cannot be started or does not finish in time."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return r.returncode, r.stdout


def located(option, default):
    """(the file or folder to open, the name to print for it): the option as given, or the default at the repo root."""
    return (option, option) if option else (ROOT / default, default)


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
        text = run(["curl", "-sfL", "-m", str(README_SECONDS - 2),
                    "https://raw.githubusercontent.com/%s/%s/README.md" % (full, branch)], README_SECONDS)[1]
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
        bodies = (run(cmd, limit)[1] for cmd, limit in (
            (["curl", "-sf", "-m", str(API_SECONDS - 2), url], API_SECONDS),
            (["bash", str(ROOT / "scripts/read-url.sh"), "--json", url], RELAY_SECONDS)))
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


def setting(config, key):
    """jev.<key> in the text of the config file, "" when its `jev:` block has no such key."""
    block = re.search(r"^jev:.*\n((?:[ \t#].*\n?|\n)*)", config, re.M)
    m = block and re.search(r'^[ \t]+%s:[ \t]*"?([^"\s#]+)' % key, block.group(1), re.M)
    return m.group(1) if m else ""


def recaptured(log, today):
    """{note slug: date} for the recapture lines of the log dated within RECAPTURE_DAYS of today; a line whose date is not
    a real date is skipped."""
    recent = {}
    for m in RECAPTURE.finditer(log):
        try:
            if (today - datetime.date.fromisoformat(m.group(1))).days <= RECAPTURE_DAYS:
                recent[m.group(2)] = m.group(1)
        except ValueError:
            pass
    return recent


def jev(pinned, *args):
    """(exit code of `jev_ask.py <pinned> <args>`, the JSON object it printed; {} when it printed none). 127 = it could not
    be started or did not finish within JEV_SECONDS."""
    code, stdout = run([sys.executable, str(JEV_ASK), "--timeout", str(JEV_SECONDS - 5), *pinned, *args], JEV_SECONDS)
    try:
        out = json.loads(stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {}
    return code, out if isinstance(out, dict) else {}


def stride(n, cap):
    """How many notes the start of the order moves each day: close to one run's worth (the cap when there are more notes than
    that, else a third of them) and sharing no factor with n, so the daily starts visit every position."""
    want = cap if 0 < cap < n else max(1, n // 3)
    for d in range(n):
        for s in (want - d, want + d):
            if 1 <= s < n and math.gcd(s, n) == 1:
                return s
    return 0


def ask_about_star_notes(args):
    """The whole run: probe, ask, print the report. Raises Off when Jev is off for the run."""
    t0 = time.monotonic()
    reference, reference_name = located(args.reference, REFERENCE)
    try:
        questions = json.loads(QUESTION.search(need(reference, reference_name)).group(1))
    except (AttributeError, ValueError):
        raise Off("no summary_from_readme question block in %s" % reference_name)
    config = need(*located(args.config, CONFIG))
    scope = re.search(r'^scope:\s*"(.+?)"', config, re.M)
    if not scope:
        raise Off("no scope in %s" % located(args.config, CONFIG)[1])
    today = args.today or datetime.datetime.now(datetime.timezone.utc).date()
    recent = recaptured(need(*located(args.log, LOG)), today)
    pinned = [x for option, key, env in (("--base-url", "base_url", "JEV_BASE_URL"), ("--model", "model", "JEV_MODEL"))
              if setting(config, key) and not os.environ.get(env)   # a set environment variable wins: jev_ask.py reads it
              for x in (option, setting(config, key))]
    code, out = jev(pinned, "probe")                           # on or off for the whole run, before anything is asked
    if code:                                                   # 2 = jev_ask.py says off; anything else = the probe failed
        raise Off(("" if code == 2 else "probe exit %d: " % code) + out.get("reason", "no reason printed"))
    notes, unread = [], []
    stars, stars_name = located(args.stars_dir, STARS)
    for file in glob.glob(os.path.join(stars, "*.md")):
        path = clean("%s/%s" % (stars_name.rstrip("/"), os.path.basename(file)), 300)   # as the CJK filter prints it
        if not NOTE_NAME.match(os.path.basename(file)):        # no star note has such a name; listed, never read
            unread.append(path)
            continue
        text = read(file)
        m = SUMMARY.search(text)
        flagged = not m or len(CJK.findall(m.group(1))) < 20   # the note step 5b's CJK filter prints: a candidate already
        if flagged and today.isoweekday() != 1:                # Monday (UTC) asks about every note
            continue
        notes.append((front(text, "captured_at"), path, file, front(text, "canonical_id").replace("github:", ""),
                      m.group(1).strip() if m else ""))

    out_dir = tempfile.mkdtemp(prefix="jev-s2-")               # outside the repo, so `git add -A` never sees a state file
    asked, fallbacks, left, rows = 0, 0, 0, []
    bands = {"act": 0, "defer": 0, "no": 0}
    notes.sort()                                               # oldest capture first: the thin notes date from the early runs
    if len(notes) > 1:                                         # the start moves each day, so a run the cap or the time budget
        start = today.toordinal() * stride(len(notes), args.cap) % len(notes)   # cuts short never leaves the same notes unasked
        notes = notes[start:] + notes[:start]
    for _, path, file, full, summary in notes:
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
        code, out = jev(pinned, "ask", "--state", state_file, "--act-min", S2_ACT_MIN, "--defer-min", S2_DEFER_MIN)
        if code == 2:                                          # jev_ask.py: Jev is off for the whole run
            raise Off(out.get("reason", "no reason printed"))
        asked += 1
        if code != 0 or not out.get("ok"):
            fallbacks += 1
            say("fallback exit=%d %s (%s)" % (code, path, clean(out.get("reason", "no reason printed"))))
            continue
        answer = out["answers"]["summary_from_readme"]
        bands[answer["band"]] += 1
        rows.append((answer["value"], answer["band"], path, slug))

    if asked:
        say("state files: %s/<owner>--<repo>.json" % clean(out_dir, 300))
    for p, band, path, slug in sorted(rows):
        if band != "act":
            say("%-5s p=%.2f %s%s" % (band, p, path, "  recaptured %s" % recent[slug] if slug in recent else ""))
    if unread:
        say("not asked, README or description unreadable: %d (%s)" % (len(unread), ", ".join(unread)))
    if left:
        say("not asked, past the cap of %d asks / %d s: %d" % (args.cap, args.budget_seconds, left))
    if unread and not asked and not left:                      # every note it tried was unreadable
        raise Off("nothing asked %d notes unreadable" % len(unread))
    say("jev: summary_from_readme %d/%d/%d/%d; fallbacks %d" % (asked, bands["act"], bands["defer"], bands["no"], fallbacks))


def main(argv=None):
    p = argparse.ArgumentParser(description="Ask Jev S2 summary_from_readme about the star notes (github-stars-sync step 5b). "
                                            "Probes first; exits 0 whenever the command line is accepted; the last stdout line "
                                            "starts with 'jev:' and is shell-safe ASCII. "
                                            "See the module docstring.")
    p.add_argument("--today", type=datetime.date.fromisoformat, metavar="YYYY-MM-DD",
                   help="override today's date (tests): a Monday asks about every note, and the 30-day recapture rule counts "
                        "from it (default: today, UTC)")
    p.add_argument("--cap", type=int, default=CAP, metavar="N", help="most asks per run (default %d)" % CAP)
    p.add_argument("--budget-seconds", type=int, default=BUDGET_SECONDS, metavar="S",
                   help="start no note later than this many seconds after the start (default %d)" % BUDGET_SECONDS)
    p.add_argument("--stars-dir", metavar="DIR", help="folder of star notes (default: %s at the repo root)" % STARS)
    p.add_argument("--log", metavar="FILE", help="log read for recapture lines (default: %s at the repo root)" % LOG)
    p.add_argument("--reference", metavar="FILE", help="file holding the S2 question JSON (default: %s)" % REFERENCE)
    p.add_argument("--config", metavar="FILE", help="file holding the scope: line and the jev: block's base_url and model "
                                                   "(default: %s)" % CONFIG)
    p.add_argument("--fixtures", metavar="DIR",
                   help="for tests and dry runs: read <owner>--<repo>.readme.md and <owner>--<repo>.json from DIR instead of "
                        "the network; a missing file means unreadable")
    args = p.parse_args(argv)
    try:
        ask_about_star_notes(args)
    except Off as e:
        say("jev: off (%s)" % clean(e))
    except Exception as e:                                     # never fail the routine: an unforeseen error is Jev off too
        say("stars-jev-s2: %s: %s" % (type(e).__name__, clean(e, 300)), sys.stderr)
        say("jev: off (internal error: %s)" % type(e).__name__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
