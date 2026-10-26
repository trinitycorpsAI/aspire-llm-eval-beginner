# Day 3 - Four tools, one method: DeepEval, Ragas, OpenAI Evals, LangSmith

Every evaluation tool has the same four parts: **test case, metric, dataset, runner**.
Today you run the same Lane replies through three of them and compare what each one sees.
All labs run offline. No API key needed.

## Setup - reuse yesterday's virtual environment

**If your venv activates normally (Windows):**

```powershell
cd aspire-llm-eval-beginner
git pull
.\day-02\.venv\Scripts\Activate.ps1
cd day-03
pip install -r requirements.txt
python check_setup.py
```

**If activation is blocked on your laptop:**

```powershell
cd aspire-llm-eval-beginner\day-03
..\day-02\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\day-02\.venv\Scripts\python.exe check_setup.py
```
(then use `..\day-02\.venv\Scripts\python.exe` wherever this page says `python`)

**Ubuntu / Mac:** `source ../day-02/.venv/bin/activate`, then the same `pip install` and `python check_setup.py`.

The install takes 2-4 minutes (Ragas brings LangChain with it). Versions are pinned so everyone gets the same results.

## Lab C - Ragas: similarity is not correctness

```powershell
python ragas_lane.py
```

Ragas compares each reply with a reference answer. Look at runs 3 and 5. Then change `THRESHOLD` at the top of the file to 0.45 and rerun.

**Your cases:** open `data/my_replies.jsonl`, copy the example line, remove the `#`, and write your own replies.
Challenge: an UNSAFE reply that scores above 0.60. Rerun `python ragas_lane.py` - your replies appear as MY-01, MY-02...

## Lab D - LangSmith: same checks, different home

```powershell
$env:LANGSMITH_TEST_TRACKING="false"
python -m pytest -q --tb=no -rf test_lane_langsmith.py
```

Same verdicts as Day 2 (`2 failed, 3 passed`), plus one test for each of your own replies.

**Your turn:** in `test_lane_langsmith.py`, remove the `#` in front of `metrics.append(NoCardDetailsRequest())`.
Your Day 2 C10 now runs inside LangSmith too. Rerun and see which of your replies it catches.

With a LangSmith account and key, set
`LANGSMITH_TEST_TRACKING="true"` and the run appears as an experiment in the LangSmith web app.
Synthetic data only - never send client data to a hosted tool without approval.

## Reference - OpenAI Evals

`openai_evals_mapping.json` shows how C3, C4, C5, C8 and the human label would be written as OpenAI Evals graders.
Reference only: OpenAI is shutting the Evals platform down (read-only from 31 Oct 2026, closed 30 Nov 2026).
The checks themselves move to any other tool unchanged.

## Files

| File | What it is |
|---|---|
| `ragas_lane.py` | Lab C - Ragas non-LLM metrics vs DeepEval vs human label |
| `test_lane_langsmith.py` | Lab D - Day 2 checks as LangSmith-tracked pytest tests |
| `openai_evals_mapping.json` | How the same checks look as OpenAI Evals graders (reference) |
| `data/golden.json` | Kavya's reference answer used by Ragas |
| `data/my_replies.jsonl` | Your own replies - used by Lab C and Lab D |
| `_shared.py` | Loads Day 1 data and Day 2 metrics for both labs |
