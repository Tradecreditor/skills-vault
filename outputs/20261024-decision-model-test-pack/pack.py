#!/usr/bin/env python3
"""Decision-model test pack: export requests, list gold labels, score runs.

Python 3.8+, standard library only.

  python3 pack.py split  [--out requests] [--model jev-1.13.0] [--flatten] [--suite A-topical]
  python3 pack.py csv    [--out cases.csv]
  python3 pack.py score  --runs runs/ [--out report.md] [--json summary.json]

cases.jsonl holds one case per line: {id, suite, request: {state, questions}, gold, ref, meta}.
Only `request` may be sent to a model. `gold`, `ref` and `meta` are the answer key.

A run file is runs/<label>.jsonl, one line per call:
  {"id": "A01", "rep": 1, "model": "jev-1.14.0", "answers": {...}, "latency_ms": 240,
   "input_tokens": 1830, "cost_usd": 0.000077, "error": null}
`answers` is the model's answers object exactly as Jev returns it (noul / choice + probabilities /
score + probabilities); the vault's jev_ask.py shape (`value`) and the LLM-baseline prompt's shape
are accepted too.
"""
import argparse, csv, glob, json, math, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
THRESH = {  # the vault's live thresholds (wiki/hot-list/_config.yaml, skills/judging-with-jev)
    "A-topical": {"q": "topical", "act": 0.80, "defer": 0.50},
    "D-same_item": {"q": "same_item", "act": 0.80, "defer": 0.50},
    "B-in_scope": {"q": "in_scope", "act": 3.0, "defer": 1.5},
    "C-type_topic": {"q": ["type", "topic"], "use_min": 0.60},
}


def load_cases(path=None):
    path = path or os.path.join(HERE, "cases.jsonl")
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


# ---------------------------------------------------------------- split / csv
def flatten(questions):
    """OpenRouter's Decisions adapter takes instructions and criteria as strings only."""
    out = {}
    for k, q in questions.items():
        q = dict(q)
        if isinstance(q.get("criteria"), (list, dict)):
            q["criteria"] = json.dumps(q["criteria"], ensure_ascii=False)
        out[k] = q
    return out


def cmd_split(a):
    os.makedirs(a.out, exist_ok=True)
    n = 0
    for c in load_cases(a.cases):
        if a.suite and c["suite"] != a.suite:
            continue
        req = {"state": c["request"]["state"], "questions": c["request"]["questions"]}
        if a.flatten:
            req["questions"] = flatten(req["questions"])
        if a.model:
            req["model"] = a.model
        with open(os.path.join(a.out, c["id"] + ".json"), "w", encoding="utf-8") as fh:
            json.dump(req, fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"wrote {n} request files to {a.out}")


def short(c):
    s = c["request"]["state"]
    if c["suite"] == "A-topical":
        return f'{s["full_name"]}: {s["description"]}'
    if c["suite"] == "B-in_scope":
        return f'{s["author"]}: {s["snippet"]}'
    if c["suite"] == "C-type_topic":
        return f'{s["title"]}'
    return f'{s["post"]["author"]}: {s["post"]["text"][:120]} || {s["repo"]["full_name"]}'


def cmd_csv(a):
    rows = []
    for c in load_cases(a.cases):
        g = c["gold"]
        if c["suite"] == "A-topical":
            gold, extra = g["topical"], g["difficulty"]
        elif c["suite"] == "D-same_item":
            gold, extra = g["same_item"], g["difficulty"]
        elif c["suite"] == "B-in_scope":
            gold, extra = g["in_scope"], f'acceptable {g["acceptable"][0]}-{g["acceptable"][1]}, band {g["band"]}'
        else:
            gold, extra = g["type"], f'topic {g["topic"] or "-"}'
        prod = "; ".join(f'{p["run"]} {p["p"]}' for p in c["ref"].get("jev_prod", []))
        rows.append([c["id"], c["suite"], c["meta"].get("question_id", ""), c["meta"].get("item", ""), gold, extra,
                     g.get("source", ""), g.get("note", ""), prod, " ".join(short(c).split())[:220]])
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "suite", "question", "item", "gold", "gold_detail", "gold_source", "note", "jev_1.13_production", "text"])
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {a.out}")


# ---------------------------------------------------------------- answer parsing
def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def noul_p(ans):
    if isinstance(ans, (int, float)):
        return float(ans)
    if not isinstance(ans, dict):
        return None
    for k in ("noul", "value", "probability", "p"):
        if k in ans and _num(ans[k]) is not None:
            return _num(ans[k])
    return None


def score_v(ans):
    if isinstance(ans, (int, float)):
        return float(ans)
    if not isinstance(ans, dict):
        return None
    for k in ("score", "value"):
        if k in ans and _num(ans[k]) is not None:
            return _num(ans[k])
    return None


def choice_probs(ans):
    if isinstance(ans, str):
        return {ans: 1.0}
    if not isinstance(ans, dict):
        return None
    probs = ans.get("probabilities")
    if isinstance(probs, dict) and probs:
        probs = {k: _num(v) or 0.0 for k, v in probs.items()}
        tot = sum(probs.values())
        return {k: v / tot for k, v in probs.items()} if tot > 0 else None
    lab = ans.get("choice", ans.get("value"))
    return {lab: 1.0} if isinstance(lab, str) else None


# ---------------------------------------------------------------- metrics helpers
def band(x, act, defer):
    return "act" if x >= act else ("defer" if x >= defer else "no")


def brier(ps, ys):
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps)


def ece(ps, ys, bins=5):
    tot, err = len(ps), 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, p in enumerate(ps) if (lo <= p < hi) or (b == bins - 1 and p == 1.0)]
        if idx:
            conf = sum(ps[i] for i in idx) / len(idx)
            acc = sum(ys[i] for i in idx) / len(idx)
            err += len(idx) / tot * abs(conf - acc)
    return err


def auroc(ps, ys):
    pos = [p for p, y in zip(ps, ys) if y]
    neg = [p for p, y in zip(ps, ys) if not y]
    if not pos or not neg:
        return None
    wins = sum(1.0 if a > b else 0.5 if a == b else 0.0 for a in pos for b in neg)
    return wins / (len(pos) * len(neg))


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    if len(xs) < 3:
        return None
    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def pct(x):
    return "-" if x is None else f"{100 * x:.0f}%"


def f3(x):
    return "-" if x is None else f"{x:.3f}"


# ---------------------------------------------------------------- scoring
def load_runs(path):
    files = sorted(glob.glob(os.path.join(path, "*.jsonl"))) if os.path.isdir(path) else [path]
    runs = {}
    for f in files:
        label = os.path.splitext(os.path.basename(f))[0]
        rows = []
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    rows.append(json.loads(line))
        runs[label] = rows
    return runs


def score_model(cases, rows):
    by_id = defaultdict(list)
    for r in rows:
        by_id[r["id"]].append(r)
    out = {"ops": {}, "suites": {}}
    lat = [r["latency_ms"] for r in rows if _num(r.get("latency_ms")) is not None and not r.get("error")]
    out["ops"] = {
        "calls": len(rows), "errors": sum(1 for r in rows if r.get("error")),
        "cases_answered": len(by_id), "cases_total": len(cases),
        "latency_p50_ms": statistics.median(lat) if lat else None,
        "latency_p90_ms": sorted(lat)[int(0.9 * (len(lat) - 1))] if lat else None,
        "input_tokens": sum(int(r.get("input_tokens") or 0) for r in rows),
        "cost_usd": sum(float(r.get("cost_usd") or 0) for r in rows) if any(r.get("cost_usd") is not None for r in rows) else None,
        "models_resolved": sorted({str(r.get("model")) for r in rows if r.get("model")}),
    }
    q_answers = sum(len(r.get("answers") or {}) for r in rows if not r.get("error"))
    out["ops"]["cost_per_1k_decisions_usd"] = (1000 * out["ops"]["cost_usd"] / q_answers) if q_answers and out["ops"]["cost_usd"] is not None else None

    def reps(cid):
        return [r for r in by_id.get(cid, []) if not r.get("error") and isinstance(r.get("answers"), dict)]

    for suite in ("A-topical", "D-same_item"):
        t = THRESH[suite]; q = t["q"]
        res = {"clear": [], "borderline": []}
        flips, stds, drift, drift_band = 0, [], [], 0
        for c in (c for c in cases if c["suite"] == suite):
            vals = [noul_p(r["answers"].get(q)) for r in reps(c["id"])]
            vals = [v for v in vals if v is not None]
            if not vals:
                continue
            p = statistics.mean(vals)
            if len(vals) > 1:
                stds.append(statistics.pstdev(vals))
                flips += len({band(v, t["act"], t["defer"]) for v in vals}) > 1
            y = bool(c["gold"][q])
            res[c["gold"]["difficulty"]].append((p, y, c["id"]))
            prod = c["ref"].get("jev_prod") or []
            if prod:
                last = prod[-1]["p"]
                drift.append(abs(p - last))
                drift_band += band(p, t["act"], t["defer"]) != band(last, t["act"], t["defer"])
        if not res["clear"] and not res["borderline"]:
            continue
        s = {}
        cl = res["clear"]
        if cl:
            ps, ys = [x[0] for x in cl], [x[1] for x in cl]
            bands = [band(p, t["act"], t["defer"]) for p in ps]
            s.update({
                "n_clear": len(cl),
                "acc_at_0.5": sum((p >= 0.5) == y for p, y in zip(ps, ys)) / len(cl),
                "auto_correct": sum((b == "act" and y) or (b == "no" and not y) for b, y in zip(bands, ys)) / len(cl),
                "auto_wrong": sum((b == "act" and not y) or (b == "no" and y) for b, y in zip(bands, ys)) / len(cl),
                "deferred": bands.count("defer") / len(cl),
                "brier": brier(ps, [float(y) for y in ys]), "ece": ece(ps, [float(y) for y in ys]), "auroc": auroc(ps, ys),
                "wrong_ids": [i for (p, y, i), b in zip(cl, bands) if (b == "act" and not y) or (b == "no" and y)],
            })
        bl = res["borderline"]
        if bl:
            s["n_borderline"] = len(bl)
            s["borderline_deferred"] = sum(t["defer"] <= p < t["act"] for p, _, _ in bl) / len(bl)
            s["borderline_acc_at_0.5"] = sum((p >= 0.5) == y for p, y, _ in bl) / len(bl)
        s["repeat_std_mean"] = statistics.mean(stds) if stds else None
        s["repeat_band_flips"] = flips if stds else None
        if drift:
            s["vs_jev_prod_mean_abs_diff"] = statistics.mean(drift)
            s["vs_jev_prod_band_changes"] = drift_band
            s["vs_jev_prod_n"] = len(drift)
        out["suites"][suite] = s

    # B: five-level score, 0-4
    t = THRESH["B-in_scope"]; q = t["q"]
    xs, gs, within, agree, missed, noise, stds, flips, wrong = [], [], 0, 0, 0, 0, [], 0, []
    for c in (c for c in cases if c["suite"] == "B-in_scope"):
        vals = [score_v(r["answers"].get(q)) for r in reps(c["id"])]
        vals = [v for v in vals if v is not None]
        if not vals:
            continue
        v = statistics.mean(vals)
        if len(vals) > 1:
            stds.append(statistics.pstdev(vals))
            flips += len({band(x, t["act"], t["defer"]) for x in vals}) > 1
        g = c["gold"]
        xs.append(v); gs.append(g["in_scope"])
        lo, hi = g["acceptable"]
        within += (lo - 0.5) <= v <= (hi + 0.5)
        mb = band(v, t["act"], t["defer"])
        gb = {"act": "act", "defer": "defer", "skip": "no"}[g["band"]]
        agree += mb == gb
        if gb == "act" and mb == "no":
            missed += 1; wrong.append(c["id"])
        if gb == "no" and mb == "act":
            noise += 1; wrong.append(c["id"])
    if xs:
        n = len(xs)
        out["suites"]["B-in_scope"] = {
            "n": n, "mae": sum(abs(a - b) for a, b in zip(xs, gs)) / n, "within_acceptable": within / n,
            "band_agreement": agree / n, "missed_act_items": missed, "noise_acted": noise, "spearman": spearman(xs, gs),
            "acted_share": sum(x >= t["act"] for x in xs) / n,
            "repeat_std_mean": statistics.mean(stds) if stds else None, "repeat_band_flips": flips if stds else None,
            "wrong_ids": wrong,
        }

    # C: two choice questions in one request
    s = {}
    for q in ("type", "topic"):
        hits, n, conf_hits, conf_n, ll, tops, ys, wrong = 0, 0, 0, 0, [], [], [], []
        for c in (c for c in cases if c["suite"] == "C-type_topic"):
            gold = c["gold"][q]
            if not gold:
                continue
            dists = [choice_probs(r["answers"].get(q)) for r in reps(c["id"])]
            dists = [d for d in dists if d]
            if not dists:
                continue
            labs = set().union(*dists)
            avg = {k: sum(d.get(k, 0.0) for d in dists) / len(dists) for k in labs}
            top = max(avg, key=avg.get)
            n += 1; ok = top == gold; hits += ok
            if not ok:
                wrong.append(c["id"])
            tops.append(avg[top]); ys.append(float(ok))
            ll.append(-math.log(max(avg.get(gold, 0.0), 1e-6)))
            if avg[top] >= THRESH["C-type_topic"]["use_min"]:
                conf_n += 1; conf_hits += ok
        if n:
            s[q] = {"n": n, "acc": hits / n, "coverage_at_0.60": conf_n / n,
                    "acc_when_used_at_0.60": (conf_hits / conf_n) if conf_n else None,
                    "log_loss": statistics.mean(ll), "ece_top": ece(tops, ys), "wrong_ids": wrong}
    if s:
        out["suites"]["C-type_topic"] = s
    return out


def render(summary):
    L = ["# Decision-model comparison", "",
         "Thresholds are the vault's live ones: topical / same_item act >= 0.80, defer 0.50-0.80; in_scope act >= 3.0, defer 1.5-3.0; "
         "type / topic used when the top probability >= 0.60. Accuracy uses the mean over repeats.", ""]
    models = list(summary)
    L += ["## Ops", "", "| model | resolved | calls | errors | answered / total | p50 ms | p90 ms | input tokens | cost USD | USD per 1k decisions |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        o = summary[m]["ops"]
        per_k = "-" if o["cost_per_1k_decisions_usd"] is None else f'{o["cost_per_1k_decisions_usd"]:.4f}'
        L.append(f'| {m} | {", ".join(o["models_resolved"]) or "-"} | {o["calls"]} | {o["errors"]} | {o["cases_answered"]} / {o["cases_total"]} | '
                 f'{o["latency_p50_ms"] or "-"} | {o["latency_p90_ms"] or "-"} | {o["input_tokens"] or "-"} | {"-" if o["cost_usd"] is None else f"{o['cost_usd']:.5f}"} | {per_k} |')
    for suite, title in (("A-topical", "A · H2 `topical` (noul, live)"), ("D-same_item", "D · H3 `same_item` (noul, configured)")):
        L += ["", f"## {title}", "",
              "| model | n clear | auto-correct | **auto-wrong** | deferred | acc@0.5 | Brier | ECE | AUROC | borderline deferred | repeat std | band flips | vs Jev 1.13 prod: mean abs diff (band changes) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for m in models:
            s = summary[m]["suites"].get(suite)
            if not s:
                continue
            vp = "-" if "vs_jev_prod_mean_abs_diff" not in s else f'{s["vs_jev_prod_mean_abs_diff"]:.3f} ({s["vs_jev_prod_band_changes"]}/{s["vs_jev_prod_n"]})'
            L.append(f'| {m} | {s.get("n_clear", 0)} | {pct(s.get("auto_correct"))} | **{pct(s.get("auto_wrong"))}** | {pct(s.get("deferred"))} | '
                     f'{pct(s.get("acc_at_0.5"))} | {f3(s.get("brier"))} | {f3(s.get("ece"))} | {f3(s.get("auroc"))} | '
                     f'{pct(s.get("borderline_deferred"))} | {f3(s.get("repeat_std_mean"))} | {"-" if s.get("repeat_band_flips") is None else s["repeat_band_flips"]} | {vp} |')
        for m in models:
            s = summary[m]["suites"].get(suite)
            if s and s.get("wrong_ids"):
                L.append(f'- {m} auto-wrong: {", ".join(s["wrong_ids"])}')
    L += ["", "## B · H1 `in_scope` (score 0-4, live)", "",
          "| model | n | MAE | within acceptable | band agreement | missed act items | noise acted | acted share | Spearman | repeat std | band flips |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        s = summary[m]["suites"].get("B-in_scope")
        if s:
            L.append(f'| {m} | {s["n"]} | {f3(s["mae"])} | {pct(s["within_acceptable"])} | {pct(s["band_agreement"])} | {s["missed_act_items"]} | '
                     f'{s["noise_acted"]} | {pct(s["acted_share"])} | {f3(s["spearman"])} | {f3(s["repeat_std_mean"])} | {s["repeat_band_flips"] if s["repeat_band_flips"] is not None else "-"} |')
    L += ["", "## C · capture-link `type` + `topic` (choice, planned)", "",
          "| model | type acc | type coverage@0.60 | type acc when used | topic acc | topic coverage@0.60 | topic acc when used | type log loss | topic log loss |",
          "|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        s = summary[m]["suites"].get("C-type_topic")
        if not s:
            continue
        ty, to = s.get("type", {}), s.get("topic", {})
        L.append(f'| {m} | {pct(ty.get("acc"))} | {pct(ty.get("coverage_at_0.60"))} | {pct(ty.get("acc_when_used_at_0.60"))} | {pct(to.get("acc"))} | '
                 f'{pct(to.get("coverage_at_0.60"))} | {pct(to.get("acc_when_used_at_0.60"))} | {f3(ty.get("log_loss"))} | {f3(to.get("log_loss"))} |')
    return "\n".join(L) + "\n"


def cmd_score(a):
    cases = load_cases(a.cases)
    runs = load_runs(a.runs)
    if not runs:
        sys.exit(f"no run files in {a.runs}")
    summary = {label: score_model(cases, rows) for label, rows in runs.items()}
    md = render(summary)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(md)
    else:
        sys.stdout.write(md)
    if a.json:
        json.dump(summary, open(a.json, "w", encoding="utf-8"), indent=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", default=None, help="path to cases.jsonl (default: next to this script)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("split", help="one {state, questions} JSON file per case")
    p.add_argument("--out", default="requests"); p.add_argument("--model"); p.add_argument("--suite")
    p.add_argument("--flatten", action="store_true", help="criteria as strings (OpenRouter's Decisions adapter)")
    p.set_defaults(f=cmd_split)
    p = sub.add_parser("csv", help="gold-label overview as CSV")
    p.add_argument("--out", default="cases.csv"); p.set_defaults(f=cmd_csv)
    p = sub.add_parser("score", help="score runs/<label>.jsonl against the gold labels")
    p.add_argument("--runs", required=True); p.add_argument("--out"); p.add_argument("--json")
    p.set_defaults(f=cmd_score)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
