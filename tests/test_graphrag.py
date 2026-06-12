import pytest

from graphrag.retriever import global_search, hybrid_search


@pytest.mark.asyncio
async def test_global_search_runs_without_cosmos():
    r = await global_search(query="anything")
    assert "community_chunks" in r


@pytest.mark.asyncio
async def test_hybrid_search_runs_without_cosmos():
    r = await hybrid_search(query="anything")
    assert "nodes" in r and "community_chunks" in r
