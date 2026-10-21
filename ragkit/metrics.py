"""Custom deterministic metrics. No LLM calls, so they're free and fully reproducible."""
import re

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

ABSTAIN = "the handbook doesn't cover this"


class CitationMetric(BaseMetric):
    """Every cited [doc_id] must be one that was actually retrieved, and answers need at least one citation."""

    def __init__(self, threshold=1.0):
        self.threshold = threshold

    def measure(self, test_case: LLMTestCase, *args, **kwargs):
        out = test_case.actual_output or ""
        retrieved = {re.match(r"\[([\w-]+)\]", c).group(1) for c in test_case.retrieval_context or []}
        cited = re.findall(r"\[([\w-]+)\]", out)
        if ABSTAIN in out.lower().replace("’", "'"):
            self.score, self.reason = 1.0, "abstained, no citation needed"
        elif not cited:
            self.score, self.reason = 0.0, "no citations"
        else:
            bad = [c for c in cited if c not in retrieved]
            self.score = 1 - len(bad) / len(cited)
            self.reason = f"invalid citations: {bad}" if bad else f"all {len(cited)} citations valid"
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Citation validity"
