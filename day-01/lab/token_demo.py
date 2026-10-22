"""Day 1 token demo - what the model actually 'reads'.

Needs: pip install tiktoken   (first run downloads the o200k_base file once)
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import tiktoken
except ImportError:
    sys.exit("tiktoken is not installed. Run:  pip install tiktoken")

SAMPLES = [
    "refund",
    "Refund",
    "REFUND",
    "Refund my order",
    "Refund 🙏",
    "HL-48213",
    "मेरा रिफंड कहाँ है",
    "பணத்தை திருப்பி தாருங்கள்",
]

enc = tiktoken.get_encoding("o200k_base")
print(f"{'text':<28} {'chars':>5} {'words':>5} {'tokens':>6}  pieces")
for text in SAMPLES:
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    print(f"{text:<28} {len(text):>5} {len(text.split()):>5} {len(ids):>6}  {pieces}")

print("\nTry your own (blank line to exit):")
while True:
    t = input("> ")
    if not t:
        break
    ids = enc.encode(t)
    print(f"  {len(t)} chars, {len(ids)} tokens: {[enc.decode([i]) for i in ids]}")
