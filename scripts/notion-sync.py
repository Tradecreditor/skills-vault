#!/usr/bin/env python3
"""notion-sync.py - one-way mirror of handoff.md "## In flight" into the Notion data source "Project Status".

    notion-sync.py [--handoff PATH] [--source LABEL] [--area LABEL] [--repo-url URL]
                   [--data-source ID] [--dry-run] [--json] [--today YYYY-MM-DD]

Each In flight row becomes (or updates) one Notion row keyed by its Project title and tagged with the Source label; rows that
left the table are set to Done. Rows of another Source are never touched, nothing is deleted or archived, the schema is never
changed (a Status / Owner / Area / Source option the plan needs must already exist). A create is never blindly retried: after a
timeout / 409 / 5xx the data source is queried first, so a page that did land is not created twice. Extra copies of one card
(same Source and Project) are set to Done, pointing at the oldest one. stdout: one summary line (or one JSON object with --json);
details go to stderr.

Exit codes (the routine branches on these, never on the message text):
    0  ok (also: dry-run ok)
    1  partial: some writes failed after retries, the others are done
    2  sync OFF for this run: NOTION_TOKEN missing (not --dry-run) or malformed, 401/403 (also on a write: the run stops at
       once), data source not found or not shared, ambiguous search (set NOTION_PROJECTS_DS), schema missing a property, a
       wrong type or a needed select option, host unreachable, any failed read, an unexpected internal error
    3  handoff parse error: file missing, no "## In flight" section, no table, no Workstream column
    4  refused locally: bad NOTION_API_BASE override, bad NOTION_VERSION, bad --today, bad command line

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
SCHEMA = {"Project": "title", "Status": "select", "Area": "select", "Next step": "rich_text",
          "Owner": "select", "Link": "url", "Last update": "date", "Source": "select"}
NO_NEXT = {"none", "—", "-", "n/a", "nothing"}
PATH_EXT = (".md", ".yaml", ".yml", ".py", ".json", ".sh")
DATE_RE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
VERSION_BEFORE = re.compile(r"(?:version|(?<![A-Za-z])v)[ -]?$", re.I)     # "Notion-Version 2026-03-11", "v2026-03-11"
TOKEN_RE = re.compile(r"[\x21-\x7e]+")
VERSION_RE = re.compile(r"\d{4}-\d{2}-\d{2}", re.A)
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
    print("notion-sync: " + scrub(msg), file=sys.stderr)


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
    if status == "Done" and (not nxt or nxt.lower() in NO_NEXT):
        first = re.split(r"(?<=[.!?])\s", state, maxsplit=1)[0] if state else ""
        text = "Done — " + first if first else "Done"
    else:
        text = nxt
    return text if len(text) <= 1900 else text[:1899] + "…"


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
    idx = {n: header.index(n) for n in ("workstream", "state", "next step", "detail") if n in header}
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
        status = classify(state, nxt)
        dates = [d for d in valid_dates(line, True) if d <= handoff_date]
        rows.append({"project": project, "status": status, "owner": owner_of(nxt),
                     "next_step": next_step_of(status, state, nxt),
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
    """Verify property names and types; return {select property: set of its existing option names}."""
    props = call(cfg, "GET", "/v1/data_sources/" + urllib.parse.quote(ds, safe="")).get("properties") or {}
    bad = [f"{n} ({t})" for n, t in SCHEMA.items() if (props.get(n) or {}).get("type") != t]
    if bad:
        raise Stop(2, "schema is missing or has the wrong type for: " + ", ".join(bad))
    return {n: {o.get("name") for o in ((props[n].get("select") or {}).get("options") or []) if isinstance(o, dict)}
            for n, t in SCHEMA.items() if t == "select"}


def check_options(options, plan):
    """The schema is never changed: every select value the plan writes must already be an option."""
    missing = []
    for prop in ("Status", "Owner", "Area", "Source"):
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
    return {"id": page["id"], "created": page.get("created_time") or "", "url": page.get("url") or
            "https://www.notion.so/" + page["id"].replace("-", ""),
            "project": rich((p.get("Project") or {}).get("title")), "Status": sel("Status"),
            "Area": sel("Area"), "Owner": sel("Owner"), "Source": sel("Source"),
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
    return {"select": {"name": v}}                     # Status, Area, Owner, Source


def make_plan(rows, existing, area, handoff_date, source):
    plan = {"create": [], "update": [], "close": [], "dup": [], "unchanged": []}
    for r in rows:
        want = {"Status": r["status"], "Area": area, "Next step": r["next_step"], "Owner": r["owner"],
                "Link": r["link"], "Last update": r["last_update"]}
        cur = (existing.get(r["project"]) or [None])[0]
        if cur is None:
            plan["create"].append({"project": r["project"], "values": dict(want, Source=source)})
            continue
        changed = {k: v for k, v in want.items() if cur[k] != v}
        if changed:
            plan["update"].append({"project": r["project"], "id": cur["id"], "values": changed})
        else:
            plan["unchanged"].append({"project": r["project"]})
    keys = {r["project"] for r in rows}
    for key, pages in existing.items():
        cur = pages[0]
        if key not in keys and cur["Status"] != "Done":
            vals = {"Status": "Done", "Next step": f"Left {source} In flight; last seen {handoff_date}.",
                    "Last update": handoff_date}
            plan["close"].append({"project": key, "id": cur["id"], "values": vals})
        for extra in pages[1:]:
            if extra["Status"] != "Done":
                vals = {"Status": "Done", "Next step": f"Duplicate card; the live card is {cur['url']}. Safe to delete by hand."}
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


def run(args):
    today = args.today or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", today) or not valid_dates(today):
        raise Stop(4, f"bad --today '{today}' (want YYYY-MM-DD)")
    override = os.environ.get("NOTION_API_BASE", "").strip()
    if override and not LOCAL_BASE.match(override):
        raise Stop(4, "NOTION_API_BASE may only point at http://127.0.0.1:<port> or http://localhost:<port>")
    version = os.environ.get("NOTION_VERSION", "").strip() or DEFAULT_VERSION
    if not VERSION_RE.fullmatch(version):
        raise Stop(4, "NOTION_VERSION must look like YYYY-MM-DD")
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
    if not TOKEN_RE.fullmatch(token):
        raise Stop(2, "NOTION_TOKEN contains invalid characters")
    opener = urllib.request.build_opener(NoRedirect)
    cfg = {"token": token, "version": version, "opener": opener, "base": (override or DEFAULT_BASE).rstrip("/")}
    try:
        given = args.data_source or os.environ.get("NOTION_PROJECTS_DS")
        ds = given or find_data_source(cfg)
        try:
            options = check_schema(cfg, ds)
        except ApiError as e:
            if e.status != 404 or not given:
                raise
            ds = database_data_source(cfg, given, e)
            options = check_schema(cfg, ds)
        res["data_source"] = ds
        existing = fetch_existing(cfg, ds, source)
    except ApiError as e:
        hint = " (not found: share the page with the integration, or use the data source id, not the database id)" \
            if e.status == 404 else ""
        raise Stop(2, str(e) + hint)
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
    if as_json:
        plan = res["plan"] and {"create": [e["project"] for e in res["plan"]["create"]],
                                "update": [{"project": e["project"], "changed": sorted(e["values"])} for e in res["plan"]["update"]],
                                "close": [e["project"] for e in res["plan"]["close"]],
                                "unchanged": [e["project"] for e in res["plan"]["unchanged"]]}
        print(json.dumps(dict(res, plan=plan), ensure_ascii=False))
        return
    c, ds8 = res["counts"], (res["data_source"] or "").replace("-", "")[:8]
    if res["dry_run"]:
        for r in res["rows"]:
            log(f"row {r['status']} | {r['owner']} | {r['last_update']} | {r['project']}")
    if c is None:
        print(f"notion-sync: dry-run rows={len(res['rows'])} source={res['source']}")
        return
    head = "dry-run rows=%d " % len(res["rows"]) if res["dry_run"] else ""
    dups = f" duplicates={c['duplicates']}" if c.get("duplicates") else ""
    print(f"notion-sync: {head}created={c['created']} updated={c['updated']} closed={c['closed']} "
          f"unchanged={c['unchanged']} failed={c['failed']}{dups} source={res['source']} data_source={ds8}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Mirror handoff.md In flight into Notion; see the module docstring for exit codes.")
    p.add_argument("--handoff", help="handoff file (default: handoff.md at the repo root)")
    p.add_argument("--source", help="Source label (default: <repo>/handoff.md)")
    p.add_argument("--area", help="Area label (default: <repo>)")
    p.add_argument("--repo-url", help="repo URL for links (default: from git remote origin)")
    p.add_argument("--data-source", help="data source id (default: NOTION_PROJECTS_DS, else search)")
    p.add_argument("--dry-run", action="store_true", help="parse and plan; never write")
    p.add_argument("--json", action="store_true", help="print one JSON object instead of the summary line")
    p.add_argument("--today", help="override today's date, YYYY-MM-DD (tests)")
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 4 if e.code else 0                      # argparse's own exit 2 would read as "sync off"
    try:
        res, code = run(args)
        res["ok"] = not (res["counts"] and res["counts"]["failed"])
        res["exit"] = code
        render(res, args.json)
        return code
    except Stop as s:
        code, reason = s.code, str(s)
    except Exception as e:                              # never a traceback: it could carry the token or a request body
        code, reason = 2, scrub(" ".join(f"internal error: {e.__class__.__name__}: {e}".split()))[:300]
    if args.json:
        print(json.dumps({"ok": False, "off": code == 2, "exit": code, "reason": reason}, ensure_ascii=False))
    elif code == 2:
        print(f"notion-sync: off ({reason})")
    else:
        print(f"notion-sync: error ({reason})", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
