"""Run first:  python check_setup.py   - tells you what works on this machine."""
import importlib
import os
import sys

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
ok = True
v = sys.version_info
print(f"Python {v.major}.{v.minor}.{v.micro}", "OK" if (3, 10) <= v[:2] <= (3, 13) else "- use Python 3.11 or 3.12")
ok &= (3, 10) <= v[:2] <= (3, 13)
inside_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
print("Virtual environment:", "active" if inside_venv else "NOT active - run .\\.venv\\Scripts\\Activate.ps1")
for pkg in ("deepeval", "pytest"):
    try:
        m = importlib.import_module(pkg)
        print(f"{pkg} {getattr(m, '__version__', '')} installed")
    except ImportError:
        ok = False
        print(f"{pkg} MISSING - run: pip install -r requirements.txt")
here = os.path.dirname(os.path.abspath(__file__))
day1 = os.path.join(here, "..", "day-01", "lab", "data", "cached_outputs.jsonl")
print("Day 1 data:", "found" if os.path.exists(day1) else "MISSING - run this from inside the repo's day-02 folder")
ok &= os.path.exists(day1)
print("API key:", "OPENAI_API_KEY set" if os.environ.get("OPENAI_API_KEY") else "none - not needed today, every Day 2 lab is offline")
print("\nREADY - run: python day2_eval.py" if ok else "\nFix the lines above, then run this again.")
