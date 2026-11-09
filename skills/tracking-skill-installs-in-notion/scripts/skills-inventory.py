#!/usr/bin/env python3
"""skills-inventory.py - record which agent skills are installed in this project (or on this computer) in the Notion data
source "Skill Installs" (page "Skills HQ"), plus a vault-only enrichment (--enrich) and a read-only audit (--audit).

    skills-inventory.py [--project LABEL] [--source LABEL] [--root DIR] [--data-source ID] [--dry-run] [--json] [--today D]
    skills-inventory.py --global [--project "global:<label>"] [--home DIR] ...
    skills-inventory.py --enrich [--vault DIR] [--json]
    skills-inventory.py --audit [--source LABEL] [--json] [--today D]

What it reads (never writes anything on disk):
  project scope (default): <root>/skills-lock.json (the `skills` CLI lockfile: skills[<name>] = {source, sourceType,
    computedHash, ...}), the agent skill folders <root>/.claude/skills/*, <root>/.agents/skills/* and <root>/skills/*
    (OpenClaw; skipped when <root> is the vault itself, whose skills/ is the library), and the Claude Code plugins enabled in
    <root>/.claude/settings.json and .claude/settings.local.json (enabledPlugins set to true).
  --global: the per-computer equivalents under <home>: ~/.claude/skills, ~/.agents/skills, ~/.gemini/skills, ~/.cursor/skills,
    ~/.openclaw/skills, ~/.claude/plugins/installed_plugins.json and ~/.claude/settings.json enabledPlugins. Project defaults to
    "global:<hostname>" (override with --project); that label is written to Notion only (Notion is private).

What it writes: one Notion row per skill (or plugin id) keyed by Skill title + Source label. Rows of another Source are never
touched. A row that this run no longer sees is set to Status "Removed" (never deleted or archived); a row seen again goes back
to "Installed". "Installed" (first seen) is written on create only; "Vault status" is written only by --enrich. The schema is
never changed; Project, Source and Agents options are created by Notion on demand when a new value is written, every other
select value (Scope, Kind, Status, Vault status) must already be an option or the run stops with exit 2 before any write.

--enrich (the vault's daily run only): reads <vault>/skills/README.md (the "Skills in this vault" table, name -> vault_status)
and sets "Vault status" on every row whose "Vault skill" box is ticked, whatever its Source. A vault skill the table does not
list gets "unknown". Nothing else is written.

--audit (read-only; names only rows of this run's Source, counts the rest): draft-installed (a vault skill whose Vault status
is draft, deprecated or unknown is Installed somewhere), stale (Installed but Last seen more than 30 days ago), unknown-vault
(Vault skill ticked, Vault status empty or unknown: --enrich has not run), removed (rows with Status Removed, a count).

Exit codes (a routine branches on these, never on the message text):
    0  ok (also: dry-run ok, enrich ok, audit ran)
    1  partial: some writes failed after retries, the others are done
    2  OFF for this run: NOTION_TOKEN missing (not --dry-run) or malformed, 401/403, data source not found or not shared,
       ambiguous search (set NOTION_SKILLS_DS), schema missing a property or of the wrong type, a needed select option missing,
       host unreachable, any failed read, an unexpected internal error
    3  local input unusable: skills-lock.json is not valid JSON, or --root / --home / --vault is not a directory
    4  refused locally: bad NOTION_API_BASE override, bad NOTION_VERSION, bad --today, bad command line

Credentials: NOTION_TOKEN (Bearer header to the API base only, never printed; the same integration as Projects HQ, which Jeff
also connects to the Skills HQ page). NOTION_API_BASE may only be http://127.0.0.1:<port> or http://localhost:<port> (tests).
Optional: NOTION_VERSION (YYYY-MM-DD), NOTION_SKILLS_DS (data source id). Python 3.9+, stdlib only.
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
DS_TITLE = "Skill Installs"
SCHEMA = {"Skill": "title", "Project": "select", "Scope": "select", "Kind": "select", "Source repo": "rich_text",
          "Agents": "multi_select", "Hash": "rich_text", "Status": "select", "Installed": "date", "Last seen": "date",
          "Vault skill": "checkbox", "Vault status": "select", "Link": "url", "Source": "select"}
FIXED_OPTIONS = ("Scope", "Kind", "Status", "Vault status")       # must exist; Project / Source / Agents are created on demand
VAULT_REPO = "Tradecreditor/skills-vault"
VAULT_STATUSES = ("draft", "reviewer-approved", "verified", "deprecated")
APPROVED = ("reviewer-approved", "verified")
STALE_DAYS = 30
RULES = ("draft-installed", "stale", "unknown-vault", "removed")
# project-scope skill folders: (relative dir, agent label). .agents/skills is shared by Codex, Cursor, Gemini CLI, Copilot...
PROJECT_DIRS = ((".claude/skills", "claude-code"), (".agents/skills", "codex"), ("skills", "openclaw"))
GLOBAL_DIRS = ((".claude/skills", "claude-code"), (".agents/skills", "codex"), (".gemini/skills", "gemini-cli"),
               (".cursor/skills", "cursor"), (".openclaw/skills", "openclaw"))
AGENT_OPTIONS = ("claude-code", "codex", "gemini-cli", "cursor", "openclaw", "other")
GITHUB_SOURCE = re.compile(r"^(?:https?://github\.com/)?([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[/#?].*)?$")
TOKEN_RE = re.compile(r"[\x21-\x7e]+")
VERSION_RE = re.compile(r"\d{4}-\d{2}-\d{2}", re.A)
MAX_TEXT = 2000
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
    emit("skills-inventory: " + scrub(msg) + "\n", sys.stderr)


def emit(text, stream=None):
    """Write text in one piece, never raising on a stream whose encoding cannot hold a character."""
    stream = stream or sys.stdout
    enc = getattr(stream, "encoding", None) or "utf-8"
    try:
        text = text.encode(enc, "backslashreplace").decode(enc)
    except (LookupError, UnicodeError):
        text = text.encode("ascii", "backslashreplace").decode("ascii")
    stream.write(text)


# ---------------------------------------------------------------- collecting what is installed

def read_json(path):
    """A JSON object from path, {} when the file is missing, Stop(3) when it is not valid JSON."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        raise Stop(3, f"cannot read {path} ({e.__class__.__name__})")
    return data if isinstance(data, dict) else {}


def skill_name(folder):
    """A folder (or symlink) under <agent>/skills whose SKILL.md exists is an installed skill."""
    try:
        if folder.name.startswith(".") or not folder.is_dir() or not (folder / "SKILL.md").is_file():
            return None
    except OSError:
        return None
    return folder.name


def scan_dirs(base, dirs):
    """{skill name: set of agent labels} from the skill folders under base."""
    found = {}
    for rel, agent in dirs:
        d = Path(base) / rel
        try:
            entries = sorted(d.iterdir()) if d.is_dir() else []
        except OSError:
            entries = []
        for folder in entries:
            name = skill_name(folder)
            if name:
                found.setdefault(name, set()).add(agent)
    return found


def lock_entries(lock):
    """{skill name: {source, sourceType, computedHash}} from a skills-lock.json object (unknown shapes are skipped)."""
    out = {}
    skills = lock.get("skills")
    if not isinstance(skills, dict):
        return out
    for name, entry in skills.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(entry, dict):
            continue
        out[name.strip()] = {k: str(entry.get(k) or "") for k in ("source", "sourceType", "computedHash")}
    return out


def enabled_plugins(*settings_files):
    """Plugin ids set to true in the given settings files (later files override earlier ones, as Claude Code merges them)."""
    state = {}
    for path in settings_files:
        plugins = read_json(path).get("enabledPlugins")
        if isinstance(plugins, dict):
            for pid, on in plugins.items():
                if isinstance(pid, str) and pid.strip():
                    state[pid.strip()] = bool(on)
    return sorted(pid for pid, on in state.items() if on)


def installed_plugins(path):
    """{plugin id: version} from ~/.claude/plugins/installed_plugins.json (both known shapes: v1 flat, v2 list per id)."""
    out = {}
    plugins = read_json(path).get("plugins")
    if not isinstance(plugins, dict):
        return out
    for pid, rec in plugins.items():
        if not isinstance(pid, str) or not pid.strip():
            continue
        recs = rec if isinstance(rec, list) else [rec]
        versions = [str(r.get("version") or "") for r in recs if isinstance(r, dict)]
        out[pid.strip()] = next((v for v in versions if v), "")
    return out


def github_repo(source):
    """'owner/repo' when source is a GitHub shorthand or URL, else None."""
    m = GITHUB_SOURCE.match((source or "").strip())
    return f"{m.group(1)}/{m.group(2)}" if m and not source.strip().startswith(".") else None


def is_vault(source, root_is_vault):
    repo = github_repo(source)
    return (repo is not None and repo.lower() == VAULT_REPO.lower()) or (root_is_vault and source.strip() in (".", "./"))


def skill_link(name, source):
    repo = github_repo(source)
    return f"https://github.com/{repo}/tree/main/skills/{name}" if repo else None


def marketplace_repo(pid, home):
    """owner/repo of a plugin id's marketplace, from ~/.claude/plugins/known_marketplaces.json when it is a GitHub source."""
    if "@" not in pid or not home:
        return ""
    market = pid.rsplit("@", 1)[1]
    rec = read_json(Path(home) / ".claude" / "plugins" / "known_marketplaces.json").get(market)
    src = (rec or {}).get("source") if isinstance(rec, dict) else None
    if isinstance(src, dict):
        return str(src.get("repo") or src.get("url") or "")
    return ""


def collect_project(root, root_is_vault):
    """Rows for one project checkout: lockfile entries, agent folders, enabled plugins."""
    root = Path(root)
    lock = lock_entries(read_json(root / "skills-lock.json"))
    dirs = [d for d in PROJECT_DIRS if not (root_is_vault and d[0] == "skills")]
    folders = scan_dirs(root, dirs)
    rows = []
    for name in sorted(set(lock) | set(folders)):
        entry = lock.get(name)
        source = entry["source"] if entry else ""
        rows.append({"skill": name, "scope": "project", "kind": "skills-cli" if entry else "folder",
                     "source_repo": source, "agents": sorted(folders.get(name, ())),
                     "hash": entry["computedHash"] if entry else "",
                     "vault": is_vault(source, root_is_vault) if entry else False, "link": skill_link(name, source)})
    for pid in enabled_plugins(root / ".claude" / "settings.json", root / ".claude" / "settings.local.json"):
        rows.append({"skill": pid, "scope": "project", "kind": "claude-plugin", "source_repo": "", "agents": ["claude-code"],
                     "hash": "", "vault": False, "link": None})
    return rows


def collect_global(home):
    """Rows for one computer: global skill folders and user-scope Claude Code plugins."""
    home = Path(home)
    folders = scan_dirs(home, GLOBAL_DIRS)
    lock = lock_entries(read_json(home / ".agents" / "skills-lock.json"))      # written by some `skills` versions for -g
    rows = []
    for name in sorted(set(folders) | set(lock)):
        entry = lock.get(name)
        source = entry["source"] if entry else ""
        rows.append({"skill": name, "scope": "global", "kind": "skills-cli" if entry else "folder",
                     "source_repo": source, "agents": sorted(folders.get(name, ())),
                     "hash": entry["computedHash"] if entry else "", "vault": is_vault(source, False),
                     "link": skill_link(name, source)})
    versions = installed_plugins(home / ".claude" / "plugins" / "installed_plugins.json")
    for pid in sorted(set(enabled_plugins(home / ".claude" / "settings.json")) | set(versions)):
        repo = marketplace_repo(pid, home)
        rows.append({"skill": pid, "scope": "global", "kind": "claude-plugin", "source_repo": repo, "agents": ["claude-code"],
                     "hash": versions.get(pid, ""), "vault": bool(repo) and repo.lower().rstrip("/") == VAULT_REPO.lower(),
                     "link": None})
    return rows


def dedupe(rows):
    """One row per skill title: the first wins, a second copy only warns."""
    seen, out = set(), []
    for r in rows:
        if r["skill"] in seen:
            log(f"warn: '{r['skill']}' appears twice; keeping the first")
            continue
        seen.add(r["skill"])
        out.append(r)
    return out


def vault_statuses(vault):
    """{skill name: vault_status} from <vault>/skills/README.md's table; Stop(3) when the file is missing."""
    path = Path(vault) / "skills" / "README.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as e:
        raise Stop(3, f"cannot read {path} ({e.__class__.__name__})")
    out = {}
    for line in text.splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", cells[0]) and cells[1] in VAULT_STATUSES:
            out[cells[0]] = cells[1]
    return out


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
            if not safe or attempt >= len(BACKOFF):
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
        raise Stop(2, f"data source '{DS_TITLE}' not found: share the Skills HQ page with the integration")
    if len(found) > 1:
        raise Stop(2, f"ambiguous: {len(found)} data sources are titled '{DS_TITLE}'; set NOTION_SKILLS_DS")
    return found[0]


def check_schema(cfg, ds):
    """Verify property names and types. Returns {select property: set of its option names}."""
    props = call(cfg, "GET", "/v1/data_sources/" + urllib.parse.quote(ds, safe="")).get("properties") or {}
    bad = [f"{n} ({t})" for n, t in SCHEMA.items() if (props.get(n) or {}).get("type") != t]
    if bad:
        raise Stop(2, "schema is missing or has the wrong type for: " + ", ".join(bad))
    return {n: {o.get("name") for o in ((props[n].get(t) or {}).get("options") or []) if isinstance(o, dict)}
            for n, t in SCHEMA.items() if t in ("select", "multi_select")}


def check_options(options, plan):
    """Fixed-vocabulary selects are never extended by this script: every value the plan writes must already be an option."""
    missing = []
    for kind in ("create", "update", "remove"):
        for e in plan[kind]:
            for prop in FIXED_OPTIONS:
                v = e["values"].get(prop)
                if v and v not in options.get(prop, ()) and (prop, v) not in missing:
                    missing.append((prop, v))
    if missing:
        names = "; ".join(f"{p} option '{v}' missing in Notion" for p, v in missing)
        raise Stop(2, f"{names}; a session with the Notion connector adds {'it' if len(missing) == 1 else 'them'} first")


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
        "Set NOTION_SKILLS_DS to that.")
    return ids[0]


def flatten(page):
    p = page.get("properties") or {}

    def sel(name):
        return ((p.get(name) or {}).get("select") or {}).get("name")

    def date(name):
        start = ((p.get(name) or {}).get("date") or {}).get("start")
        return start[:10] if start else None
    return {"id": page["id"], "created": page.get("created_time") or "", "url": page.get("url") or
            "https://www.notion.so/" + page["id"].replace("-", ""),
            "skill": rich((p.get("Skill") or {}).get("title")), "Project": sel("Project"), "Scope": sel("Scope"),
            "Kind": sel("Kind"), "Status": sel("Status"), "Vault status": sel("Vault status"), "Source": sel("Source"),
            "Source repo": rich((p.get("Source repo") or {}).get("rich_text")), "Hash": rich((p.get("Hash") or {}).get("rich_text")),
            "Agents": sorted(o.get("name") for o in ((p.get("Agents") or {}).get("multi_select") or []) if isinstance(o, dict)),
            "Vault skill": bool((p.get("Vault skill") or {}).get("checkbox")),
            "Link": (p.get("Link") or {}).get("url"), "Installed": date("Installed"), "Last seen": date("Last seen")}


def query(cfg, ds, flt=None):
    rows, cursor = [], None
    while True:
        body = {"page_size": 100}
        if flt:
            body["filter"] = flt
        if cursor:
            body["start_cursor"] = cursor
        res = call(cfg, "POST", f"/v1/data_sources/{urllib.parse.quote(ds, safe='')}/query", body)
        rows += [flatten(pg) for pg in res.get("results", []) if not (pg.get("in_trash") or pg.get("archived"))]
        cursor = res.get("next_cursor")
        if not res.get("has_more") or not cursor:
            return rows


def fetch_existing(cfg, ds, source):
    """{skill title: [live row, extra copies...]} of this Source, oldest created_time first."""
    existing = {}
    for cur in query(cfg, ds, {"property": "Source", "select": {"equals": source}}):
        if cur["Source"] != source:
            continue                              # defence in depth: only ever act on this source's rows
        existing.setdefault(cur["skill"], []).append(cur)
    for key, pages in existing.items():
        pages.sort(key=lambda c: c["created"] or "￿")
        if len(pages) > 1:
            log(f"duplicate Notion row '{key}' x{len(pages)}; updating the oldest only")
    return existing


def to_prop(name, v):
    def txt(s):
        return {"type": "text", "text": {"content": s}}
    if name == "Skill":
        return {"title": [txt(v[:MAX_TEXT])]}
    if name in ("Source repo", "Hash"):
        return {"rich_text": [txt(v[i:i + MAX_TEXT]) for i in range(0, len(v), MAX_TEXT)] if v else []}
    if name == "Agents":
        return {"multi_select": [{"name": a} for a in v]}
    if name == "Vault skill":
        return {"checkbox": bool(v)}
    if name == "Link":
        return {"url": v or None}
    if name in ("Installed", "Last seen"):
        return {"date": {"start": v}}
    return {"select": {"name": v}}                     # Project, Scope, Kind, Status, Vault status, Source


def make_plan(rows, existing, project, source, today):
    plan = {"create": [], "update": [], "remove": [], "unchanged": []}
    for r in rows:
        agents = [a if a in AGENT_OPTIONS else "other" for a in r["agents"]]
        want = {"Project": project, "Scope": r["scope"], "Kind": r["kind"], "Source repo": r["source_repo"],
                "Agents": sorted(set(agents)), "Hash": r["hash"], "Status": "Installed", "Vault skill": r["vault"],
                "Link": r["link"], "Last seen": today}
        cur = (existing.get(r["skill"]) or [None])[0]
        if cur is None:
            plan["create"].append({"skill": r["skill"], "values": dict(want, Source=source, Installed=today)})
            continue
        changed = {k: v for k, v in want.items() if cur[k] != v}
        if "Last seen" in changed and cur["Last seen"] and cur["Last seen"] >= today:
            del changed["Last seen"]                      # Last seen only moves forward
        if changed:
            plan["update"].append({"skill": r["skill"], "id": cur["id"], "values": changed})
        else:
            plan["unchanged"].append({"skill": r["skill"]})
    keys = {r["skill"] for r in rows}
    for key, pages in existing.items():
        cur = pages[0]
        if key not in keys and cur["Status"] != "Removed":
            plan["remove"].append({"skill": key, "id": cur["id"], "values": {"Status": "Removed"}})
    return plan


def maybe_landed(e):
    """True when a failed create may nevertheless have been processed by Notion."""
    if isinstance(e, Unreachable):
        return e.ambiguous
    return e.status in (0, 409) or (e.status >= 500 and e.status != 529)      # 0: a 2xx whose body was not JSON


def find_created(cfg, ds, source, title):
    flt = {"and": [{"property": "Source", "select": {"equals": source}}, {"property": "Skill", "title": {"equals": title}}]}
    return any(c["Source"] == source and c["skill"] == title for c in query(cfg, ds, flt))


def create_page(cfg, ds, entry):
    """POST a new row. Never a blind retry: after a timeout / 409 / 5xx look for the row first, then try once more."""
    title, source = entry["skill"], entry["values"]["Source"]
    body = {"parent": {"type": "data_source_id", "data_source_id": ds}, "properties":
            {"Skill": to_prop("Skill", title), **{k: to_prop(k, v) for k, v in entry["values"].items()}}}
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
    counts = {"created": 0, "updated": 0, "removed": 0, "unchanged": len(plan["unchanged"]), "failed": 0}
    jobs = [("created", e, lambda e=e: create_page(cfg, ds, e)) for e in plan["create"]]
    for kind, key in (("updated", "update"), ("removed", "remove")):
        jobs += [(kind, e, lambda e=e: call(cfg, "PATCH", "/v1/pages/" + urllib.parse.quote(e["id"], safe=""),
                                            {"properties": {k: to_prop(k, v) for k, v in e["values"].items()}}))
                 for e in plan[key]]
    for kind, entry, job in jobs:
        try:
            job()
            counts[kind] += 1
            log(f"{kind} '{entry['skill']}'")
        except ApiError as e:
            log(f"FAILED {kind} '{entry['skill']}': {e}")
            if e.status in (401, 403):                  # the token lost its right to write: do not hammer on
                done = counts["created"] + counts["updated"] + counts["removed"]
                raise Stop(2, f"HTTP {e.status} during writes; {done} writes done before it")
            counts["failed"] += 1
        except Unreachable as e:
            counts["failed"] += 1
            log(f"FAILED {kind} '{entry['skill']}': {e}")
    return counts


# ---------------------------------------------------------------- enrich (vault only) and audit (read-only)

def enrich_plan(rows, statuses):
    """Updates for every row with Vault skill ticked whose Vault status differs from the vault's table."""
    plan = []
    for c in rows:
        if not c["Vault skill"]:
            continue
        want = statuses.get(c["skill"], "unknown")
        if c["Vault status"] != want:
            plan.append({"skill": c["skill"], "id": c["id"], "values": {"Vault status": want}})
    return plan


def run_enrich(args):
    cfg, _ = connection()
    vault = Path(args.vault or ROOT)
    statuses = vault_statuses(vault)
    try:
        ds, options = resolve(cfg, args)
        rows = query(cfg, ds, {"property": "Vault skill", "checkbox": {"equals": True}})
    except ApiError as e:
        raise Stop(2, str(e) + (NOT_FOUND_HINT if e.status == 404 else ""))
    except Unreachable as e:
        raise Stop(2, str(e))
    plan = enrich_plan(rows, statuses)
    missing = sorted({e["values"]["Vault status"] for e in plan} - set(options.get("Vault status", ())))
    if missing:
        raise Stop(2, "Vault status option(s) missing in Notion: " + ", ".join(missing))
    counts = {"enriched": 0, "unchanged": len(rows) - len(plan), "failed": 0}
    if args.dry_run:
        for e in plan:
            log(f"dry-run enrich '{e['skill']}' -> {e['values']['Vault status']}")
        counts["enriched"] = len(plan)
    else:
        for e in plan:
            try:
                call(cfg, "PATCH", "/v1/pages/" + urllib.parse.quote(e["id"], safe=""),
                     {"properties": {"Vault status": to_prop("Vault status", e["values"]["Vault status"])}})
                counts["enriched"] += 1
                log(f"enriched '{e['skill']}' -> {e['values']['Vault status']}")
            except ApiError as e2:
                if e2.status in (401, 403):
                    raise Stop(2, f"HTTP {e2.status} during writes; {counts['enriched']} writes done before it")
                counts["failed"] += 1
                log(f"FAILED enrich '{e['skill']}': {e2}")
            except Unreachable as e2:
                counts["failed"] += 1
                log(f"FAILED enrich '{e['skill']}': {e2}")
    res = {"ok": not counts["failed"], "enrich": True, "dry_run": args.dry_run, "counts": counts,
           "vault_skills": len(statuses), "data_source": ds.replace("-", "")[:8]}
    return res, (1 if counts["failed"] else 0)


def audit_rows(rows, today, source):
    today_d = datetime.date.fromisoformat(today)
    out = []

    def add(rule, row, detail):
        out.append({"rule": rule, "row": f"{row['skill']} @ {row['Project'] or '?'}", "detail": detail,
                    "mine": row["Source"] == source})
    for c in rows:
        if c["Status"] == "Installed" and c["Vault skill"] and c["Vault status"] not in APPROVED:
            add("draft-installed", c, f"vault skill with status {c['Vault status'] or 'unknown'} is installed")
    for c in rows:
        if c["Status"] != "Installed":
            continue
        try:
            age = (today_d - datetime.date.fromisoformat(c["Last seen"] or "")).days
        except ValueError:
            add("stale", c, "Installed, no Last seen")
            continue
        if age > STALE_DAYS:
            add("stale", c, f"last seen {c['Last seen']} ({age} days): run the inventory in that project")
    for c in rows:
        if c["Vault skill"] and c["Vault status"] in (None, "", "unknown"):
            add("unknown-vault", c, "Vault status not filled: the vault's --enrich run has not seen it")
    for c in rows:
        if c["Status"] == "Removed":
            add("removed", c, f"removed; last seen {c['Last seen'] or '?'}")
    order = {r: i for i, r in enumerate(RULES)}
    out.sort(key=lambda v: order[v["rule"]])
    return out


def run_audit(args):
    if args.dry_run:
        raise Stop(4, "--audit and --dry-run cannot be combined")
    today = check_today(args)
    cfg, _ = connection()
    source = args.source or default_labels(args)[1]
    try:
        ds, _ = resolve(cfg, args)
        rows = query(cfg, ds)
    except ApiError as e:
        raise Stop(2, str(e) + (NOT_FOUND_HINT if e.status == 404 else ""))
    except Unreachable as e:
        raise Stop(2, str(e))
    violations = audit_rows(rows, today, source)
    installed = [c for c in rows if c["Status"] == "Installed"]
    counts = {"rows": len(rows), "installed": len(installed), "projects": len({c["Project"] for c in installed if c["Project"]}),
              "violations": len([v for v in violations if v["rule"] != "removed"])}
    for rule in RULES:
        counts[rule] = len([v for v in violations if v["rule"] == rule])
    shown = [{"rule": v["rule"], "row": v["row"], "detail": v["detail"]} for v in violations if v["mine"] and v["rule"] != "removed"]
    other = len([v for v in violations if not v["mine"] and v["rule"] != "removed"])
    return {"ok": True, "audit": True, "counts": counts, "violations": shown, "other_source_violations": other,
            "data_source": ds.replace("-", "")[:8]}, 0


# ---------------------------------------------------------------- command line

def repo_identity(root):
    try:
        out = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=str(root), capture_output=True,
                             text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    parts = [p for p in re.split(r"[/:]", re.sub(r"\.git$", "", out.rstrip("/"))) if p]
    if re.search(r"://|@", out) and len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, Path(root).name


def default_labels(args):
    """(Project label, Source label) for this run."""
    if args.global_scope:
        label = args.project or "global:" + (socket.gethostname().split(".")[0] or "unknown")
        return label, args.source or label
    owner, repo = repo_identity(args.root or ROOT)
    project = args.project or repo
    return project, args.source or f"{repo}/skills-lock.json"


NOT_FOUND_HINT = " (not found: share the Skills HQ page with the integration, or use the data source id, not the database id)"


def check_today(args):
    today = args.today or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    try:
        datetime.date.fromisoformat(today)
    except ValueError:
        raise Stop(4, f"bad --today '{today}' (want YYYY-MM-DD)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", today):
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


def connection():
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
    """(data source id, select options): find the data source and check its schema."""
    given = args.data_source or os.environ.get("NOTION_SKILLS_DS")
    ds = given or find_data_source(cfg)
    try:
        options = check_schema(cfg, ds)
    except ApiError as e:
        if e.status != 404 or not given:
            raise
        ds = database_data_source(cfg, given, e)
        options = check_schema(cfg, ds)
    return ds, options


def run(args):
    if args.audit:
        return run_audit(args)
    if args.enrich:
        return run_enrich(args)
    today = check_today(args)
    override, version = api_settings()
    if args.global_scope:
        home = Path(args.home or Path.home())
        if not home.is_dir():
            raise Stop(3, f"--home {home} is not a directory")
        rows = dedupe(collect_global(home))
    else:
        root = Path(args.root or ROOT)
        if not root.is_dir():
            raise Stop(3, f"--root {root} is not a directory")
        root_is_vault = (root / "skills" / "vault-capture" / "SKILL.md").is_file() and (root / "CLAUDE.md").is_file()
        rows = dedupe(collect_project(root, root_is_vault))
    project, source = default_labels(args)
    res = {"ok": True, "dry_run": args.dry_run, "project": project, "source": source, "data_source": None,
           "rows": rows, "plan": None, "counts": None}
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        if args.dry_run:
            return res, 0
        raise Stop(2, "NOTION_TOKEN not set")
    cfg = token_config(token, version, override)
    try:
        ds, options = resolve(cfg, args)
        res["data_source"] = ds
        existing = fetch_existing(cfg, ds, source)
    except ApiError as e:
        raise Stop(2, str(e) + (NOT_FOUND_HINT if e.status == 404 else ""))
    except Unreachable as e:
        raise Stop(2, str(e))
    plan = res["plan"] = make_plan(rows, existing, project, source, today)
    check_options(options, plan)
    if args.dry_run:
        res["counts"] = {"created": len(plan["create"]), "updated": len(plan["update"]), "removed": len(plan["remove"]),
                         "unchanged": len(plan["unchanged"]), "failed": 0}
        for kind in ("create", "update", "remove"):
            for e in plan[kind]:
                log(f"dry-run {kind} '{e['skill']}' {sorted(e['values'])}")
        return res, 0
    res["counts"] = execute(cfg, ds, plan)
    return res, (1 if res["counts"]["failed"] else 0)


def render(res, as_json):
    if as_json:
        if res.get("plan") is not None:
            res = dict(res, plan={"create": [e["skill"] for e in res["plan"]["create"]],
                                  "update": [{"skill": e["skill"], "changed": sorted(e["values"])} for e in res["plan"]["update"]],
                                  "remove": [e["skill"] for e in res["plan"]["remove"]],
                                  "unchanged": [e["skill"] for e in res["plan"]["unchanged"]]})
        emit(json.dumps(res, ensure_ascii=False) + "\n")
        return
    if res.get("audit"):
        c = res["counts"]
        lines = ["skills-audit: " + " ".join(f"{k}={c[k]}" for k in c)]
        lines += [f"- [{v['rule']}] {v['row']} — {v['detail']}" for v in res["violations"]]
        if res["other_source_violations"]:
            lines.append(f"- {res['other_source_violations']} more violation(s) on rows from other projects; details only in "
                         "Notion (this repository is public).")
        emit("\n".join(lines) + "\n")
        return
    if res.get("enrich"):
        c = res["counts"]
        head = "dry-run " if res["dry_run"] else ""
        emit(f"skills-inventory: {head}enriched={c['enriched']} unchanged={c['unchanged']} failed={c['failed']} "
             f"vault_skills={res['vault_skills']} data_source={res['data_source']}\n")
        return
    c, ds8 = res["counts"], (res["data_source"] or "").replace("-", "")[:8]
    if res["dry_run"]:
        for r in res["rows"]:
            log(f"row {r['scope']} | {r['kind']} | {','.join(r['agents']) or '-'} | {'vault' if r['vault'] else '-'} | {r['skill']}")
    if c is None:
        emit(f"skills-inventory: dry-run rows={len(res['rows'])} project={res['project']} source={res['source']}\n")
        return
    head = "dry-run rows=%d " % len(res["rows"]) if res["dry_run"] else ""
    emit(f"skills-inventory: {head}created={c['created']} updated={c['updated']} removed={c['removed']} "
         f"unchanged={c['unchanged']} failed={c['failed']} source={res['source']} data_source={ds8}\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="Record installed agent skills in Notion; see the module docstring for exit codes.")
    p.add_argument("--project", help="Project label (default: the repo name; --global: global:<hostname>)")
    p.add_argument("--source", help="Source label, the rows this run owns (default: <repo>/skills-lock.json or the global label)")
    p.add_argument("--root", help="project checkout to scan (default: this script's repo root)")
    p.add_argument("--global", dest="global_scope", action="store_true", help="scan the computer's global skill folders instead")
    p.add_argument("--home", help="home directory for --global (default: the user's)")
    p.add_argument("--enrich", action="store_true", help="vault only: fill Vault status on every vault-skill row from skills/README.md")
    p.add_argument("--vault", help="vault checkout for --enrich (default: this script's repo root)")
    p.add_argument("--data-source", help="data source id (default: NOTION_SKILLS_DS, else search)")
    p.add_argument("--dry-run", action="store_true", help="collect and plan; never write")
    p.add_argument("--json", action="store_true", help="print one JSON object instead of the summary line")
    p.add_argument("--audit", action="store_true", help="read-only check of every row; see the docstring")
    p.add_argument("--today", help="override today's date, YYYY-MM-DD (tests)")
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 4 if e.code else 0                      # argparse's own exit 2 would read as "off"
    try:
        if args.audit and args.enrich:
            raise Stop(4, "--audit and --enrich cannot be combined")
        res, code = run(args)
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
        emit(f"skills-inventory: off ({reason})\n")
    else:
        emit(f"skills-inventory: error ({reason})\n", sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
