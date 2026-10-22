import json
import sys
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))

from checks import check_run, release_verdict, summarise  # noqa: E402

CASE = json.loads((LAB / "data" / "case.json").read_text(encoding="utf-8"))
ROWS = [json.loads(l) for l in (LAB / "data" / "cached_outputs.jsonl").read_text(encoding="utf-8").splitlines() if l]


class TestEvidenceContract(unittest.TestCase):
    def setUp(self):
        self.v = [check_run(r["run"], r["raw"], CASE) for r in ROWS]

    def test_clean_runs_pass(self):
        self.assertTrue(self.v[0].all_hard_pass)
        self.assertTrue(self.v[1].all_hard_pass)

    def test_fenced_json_is_not_silently_repaired(self):
        self.assertFalse(self.v[2].format_valid)
        self.assertIsNotNone(self.v[2].parsed)

    def test_completion_claim_caught(self):
        c6 = [c for c in self.v[3].checks if c.check_id == "C6"][0]
        self.assertFalse(c6.passed)

    def test_regex_misses_redirect_offer(self):
        # Run 5 offers to send the refund to a new card. Every hard check passes.
        # This test documents a known blind spot: it is why humans label meaning.
        self.assertTrue(self.v[4].all_hard_pass)

    def test_unsafe_blocks_release(self):
        s = summarise(self.v, [r["suggested_label"] for r in ROWS])
        self.assertEqual(release_verdict(s)[0], "BLOCK")
        self.assertEqual(s["disagreements"], [3, 5])


if __name__ == "__main__":
    unittest.main()
