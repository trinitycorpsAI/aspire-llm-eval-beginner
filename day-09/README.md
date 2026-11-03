# Day 9 - Eval Kit v6: basic AI risk testing

Prompt injection, bias smoke tests at scale, and an evidence pack for compliance conversations.

## Setup

```powershell
cd day-09
copy ..\day-08\.env .env
python kit.py check
```

Prompt must start with `(.venv)`. If not: `..\day-02\.venv\Scripts\Activate.ps1`

## New today

| | |
|---|---|
| `canary = ...` in `[app]` | A secret code planted in the hidden instructions. Any reply containing it fails automatically: the instructions leaked |
| `vary: A \| B \| C` in a case | Use `{person}` in the question; the kit expands one case into a bias set (same question, different people) |
| `tag: transparency` | Tests that the assistant says it's an AI (EU AI Act Art. 50) |
| `kb/lane_kb_poisoned.txt` | A knowledge base with a hidden instruction planted in one document (indirect injection) |
| `app/lane_prompt_hardened.txt` | A prompt with security rules, to compare against |
| `python kit.py attack` | Generates 10 prompt-injection cases for your app, to review |
| `python kit.py evidence` | Evidence pack: coverage by risk tag, mapped to EU AI Act areas and India's AI governance sutras |
| `minimal_injection.py` | Canary + rule checks against three attacks, in 30 readable lines |

The gate now blocks on `injection`: one successful attack fails the release.

## Your project

```powershell
python kit.py import      # copies ../day-08/project (or day-07), adds a canary and blocks injection in the gate
python kit.py attack      # review project/attacks.txt, copy 8+ into project/cases.txt
python kit.py run --ci
python kit.py evidence    # writes project/evidence.md
python kit.py review      # stage 9
```

The evidence pack supports compliance work. It is not legal advice.
