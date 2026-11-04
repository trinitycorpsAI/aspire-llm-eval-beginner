# LLM Evaluation - Beginner Track (Aspire Systems)

Delivered by TrinityCorps. Ten 2-hour sessions, one story.

**The story.** Harbour & Lane, a UK home-and-kitchen retailer, is putting an AI
assistant called Lane in front of customers. Kavya, a QE engineer, has to decide
whether it is safe to release. Every day adds one more kind of evidence.

| Day | Topic | Folder |
|---|---|---|
| 1 | GenAI & LLM foundations for QA | `day-01` |
| 2 | The eval lifecycle, setup, DeepEval | `day-02` |
| 3 | Ragas, OpenAI Evals, LangSmith, framework anatomy | `day-03` |
| 4 | Relevancy & faithfulness | `day-04` |
| 5 | Hallucination, toxicity, bias, PII | `day-05` |
| 6 | LLM-as-a-judge, G-Eval | `day-06` |
| 7 | Building eval datasets | `day-07` |
| 8 | Evaluating RAG outputs | `day-08` |
| 9 | Prompt injection, bias, EU AI Act, India AI guidance | coming |
| 10 | Capstone | `day-10` |

## Day 10

- `day-10/` - Capstone: choose 5 metrics (`project/metrics.md`), run the full suite, `python kit.py report` for your findings, present and peer-review. `python kit.py import` brings your Day 9 project. Start with `day-10/README.md`.

## Day 9

- `day-09/` - Eval Kit v6: prompt-injection suite with a canary check, vary: bias sets, poisoned-document test, evidence pack (EU AI Act / India guidance areas). `python kit.py import` brings your Day 8 project. Start with `day-09/README.md`.

## Day 8

- `day-08/` - Eval Kit v5: knowledge bases, retrieval, context precision/recall, answer correctness. `python kit.py import` brings your Day 7 project. Start with `day-08/README.md`.

## Day 7

- `day-07/` - Eval Kit v4: golden datasets from logs, hygiene lint, CI gate with JUnit, and your own complete test project (`python kit.py start <app>`). Start with `day-07/README.md`.

## Day 6

- `day-06/` - Eval Kit v3: your own rubrics (G-Eval), calibration against human labels. Start with `day-06/README.md`. Copy your key: `copy ..\day-05\.env .env`.

## Day 5

- `day-05/` - Eval Kit v2: hallucination, toxicity, bias pairs, personal-data checks. Start with `day-05/README.md`. Copy your key: `copy ..\day-04\.env .env`.

## Day 4

- `day-04/` - the Eval Kit: test an AI assistant yourself (relevancy, faithfulness, your own cases). Start with `day-04/README.md`. Needs an API key in `day-04/.env`.

## Day 3

- `day-03/` - Ragas and LangSmith on the same Lane replies. Start with `day-03/README.md`.

## Day 2

- Session page: shared in the chat
- `day-02/` - C1-C5 and your own C10 as DeepEval metrics. Start with `day-02/README.md`.

## Day 1

- `day-01/Day1_Session.html` - open in any browser (download it first; GitHub shows HTML as code)
- `day-01/lab/` - five-run variance lab. Start with `lab/README.md`.

All data is synthetic. No real customer information is used anywhere.
