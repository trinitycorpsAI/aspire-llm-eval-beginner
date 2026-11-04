# Day 10 - Capstone: build, run and report an eval suite for your agent

Your project from Days 7-9 is your capstone. Today you choose its 5 headline metrics,
run the full suite, report your findings, present your release decision and review a colleague's work.

## Setup

```powershell
cd day-10
copy ..\day-09\.env .env
python kit.py import          # brings your day-09 project (or day-08 / day-07) + capstone files
```

Prompt must start with `(.venv)`. If not: `..\day-02\.venv\Scripts\Activate.ps1`

## Capstone steps

| Step | File / command |
|---|---|
| 1 · Choose 5 headline metrics, linked to your risks | `project/metrics.md` |
| 2 · Make sure each one is switched on with the right pass mark | `project/project.ini` |
| 3 · Run the full suite with the gate | `python kit.py run --ci` |
| 4 · Calibrate your rubric if you changed it | `python kit.py calibrate` |
| 5 · Decide: RELEASE / CONDITIONAL / BLOCK | `project/verdict.md` |
| 6 · Evidence pack | `python kit.py evidence` |
| 7 · Findings report to present from | `python kit.py report` → `project/findings.md` |
| 8 · Check everything | `python kit.py review` (10 stages) |
| 9 · Review a colleague | `project/peer_review.md` |

Other checks from earlier days can stay on as supporting checks; the 5 in `metrics.md` are the ones you report and defend.

Present in 3 minutes: decision (30s) → 5 metrics and why (60s) → top defects with evidence (60s) → gaps and next step (30s).
