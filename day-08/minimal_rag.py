"""Day 8: evaluating a RAG answer in 35 lines - read this one.

    python minimal_rag.py

RAG = retrieve documents, then answer from them. So there are TWO things to test:
  retrieval  - did we fetch the right documents?   (context precision, context recall)
  generation - did we answer correctly from them?  (faithfulness, answer correctness)
"""
import os
from pathlib import Path

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from openai import OpenAI

import kit                                                   # reuse the kit's simple retriever

for line in Path(__file__).with_name(".env").read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()

question = "Can I return an unused toaster I got 20 days ago? Do I pay the postage?"
reference = ("Yes. Change-of-mind returns are accepted within 30 days for unused items in original packaging, "
             "and we email a prepaid returns label.")                  # the ideal answer, from the RIGHT document

docs = kit.load_kb("kb/lane_kb.txt")
hits = kit.retrieve(question, docs, k=3)                                # 1. RETRIEVE
retrieved = [f"{cid} | {title}: {text}" for cid, title, text, _ in hits]
print("Retrieved:", [cid for cid, *_ in hits])

reply = OpenAI().chat.completions.create(model="gpt-4.1-mini", messages=[      # 2. GENERATE from what was retrieved
    {"role": "system", "content": "Answer only from these extracts:\n" + "\n".join(retrieved)},
    {"role": "user", "content": question}]).choices[0].message.content
print("Reply:", reply, "\n")

case = LLMTestCase(input=question, actual_output=reply,                 # 3. ONE TEST CASE, three inputs that matter
                   retrieval_context=retrieved, expected_output=reference)
for metric in (ContextualPrecisionMetric(threshold=0.7, model="gpt-4.1-mini"),  # right documents ranked first?
               ContextualRecallMetric(threshold=0.7, model="gpt-4.1-mini"),     # everything needed was retrieved?
               FaithfulnessMetric(threshold=0.7, model="gpt-4.1-mini")):        # reply backed by what was retrieved?
    metric.measure(case)
    print(f"{metric.__name__:<22} {metric.score:.2f}  {'PASS' if metric.is_successful() else 'FAIL'}  - {metric.reason[:110]}")
