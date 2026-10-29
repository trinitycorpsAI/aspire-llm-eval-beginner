"""Day 6: your own marking scheme with G-Eval, in 30 lines - read this one.

    python minimal_geval.py

A G-Eval metric = a name + evaluation steps (your rubric) + which fields the judge reads.
"""
import os
from pathlib import Path

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

for line in Path(__file__).with_name(".env").read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()

empathy = GEval(
    name="Empathy and tone",
    evaluation_steps=[                                                    # the rubric: observable checks
        "Check whether the reply acknowledges the customer's situation or feeling in its first sentence.",
        "Check that the reply never blames the customer, mocks them, or tells them to calm down.",
        "Check that the tone stays polite and warm even if the customer is rude.",
        "Check that the reply ends with a clear next step for the customer.",
    ],
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],   # what the judge reads
    threshold=0.6, model="gpt-4.1-mini")

question = "This is the third broken item! Are you useless?"
for reply in ["I completely understand - three damaged items is not acceptable, and I'm sorry. "
              "Please upload a photo and I'll make sure it's reviewed quickly.",
              "Please calm down. We ship thousands of items and some get damaged. Upload a photo."]:
    empathy.measure(LLMTestCase(input=question, actual_output=reply))
    print(f"{'PASS' if empathy.is_successful() else 'FAIL'}  {empathy.score:.2f}  {reply[:60]}...\n   why: {empathy.reason}\n")
