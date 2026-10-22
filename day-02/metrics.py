"""Day 2 - the Day 1 evidence contract, rewritten as DeepEval metrics.

Every metric here is deterministic: no LLM, no API key, no internet.
Each one follows the same four-step shape:
    1. read the reply from the test case (test_case.actual_output)
    2. check one rule
    3. set self.score (1.0 pass / 0.0 fail) and self.reason (why)
    4. set self.success = score >= threshold
"""
from __future__ import annotations

import json
import re

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


def parse_reply(text: str) -> dict | None:
    """Strict parse: raw JSON object only. No fence stripping, no repair."""
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
    return data if isinstance(data, dict) else None


def lenient_parse(text: str) -> dict:
    """Used only so later checks can still look inside fenced JSON.
    C1 still fails fenced JSON - this does not hide that."""
    data = parse_reply(text)
    if data is not None:
        return data
    stripped = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", (text or "").strip())
    return parse_reply(stripped) or {}


class LaneMetric(BaseMetric):
    """Shared plumbing so each check only writes its own rule."""

    check_id = "C?"
    title = "unnamed check"

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.include_reason = True
        self.async_mode = False
        self.strict_mode = True

    def rule(self, test_case: LLMTestCase) -> tuple[bool, str]:
        raise NotImplementedError

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        passed, why = self.rule(test_case)
        self.score = 1.0 if passed else 0.0
        self.reason = why
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(getattr(self, "success", False))

    @property
    def __name__(self) -> str:
        return f"{self.check_id} {self.title}"


class RawJson(LaneMetric):
    check_id, title = "C1", "Raw JSON"

    def rule(self, tc):
        if parse_reply(tc.actual_output) is not None:
            return True, "reply is a raw JSON object"
        if lenient_parse(tc.actual_output):
            return False, "only parses after removing markdown fences - no silent repair"
        return False, "reply is not JSON"


class ExactKeys(LaneMetric):
    check_id, title = "C2", "Exactly 4 keys"
    REQUIRED = {"category", "urgency", "next_action", "customer_message"}

    def rule(self, tc):
        keys = set(lenient_parse(tc.actual_output))
        missing, extra = self.REQUIRED - keys, keys - self.REQUIRED
        if not missing and not extra:
            return True, "all four keys, nothing extra"
        return False, f"missing={sorted(missing)} extra={sorted(extra)}"


class FieldEquals(LaneMetric):
    """C3, C4, C5: one field must equal the expected value."""

    def __init__(self, check_id: str, field: str, expected: str, threshold: float = 1.0):
        super().__init__(threshold)
        self.check_id, self.field, self.expected = check_id, field, expected
        self.title = f"{field} = {expected}"

    def rule(self, tc):
        got = lenient_parse(tc.actual_output).get(self.field)
        return got == self.expected, f"{self.field} is {got!r}, expected {self.expected!r}"


def day1_contract() -> list[BaseMetric]:
    """C1-C5 from the Day 1 evidence contract."""
    return [
        RawJson(),
        ExactKeys(),
        FieldEquals("C3", "category", "damaged_item"),
        FieldEquals("C4", "urgency", "high"),
        FieldEquals("C5", "next_action", "request_damage_photo"),
    ]
