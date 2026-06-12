"""Integration tests for the Quart routes."""
import pytest


@pytest.mark.asyncio
async def test_config_route(client):
    res = await client.get("/config")
    assert res.status_code == 200
    data = await res.get_json()
    assert "streamingEnabled" in data
    assert "verifierEnabled" in data


@pytest.mark.asyncio
async def test_chat_nonstream(client):
    res = await client.post(
        "/chat/nonstream",
        json={"messages": [{"role": "user", "content": "what is chunking?"}], "context": {"overrides": {}}},
    )
    assert res.status_code == 200
    data = await res.get_json()
    assert "answer" in data


@pytest.mark.asyncio
async def test_sql_plan(client):
    res = await client.post("/sql/plan", json={"change_request": "Add LOYALTY_TIER VARCHAR(20) to ODS.CUSTOMER"})
    assert res.status_code == 200
    bundle = await res.get_json()
    assert "parsed" in bundle and "validation" in bundle
