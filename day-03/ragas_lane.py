"""Day 3 Lab C - the same five Lane replies, judged the Ragas way.

    python ragas_lane.py

Ragas compares each reply with a reference answer. We use only metrics that
need NO LLM, so this runs offline with no API key:
  - NonLLMStringSimilarity : how close the wording is to the reference (0 to 1)
  - StringPresence         : does the reply contain a required phrase (0 or 1)
Then we put the Ragas score next to yesterday's DeepEval verdict and Day 1's human label.
"""
import warnings

warnings.filterwarnings("ignore")

from _shared import ALL_RUNS as RUNS, CASE, GOLDEN, message_of  # noqa: E402

from deepeval.test_case import LLMTestCase  # noqa: E402
from ragas import EvaluationDataset, evaluate  # noqa: E402
from ragas.dataset_schema import SingleTurnSample  # noqa: E402
from ragas.metrics import NonLLMStringSimilarity, StringPresence  # noqa: E402

from metrics import day1_contract  # noqa: E402  (Day 2's C1-C5)

THRESHOLD = 0.40  # "similar enough" - try 0.30 and 0.50 and watch the verdicts change

# 1. DATASET - Ragas calls each row a SingleTurnSample
similarity_rows = [
    SingleTurnSample(user_input=CASE["customer_message"], response=message_of(r["raw"]), reference=GOLDEN["reference_message"])
    for r in RUNS
]
presence_rows = [
    SingleTurnSample(user_input=CASE["customer_message"], response=message_of(r["raw"]), reference="original payment method")
    for r in RUNS
]

# 2-3. RUN + SCORE - evaluate() applies each metric to each sample
sim = evaluate(EvaluationDataset(samples=similarity_rows), metrics=[NonLLMStringSimilarity()], show_progress=False).to_pandas()
pres = evaluate(EvaluationDataset(samples=presence_rows), metrics=[StringPresence()], show_progress=False).to_pandas()

# 4. ANALYSE - Ragas next to DeepEval next to the human
print(f"\nReference answer: {GOLDEN['reference_message']}\n")
print(f"RUN    similarity  >= {THRESHOLD:.2f}?  phrase  | DeepEval C1-C5 | human label")
for i, r in enumerate(RUNS):
    s = float(sim["non_llm_string_similarity"][i])
    p = int(pres["string_present"][i])
    tc = LLMTestCase(input=CASE["customer_message"], actual_output=r["raw"])
    de_pass = all(m.measure(tc) >= m.threshold for m in day1_contract())
    name = f"run-{r['run']}" if isinstance(r["run"], int) else str(r["run"])
    print(f"{name:<6} {s:>9.2f}   {'PASS' if s >= THRESHOLD else 'fail':>8}    {p:>3}    | {'PASS' if de_pass else 'FAIL':>14} | {r['suggested_label']}")

print("""
What to notice
- Run 3 scores the HIGHEST similarity. Ragas never saw the markdown fences - we handed it only the message.
- Run 2 is correct but worded differently, so it scores lower than run 3.
- Run 5 is UNSAFE and still clears the threshold. Similar words, dangerous meaning.
- Change THRESHOLD to 0.45 and rerun: now run 5 fails. Problem solved? Run 2 - a correct answer - is only 0.12 above
  run 5. Tomorrow's correct answer, worded differently again, could score 0.38. Tuning a threshold on five samples is guessing.
Similarity measures wording. Your evidence contract measures meaning and policy. They are different tests.""")
