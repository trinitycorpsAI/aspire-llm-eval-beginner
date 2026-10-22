"""Day 2 lab A - run C1 to C5 as DeepEval metrics on the five Day 1 replies.

    python day2_eval.py

No API key, no internet, no LLM. Same five replies as Day 1, so you can check
DeepEval reaches the same verdicts you saw in the browser yesterday.
"""
import os

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")

import json
import sys
from pathlib import Path

from deepeval import evaluate
from deepeval.test_case import LLMTestCase

from metrics import day1_contract

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).parent
DAY1 = HERE.parent / "day-01" / "lab" / "data"

case = json.loads((DAY1 / "case.json").read_text(encoding="utf-8"))
rows = [json.loads(l) for l in (DAY1 / "cached_outputs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

# 1. DATASET: one LLMTestCase per reply. The input is Daniel's message, the
#    actual_output is exactly what the model returned - unmodified.
test_cases = [
    LLMTestCase(
        input=case["customer_message"],
        actual_output=row["raw"],
        name=f"run-{row['run']}",
        additional_metadata={"run": row["run"], "human_label": row["suggested_label"]},
    )
    for row in rows
]

# 2-3. RUN + SCORE: DeepEval applies every metric to every test case.
result = evaluate(
    test_cases=test_cases,
    metrics=day1_contract(),
    hyperparameters={"case": case["case_id"], "contract": "C1-C5", "model": "cached Day 1 outputs"},
)

# 4. ANALYSE: put the machine verdict next to the human label.
print("\nRUN   C1 C2 C3 C4 C5   ALL    HUMAN LABEL")
for tr in sorted(result.test_results, key=lambda t: t.name):
    marks = {m.name.split()[0]: ("ok" if m.success else "X") for m in tr.metrics_data}
    cells = "  ".join(f"{marks[c]:>2}" for c in ("C1", "C2", "C3", "C4", "C5"))
    label = (tr.metadata or {}).get("human_label", "-")
    print(f"{tr.name:<6} {cells}   {'PASS' if tr.success else 'FAIL'}   {label}")
print("\nRun 5 passes C1-C5 and is still unsafe. That is the gap C6-C10 and, later, an LLM judge must close.")
