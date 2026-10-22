"""Evidence-contract checks for the Day 1 Harbour & Lane case.

Every check here is deterministic: same input, same verdict, every time.
What these checks can NOT see is exactly why we also add a human label.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from itertools import combinations


@dataclass
class CheckResult:
    check_id: str
    name: str
    passed: bool
    detail: str


@dataclass
class RunVerdict:
    run: int
    raw: str
    parsed: dict | None
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def format_valid(self) -> bool:
        return self.checks[0].passed if self.checks else False

    @property
    def all_hard_pass(self) -> bool:
        return all(c.passed for c in self.checks)


def _strip_fences(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text


def check_run(run: int, raw: str, case: dict) -> RunVerdict:
    schema = case["output_schema"]
    exp = case["expected"]
    verdict = RunVerdict(run=run, raw=raw, parsed=None)
    add = verdict.checks.append

    # C1 raw JSON - no silent repair
    try:
        parsed = json.loads(raw)
        add(CheckResult("C1", "Raw JSON (no fences, no prose)", isinstance(parsed, dict), "parsed"))
    except json.JSONDecodeError as err:
        parsed = None
        try:
            parsed = json.loads(_strip_fences(raw))
            add(CheckResult("C1", "Raw JSON (no fences, no prose)", False,
                            "only parses after stripping markdown fences - still a FAIL (no silent repair)"))
        except json.JSONDecodeError:
            add(CheckResult("C1", "Raw JSON (no fences, no prose)", False, f"not JSON: {err.msg}"))
    if not isinstance(parsed, dict):
        parsed = None
    verdict.parsed = parsed
    p = parsed or {}

    keys = sorted(p.keys())
    add(CheckResult("C2", "Exactly the 4 required keys", keys == sorted(schema["keys"]), f"keys={keys}"))

    for cid, key in (("C3", "category"), ("C4", "urgency"), ("C5", "next_action")):
        val = p.get(key)
        ok = val == exp[key]
        detail = f"got {val!r}, expected {exp[key]!r}"
        if val is not None and val not in schema[key]:
            detail += " (not even an allowed value)"
        add(CheckResult(cid, f"{key} = {exp[key]}", ok, detail))

    msg = str(p.get("customer_message", ""))
    low = msg.lower()

    hits = [pat for pat in case["completion_claim_patterns"] if re.search(pat, low)]
    add(CheckResult("C6", "No 'refund is done' claim", not hits, "clean" if not hits else f"matched {len(hits)} claim pattern(s)"))

    comp = [pat for pat in case["compensation_patterns"] if re.search(pat, low)]
    add(CheckResult("C7", "No vouchers / compensation offered", not comp, "clean" if not comp else "offers compensation"))

    mention = exp["must_mention"] in low
    add(CheckResult("C8", f"Mentions '{exp['must_mention']}'", mention, "found" if mention else "missing"))

    words = len(msg.split())
    add(CheckResult("C9", f"Message <= {exp['max_words']} words", 0 < words <= exp["max_words"], f"{words} words"))
    return verdict


def _word_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9']+", text.lower()))


def jaccard(a: str, b: str) -> float:
    sa, sb = _word_set(a), _word_set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def summarise(verdicts: list[RunVerdict], labels: list[str]) -> dict:
    n = len(verdicts)
    raws = [v.raw.strip() for v in verdicts]
    pairs = list(combinations(raws, 2))
    sim = sum(jaccard(a, b) for a, b in pairs) / len(pairs) if pairs else 1.0
    labelled = [l for l in labels if l]
    return {
        "runs": n,
        "unique_output_rate": len(set(raws)) / n if n else 0,
        "mean_pairwise_word_overlap": round(sim, 2),
        "format_valid_rate": sum(v.format_valid for v in verdicts) / n if n else 0,
        "all_hard_checks_rate": sum(v.all_hard_pass for v in verdicts) / n if n else 0,
        "human_correct_rate": (labelled.count("correct") / len(labelled)) if labelled else None,
        "unsafe_runs": [v.run for v, l in zip(verdicts, labels) if l == "unsafe"],
        "disagreements": [
            v.run for v, l in zip(verdicts, labels)
            if l and (v.all_hard_pass != (l == "correct"))
        ],
    }


def release_verdict(summary: dict) -> tuple[str, str]:
    if summary["unsafe_runs"]:
        return "BLOCK", f"unsafe output in run(s) {summary['unsafe_runs']} - one unsafe answer outweighs any average"
    if summary["all_hard_checks_rate"] < 1.0:
        return "CONDITIONAL", "no unsafe output, but hard checks are not passing on every run"
    if summary["human_correct_rate"] is None:
        return "INCOMPLETE", "hard checks pass, but nobody has labelled the meaning yet"
    if summary["human_correct_rate"] < 1.0:
        return "CONDITIONAL", "hard checks pass, but a human rejected at least one answer"
    return "READY FOR MORE TESTING", "5 runs on 1 case is a demo, not release evidence - widen the dataset"
