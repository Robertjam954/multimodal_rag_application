"""Unit tests for the Verifier."""
import pytest

from agents.verifier import verify_claim
from approaches.approach import Citation, Claim, DataPoints


@pytest.mark.asyncio
async def test_no_citations_is_unsupported():
    v = await verify_claim(Claim(sentence="x", citation_ids=[]), DataPoints(citations=[]))
    assert v.label == "unsupported"
    assert "no citation" in v.reason.lower()


@pytest.mark.asyncio
async def test_cited_id_not_in_set_is_unsupported():
    dp = DataPoints(citations=[Citation(id="other", source_file="f.pdf", content_snippet="...")])
    v = await verify_claim(Claim(sentence="x", citation_ids=["missing"]), dp)
    assert v.label == "unsupported"
