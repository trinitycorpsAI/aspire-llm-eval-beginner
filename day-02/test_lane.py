"""Day 2 lab A, pytest style - the way DeepEval runs in a CI pipeline.

    deepeval test run test_lane.py
    (or)  python -m pytest -q test_lane.py
"""
import os

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")

import json
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from metrics import day1_contract

DAY1 = Path(__file__).parent.parent / "day-01" / "lab" / "data"
CASE = json.loads((DAY1 / "case.json").read_text(encoding="utf-8"))
ROWS = [json.loads(l) for l in (DAY1 / "cached_outputs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


@pytest.mark.parametrize("row", ROWS, ids=[f"run-{r['run']}" for r in ROWS])
def test_lane_contract(row):
    assert_test(
        LLMTestCase(input=CASE["customer_message"], actual_output=row["raw"]),
        day1_contract(),
    )
