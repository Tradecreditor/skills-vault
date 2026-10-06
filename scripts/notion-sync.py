#!/usr/bin/env python3
"""notion-sync.py - one-way mirror of handoff.md "## In flight" into the Notion data source "Project Status", plus a read-only
board-policy audit (--audit).

    notion-sync.py [--handoff PATH] [--source LABEL] [--area LABEL] [--repo-url URL]
                   [--data-source ID] [--dry-run] [--json] [--today YYYY-MM-DD]
    notion-sync.py --audit [--json] [--today YYYY-MM-DD] [--source LABEL] [--data-source ID]

Sync: each In flight row becomes (or updates) one Notion row keyed by its Project title and tagged with the Source label; rows
that left the table are set to Done (a row already Done or Dropped is left alone, and a Done / Dropped card is never moved back
out of its column: a row that says otherwise only warns on stderr; rename the Workstream to open a new card). Rows of another
Source are never touched,
nothing is deleted or archived, the schema is never changed (a Status / Priority / Owner / Area / Source option the plan needs
must already exist). A create is never blindly retried: after a timeout / 409 / 5xx the data source is queried first, so a page
that did land is not created twice. Extra copies of one card (same Source and Project) are set to Done, pointing at the oldest
one (copies already Done or Dropped are skipped). stdout: one summary line (or one JSON object with --json); details go to stderr.

In flight columns: Workstream (required); State, Next step, Detail; and optionally Status, Priority, Owner (header names are
case-insensitive, order is free). Status: Backlog | In progress | Waiting on Josep (or Waiting) | Blocked | Done | Dropped. Owner:
Josep | Claude Code | Routine. Priority: P0..P3. A valid Status / Owner overrides the rules derived from State and Next step; an
empty one uses the rules; an unknown one warns on stderr and uses the rules. An empty or unknown Priority is not written on an
update (the value in Notion is left alone) and is created as P2, the board-policy default. A status change also sets Last update
to the handoff date (Last update only moves forward). A Dropped row gets Next step "Dropped: <first sentence of State>" and a
warning when it has no reason. Target date (optional Notion property) is never written by the sync.

--audit (needs NOTION_TOKEN; never parses handoff.md, never writes): reads every card of the data source and checks the board
policy (skills/tracking-projects-in-notion/references/board-policy.md): wip, p0, missing, stale, waiting, blocked, target,
overdue, evidence (Done with no Link, with only the handoff.md fallback Link, or closed by leaving In flight), dropped, dup;
`missing` covers Owner, Next step, Priority, Area, Status (empty or not a policy column), Project and Last update. Output is public-safe: titles are printed only for cards whose Source equals this run's source
label; every other card appears as a count. Violations are reported, not failures: exit 0 whenever the audit ran.

Exit codes (the routine branches on these, never on the message text):
    0  ok (also: dry-run ok, audit ran)
    1  partial: some writes failed after retries, the others are done
    2  sync OFF for this run: NOTION_TOKEN missing (not --dry-run) or malformed, 401/403 (also on a write: the run stops at
       once), data source not found or not shared, ambiguous search (set NOTION_PROJECTS_DS), schema missing a property (Priority
       is required, Target date is not), a wrong type or a needed select option, host unreachable, any failed read, an
       unexpected internal error
    3  handoff parse error: file missing, no "## In flight" section, no table, no Workstream column
    4  refused locally: bad NOTION_API_BASE override, bad NOTION_VERSION, bad --today, bad command line (also --audit with
       --dry-run)

Credentials: NOTION_TOKEN (Bearer header to the API base only, never printed). NOTION_API_BASE may only be
http://127.0.0.1:<port> or http://localhost:<port> (tests). Optional: NOTION_VERSION (YYYY-MM-DD), NOTION_PROJECTS_DS (data source id). Python 3.9+, stdlib only.
"""
import argparse
import datetime
import http.client
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE = "https://api.notion.com"
DEFAULT_VERSION = "2026-03-11"
LOCAL_BASE = re.compile(r"^http://(127\.0\.0\.1|localhost):\d+/?$")
MIN_INTERVAL = 0.34                 # seconds between requests (~3 per second)
BACKOFF = (1, 2, 4)                 # retry delays; also the retry count
RETRY_AFTER_MAX = 30
TIMEOUT = 30
DS_TITLE = "Project Status"
SCHEMA = {"Project": "title", "Status": "select", "Priority": "select", "Area": "select", "Next step": "rich_text",
          "Owner": "select", "Link": "url", "Last update": "date", "Source": "select"}
TARGET_DATE = "Target date"         # optional date property: read by --audit, never required, never written
STATUSES = ("Backlog", "In progress", "Waiting on Josep", "Blocked", "Done", "Dropped")
OWNERS = ("Josep", "Claude Code", "Routine")
PRIORITIES = ("P0", "P1", "P2", "P3")
DEFAULT_PRIORITY = "P2"             # board policy section 2: a new card without a Priority gets P2 (never applied to an update)
CLOSED = ("Done", "Dropped")
STATUS_WORDS = dict({s.lower(): s for s in STATUSES}, waiting="Waiting on Josep")
OWNER_WORDS = {o.lower(): o for o in OWNERS}
PRIORITY_WORDS = {p.lower(): p for p in PRIORITIES}
WIP_LIMITS = {"Josep": 3, "Claude Code": 5}                                         # board policy section 5
STALE_DAYS = {"In progress": 14, "Blocked": 14, "Waiting on Josep": 7}              # board policy section 5
RULES = ("wip", "p0", "missing", "stale", "waiting", "blocked", "target", "overdue", "evidence", "dropped", "dup")
NO_NEXT = {"none", "—", "-", "n/a", "nothing"}
PATH_EXT = (".md", ".yaml", ".yml", ".py", ".json", ".sh")
DATE_RE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
VERSION_BEFORE = re.compile(r"(?<![A-Za-z])(?:version|v)[ -]?$", re.I)     # "Notion-Version 2026-03-11", "v2026-03-11"
TOKEN_RE = re.compile(r"[\x21-\x7e]+")
VERSION_RE = re.compile(r"\d{4}-\d{2}-\d{2}", re.A)
HANDOFF_LINK = re.compile(r"/blob/[^/?#]+/handoff\.md(?:[?#].*)?$", re.I)     # link_of's last-resort fallback: not evidence
URL_STOP = re.compile(r"[\s)>\]`<*\"'|]")
MAX_URL = 2000
_last_request = [0.0]


class Stop(Exception):
    def __init__(self, code, reason):
        super().__init__(scrub(reason))
        self.code = code


class ApiError(Exception):
    def __init__(self, status, code, message):
        super().__init__(scrub(f"HTTP {status} {code}: {message}")[:300])      # scrub first: a cut token would slip through
        self.status = status


class Unreachable(Exception):
    def __init__(self, message, ambiguous=False):
        super().__init__(message)
        self.ambiguous = ambiguous                  # the request may have been processed (timeout, dropped connection)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):   # never forward the Authorization header anywhere else
        return None


def scrub(text):
    token = os.environ.get("NOTION_TOKEN", "").strip()
    return text.replace(token, "***") if token else text


def log(msg):
    emit("notion-sync: " + scrub(msg) + "\n", sys.stderr)


def emit(text, stream=None):
    """Write text in one piece, never raising on a stream whose encoding cannot hold a character (a card title, an em dash):
    such characters come out as \\uXXXX instead of crashing a half-printed report."""
    stream = stream or sys.stdout
    enc = getattr(stream, "encoding", None) or "utf-8"
    try:
        text = text.encode(enc, "backslashreplace").decode(enc)
    except (LookupError, UnicodeError):
        text = text.encode("ascii", "backslashreplace").decode("ascii")
    stream.write(text)


# ---------------------------------------------------------------- parsing handoff.md

def split_row(line, protect=True):
    s, cells, buf, tick, i = line.strip(), [], [], False, 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and s[i + 1:i + 2] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "`" and protect:
            tick = not tick
        if ch == "|" and not tick:
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    if tick:                                        # unbalanced backtick: do not let it swallow the row
        return split_row(line, False)
    cells.append("".join(buf))
    if s.startswith("|") and cells[0].strip() == "":
        cells = cells[1:]
    if s.endswith("|") and cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return cells


def clean(text):
    t = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    t = re.sub(r"\[\[([^\]|]*)(?:\|([^\]]*))?\]\]", lambda m: m.group(2) or m.group(1), t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    for junk in ("**", "__", "`"):
        t = t.replace(junk, "")
    return re.sub(r"\s+", " ", t).strip()


def trim_project(text):
    """Drop ONE trailing balanced top-level parenthetical group, then trailing dashes/colons."""
    if text.endswith(")"):
        depth = 0
        for i in range(len(text) - 1, -1, -1):
            if text[i] == ")":
                depth += 1
            elif text[i] == "(":
                depth -= 1
                if depth == 0:
                    text = text[:i] if i > 0 and text[i - 1].isspace() else text    # "f(x)" is a name, not a note
                    break
    return text.rstrip(" —-:")[:200]


def classify(state, nxt):
    s, n = state.lower(), nxt.lower()
    if not n or n in NO_NEXT or n.startswith(("done", "fixed", "closed")):
        return "Done"
    if s.startswith(("done", "closed", "finished")) and not n.startswith("josep"):
        return "Done"
    if s.startswith("blocked") or n.startswith("blocked"):
        return "Blocked"
    if s.startswith("not started"):
        return "Backlog"
    if n.startswith("josep"):
        return "Waiting on Josep"
    return "In progress"


def owner_of(nxt):
    n = nxt.lower()
    if n.startswith("josep"):
        return "Josep"
    return "Routine" if n.startswith(("routine", "next scheduled run")) else "Claude Code"


def next_step_of(status, state, nxt):
    if status in CLOSED and (not nxt or nxt.lower() in NO_NEXT):
        first = re.split(r"(?<=[.!?])\s", state, maxsplit=1)[0] if state else ""
        text = (f"{status}: {first}" if status == "Dropped" else f"{status} — {first}") if first else status
    else:
        text = nxt
    return text if len(text) <= 1900 else text[:1899] + "…"


def explicit(project, column, raw, words, fallback):
    """The canonical value of an explicit handoff cell, or None when it is empty or unknown (unknown warns)."""
    value = clean(raw)
    if not value:
        return None
    found = words.get(value.lower())
    if not found:
        log(f"warn: row '{project}': unknown {column} '{value[:80]}'; {fallback}")
    return found


def valid_dates(text, skip_versions=False):
    out = []
    for m in DATE_RE.finditer(text):
        if skip_versions and VERSION_BEFORE.search(text[:m.start()]):
            continue
        try:
            datetime.date.fromisoformat(m.group(0))
            out.append(m.group(0))
        except ValueError:
            pass
    return out


def repo_path(span):
    s = span.strip()
    if not s or re.search(r"[\s\[\]<>|*?{}\"'\\]", s) or s.startswith(("/", "~", "-", "http")):
        return None
    s = re.sub(r":\d+(?:-\d+)?$", "", re.sub(r"#.*$", "", s))
    s = s[2:] if s.startswith("./") else s
    if not s or ".." in s.split("/"):
        return None
    return s if ("/" in s or s.endswith(PATH_EXT)) else None


def urls_in(detail):
    """http(s) URLs of a Detail cell, left to right. A markdown link keeps its balanced parentheses; a bare URL stops at
    whitespace or any of ) > ] ` < * " ' | and loses trailing * _ . , ; :. URLs over MAX_URL chars are dropped."""
    for m in re.finditer(r"https?://", detail):
        start, i = m.start(), m.start()
        if detail[max(0, start - 2):start] == "](":
            depth = 0
            while i < len(detail) and not detail[i].isspace():
                if detail[i] == "(":
                    depth += 1
                elif detail[i] == ")":
                    if depth == 0:
                        break
                    depth -= 1
                i += 1
            url = detail[start:i]
        else:
            stop = URL_STOP.search(detail, start)
            url = detail[start:stop.start() if stop else len(detail)].rstrip("*_.,;:")
        if len(url) <= MAX_URL and not re.fullmatch(r"https?://", url):
            yield url


def link_of(detail, row_text, repo_url):
    detail = re.sub(r"<br\s*/?>", " ", detail, flags=re.I)
    url = next(urls_in(detail), None)
    if url:
        return url
    if not repo_url:
        return None
    for span in re.findall(r"`([^`]+)`", detail):
        path = repo_path(span)
        if path:
            kind = "tree" if path.endswith("/") else "blob"
            return f"{repo_url}/{kind}/main/{urllib.parse.quote(path, safe='/@+,=:~')}"
    m = re.search(r"PR\s*#(\d+)", row_text)
    return f"{repo_url}/pull/{m.group(1)}" if m else f"{repo_url}/blob/main/handoff.md"


def parse_handoff(text, today, repo_url):
    """Return (handoff_date, rows). Raises Stop(3) when the file has no usable In flight table."""
    lines = text.splitlines()
    handoff_date = today
    for ln in lines:
        if re.match(r"[\s>*_]*Last updated:", ln):
            handoff_date = (valid_dates(ln) or [today])[0]
            break
    start = next((i for i, ln in enumerate(lines) if re.match(r"## In flight\b", ln)), None)
    if start is None:
        raise Stop(3, "no '## In flight' section in the handoff")
    table = []
    for ln in lines[start + 1:]:
        if ln.startswith("## "):
            break
        if ln.lstrip().startswith("|"):
            table.append(ln)
        elif table:
            break
    if not table:
        raise Stop(3, "no table under '## In flight'")
    header = [clean(c).lower() for c in split_row(table[0])]
    if "workstream" not in header:
        raise Stop(3, "the In flight table has no Workstream column")
    idx = {n: header.index(n) for n in ("workstream", "status", "priority", "owner", "state", "next step", "detail")
           if n in header}
    rows, seen = [], set()
    for line in table[1:]:
        cells = split_row(line)
        if cells and all(re.fullmatch(r":?-+:?", c.strip()) for c in cells):
            continue

        def cell(name):
            return cells[idx[name]] if name in idx and idx[name] < len(cells) else ""
        project = trim_project(clean(cell("workstream")))
        if not project:
            log("skipped a row with an empty Workstream")
            continue
        if project in seen:
            log(f"duplicate project '{project}' in the handoff; keeping the first")
            continue
        seen.add(project)
        state, nxt = clean(cell("state")), clean(cell("next step"))
        status = explicit(project, "Status", cell("status"), STATUS_WORDS, "using the rule-based status") \
            or classify(state, nxt)
        owner = explicit(project, "Owner", cell("owner"), OWNER_WORDS, "using the rule-based owner") or owner_of(nxt)
        priority = explicit(project, "Priority", cell("priority"), PRIORITY_WORDS, "leaving Priority unset")
        dates = [d for d in valid_dates(line, True) if d <= handoff_date]
        next_step = next_step_of(status, state, nxt)
        if status == "Dropped" and not re.match(r"dropped:\s*\S", next_step, re.I):
            log(f"warn: row '{project}': Dropped without a reason; put 'Dropped: <reason>' in Next step or a sentence in State")
        rows.append({"project": project, "status": status, "priority": priority, "owner": owner,
                     "next_step": next_step,
                     "last_update": max(dates) if dates else handoff_date,
                     "link": link_of(cell("detail"), line, repo_url)})
    return handoff_date, rows


# ---------------------------------------------------------------- Notion REST

def pace():
    wait = MIN_INTERVAL - (time.monotonic() - _last_request[0])
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.monotonic()


def error_info(e):
    try:
        body = json.loads(e.read().decode("utf-8", "replace"))
        return e.code, str(body.get("code", "")), str(body.get("message", ""))
    except (ValueError, AttributeError):
        return e.code, "", e.reason if isinstance(e.reason, str) else ""


def retry_delay(e, attempt, safe=True):
    """Seconds to wait before retrying, or None. 429/529 mean "not processed" and always retry; 409/5xx only when safe."""
    if attempt >= len(BACKOFF):
        return None
    if e.code in (429, 529):
        try:
            return min(max(float(e.headers.get("Retry-After", "1")), 0.0), RETRY_AFTER_MAX)
        except ValueError:
            return 1.0
    return BACKOFF[attempt] if safe and e.code in (409, 500, 502, 503, 504) else None


def is_timeout(e):
    return isinstance(e, (socket.timeout, TimeoutError)) or isinstance(getattr(e, "reason", None), (socket.timeout, TimeoutError))


def call(cfg, method, path, body=None, safe=True):
    """One REST call. safe=False (a create): an outcome that may have been processed is raised at once, never retried."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Authorization": "Bearer " + cfg["token"], "Notion-Version": cfg["version"], "Content-Type": "application/json"}
    host = urllib.parse.urlsplit(cfg["base"]).hostname
    for attempt in range(len(BACKOFF) + 1):
        pace()
        req = urllib.request.Request(cfg["base"] + path, data=data, method=method, headers=headers)
        try:
            with cfg["opener"].open(req, timeout=TIMEOUT) as r:
                raw = r.read()
        except urllib.error.HTTPError as e:
            delay = retry_delay(e, attempt, safe)
            if delay is None:
                raise ApiError(*error_info(e))
        except ValueError as e:                     # e.g. a header value http.client refuses to send
            raise Unreachable(f"request could not be sent ({e.__class__.__name__})")
        except (OSError, http.client.HTTPException) as e:
            reason = getattr(e, "reason", e)
            if not is_timeout(e):
                lost = isinstance(reason, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, http.client.HTTPException))
                raise Unreachable(scrub(f"cannot reach {host} ({reason})"), ambiguous=lost and not safe)
            if not safe:
                raise Unreachable(f"timeout after {TIMEOUT}s", ambiguous=True)
            if attempt >= len(BACKOFF):
                raise Unreachable(f"timeout after {TIMEOUT}s", ambiguous=True)
            delay = BACKOFF[attempt]
        else:
            try:
                return json.loads(raw.decode("utf-8"))
            except ValueError:
                raise ApiError(0, "bad_response", "response was not JSON")
        time.sleep(delay)


def rich(arr):
    return "".join(x.get("plain_text") or (x.get("text") or {}).get("content", "") for x in arr or [])


def find_data_source(cfg):
    found, cursor = [], None
    for _ in range(5):
        body = {"query": DS_TITLE, "filter": {"property": "object", "value": "data_source"}, "page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = call(cfg, "POST", "/v1/search", body)
        for r in res.get("results", []):
            title = r["name"] if isinstance(r.get("name"), str) and r["name"] else rich(r.get("title"))
            if title == DS_TITLE and not (r.get("in_trash") or r.get("archived")):
                found.append(r["id"])
        cursor = res.get("next_cursor")
        if not res.get("has_more") or not cursor:
            break
    if not found:
        raise Stop(2, f"data source '{DS_TITLE}' not found: share the page with the integration")
    if len(found) > 1:
        raise Stop(2, f"ambiguous: {len(found)} data sources are titled '{DS_TITLE}'; set NOTION_PROJECTS_DS")
    return found[0]


def check_schema(cfg, ds):
    """Verify property names and types. Returns ({select property: set of its option names}, has Target date property)."""
    props = call(cfg, "GET", "/v1/data_sources/" + urllib.parse.quote(ds, safe="")).get("properties") or {}
    bad = [f"{n} ({t})" for n, t in SCHEMA.items() if (props.get(n) or {}).get("type") != t]
    if bad:
        raise Stop(2, "schema is missing or has the wrong type for: " + ", ".join(bad))
    options = {n: {o.get("name") for o in ((props[n].get("select") or {}).get("options") or []) if isinstance(o, dict)}
               for n, t in SCHEMA.items() if t == "select"}
    return options, (props.get(TARGET_DATE) or {}).get("type") == "date"


def check_options(options, plan):
    """The schema is never changed: every select value the plan writes must already be an option."""
    missing = []
    for prop in ("Status", "Priority", "Owner", "Area", "Source"):
        for kind in ("create", "update", "close", "dup"):
            for e in plan[kind]:
                v = e["values"].get(prop)
                if v and v not in options.get(prop, ()) and (prop, v) not in missing:
                    missing.append((prop, v))
    if missing:
        names = "; ".join(f"{p} option '{v}' missing in Notion" for p, v in missing)
        raise Stop(2, f"{names}; add {'it' if len(missing) == 1 else 'them'} by hand")


def database_data_source(cfg, given, err):
    """An explicit id that 404s as a data source may be a database id: use its only data source, else re-raise err."""
    try:
        sources = call(cfg, "GET", "/v1/databases/" + urllib.parse.quote(given, safe="")).get("data_sources") or []
    except ApiError:
        raise err
    ids = [x["id"] for x in sources if isinstance(x, dict) and isinstance(x.get("id"), str)]
    if len(sources) != 1 or len(ids) != 1:
        raise err
    log(f"note: {given.replace('-', '')[:8]} is a database id; using its data source {ids[0].replace('-', '')[:8]}. "
        "Set NOTION_PROJECTS_DS to that.")
    return ids[0]


def flatten(page):
    p = page.get("properties") or {}

    def sel(name):
        return ((p.get(name) or {}).get("select") or {}).get("name")
    start = ((p.get("Last update") or {}).get("date") or {}).get("start")
    target = ((p.get(TARGET_DATE) or {}).get("date") or {}).get("start")
    return {"id": page["id"], "created": page.get("created_time") or "", "url": page.get("url") or
            "https://www.notion.so/" + page["id"].replace("-", ""),
            "project": rich((p.get("Project") or {}).get("title")), "Status": sel("Status"),
            "Area": sel("Area"), "Owner": sel("Owner"), "Source": sel("Source"), "Priority": sel("Priority"),
            "Target date": target[:10] if target else None,
            "Next step": rich((p.get("Next step") or {}).get("rich_text")),
            "Link": (p.get("Link") or {}).get("url"), "Last update": start[:10] if start else None}


def fetch_existing(cfg, ds, source):
    """{Project title: [live card, extra copies...]}, oldest created_time first (the oldest is the live card)."""
    existing, cursor = {}, None
    while True:
        body = {"filter": {"property": "Source", "select": {"equals": source}}, "page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = call(cfg, "POST", f"/v1/data_sources/{urllib.parse.quote(ds, safe='')}/query", body)
        for page in res.get("results", []):
            cur = flatten(page)
            if page.get("in_trash") or page.get("archived") or cur["Source"] != source:
                continue                              # defence in depth: only ever act on this source's live rows
            existing.setdefault(cur["project"], []).append(cur)
        cursor = res.get("next_cursor")
        if not res.get("has_more") or not cursor:
            for key, pages in existing.items():
                pages.sort(key=lambda c: c["created"] or "\uffff")      # stable: unknown created_time keeps API order
                if len(pages) > 1:
                    log(f"duplicate Notion row '{key}' x{len(pages)}; the oldest is the live card")
            return existing


def to_prop(name, v):
    def txt(s):
        return {"type": "text", "text": {"content": s}}
    if name == "Project":
        return {"title": [txt(v)]}
    if name == "Next step":
        return {"rich_text": [txt(v[i:i + 2000]) for i in range(0, len(v), 2000)]}
    if name == "Link":
        return {"url": v}
    if name == "Last update":
        return {"date": {"start": v}}
    return {"select": {"name": v}}                     # Status, Priority, Area, Owner, Source


def make_plan(rows, existing, area, handoff_date, source):
    plan = {"create": [], "update": [], "close": [], "dup": [], "unchanged": []}
    for r in rows:
        want = {"Status": r["status"], "Area": area, "Next step": r["next_step"], "Owner": r["owner"],
                "Link": r["link"], "Last update": r["last_update"]}
        if r.get("priority"):
            want["Priority"] = r["priority"]                # empty: Notion's value is left alone on an update
        cur = (existing.get(r["project"]) or [None])[0]
        if cur is None:
            plan["create"].append({"project": r["project"], "values": dict(want, Source=source,
                                                                           Priority=want.get("Priority", DEFAULT_PRIORITY))})
            continue
        if cur["Status"] in CLOSED and r["status"] != cur["Status"]:
            log(f"warn: card '{r['project']}' is {cur['Status']} in Notion but its row says {r['status']}; not reopened "
                "(a closed card never leaves its column): rename the Workstream to open a new card")
            plan["unchanged"].append({"project": r["project"]})
            continue
        if cur["Status"] != r["status"]:                    # a move updates Last update, even if the row's own dates are older
            want["Last update"] = max(r["last_update"], handoff_date)
        changed = {k: v for k, v in want.items() if cur[k] != v}
        if "Last update" in changed and cur["Last update"] and cur["Last update"] >= want["Last update"]:
            del changed["Last update"]                      # Last update only moves forward: a bump is not undone by the row's date
        if changed:
            plan["update"].append({"project": r["project"], "id": cur["id"], "values": changed})
        else:
            plan["unchanged"].append({"project": r["project"]})
    keys = {r["project"] for r in rows}
    for key, pages in existing.items():
        cur = pages[0]
        if key not in keys and cur["Status"] not in CLOSED:
            vals = {"Status": "Done", "Next step": f"Left {source} In flight; last seen {handoff_date}.",
                    "Last update": handoff_date}
            plan["close"].append({"project": key, "id": cur["id"], "values": vals})
        for extra in pages[1:]:
            if extra["Status"] not in CLOSED:
                vals = {"Status": "Done", "Next step": f"Duplicate card; the live card is {cur['url']}.",
                        "Last update": handoff_date}
                plan["dup"].append({"project": key, "id": extra["id"], "values": vals})
    return plan


def maybe_landed(e):
    """True when a failed create may nevertheless have been processed by Notion."""
    if isinstance(e, Unreachable):
        return e.ambiguous
    return e.status in (0, 409) or (e.status >= 500 and e.status != 529)      # 0: a 2xx whose body was not JSON


def find_created(cfg, ds, source, title):
    body = {"filter": {"and": [{"property": "Source", "select": {"equals": source}},
                               {"property": "Project", "title": {"equals": title}}]}, "page_size": 100}
    res = call(cfg, "POST", f"/v1/data_sources/{urllib.parse.quote(ds, safe='')}/query", body)
    for page in res.get("results", []):
        cur = flatten(page)
        if not (page.get("in_trash") or page.get("archived")) and cur["Source"] == source and cur["project"] == title:
            return True
    return False


def create_page(cfg, ds, entry):
    """POST a new page. Never a blind retry: after a timeout / 409 / 5xx look for the page first, then try once more."""
    title, source = entry["project"], entry["values"]["Source"]
    body = {"parent": {"type": "data_source_id", "data_source_id": ds}, "properties":
            {"Project": to_prop("Project", title), **{k: to_prop(k, v) for k, v in entry["values"].items()}}}
    for attempt in (0, 1):
        try:
            call(cfg, "POST", "/v1/pages", body, safe=False)
            return
        except (ApiError, Unreachable) as e:
            if attempt or not maybe_landed(e):
                raise
            log(f"create '{title}' not confirmed ({e}); checking Notion before any retry")
            if find_created(cfg, ds, source, title):
                log(f"'{title}' is in Notion already; not creating it again")
                return
            time.sleep(BACKOFF[0])


def execute(cfg, ds, plan):
    counts = {"created": 0, "updated": 0, "closed": 0, "duplicates": 0, "unchanged": len(plan["unchanged"]), "failed": 0}
    jobs = [("created", e, lambda e=e: create_page(cfg, ds, e)) for e in plan["create"]]
    for kind, key in (("updated", "update"), ("closed", "close"), ("duplicates", "dup")):
        jobs += [(kind, e, lambda e=e: call(cfg, "PATCH", "/v1/pages/" + urllib.parse.quote(e["id"], safe=""),
                                            {"properties": {k: to_prop(k, v) for k, v in e["values"].items()}}))
                 for e in plan[key]]
    for kind, entry, job in jobs:
        try:
            job()
            counts[kind] += 1
            log(f"{kind} '{entry['project']}'")
        except ApiError as e:
            log(f"FAILED {kind} '{entry['project']}': {e}")
            if e.status in (401, 403):                  # the token lost its right to write: do not hammer on
                done = sum(counts[k] for k in ("created", "updated", "closed", "duplicates"))
                raise Stop(2, f"HTTP {e.status} during writes; {done} writes done before it")
            counts["failed"] += 1
        except Unreachable as e:
            counts["failed"] += 1
            log(f"FAILED {kind} '{entry['project']}': {e}")
    return counts


# ---------------------------------------------------------------- audit (read-only)

def fetch_all(cfg, ds):
    """Every live card of the data source (no filter), following next_cursor."""
    cards, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = call(cfg, "POST", f"/v1/data_sources/{urllib.parse.quote(ds, safe='')}/query", body)
        cards += [flatten(pg) for pg in res.get("results", []) if not (pg.get("in_trash") or pg.get("archived"))]
        cursor = res.get("next_cursor")
        if not res.get("has_more") or not cursor:
            return cards


def audit_cards(cards, today, source, has_target):
    """Board-policy violations as [{"rule", "card", "detail", "mine"}]. card is None for the per-Owner rules (wip, p0), which
    name only an Owner; otherwise "mine" is True only for a card whose Source is this run's source (the only ones that may be
    named in output)."""
    today_d = datetime.date.fromisoformat(today)
    open_cards = [c for c in cards if c["Status"] not in CLOSED]
    out = []

    def add(rule, card, detail):
        out.append({"rule": rule, "card": (card["project"] or "(untitled)") if card else None, "detail": detail,
                    "mine": card is None or card["Source"] == source})

    for owner, limit in WIP_LIMITS.items():
        n = len([c for c in cards if c["Status"] == "In progress" and c["Owner"] == owner])
        if n > limit:
            add("wip", None, f"{owner}: {n} In progress > {limit}")
    for owner in sorted({c["Owner"] for c in open_cards if c["Owner"]}):
        n = len([c for c in open_cards if c["Owner"] == owner and c["Priority"] == "P0"])
        if n > 1:
            add("p0", None, f"{owner}: {n} open P0 > 1")
    for c in open_cards:
        lacking = [name for name, v in (("Owner", c["Owner"]), ("Next step", c["Next step"]), ("Priority", c["Priority"]),
                                        ("Area", c["Area"]), ("Status", c["Status"] in STATUSES),
                                        ("Project", c["project"]),
                                        # a missing Last update on a card the stale rule watches is reported there, once
                                        ("Last update", c["Last update"] or c["Status"] in STALE_DAYS)) if not v]
        if lacking:
            add("missing", c, "missing " + ", ".join(lacking))
    for c in cards:
        limit = STALE_DAYS.get(c["Status"])
        if limit is None:
            continue
        try:
            age = (today_d - datetime.date.fromisoformat(c["Last update"] or "")).days
        except ValueError:
            add("stale", c, f"{c['Status']}, no last update")
            continue
        if age > limit:
            add("stale", c, f"{c['Status']}, last update {c['Last update']} ({age} days)")
    for c in cards:
        if c["Status"] == "Waiting on Josep" and not re.match(r"josep:\s*\S", c["Next step"], re.I):
            add("waiting", c, "Waiting on Josep but Next step is not 'Josep: <what is needed>'")
    for c in cards:
        if c["Status"] == "Blocked" and not c["Next step"]:
            add("blocked", c, "Blocked without a Next step")
    if has_target:
        for c in open_cards:
            if c["Priority"] == "P0" and not c["Target date"]:
                add("target", c, f"{c['Priority']} without a Target date")
        for c in open_cards:
            if c["Target date"] and c["Target date"] < today:
                add("overdue", c, f"Target date {c['Target date']} has passed")
    for c in cards:
        if c["Status"] == "Done":
            if not c["Link"]:
                add("evidence", c, "Done without a Link")
            elif HANDOFF_LINK.search(c["Link"]):
                add("evidence", c, "Done, but the Link is only the handoff.md fallback, not evidence")
            elif c["Source"] and c["Next step"].startswith(f"Left {c['Source']} In flight"):
                add("evidence", c, "Done by leaving In flight: no evidence recorded")
    for c in cards:
        if c["Status"] == "Dropped" and not re.match(r"dropped:\s*\S", c["Next step"], re.I):
            add("dropped", c, "Dropped but Next step is not 'Dropped: <reason>'")
    groups = {}
    for c in open_cards:
        groups.setdefault((c["Source"], c["project"]), []).append(c)
    for group in groups.values():
        for extra in sorted(group, key=lambda c: c["created"] or "\uffff")[1:]:
            add("dup", extra, "duplicate of an older open card")
    order = {r: i for i, r in enumerate(RULES)}
    out.sort(key=lambda v: order[v["rule"]])                  # stable: API order inside a rule
    return out, len(cards), len(open_cards)


def run_audit(args):
    if args.dry_run:
        raise Stop(4, "--audit and --dry-run cannot be combined")
    today = check_today(args)
    cfg, override = connection(args)
    source = args.source or f"{repo_identity()[1]}/handoff.md"
    try:
        ds, _, has_target = resolve(cfg, args)
        cards = fetch_all(cfg, ds)
    except ApiError as e:
        raise Stop(2, str(e) + (NOT_FOUND_HINT if e.status == 404 else ""))
    except Unreachable as e:
        raise Stop(2, str(e))
    violations, n_cards, n_open = audit_cards(cards, today, source, has_target)
    counts = {"cards": n_cards, "open": n_open, "violations": len(violations)}
    for rule in RULES:
        counts[rule] = None if rule in ("target", "overdue") and not has_target else \
            len([v for v in violations if v["rule"] == rule])
    shown = [{"rule": v["rule"], "card": v["card"], "detail": v["detail"]} for v in violations if v["mine"]]
    return {"ok": True, "audit": True, "counts": counts, "violations": shown,
            "other_source_violations": len([v for v in violations if not v["mine"]]), "data_source": ds.replace("-", "")[:8]}, 0


def render_audit(res, as_json):
    if as_json:
        emit(json.dumps(res, ensure_ascii=False) + "\n")
        return
    c = res["counts"]
    lines = ["notion-audit: " + " ".join(f"{k}={'n/a' if c[k] is None else c[k]}" for k in c)]
    lines += [f"- [{v['rule']}] {v['card'] + ' — ' if v['card'] else ''}{v['detail']}" for v in res["violations"]]
    k = res["other_source_violations"]
    if k:
        lines.append(f"- {k} more violation(s) on cards from other sources; details only in Notion (this repository is public).")
    emit("\n".join(lines) + "\n")                    # one write: the report is never half-printed


# ---------------------------------------------------------------- command line

def repo_identity():
    try:
        out = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=str(ROOT), capture_output=True,
                             text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    parts = [p for p in re.split(r"[/:]", re.sub(r"\.git$", "", out.rstrip("/"))) if p]
    if re.search(r"://|@", out) and len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, ROOT.name


NOT_FOUND_HINT = " (not found: share the page with the integration, or use the data source id, not the database id)"


def check_today(args):
    today = args.today or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", today) or not valid_dates(today):
        raise Stop(4, f"bad --today '{today}' (want YYYY-MM-DD)")
    return today


def api_settings():
    """(base override, Notion-Version), refusing a foreign base or a malformed version."""
    override = os.environ.get("NOTION_API_BASE", "").strip()
    if override and not LOCAL_BASE.match(override):
        raise Stop(4, "NOTION_API_BASE may only point at http://127.0.0.1:<port> or http://localhost:<port>")
    version = os.environ.get("NOTION_VERSION", "").strip() or DEFAULT_VERSION
    if not VERSION_RE.fullmatch(version):
        raise Stop(4, "NOTION_VERSION must look like YYYY-MM-DD")
    return override, version


def connection(args):
    """The request config, or Stop(2) when there is no usable token. (Only a dry run may go on without one: see run().)"""
    override, version = api_settings()
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        raise Stop(2, "NOTION_TOKEN not set")
    return token_config(token, version, override), override


def token_config(token, version, override):
    if not TOKEN_RE.fullmatch(token):
        raise Stop(2, "NOTION_TOKEN contains invalid characters")
    return {"token": token, "version": version, "opener": urllib.request.build_opener(NoRedirect),
            "base": (override or DEFAULT_BASE).rstrip("/")}


def resolve(cfg, args):
    """(data source id, select options, has Target date): find the data source and check its schema."""
    given = args.data_source or os.environ.get("NOTION_PROJECTS_DS")
    ds = given or find_data_source(cfg)
    try:
        options, has_target = check_schema(cfg, ds)
    except ApiError as e:
        if e.status != 404 or not given:
            raise
        ds = database_data_source(cfg, given, e)
        options, has_target = check_schema(cfg, ds)
    return ds, options, has_target


def run(args):
    if args.audit:
        return run_audit(args)
    today = check_today(args)
    override, version = api_settings()
    path = args.handoff or str(ROOT / "handoff.md")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, ValueError) as e:
        raise Stop(3, f"cannot read {path} ({e.__class__.__name__})")
    owner, repo = (None, "") if (args.source and args.area and args.repo_url) else repo_identity()
    source, area = args.source or f"{repo}/handoff.md", args.area or repo
    repo_url = args.repo_url or (f"https://github.com/{owner}/{repo}" if owner else None)
    handoff_date, rows = parse_handoff(text, today, repo_url.rstrip("/") if repo_url else None)
    res = {"ok": True, "dry_run": args.dry_run, "source": source, "area": area, "data_source": None,
           "handoff_date": handoff_date, "rows": rows, "plan": None, "counts": None}
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        if args.dry_run:
            return res, 0
        raise Stop(2, "NOTION_TOKEN not set")
    cfg = token_config(token, version, override)
    try:
        ds, options, _ = resolve(cfg, args)
        res["data_source"] = ds
        existing = fetch_existing(cfg, ds, source)
    except ApiError as e:
        raise Stop(2, str(e) + (NOT_FOUND_HINT if e.status == 404 else ""))
    except Unreachable as e:
        raise Stop(2, str(e))
    plan = res["plan"] = make_plan(rows, existing, area, handoff_date, source)
    check_options(options, plan)
    if args.dry_run:
        res["counts"] = {"created": len(plan["create"]), "updated": len(plan["update"]), "closed": len(plan["close"]),
                         "duplicates": len(plan["dup"]), "unchanged": len(plan["unchanged"]), "failed": 0}
        for kind in ("create", "update", "close", "dup"):
            for e in plan[kind]:
                log(f"dry-run {kind} '{e['project']}' {sorted(e['values'])}")
        return res, 0
    res["counts"] = execute(cfg, ds, plan)
    return res, (1 if res["counts"]["failed"] else 0)


def render(res, as_json):
    if res.get("audit"):
        return render_audit(res, as_json)
    if as_json:
        plan = res["plan"] and {"create": [e["project"] for e in res["plan"]["create"]],
                                "update": [{"project": e["project"], "changed": sorted(e["values"])} for e in res["plan"]["update"]],
                                "close": [e["project"] for e in res["plan"]["close"]],
                                "unchanged": [e["project"] for e in res["plan"]["unchanged"]]}
        emit(json.dumps(dict(res, plan=plan), ensure_ascii=False) + "\n")
        return
    c, ds8 = res["counts"], (res["data_source"] or "").replace("-", "")[:8]
    if res["dry_run"]:
        for r in res["rows"]:
            log(f"row {r['status']} | {r['priority'] or '-'} | {r['owner']} | {r['last_update']} | {r['project']}")
    if c is None:
        emit(f"notion-sync: dry-run rows={len(res['rows'])} source={res['source']}\n")
        return
    head = "dry-run rows=%d " % len(res["rows"]) if res["dry_run"] else ""
    dups = f" duplicates={c['duplicates']}" if c.get("duplicates") else ""
    emit(f"notion-sync: {head}created={c['created']} updated={c['updated']} closed={c['closed']} "
         f"unchanged={c['unchanged']} failed={c['failed']}{dups} source={res['source']} data_source={ds8}\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="Mirror handoff.md In flight into Notion; see the module docstring for exit codes.")
    p.add_argument("--handoff", help="handoff file (default: handoff.md at the repo root)")
    p.add_argument("--source", help="Source label (default: <repo>/handoff.md)")
    p.add_argument("--area", help="Area label (default: <repo>)")
    p.add_argument("--repo-url", help="repo URL for links (default: from git remote origin)")
    p.add_argument("--data-source", help="data source id (default: NOTION_PROJECTS_DS, else search)")
    p.add_argument("--dry-run", action="store_true", help="parse and plan; never write")
    p.add_argument("--json", action="store_true", help="print one JSON object instead of the summary line")
    p.add_argument("--audit", action="store_true", help="read-only board-policy check of every card; see the docstring")
    p.add_argument("--today", help="override today's date, YYYY-MM-DD (tests)")
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 4 if e.code else 0                      # argparse's own exit 2 would read as "sync off"
    try:
        res, code = run(args)
        res["ok"] = res.get("audit", False) or not (res["counts"] and res["counts"]["failed"])
        res["exit"] = code
        render(res, args.json)
        return code
    except Stop as s:
        code, reason = s.code, str(s)
    except Exception as e:                              # never a traceback: it could carry the token or a request body
        code, reason = 2, scrub(" ".join(f"internal error: {e.__class__.__name__}: {e}".split()))[:300]
    if args.json:
        emit(json.dumps({"ok": False, "off": code == 2, "exit": code, "reason": reason}, ensure_ascii=False) + "\n")
    elif code == 2:
        emit(f"notion-sync: off ({reason})\n")
    else:
        emit(f"notion-sync: error ({reason})\n", sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
