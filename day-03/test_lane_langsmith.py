"""Day 3 Lab D - the Day 2 checks, the LangSmith way.

Offline (no account, no key - this is what we run in class):
    $env:LANGSMITH_TEST_TRACKING="false"
    python -m pytest -q --tb=no -rf test_lane_langsmith.py

With a LangSmith account (optional - results appear as an experiment in the web UI):
    $env:LANGSMITH_API_KEY="lsv2_..."
    $env:LANGSMITH_TEST_TRACKING="true"
    python -m pytest -q --tb=no -rf test_lane_langsmith.py

Only synthetic data. Never send client data to a hosted tool without approval.
"""
import pytest
from langsmith import testing as t

from _shared import ALL_RUNS, CASE
from deepeval.test_case import LLMTestCase
from metrics import day1_contract
from my_c10 import NoCardDetailsRequest  # your Day 2 C10 (day-02/my_c10.py)


@pytest.mark.langsmith
@pytest.mark.parametrize("row", ALL_RUNS, ids=[str(r["run"]) if not isinstance(r["run"], int) else f"run-{r['run']}" for r in ALL_RUNS])
def test_lane_contract(row):
    t.log_inputs({"customer_message": CASE["customer_message"], "run": row["run"]})
    t.log_outputs({"raw_reply": row["raw"]})
    t.log_reference_outputs({"human_label": row["suggested_label"]})

    tc = LLMTestCase(input=CASE["customer_message"], actual_output=row["raw"])
    metrics = day1_contract()
    # YOUR TURN: remove the # on the next line to add the C10 you wrote on Day 2
    # metrics.append(NoCardDetailsRequest())
    failed = []
    for metric in metrics:
        metric.measure(tc)
        t.log_feedback(key=metric.__name__, score=metric.score)  # one feedback score per check
        if not metric.success:
            failed.append(f"{metric.__name__}: {metric.reason}")
    assert not failed, "; ".join(failed)
