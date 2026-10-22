"""Run this first. It tells you which lab paths will work on your machine."""
import json
import os
import sys
import urllib.request

print(f"Python {sys.version.split()[0]}", "OK" if sys.version_info >= (3, 10) else "- please use 3.10 or newer")
try:
    import tiktoken  # noqa: F401
    print("tiktoken installed - token_demo.py will work")
except ImportError:
    print("tiktoken missing - run: pip install tiktoken  (only needed for token_demo.py)")
try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
        models = [m["name"] for m in json.loads(r.read())["models"]]
    print("Ollama running. Models:", models or "none - run: ollama pull llama3.2:3b")
except Exception:
    print("Ollama not running - fine for today; cached mode needs nothing")
print("OPENAI_API_KEY", "set" if os.environ.get("OPENAI_API_KEY") else "not set (not needed today)")
print("\nCached mode always works:  python lab_day1.py")
