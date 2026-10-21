"""Offline tests: retriever and citation metric, no API calls."""
from deepeval.test_case import LLMTestCase

from ragkit.metrics import CitationMetric
from ragkit.retriever import BM25, load_chunks


def test_retriever_finds_the_right_doc():
    ix = BM25(load_chunks())
    assert ix.search("How many PTO days carry over?")[0].doc_id == "pto"
    assert ix.search("two-factor authentication SMS")[0].doc_id == "security"
    assert ix.search("doctor's note sick")[0].doc_id == "sick_leave"


def _tc(output):
    return LLMTestCase(input="q", actual_output=output,
                       retrieval_context=["[pto] PTO: ...", "[expenses] Expenses: ..."])


def test_citation_metric():
    m = CitationMetric()
    assert m.measure(_tc("You can carry over 5 days [pto].")) == 1.0
    assert m.measure(_tc("You can carry over 5 days.")) == 0.0
    assert m.measure(_tc("5 days [pto]. Lost on 1 Jan [security].")) == 0.5
    assert m.measure(_tc("The handbook doesn't cover this.")) == 1.0
