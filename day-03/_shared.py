"""Helpers shared by the Day 3 labs. Loads Day 1 data and Day 2 metrics."""
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
HERE = Path(__file__).parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "day-02"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DAY1 = REPO / "day-01" / "lab" / "data"
CASE = json.loads((DAY1 / "case.json").read_text(encoding="utf-8"))
RUNS = [json.loads(l) for l in (DAY1 / "cached_outputs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
GOLDEN = json.loads((HERE / "data" / "golden.json").read_text(encoding="utf-8"))


def message_of(raw: str) -> str:
    """The customer_message inside a reply (fences tolerated here - C1 judges format separately)."""
    text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", raw.strip())
    try:
        return str(json.loads(text).get("customer_message", ""))
    except json.JSONDecodeError:
        return ""


def _load_jsonl(path: Path) -> list[dict]:
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as err:
            print(f"!! {path.name} line {n} is not valid JSON ({err.msg}) - check quotes and commas. Skipped.")
    return rows


def my_runs() -> list[dict]:
    """Learner-written replies from data/my_replies.jsonl, shaped like the Day 1 runs."""
    out = []
    for r in _load_jsonl(HERE / "data" / "my_replies.jsonl"):
        reply = {k: r.get(k) for k in ("category", "urgency", "next_action", "customer_message")}
        out.append({"run": r.get("id", "MY-?"), "raw": json.dumps(reply), "suggested_label": r.get("human_label", "-")})
    return out


ALL_RUNS = RUNS + my_runs()
