# Day 6 - Eval Kit v3: LLM-as-a-judge with your own rubrics (G-Eval)

## Setup

```powershell
cd day-06
copy ..\day-05\.env .env
python kit.py check
```

Prompt must start with `(.venv)`. If not: `..\day-02\.venv\Scripts\Activate.ps1`

## New today

| File | What it is |
|---|---|
| `rubrics/empathy.txt` | A marking scheme for tone, as steps the judge follows |
| `rubrics/follows_expected.txt` | Turns the `expected:` line of each case into a check |
| `rubrics/template.txt` | Copy this to write your own rubric |
| `tests/calibration.txt` | 12 replies already labelled good/bad by the product owner |
| `calibrate.ini` | Settings to test the judge against those labels |
| `minimal_geval.py` | G-Eval in 30 readable lines |

## A rubric

```
name: Empathy and tone
threshold: 0.6
uses: question, reply
steps:
- Check whether the reply acknowledges the customer's situation or feeling in its first sentence.
- Check that the reply never blames the customer, mocks them, or tells them to calm down.
```

`uses` can be any of: `question`, `reply`, `expected`, `policy`.

## Commands

```powershell
python kit.py run                  # test Lane with your rubrics (kit.ini)
python kit.py run calibrate.ini    # judge the judge: agreement with the product owner
```

In `calibrate.ini`, set `repeats = 3` to see how much the judge's score moves between runs.
