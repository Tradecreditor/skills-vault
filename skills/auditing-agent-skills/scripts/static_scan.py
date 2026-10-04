#!/usr/bin/env python3
"""Deterministic static scan of one Agent-Skills folder (stdlib only; reads files, never runs them).

Usage:
  python3 static_scan.py <skill-dir>              JSON report on stdout
  python3 static_scan.py --all <skills-root>      JSON array, one report per <skills-root>/*/SKILL.md
  python3 static_scan.py --hash <skill-dir>       content hash only (the value stored as metadata.review_hash)

Exit: 0 no block finding, 1 at least one block finding, 2 usage or read error.

Two classes of finding:
  block   no legitimate use inside a skill; any one of them rejects the skill and no reviewer can override it
  review  legitimate in many skills but risky; the reviewer must judge every rule id that fired

Every file under the folder is scanned and hashed, including dot-folders and ignored names such as node_modules/;
symlinks and images whose bytes are not that image format are block findings.
The patterns below are written so this file does not match itself (escaped dots, character classes),
because the auditing skill is scanned like any other.
"""
import hashlib
import json
import os
import re
import sys

VERSION = "static_scan.py 3"
MAX_TEXT_BYTES = 2_000_000
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp"}
EXEC_EXT = {".sh", ".bash", ".zsh", ".ps1", ".psm1", ".bat", ".cmd", ".py", ".js", ".mjs", ".cjs", ".ts",
            ".rb", ".pl", ".php", ".go", ".rs", ".lua", ".exe", ".dll", ".so", ".dylib", ".jar", ".bin", ".wasm"}
# Review bookkeeping written by the skill-review routine; excluded from the hash so recording a verdict
# does not change the hash it records.
# Only direct children of the frontmatter's top-level metadata: block (two-space indent) are excluded.
REVIEW_KEYS = re.compile(r"^  (vault_status|reviewed_at|reviewed_by|review_hash|review_report|review_scope):")
B64_LINE = re.compile(r"^[A-Za-z0-9+/]{40,}={0,2}$")

# Invisible or direction-changing characters, Unicode tag characters and variation selectors (the usual carriers of
# invisible instructions). U+FE0E / U+FE0F are allowed only singly, right after a non-ASCII character (emoji presentation).
HIDDEN = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\u00ad\ufe00-\ufe0d"
                    "\U000e0000-\U000e007f\U000e0100-\U000e01ef]")
EMOJI_VS = re.compile("[\ufe0e\ufe0f]")
SHOW = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\u00ad\ufe00-\ufe0f"
                  "\U000e0000-\U000e007f\U000e0100-\U000e01ef]")
IMAGE_MAGIC = {".png": (b"\x89PNG\r\n\x1a\n",), ".jpg": (b"\xff\xd8\xff",), ".jpeg": (b"\xff\xd8\xff",),
               ".gif": (b"GIF87a", b"GIF89a"), ".webp": (b"RIFF",), ".ico": (b"\x00\x00\x01\x00",), ".bmp": (b"BM",)}

BLOCK_RULES = [
    ("B1", "hidden or direction-changing Unicode", None),  # handled by HIDDEN, per character
    ("B2", "long encoded blob (base64 / hex)",
     re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{200,}={0,2}(?![A-Za-z0-9+/=])|(?<![0-9a-fA-F])[0-9a-fA-F]{200,}(?![0-9a-fA-F])")),
    ("B3", "decode-then-execute",
     re.compile(r"base64\s+(-d|--decode)[^\n]*\|\s*(sudo\s+)?(ba|z|da)?sh\b|eval\s*\(\s*(atob|Buffer\.from|base64)|exec\s*\(\s*(base64|codecs|zlib|bytes\.fromhex)|FromBase64Strin[g][^\n]*(iex|Invoke-Expression)", re.I)),
    ("B4", "reads credential stores",
     re.compile(r"~/\.ss[h]/|\bid_(rsa|ed25519|ecdsa)\b|\.aws/credential[s]|\.netr[c]\b|\.git-credential[s]|\.docker/config\.json|/etc/shado[w]|find-(generic|internet)-passwor[d]|\bLogin\.keychain|\.config/gh/hosts\.y[a]ml", re.I)),
    ("B5", "harvests environment variables",
     re.compile(r"\b(printenv|env)\s*\|\s*(curl|wget|nc|ncat|base64|xxd)|JSON\.stringify\s*\(\s*process\.env\s*\)|dict\s*\(\s*os\.environ\s*\)|os\.environ\.copy\s*\(\s*\)[^\n]*(post|send|request)|Get-ChildItem\s+env:[^\n]*\|", re.I)),
    ("B6", "known exfiltration endpoint",
     re.compile(r"webhook\.sit[e]|requestbi[n]|pipedream\.ne[t]|ngrok(-free)?\.(io|app|dev)|interact\.s[h]|oast\.(fun|pro|live|site|online|me)|burpcollaborato[r]|pastebin\.com/ap[i]|discord(app)?\.com/api/webhook[s]|hooks\.slack\.com/service[s]|transfer\.s[h]\b", re.I)),
    ("B7", "reverse shell",
     re.compile(r"/dev/tc[p]/|\b(nc|ncat|netcat)\b[^\n]*\s-[ec]\s|bash\s+-i\s*>&|socat\b[^\n]*exe[c]:", re.I)),
    ("B8", "instruction override or concealment from the user",
     re.compile(r"ignore\s+(all\s+|any\s+)?(the\s+|your\s+)?(previous|prior|above|earlier|system)\s+(instructions|prompts?|rules)|disregard\s+(all\s+|the\s+|your\s+)?(previous|prior|system|above)\s+(instructions|prompts?|rules)|(do\s+not|don't|never)\s+(tell|inform|mention\s+(this\s+)?to|reveal\s+(this\s+)?to|show)\s+the\s+user|without\s+(telling|informing|asking|notifying)\s+the\s+user|you\s+are\s+now\s+(in\s+)?(developer|DAN|jailbreak)", re.I)),
    ("B9", "destructive command on root or home",
     re.compile(r"\brm\s+-[a-z]*r[a-z]*f?[a-z]*\s+(--no-preserve-root\s+)?(/|~|\$HOME|\$\{HOME\})(\s|$|/\*)|\bmkfs(\.\w+)?\s+/dev/|\bdd\s+[^\n]*of=/dev/(sd|nvme|disk|hd)", re.I)),
    ("B10", "hard-coded secret",
     re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}|\bsk-(proj-)?[A-Za-z0-9]{32,}|\bghp_[A-Za-z0-9]{36}\b|github_pat_[A-Za-z0-9_]{40,}|\bAKIA[0-9A-Z]{16}\b|\bxox[baprs]-[A-Za-z0-9-]{10,}|\bapikey_[A-Za-z0-9]{16,}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KE[Y]-----")),
    ("B11", "binary, unreadable, symlinked or disguised file (cannot be reviewed)", None),  # handled per file
]

REVIEW_RULES = [
    ("R1", "pipes a download into an interpreter",
     re.compile(r"\b(curl|wget|iwr|irm|Invoke-WebRequest|Invoke-RestMethod)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|da)?sh\b|\b(curl|wget|iwr|irm|Invoke-WebRequest|Invoke-RestMethod)\b[^\n|]*\|\s*(sudo\s+)?(python3?|node|perl|ruby|iex|Invoke-Expression)\b", re.I)),
    ("R2", "installs third-party software",
     re.compile(r"\bnpm\s+(i|install|add)\b|\bnpx\s+(-y|--yes)\b|\bnpx\s+skills\s+add\b|\b(pnpm|yarn)\s+(add|dlx)\b|\bpip3?\s+install\b|\buv\s+(tool\s+install|pip\s+install|add)\b|\buvx\s|\bpipx\s+(install|run)\b|\bgo\s+install\b|\bcargo\s+install\b|\bbrew\s+install\b|\bgit\s+clone\b|\bdocker\s+(run|pull|build)\b|\b(claude|codex|gemini)\s+(plugin\s+install|mcp\s+add|extensions?\s+install)\b|/plugin\s+(install|marketplace\s+add)\b|\bapt(-get)?\s+install\b|\bwinget\s+install\b", re.I)),
    ("R3", "elevated privileges or loose permissions",
     re.compile(r"\bsudo\s|\bchmod\s+(-R\s+)?(777|666|a\+w|\+s|u\+s)\b|\bRunAs\b|-Verb\s+RunAs", re.I)),
    ("R4", "dynamic code execution",
     re.compile(r"\beval\s*\(|\bexec\s*\(|\bsubprocess\.|\bos\.(system|popen|exec\w*)\s*\(|\bchild_process\b|\bnew\s+Function\s*\(|\bpickle\.loads?\s*\(|\byaml\.load\s*\((?![^)]*SafeLoader)|\bInvoke-Expression\b|\biex\b|\bshell\s*=\s*True\b", re.I)),
    ("R5", "network access",
     re.compile(r"\bcurl\s|\bwget\s|\bfetch\s*\(|\brequests\.(get|post|put|delete|patch)\s*\(|\burllib\.request\b|\bhttp\.client\b|\baxios\b|\bInvoke-(WebRequest|RestMethod)\b|\bsocket\.socket\s*\(", re.I)),
    ("R6", "handles secrets or tokens",
     re.compile(r"\b[A-Z][A-Z0-9_]*(API_KEY|TOKEN|SECRET|PASSWORD|PRIVATE_KEY)\b|\bgh\s+auth\s+token\b|Authorization:\s*Bearer|\bcookies?\b|storageState", re.I)),
    ("R7", "weakens agent permissions or sandbox",
     re.compile(r"--dangerously-skip-permissions|\bbypassPermissions\b|--yolo\b|--no-sandbox\b|--full-auto\b|danger-full-access|approval[_-]policy|\bdefaultMode\b|--allow-all-tools|--trust-all", re.I)),
    ("R8", "writes agent configuration (settings, hooks, MCP, memory files)",
     re.compile(r"~/\.claude/|\.claude/settings(\.local)?\.json|~/\.codex/|\.codex/config\.toml|~/\.gemini/|\.mcp\.json\b|claude_desktop_config\.json|\"hooks\"\s*:|\bPreToolUse\b|\bPostToolUse\b|\bSessionStart\b|>>?\s*(CLAUDE|AGENTS|GEMINI)\.md", re.I)),
    ("R9", "persistence (scheduled jobs, startup, shell profiles)",
     re.compile(r"\bcrontab\b|\blaunchctl\b|LaunchAgents|LaunchDaemons|\bsystemctl\s+(--user\s+)?enable\b|>>\s*~/\.(bashrc|zshrc|profile|bash_profile|zprofile)|\bschtasks\b|\\Start Menu\\Programs\\Startup|Register-ScheduledTask", re.I)),
    ("R10", "deletes or rewrites data",
     re.compile(r"\brm\s+-[a-z]*r[a-z]*f|\bRemove-Item\b[^\n]*-Recurse|\bshutil\.rmtree\b|\bgit\s+push\s+[^\n]*(--force|-f\b)|\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[a-z]*f|\bDROP\s+(TABLE|DATABASE)\b|\btruncate\s+-s\s*0\b", re.I)),
    ("R11", "ships executable code", None),  # handled per file
]

SECRET_MASK = BLOCK_RULES[9][2]


def hidden(line, first_line=False):
    if first_line and line.startswith("\ufeff"):
        line = line[1:]
    if HIDDEN.search(line):
        return True
    for m in EMOJI_VS.finditer(line):
        i = m.start()
        if i == 0 or ord(line[i - 1]) < 0x80 or EMOJI_VS.match(line, i + 1):
            return True
    return False


def excerpt(line):
    s = SHOW.sub(lambda m: ("\\u%04x" if ord(m.group(0)) < 0x10000 else "\\U%08x") % ord(m.group(0)), line.strip())
    s = SECRET_MASK.sub("[MASKED]", s)
    return s[:160] + ("..." if len(s) > 160 else "")


def normalized_bytes(rel, data):
    if os.path.basename(rel) != "SKILL.md":
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    lines = text.replace("\r\n", "\n").split("\n")
    out, in_fm, in_meta = [], False, False
    for i, ln in enumerate(lines):
        if i == 0 and ln == "---":
            in_fm = True
        elif in_fm and ln == "---":
            in_fm = in_meta = False
        elif in_fm and not ln.startswith((" ", "\t")):
            in_meta = ln.rstrip() == "metadata:"
        elif in_meta and REVIEW_KEYS.match(ln):
            continue
        out.append(ln)
    return "\n".join(out).encode("utf-8")


def walk(skill_dir):
    """Every entry under the folder, hidden and ignored ones included; symlinks are listed, never followed."""
    def unreadable(err):
        raise err  # fail closed: a folder that cannot be listed cannot be reviewed

    files = []
    for root, dirs, names in os.walk(skill_dir, followlinks=False, onerror=unreadable):
        dirs.sort()
        for n in sorted(names) + [d for d in dirs if os.path.islink(os.path.join(root, d))]:
            p = os.path.join(root, n)
            files.append((os.path.relpath(p, skill_dir).replace(os.sep, "/"), p))
    return sorted(files)


def content_hash(skill_dir):
    h = hashlib.sha256()
    for rel, p in walk(skill_dir):
        if os.path.islink(p):
            data = b"symlink -> " + os.readlink(p).encode("utf-8", "replace")
        else:
            with open(p, "rb") as f:
                data = normalized_bytes(rel, f.read())
        h.update(rel.encode("utf-8") + b"\0" + data + b"\0")
    return h.hexdigest()


def scan(skill_dir):
    skill_dir = os.path.normpath(skill_dir)
    name = os.path.basename(skill_dir)
    report = {"skill": name, "path": skill_dir, "scanner": VERSION, "content_hash": content_hash(skill_dir),
              "files": [], "block": [], "review": []}
    for rel, p in walk(skill_dir):
        ext = os.path.splitext(rel)[1].lower()
        if os.path.islink(p):
            report["files"].append({"path": rel, "bytes": 0, "kind": "symlink", "executable": False})
            report["block"].append({"rule": "B11", "title": BLOCK_RULES[10][1], "file": rel, "line": 0,
                                    "excerpt": "symlink -> %s" % excerpt(os.readlink(p))})
            continue
        size = os.path.getsize(p)
        executable = os.access(p, os.X_OK) or ext in EXEC_EXT
        entry = {"path": rel, "bytes": size, "kind": "text", "executable": executable}
        report["files"].append(entry)
        with open(p, "rb") as f:
            data = f.read(MAX_TEXT_BYTES + 1)
        if ext in IMAGE_EXT:
            entry["kind"] = "image"
            magic = IMAGE_MAGIC[ext]
            if not any(data.startswith(m) for m in magic) or (ext == ".webp" and data[8:12] != b"WEBP"):
                report["block"].append({"rule": "B11", "title": BLOCK_RULES[10][1], "file": rel, "line": 0,
                                        "excerpt": "%s extension but the content is not that image format" % ext})
            continue
        try:
            text = data.decode("utf-8")
            if "\x00" in text or size > MAX_TEXT_BYTES:
                raise UnicodeDecodeError("utf-8", b"", 0, 1, "binary")
        except UnicodeDecodeError:
            entry["kind"] = "binary"
            report["block"].append({"rule": "B11", "title": BLOCK_RULES[10][1], "file": rel, "line": 0,
                                    "excerpt": "%d bytes, not UTF-8 text" % size})
            continue
        if executable:
            report["review"].append({"rule": "R11", "title": REVIEW_RULES[10][1], "file": rel, "line": 0,
                                     "excerpt": "%s, %d lines" % (ext or "no extension", text.count("\n") + 1)})
        run_start, run_chars, run_lines = 0, 0, 0
        for no, line in enumerate(text.splitlines() + [""], 1):
            if B64_LINE.match(line.strip()):
                if not run_lines:
                    run_start = no
                run_chars, run_lines = run_chars + len(line.strip()), run_lines + 1
                continue
            if run_lines >= 3 and run_chars >= 200:
                report["block"].append({"rule": "B2", "title": BLOCK_RULES[1][1], "file": rel, "line": run_start,
                                        "excerpt": "%d lines of base64-like text, %d characters" % (run_lines, run_chars)})
            run_chars, run_lines = 0, 0
        for no, line in enumerate(text.splitlines(), 1):
            if hidden(line, first_line=(no == 1)):
                report["block"].append({"rule": "B1", "title": BLOCK_RULES[0][1], "file": rel, "line": no,
                                        "excerpt": excerpt(line)})
            for rid, title, rx in BLOCK_RULES:
                if rx is not None and rx.search(line):
                    report["block"].append({"rule": rid, "title": title, "file": rel, "line": no, "excerpt": excerpt(line)})
            for rid, title, rx in REVIEW_RULES:
                if rx is not None and rx.search(line):
                    report["review"].append({"rule": rid, "title": title, "file": rel, "line": no, "excerpt": excerpt(line)})
    by_rule = {}
    for f in report["block"] + report["review"]:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    report["summary"] = {"block": len(report["block"]), "review": len(report["review"]),
                         "review_rules": sorted({f["rule"] for f in report["review"]}, key=lambda r: int(r[1:])),
                         "by_rule": dict(sorted(by_rule.items(), key=lambda kv: (kv[0][0], int(kv[0][1:]))))}
    report["floor"] = "REJECT" if report["block"] else "NEEDS_REVIEW"
    return report


def main(argv):
    try:
        if len(argv) == 3 and argv[1] == "--hash":
            print(content_hash(argv[2]))
            return 0
        if len(argv) == 3 and argv[1] == "--all":
            root = argv[2]
            dirs = [os.path.join(root, d) for d in sorted(os.listdir(root))
                    if os.path.isfile(os.path.join(root, d, "SKILL.md"))]
            reports = [scan(d) for d in dirs]
            print(json.dumps(reports, ensure_ascii=False, indent=1))
            return 1 if any(r["block"] for r in reports) else 0
        if len(argv) == 2 and os.path.isfile(os.path.join(argv[1], "SKILL.md")):
            r = scan(argv[1])
            print(json.dumps(r, ensure_ascii=False, indent=1))
            return 1 if r["block"] else 0
    except OSError as e:
        print("static_scan: %s" % e, file=sys.stderr)
        return 2
    print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
