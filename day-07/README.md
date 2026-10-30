# Day 7 - Golden datasets, and your own complete test project

Hour 1: build a 30-row golden dataset from real-looking chat logs, check its hygiene,
and run it as an automated suite with a release gate.
Hour 2: build the complete test project for YOUR domain app - you will keep using it on Days 8-10.

## Setup

```powershell
cd day-07
copy ..\day-06\.env .env
python kit.py start insurance      # or: lane, payments, media, education
```

Prompt must start with `(.venv)`. If not: `..\day-02\.venv\Scripts\Activate.ps1`

## Commands (all from day-07)

| Command | What it does | Needs key? |
|---|---|---|
| `python kit.py start <app>` | Creates `project/` for your app | no |
| `python kit.py curate` | Raw logs → de-duplicated, personal-data-masked, tagged candidates | no |
| `python kit.py draft` | AI suggests extra synthetic cases | yes |
| `python kit.py lint` | Dataset hygiene: 30 rows, IDs, tags, coverage, no personal data | no |
| `python kit.py run` | Ask the app every case, check everything, write a report | yes |
| `python kit.py run --ci` | Same + quality gate + `reports/junit.xml` + exit code | yes |
| `python kit.py calibrate` | Your rubric vs your own good/bad labels | yes |
| `python kit.py review` | Your scorecard: 7 stages, 7 stars | no |

## Your project folder

| File | Stage |
|---|---|
| `project/risks.md` | 1 - five risks and what "pass" means |
| `project/cases.txt` | 2, 3 - your golden dataset (30 rows) with rules |
| `project/project.ini` | 4, 6 - checks, thresholds, the release gate |
| `project/rubrics/` | 5 - your rubric |
| `project/calibration.txt` | 5 - label 6 replies, then `calibrate` |
| `project/verdict.md` | 7 - RELEASE / CONDITIONAL / BLOCK with evidence |

Tags used in datasets: `policy, personal-data, credentials, tone, out-of-scope, injection, false-premise, fairness, other`

`templates/github-actions-eval.yml` shows how the same `run --ci` works in a GitHub Actions pipeline (Day 8+).
