"""Day 3 setup check:  python check_setup.py"""
import importlib
import os
import sys

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
ok = True
v = sys.version_info
if (3, 10) <= v[:2] <= (3, 13):
    print(f"Python {v.major}.{v.minor}.{v.micro} OK")
elif v[:2] >= (3, 14):
    print(f"Python {v.major}.{v.minor}.{v.micro} - newer than we tested; fine if the labs run")
else:
    ok = False
    print(f"Python {v.major}.{v.minor}.{v.micro} - too old, install 3.11 or 3.12")
inside = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
print("Virtual environment:", "active" if inside else "not active (fine if you run .venv\\Scripts\\python.exe directly)")
for pkg in ("deepeval", "ragas", "langsmith", "pytest", "rapidfuzz"):
    try:
        m = importlib.import_module(pkg)
        print(f"{pkg} {getattr(m, '__version__', '')} installed")
    except Exception as err:  # ragas raises non-ImportError when langchain versions clash
        ok = False
        print(f"{pkg} PROBLEM ({type(err).__name__}) - run: pip install -r requirements.txt")
here = os.path.dirname(os.path.abspath(__file__))
for need in (("day-01", "lab", "data", "cached_outputs.jsonl"), ("day-02", "metrics.py")):
    found = os.path.exists(os.path.join(here, "..", *need))
    ok &= found
    print("/".join(need), "found" if found else "MISSING - git pull, or run from the repo's day-03 folder")
print("\nREADY - run: python ragas_lane.py" if ok else "\nFix the lines above, then run this again.")
