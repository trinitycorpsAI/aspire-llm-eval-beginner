# Day 8 - Eval Kit v5: testing RAG (answers from documents)

## Setup

```powershell
cd day-08
copy ..\day-07\.env .env
python kit.py check
```

Prompt must start with `(.venv)`. If not: `..\day-02\.venv\Scripts\Activate.ps1`

## New today

| | |
|---|---|
| `kb/lane_kb.txt` | Lane's knowledge base: one document per `## ID | title` block |
| `[rag]` in `kit.ini` | `enabled`, `kb`, `top_k` (how many documents the app gets per question) |
| `reference:` in a case | The ideal answer, written from the right document |
| `python kit.py ask "..."` | See what was retrieved and what the app answered |
| `python kit.py import` | Bring your Day 7 project here and give it your domain's knowledge base |
| `minimal_rag.py` | Retrieve → generate → evaluate, in 35 readable lines |

## RAG checks (in `[checks]`)

| Check | Question it answers | Needs |
|---|---|---|
| `context_precision` | Were the right documents ranked at the top? | `reference:` |
| `context_recall` | Was everything needed to answer retrieved? | `reference:` |
| `context_relevancy` | How much of what was retrieved is relevant? | - |
| `faithfulness` | Is the reply backed by what was retrieved? | - |
| `rubrics/answer_correctness.txt` | Is the reply actually right, compared with the reference? | `reference:` |

## Your project

```powershell
python kit.py import                 # copies ../day-07/project and adds project/kb.txt
python kit.py ask "a question your users ask"
python kit.py run --ci
python kit.py review                 # now 8 stars
```

No Day 7 project? `python kit.py start <app>`, then `python kit.py import --kb-only`.
