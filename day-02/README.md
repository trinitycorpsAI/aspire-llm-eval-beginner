# Day 2 - From blueprint to code: the eval lifecycle and DeepEval

Yesterday you designed checks C1-C10 by hand. Today they become code.
Every lab runs **offline**: no API key, no LLM call, no cost.

## Setup

**Windows (PowerShell)** - from the folder where you cloned the repo:

```powershell
git pull
cd day-02
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python check_setup.py
```

**Ubuntu / Mac:**

```bash
git pull
cd day-02
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python check_setup.py
```

## Lab A - C1 to C5 as DeepEval metrics

```powershell
python day2_eval.py                          # script style: evaluate()
python -m pytest -q --tb=no -rf test_lane.py # CI style: one test per run
```

Expected: runs 1, 2, 5 pass; run 3 fails C1; run 4 fails C5 (`2 failed, 3 passed`).
Run 5 passing is not a bug. It is the lesson.

## Lab B - write your own C10, then add your own cases

1. Open `my_c10.py`, fill in the two TODOs in `rule()`, save, run `python my_c10.py`.
2. Open `data/c10_outputs.jsonl`. Copy the line starting `# {"id": "MY-01"`, remove the `#`,
   write your own Lane reply and say whether it should `pass` or `fail`. Add at least two.
3. Run `python my_c10.py` again. Does your rule agree with your own cases?

C10-05 cannot be caught by a keyword rule - work out why. Kavya's version: `python solutions/c10_solution.py`

## Stretch - evaluate AI-written test cases, then write T8

```powershell
cd stretch\ai_testcase_generator
python check_testcases.py
```

Open `check_testcases.py`, find `YOUR TURN - T8`, fill in the two TODOs, rerun. Runs B and C should now fail T8.
Kavya's version: `python solution_t8.py`

## Troubleshooting (everything we hit in class)

| Problem | Fix |
|---|---|
| PowerShell opens in `C:\WINDOWS\system32` | Go to your repo first: `cd ~` then type `cd asp` and press **Tab** |
| `fatal: not a git repository` | You are one folder too high. `cd` into `aspire-llm-eval-beginner` |
| `git` is not recognised | Download the repo instead: GitHub > **Code** > **Download ZIP** > Extract All |
| Installed git or Python but still "not recognised" | Close the terminal and open a new one |
| `Python was not found` when typing `python3` | On Windows the command is `python`, not `python3` |
| `py -3.12`: No suitable Python runtime | Use `python -m venv .venv` with the Python you have |
| `Activate.ps1 cannot be loaded` | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again |
| Still blocked (company policy) | Skip activation. Use `.\.venv\Scripts\python.exe` instead of `python` everywhere |
| Prompt has no `PS` (Command Prompt) | Activate with `.venv\Scripts\activate.bat` |
| `deepeval.exe` blocked by Application Control | Use `python -m pytest ...` (above) instead of `deepeval test run` |
| `deepeval test run` crashes in `cache_test_case` | Repo is in OneDrive or the cache file is locked. Use pytest; move the repo to `C:\aspire-llm-eval-beginner` |
| Strange characters / UnicodeEncodeError | `$env:PYTHONUTF8=1` then run again |
| Long red pytest output | Add `--tb=no -rf` for a short summary |

## Files

| File | What it is |
|---|---|
| `metrics.py` | C1-C5 as DeepEval metrics (read this one) |
| `day2_eval.py` | Runs C1-C5 on the five Day 1 replies with `evaluate()` |
| `test_lane.py` | Same checks as pytest tests |
| `my_c10.py` | Your C10 - template with TODOs and hints |
| `data/c10_outputs.jsonl` | Six messages to test your C10 on |
| `solutions/c10_solution.py` | Kavya's C10 |
| `stretch/ai_testcase_generator/` | Evaluate AI-generated test cases for an insurance story |
