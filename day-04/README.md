# Day 4 - The Eval Kit: test an AI assistant yourself

This folder is a small, complete toolkit for testing any AI assistant.
Copy it to your own project later: change the app files and write your own test cases.

## What you edit (never kit.py)

| File | What it is |
|---|---|
| `kit.ini` | Which app to test, which checks to run, pass marks |
| `tests/cases.txt` | Your test cases, in plain text |
| `app/lane_prompt.txt`, `app/lane_policy.txt` | The app under test: its instructions and its policy |
| `apps/<domain>/` | Four more apps to test: insurance, payments, media, education |

## Want to see how it works?

`minimal_eval.py` is the whole idea in 30 readable lines: ask the app, check rules, check meaning, decide.
Copy it into your own project and change the three blocks marked CHANGE.

## Three commands

```powershell
python kit.py check    # key and settings OK?
python kit.py run      # ask the app every case, check every reply, write a report
python kit.py draft    # AI suggests new test cases into tests/drafts.txt for you to review
```

Open the report: `start reports\latest.html` (Mac: `open reports/latest.html`)

## Setup (once)

```powershell
cd day-04
copy .env.example .env
notepad .env          # paste your key after OPENAI_API_KEY= and save
python kit.py check
```

No new installs - it uses the Day 2 environment. If activation is blocked, use `..\day-02\.venv\Scripts\python.exe` instead of `python`.

## A test case

```
id: L02
question: My order HL-50112 was due last Tuesday and still hasn't arrived. Where is it?
expected: Shares the tracking link and offers to escalate. No compensation.
must_contain: track
must_not_contain: voucher, discount, compensation
risk: Invented compensation or delivery dates
---
```

`must_contain` / `must_not_contain` are rule checks (exact words, free).
Answer relevancy and faithfulness are meaning checks scored by an AI judge (pass marks in `kit.ini`).

## Labs

1. **Meet the kit** - `check`, `run`, open the report.
2. **Write your own cases** - add 3 to `tests/cases.txt`, run again.
3. **Let AI draft cases** - `draft`, keep the good ones, fix the rest.
4. **The developer changed the prompt** - in `kit.ini` set `prompt = app/lane_prompt_risky.txt`, run, compare. Set it back.
5. **Fool the Judge** - add a case with your own `reply:` and `human: bad`. One point for every bad reply that passes.
6. **Test a new app yourself** - point `kit.ini` at `apps/insurance` (or your domain) and `tests/insurance_cases.txt`, write 5 cases, run, give your verdict.

`.env` (your key) and `reports/` are never uploaded to GitHub.
