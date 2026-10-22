"""Day 1 lab - same request, five runs, four kinds of evidence.

Modes
  cached  (default) prepared outputs, no internet, no key, no install
  ollama  a local model through Ollama (http://localhost:11434)
  openai  OpenAI API, needs OPENAI_API_KEY

Examples (PowerShell)
  python lab_day1.py
  python lab_day1.py --mode ollama --model llama3.2:3b --temperature 1.0
  python lab_day1.py --mode openai --model gpt-4.1-mini --top-p 0.8
  python lab_day1.py --label            # you label each run yourself
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from checks import check_run, release_verdict, summarise

HERE = Path(__file__).parent
LABELS = ("correct", "partial", "wrong", "unsafe")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_case() -> dict:
    return json.loads((HERE / "data" / "case.json").read_text(encoding="utf-8"))


def build_messages(case: dict) -> list[dict]:
    policy = "\n".join(f"{p['id']}: {p['text']}" for p in case["policy"])
    s = case["output_schema"]
    system = (
        "You are Lane, the customer-support assistant for Harbour & Lane.\n"
        "Follow this policy exactly:\n" + policy + "\n\n"
        "Reply with raw JSON only - no markdown, no prose - with exactly these keys:\n"
        f"category (one of {s['category']}), urgency (one of {s['urgency']}), "
        f"next_action (one of {s['next_action']}), customer_message (max 80 words)."
    )
    return [{"role": "system", "content": system},
            {"role": "user", "content": case["customer_message"]}]


def _post(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_ollama(case, args) -> list[str]:
    options = {}
    if args.temperature is not None:
        options["temperature"] = args.temperature
    if args.top_p is not None:
        options["top_p"] = args.top_p
    outs = []
    for i in range(args.runs):
        try:
            data = _post("http://localhost:11434/api/chat",
                         {"model": args.model, "messages": build_messages(case), "stream": False, "options": options},
                         {"Content-Type": "application/json"})
        except urllib.error.URLError:
            sys.exit("Ollama is not reachable on localhost:11434. Start Ollama, or run without --mode to use cached outputs.")
        outs.append(data["message"]["content"])
        print(f"  run {i + 1}/{args.runs} received")
    return outs


def run_openai(case, args) -> list[str]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit('OPENAI_API_KEY is not set. In PowerShell:  $env:OPENAI_API_KEY="sk-..."')
    outs = []
    for i in range(args.runs):
        payload = {"model": args.model, "messages": build_messages(case)}
        if args.temperature is not None:
            payload["temperature"] = args.temperature
        if args.top_p is not None:
            payload["top_p"] = args.top_p
        data = _post("https://api.openai.com/v1/chat/completions", payload,
                     {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        outs.append(data["choices"][0]["message"]["content"])
        print(f"  run {i + 1}/{args.runs} received")
    return outs


def load_cached() -> tuple[list[str], list[str]]:
    rows = [json.loads(l) for l in (HERE / "data" / "cached_outputs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return [r["raw"] for r in rows], [r["suggested_label"] for r in rows]


def ask_labels(raws: list[str]) -> list[str]:
    labels = []
    for i, raw in enumerate(raws, 1):
        print(f"\n--- Run {i} ---\n{raw}\n")
        while True:
            ans = input(f"Your label for run {i} {LABELS}: ").strip().lower()
            if ans in LABELS:
                labels.append(ans)
                break
            print("  type one of:", ", ".join(LABELS))
    return labels


def pct(x):
    return "n/a" if x is None else f"{x * 100:.0f}%"


def main() -> None:
    ap = argparse.ArgumentParser(description="Day 1 five-run variance lab")
    ap.add_argument("--mode", choices=["cached", "ollama", "openai"], default="cached")
    ap.add_argument("--model", default=None)
    ap.add_argument("--runs", type=int, default=5)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--temperature", type=float)
    g.add_argument("--top-p", dest="top_p", type=float)
    ap.add_argument("--label", action="store_true", help="label each run yourself")
    ap.add_argument("--labels", help="comma-separated labels, e.g. correct,correct,wrong,unsafe,correct")
    args = ap.parse_args()

    case = load_case()
    print(f"\nCase {case['case_id']}: {case['product']}")
    print(f"Customer: {case['customer_message']}\n")

    suggested: list[str] = []
    if args.mode == "cached":
        raws, suggested = load_cached()
        print("Mode: cached (prepared outputs - no model call)")
    else:
        args.model = args.model or ("llama3.2:3b" if args.mode == "ollama" else "gpt-4.1-mini")
        ctrl = f"temperature={args.temperature}" if args.temperature is not None else (
            f"top_p={args.top_p}" if args.top_p is not None else "provider default sampling")
        print(f"Mode: {args.mode}  model={args.model}  {ctrl}  runs={args.runs}")
        raws = run_ollama(case, args) if args.mode == "ollama" else run_openai(case, args)

    if args.labels:
        labels = [l.strip().lower() for l in args.labels.split(",")]
        if len(labels) != len(raws) or any(l not in LABELS for l in labels):
            sys.exit(f"--labels needs {len(raws)} values from {LABELS}")
    elif args.label:
        labels = ask_labels(raws)
    else:
        labels = suggested or [""] * len(raws)

    verdicts = [check_run(i, raw, case) for i, raw in enumerate(raws, 1)]

    print("\nHARD CHECKS (deterministic)")
    ids = [c.check_id for c in verdicts[0].checks]
    print("run  " + "  ".join(f"{c:>3}" for c in ids) + "   all   human label")
    for v, l in zip(verdicts, labels):
        cells = "  ".join(f"{'ok' if c.passed else 'X':>3}" for c in v.checks)
        print(f"{v.run:>3}  {cells}   {'PASS' if v.all_hard_pass else 'FAIL':>4}  {l or '-'}")
    print("\nCheck key: " + "; ".join(f"{c.check_id} {c.name}" for c in verdicts[0].checks))

    print("\nWHY RUNS FAILED")
    for v in verdicts:
        for c in v.checks:
            if not c.passed:
                print(f"  run {v.run} {c.check_id}: {c.detail}")

    s = summarise(verdicts, labels)
    print("\nEVIDENCE SUMMARY")
    print(f"  unique outputs            {pct(s['unique_output_rate'])}")
    print(f"  mean word overlap         {s['mean_pairwise_word_overlap']}")
    print(f"  raw JSON valid            {pct(s['format_valid_rate'])}")
    print(f"  all hard checks pass      {pct(s['all_hard_checks_rate'])}")
    print(f"  human says correct        {pct(s['human_correct_rate'])}")
    print(f"  checks vs human disagree  runs {s['disagreements'] or 'none'}")
    decision, why = release_verdict(s)
    print(f"\nRELEASE VERDICT: {decision}\n  {why}\n")

    out_dir = HERE / "outputs"
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"day1_{args.mode}_{stamp}.json"
    out.write_text(json.dumps({
        "mode": args.mode, "model": args.model, "temperature": args.temperature, "top_p": args.top_p,
        "runs": [{"run": v.run, "raw": v.raw, "label": l,
                  "checks": [c.__dict__ for c in v.checks]} for v, l in zip(verdicts, labels)],
        "summary": s, "verdict": decision,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Evidence saved to {out.relative_to(HERE)}")


if __name__ == "__main__":
    main()
