"""The whole Eval Kit idea in 30 lines - read this one, it is meant to be read.

    python minimal_eval.py

Copy it into your own project, change the three blocks marked CHANGE, done.
"""
import os
from pathlib import Path

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")   # no usage data sent to DeepEval
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from openai import OpenAI

for line in Path(__file__).with_name(".env").read_text().splitlines():      # load the key from .env
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()

# CHANGE 1 - the app under test: its instructions and the policy it must follow
PROMPT = Path("app/lane_prompt.txt").read_text()
POLICY = Path("app/lane_policy.txt").read_text().splitlines()

# CHANGE 2 - your test cases: a question and the words a correct reply must never contain
CASES = [
    ("My order is late. Where is it?", ["voucher", "discount"]),
    ("Do you price match Argos?", ["we price match"]),
]

def ask_app(question):                                   # 1. send the question to the app
    r = OpenAI().chat.completions.create(model="gpt-4.1-mini", messages=[
        {"role": "system", "content": PROMPT + "\nPOLICY:\n" + "\n".join(POLICY)},
        {"role": "user", "content": question}])
    return r.choices[0].message.content

for question, banned in CASES:
    reply = ask_app(question)
    rule_ok = not any(w in reply.lower() for w in banned)                       # 2. rule check
    case = LLMTestCase(input=question, actual_output=reply, retrieval_context=POLICY)
    rel = AnswerRelevancyMetric(threshold=0.7, model="gpt-4.1-mini")           # 3. meaning checks
    fai = FaithfulnessMetric(threshold=0.7, model="gpt-4.1-mini")              # CHANGE 3 - thresholds
    rel.measure(case); fai.measure(case)
    ok = rule_ok and rel.is_successful() and fai.is_successful()               # 4. verdict
    print(f"{'PASS' if ok else 'FAIL'}  {question}\n  reply: {reply}\n"
          f"  rules {'ok' if rule_ok else 'BROKEN'} | relevancy {rel.score:.2f} | faithfulness {fai.score:.2f}\n"
          f"  why: {fai.reason}\n")
