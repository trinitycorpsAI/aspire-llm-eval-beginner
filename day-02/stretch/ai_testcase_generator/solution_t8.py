"""Stretch / homework - evaluate AI-generated test cases with DeepEval.

This is the same idea as Lane, pointed at your own daily work: when Claude,
Copilot, Devin or Kiro writes test cases for you, how do you know they are good?

    python check_testcases.py

Three AI outputs for insurance user story CLM-214 are in ai_outputs.jsonl.
Seven deterministic checks (T1-T7) run on each. Then read the human notes.
"""
import os
import sys

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
from pathlib import Path

from deepeval.test_case import LLMTestCase

from metrics import LaneMetric

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).parent
STORY = json.loads((HERE / "user_story.json").read_text(encoding="utf-8"))
VALID_ACS = set(STORY["acceptance_criteria"])
KEYS = {"id", "title", "covers", "type", "steps", "expected"}
VAGUE = ("should work", "works fine", "as expected", "works properly", "no issues")


def cases(tc):
    try:
        data = json.loads(tc.actual_output)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        import re
        try:
            return json.loads(re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", tc.actual_output.strip()))
        except json.JSONDecodeError:
            return []


class T(LaneMetric):
    def __init__(self, check_id, title, fn):
        super().__init__()
        self.check_id, self.title, self.fn = check_id, title, fn

    def rule(self, tc):
        return self.fn(tc)


def t1(tc):
    try:
        ok = isinstance(json.loads(tc.actual_output), list)
        return ok, "raw JSON array" if ok else "JSON but not an array"
    except json.JSONDecodeError:
        return False, "not raw JSON (fenced or prose)"

def t2(tc):
    bad = [c.get("id", "?") for c in cases(tc) if set(c) != KEYS]
    return not bad, "all cases have the 6 keys" if not bad else f"wrong keys in {bad}"

def t3(tc):
    ids = [c.get("id") for c in cases(tc)]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    return not dup, "IDs unique" if not dup else f"duplicate IDs {dup}"

def t4(tc):
    covered = {a for c in cases(tc) for a in c.get("covers", [])}
    missing = sorted(VALID_ACS - covered)
    return not missing, "every AC covered" if not missing else f"no test for {missing}"

def t5(tc):
    invented = sorted({a for c in cases(tc) for a in c.get("covers", [])} - VALID_ACS)
    return not invented, "only real ACs" if not invented else f"tests invented requirement {invented}"

def t6(tc):
    vague = [c["id"] for c in cases(tc) if any(v in c.get("expected", "").lower() for v in VAGUE)]
    return not vague, "expected results are specific" if not vague else f"vague expected result in {vague}"

def t7(tc):
    kinds = {c.get("type") for c in cases(tc)}
    ok = {"negative", "boundary"} <= kinds
    return ok, "has negative and boundary tests" if ok else f"types present: {sorted(kinds)}"


# ---------------------------------------------------------------------------
# YOUR TURN - T8
# Run C's TC-01 "covers" AC-2 but only tries a VALID date. T4 trusted the label.
# Rule: every acceptance criterion needs at least one negative OR boundary test.
# Fill in the two TODO lines, save, rerun. (this file IS Kavya's version)
# ---------------------------------------------------------------------------
def t8(tc):
    tested_hard = set()
    for c in cases(tc):
        if c.get("type") in ("negative", "boundary"):
            tested_hard.update(c.get("covers", []))
    missing = sorted(VALID_ACS - tested_hard)
    return not missing, "every AC has a negative/boundary test" if not missing else f"only happy-path tests for {missing}"


METRICS = [T("T1", "Raw JSON array", t1), T("T2", "6 keys per case", t2), T("T3", "Unique IDs", t3),
           T("T4", "Every AC covered", t4), T("T5", "No invented requirements", t5),
           T("T6", "Specific expected results", t6), T("T7", "Negative + boundary tests", t7),
           T("T8", "Every AC tested the hard way", t8)]

if __name__ == "__main__":
    print(f"Story {STORY['story_id']}: {STORY['story']}\n")
    for row in (json.loads(l) for l in (HERE / "ai_outputs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()):
        tc = LLMTestCase(input=STORY["prompt_given_to_ai"], actual_output=row["raw"])
        print(row["tool"])
        for m in METRICS:
            m.measure(tc)
            print(f"  {m.check_id} {'ok' if m.success else 'X '} {m.title:<28} {m.reason}")
        print(f"  Human note: {row['human_note']}\n")
    print("Your homework: what would a human still need to check that T1-T7 cannot?")
