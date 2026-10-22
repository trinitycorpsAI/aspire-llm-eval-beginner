# Day 2 - From blueprint to code: the eval lifecycle and DeepEval

Yesterday you designed checks C1-C10 by hand. Today they become code.
Every lab today runs **offline**: no API key, no LLM call, no cost.

## Setup (Windows PowerShell, from the repo root)

```powershell
git pull
cd day-02
py -3.12 -m venv .venv          # or: python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python check_setup.py
```

If `Activate.ps1` is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again.
If you see strange characters or a Unicode error in the output: `$env:PYTHONUTF8=1`

## Lab A - C1 to C5 as DeepEval metrics

```powershell
python day2_eval.py               # script style: evaluate()
deepeval test run test_lane.py    # pytest style: how it runs in CI
```

Expected: runs 1, 2, 5 pass; run 3 fails C1; run 4 fails C5. Pass rate 60%.
Run 5 passing is not a bug in the code. It is the lesson.

Open `metrics.py` to read how each check is built. Every metric has the same four steps.

## Lab B - write your own C10

Open `my_c10.py`, fill in the two TODOs, then:

```powershell
python my_c10.py
```

Aim for "yes" in the agrees column. One case (C10-05) cannot be caught by a keyword rule - work out why.
Kavya's version: `python solutions/c10_solution.py`

## Stretch / homework - evaluate AI-written test cases

```powershell
cd stretch\ai_testcase_generator
python check_testcases.py
```

An AI wrote test cases for an insurance user story three times. Seven checks (T1-T7) decide which output you would trust.
Question to bring tomorrow: what would a human still need to check that T1-T7 cannot?

## Files

| File | What it is |
|---|---|
| `metrics.py` | C1-C5 as DeepEval metrics (read this one) |
| `day2_eval.py` | Runs C1-C5 on the five Day 1 replies with `evaluate()` |
| `test_lane.py` | Same checks as pytest tests for `deepeval test run` |
| `my_c10.py` | Your C10 - template with TODOs and hints |
| `data/c10_outputs.jsonl` | Six messages to test your C10 on |
| `solutions/c10_solution.py` | Kavya's C10 |
| `stretch/ai_testcase_generator/` | Evaluate AI-generated test cases for an insurance story |
