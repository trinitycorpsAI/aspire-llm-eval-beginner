# Day 1 lab: same request, five runs, four kinds of evidence

You are Kavya, a QE engineer. The product team wants to ship **Lane**, the
customer-support assistant for Harbour & Lane (a fictional UK retailer).
The demo looked great. Your job is to decide what "passed" actually means.

The lab compares five answers to the **same** customer message on four separate things:

1. **Surface variance** - did the wording change?
2. **Format** - is it raw JSON a system can consume?
3. **Hard checks** - deterministic rules from the evidence contract (C1-C9)
4. **Human label** - does the answer mean the right thing? (correct / partial / wrong / unsafe)

Five runs is a teaching demonstration, not a reliability estimate.

## Step 0 - check your machine (PowerShell)

```powershell
cd day-01\lab
python check_setup.py
```

## Path A - cached mode (works for everyone, no install, no key)

```powershell
python lab_day1.py
```

Then label the runs yourself instead of using the suggested labels:

```powershell
python lab_day1.py --label
```

## Path B - token demo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python token_demo.py
```

If `Activate.ps1` is blocked, run once:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Path C - live model (optional)

Local model through Ollama (free, runs on your laptop, ~2 GB download):

```powershell
ollama pull llama3.2:3b
python lab_day1.py --mode ollama --temperature 1.0 --label
python lab_day1.py --mode ollama --temperature 0 --label
```

OpenAI API (only if your team has given you a key):

```powershell
$env:OPENAI_API_KEY="sk-..."
python lab_day1.py --mode openai --model gpt-4.1-mini --temperature 1.0 --label
```

Use **either** `--temperature` **or** `--top-p`, never both. The script refuses both.

## What to bring back to class

- Your summary table and release verdict
- One run where the hard checks and your label **disagreed**, and why

## Tests

```powershell
python -m unittest discover -s tests -v
```

Test `test_regex_misses_redirect_offer` passes on purpose: it documents a blind spot
of deterministic checks. Read it.

Every run writes its evidence to `outputs\` as JSON.
