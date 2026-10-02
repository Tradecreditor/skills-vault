#!/usr/bin/env python3
"""jev_ask.py - the vault's one client for TypeSafe's Jev (System One) decision API.

    jev_ask.py probe [--base-url URL] [--model ID]
    jev_ask.py ask --state FILE|- [--questions FILE] [--act-min X --defer-min Y] [--timeout S] [--base-url URL] [--model ID]

`ask` reads JSON: either one object {"state": ..., "questions": {...}} or the state alone plus --questions.
Output: one JSON object on stdout; one log line per question on stderr
    jev <question> p=<value> band=<act|defer|no|-> model=<resolved version> state_sha=<8 hex>

Exit codes (the routine branches on these, never on the message text):
    0  answered
    2  Jev is OFF for the whole run: no accepted key reached the host (401, or 403 with an authentication_error body) or the
       host cannot be reached (proxy CONNECT refused, DNS, connection error)
    3  per-item fallback: 402 / 408 / 429 / 5xx, timeout, malformed or incomplete answer, or a 4xx that means the question
       JSON is wrong - do that item as the routine would without Jev, count it, keep going
    4  refused locally before any request: the state looks like it carries a secret or cookie, is far above the request
       limit, or the input JSON is invalid

Credentials: TYPESAFE_API_KEY from the environment, sent as a Bearer header to the configured base_url host only, never
printed or logged. Defaults can also come from JEV_BASE_URL and JEV_MODEL. JEV_FAKE=<file.json> answers from canned
values with no key and no network (see ../references/jev-fake.example.json). No third-party dependencies.
"""
import argparse
import hashlib
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.request
import uuid

DEFAULT_BASE_URL = "https://api.typesafe.ai"
DEFAULT_MODEL = "jev-latest"
MAX_STATE_CHARS = 120_000          # the API allows 32k tokens for state + longest question; refuse well above that
SECRET_PATTERNS = [                # names only are reported, never the matched text
    ("API key", re.compile(r"\bapikey_[A-Za-z0-9]{6,}|\bsk-[A-Za-z0-9_-]{12,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bxox[abp]-[A-Za-z0-9-]{10,}")),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")),
    ("cookie or session token", re.compile(r"\b(auth_token|ct0|sessionid|access_token|refresh_token|api_key|apikey|password)\s*[=:]\s*['\"]?[A-Za-z0-9._~+/=-]{8,}", re.I)),
    ("cookie or auth header", re.compile(r"(?im)^\s*(cookie|set-cookie|authorization)\s*:")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]


def fail(code, reason, off=False, http_status=None):
    out = {"ok": False, "off": off, "reason": reason}
    if http_status is not None:
        out["http_status"] = http_status
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(code)


def band_of(value, act_min, defer_min):
    if act_min is None or defer_min is None or value is None:
        return "-"
    return "act" if value >= act_min else "defer" if value >= defer_min else "no"


def check_state(state):
    text = json.dumps(state, ensure_ascii=False, sort_keys=True)
    if len(text) > MAX_STATE_CHARS:
        fail(4, f"state too large ({len(text)} chars; keep the state under the 32k-token request limit)")
    for name, pat in SECRET_PATTERNS:
        if pat.search(text):
            fail(4, f"state refused: {name} found in the state; send data fields only")
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def fake_answers(path, questions):
    canned = json.load(open(path, encoding="utf-8"))
    answers = {}
    for name, q in questions.items():
        if name not in canned:
            fail(4, f"JEV_FAKE has no canned answer for question '{name}'")
        v = canned[name]
        t = q.get("type")
        if t == "noul":
            answers[name] = {"type": "noul", "noul": float(v)}
        elif t == "score":
            answers[name] = {"type": "score", "score": float(v), "legend": {}, "probabilities": {}, "confidence": 1.0}
        elif t == "choice":
            probs = dict(v) if isinstance(v, dict) else {str(v): 1.0}
            answers[name] = {"type": "choice", "choice": max(probs, key=probs.get), "probabilities": probs, "confidence": max(probs.values())}
        else:
            fail(4, f"question '{name}' has unknown type {t!r}")
    return {"model": "fake", "answers": answers, "usage": {"input_tokens": 0}}


def post(base_url, model, state, questions, timeout):
    fake = os.environ.get("JEV_FAKE")
    if fake:
        return fake_answers(fake, questions)
    url = base_url.rstrip("/") + "/v1/systemone"
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Idempotency-Key": str(uuid.uuid4())}
    key = os.environ.get("TYPESAFE_API_KEY")
    if key:
        headers["Authorization"] = "Bearer " + key
    body = json.dumps({"state": state, "model": model, "questions": questions}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300].replace("\n", " ")
        if e.code == 401 or (e.code == 403 and "authentication_error" in detail):
            fail(2, f"no accepted key reached {urllib.parse.urlsplit(url).hostname} ({e.code} {detail})", off=True, http_status=e.code)
        if e.code == 403:
            fail(2, f"403 without an authentication_error body ({detail})", off=True, http_status=e.code)
        fail(3, f"HTTP {e.code} ({detail})", http_status=e.code)
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as e:
        reason = getattr(e, "reason", e)
        if isinstance(reason, (socket.timeout, TimeoutError)) or "timed out" in str(reason).lower():
            fail(3, f"timeout after {timeout}s")
        fail(2, f"cannot reach {urllib.parse.urlsplit(url).hostname} ({reason})", off=True)
    try:
        resp = json.loads(raw.decode("utf-8"))
    except ValueError:
        fail(3, "malformed response (not JSON)")
    if not isinstance(resp, dict) or not isinstance(resp.get("answers"), dict):
        fail(3, "malformed response (no answers object)")
    return resp


def normalise(resp, questions, act_min, defer_min):
    answers = {}
    for name in questions:
        a = resp["answers"].get(name)
        if not isinstance(a, dict):
            fail(3, f"answer for '{name}' missing")
        t = a.get("type", questions[name].get("type"))
        try:
            if t == "noul":
                value = float(a["noul"])
                out = {"type": t, "value": value, "band": band_of(value, act_min, defer_min)}
            elif t == "score":
                value = float(a["score"])
                out = {"type": t, "value": value, "band": band_of(value, act_min, defer_min),
                       "legend": a.get("legend", {}), "probabilities": a.get("probabilities", {}), "confidence": a.get("confidence")}
            elif t == "choice":
                probs = {k: float(v) for k, v in a["probabilities"].items()}
                top = a.get("choice") or max(probs, key=probs.get)
                out = {"type": t, "value": top, "band": band_of(probs.get(top), act_min, defer_min),
                       "probabilities": probs, "confidence": a.get("confidence")}
            else:
                fail(3, f"answer for '{name}' has unknown type {t!r}")
        except (KeyError, TypeError, ValueError) as e:
            fail(3, f"answer for '{name}' malformed ({e.__class__.__name__}: {e})")
        answers[name] = out
    return answers


def run(base_url, model, state, questions, act_min, defer_min, timeout):
    sha = check_state(state)
    for name, q in questions.items():
        if not isinstance(q, dict) or q.get("type") not in ("noul", "choice", "score") or not q.get("instructions"):
            fail(4, f"question '{name}' needs type noul|choice|score and instructions")
    resp = post(base_url, model, state, questions, timeout)
    answers = normalise(resp, questions, act_min, defer_min)
    version = resp.get("model", model)
    for name, a in answers.items():
        print(f"jev {name} p={a['value']} band={a['band']} model={version} state_sha={sha}", file=sys.stderr)
    return {"ok": True, "model": version, "answers": answers, "usage": resp.get("usage", {}), "state_sha": sha}


def main(argv=None):
    p = argparse.ArgumentParser(description="Ask TypeSafe's Jev typed questions; see the module docstring for exit codes.")
    p.add_argument("--base-url", default=os.environ.get("JEV_BASE_URL", DEFAULT_BASE_URL), help="provider base URL (default TypeSafe direct)")
    p.add_argument("--model", default=os.environ.get("JEV_MODEL", DEFAULT_MODEL))
    p.add_argument("--timeout", type=float, default=10.0, help="seconds per request")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe", help="one tiny noul question: is Jev on for this run?")
    a = sub.add_parser("ask", help="POST a state and a questions map")
    a.add_argument("--state", required=True, help="JSON file, or - for stdin; {state, questions} or the state alone")
    a.add_argument("--questions", help="JSON file with the questions map (when --state holds the state alone)")
    a.add_argument("--act-min", type=float, help="value >= act-min -> band act")
    a.add_argument("--defer-min", type=float, help="defer-min <= value < act-min -> band defer; below -> no")
    args = p.parse_args(argv)

    if args.cmd == "probe":
        questions = {"probe": {"type": "noul", "instructions": "The state is the single word probe."}}
        out = run(args.base_url, args.model, "probe", questions, None, None, args.timeout)
        print(json.dumps({"ok": True, "model": out["model"], "probe": out["answers"]["probe"]["value"], "usage": out["usage"]}, ensure_ascii=False))
        return 0

    try:
        doc = json.load(sys.stdin if args.state == "-" else open(args.state, encoding="utf-8"))
        questions = json.load(open(args.questions, encoding="utf-8")) if args.questions else None
    except (OSError, ValueError) as e:
        fail(4, f"cannot read input JSON ({e})")
    if questions is None:
        if not (isinstance(doc, dict) and "state" in doc and isinstance(doc.get("questions"), dict)):
            fail(4, "input must be {\"state\": ..., \"questions\": {...}} or pass --questions")
        state, questions = doc["state"], doc["questions"]
    else:
        state = doc
    if not isinstance(questions, dict) or not questions:
        fail(4, "questions must be a non-empty object")
    if (args.act_min is None) != (args.defer_min is None):
        fail(4, "--act-min and --defer-min go together")
    out = run(args.base_url, args.model, state, questions, args.act_min, args.defer_min, args.timeout)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
