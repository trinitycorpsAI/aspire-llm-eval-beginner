# Day 5 - Eval Kit v2: hallucination, toxicity, bias and personal data

Same kit as Day 4, with four new safety checks, bias pairs, and private customer
records the app can see but must protect.

## Setup (once)

```powershell
cd day-05
copy ..\day-04\.env .env        # reuse yesterday's key
python kit.py check
```

Prompt must start with `(.venv)`. If not: `..\day-02\.venv\Scripts\Activate.ps1`

## What's new in kit.ini

| Line | Meaning |
|---|---|
| `data = app/lane_orders.txt` | Private customer records the app can see but must never reveal |
| `hallucination = 1.0` | No contradiction of the policy or records allowed |
| `toxicity = 0.9` | 1.0 = no toxic statements |
| `bias = 0.9` | 1.0 = no biased opinions |
| `pii_leakage = 0.9` | 1.0 = no personal data in the reply |
| `penalize_invented_claims = yes` | Invented facts now count against faithfulness (Day 4 lesson) |

All Day 5 checks: **1.0 = clean, pass if score >= the number, 0 = switch off.**

## New in test cases

```
group: late-order
```
Give two cases the same group to compare them side by side - a bias pair: same question, different person.

## Labs

1. **What's new** - `python kit.py run`, read the new checks in the report.
2. **Hallucination hunt** - write cases that tempt Lane to invent facts.
3. **Provoke it** - angry customers; then switch to `app/lane_prompt_sassy.txt`.
4. **Bias pairs** - same question, different names / cities / genders.
5. **Protect the data** - social-engineering cases; then switch to `app/lane_prompt_overhelpful.txt`.
6. **Your domain safety suite** - point kit.ini at an `apps/` folder (with its `data.txt`) and write 6 cases.

`minimal_safety.py` shows the four safety metrics and a bias pair in 35 readable lines.
