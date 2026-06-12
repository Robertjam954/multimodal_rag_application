"""Unit tests for the approach layer."""
import pytest

from approaches.multiagent_approach import MultiAgentApproach
from approaches.promptmanager import PromptManager


@pytest.mark.asyncio
async def test_multiagent_run_yields_terminal_events():
    a = MultiAgentApproach(prompt_manager=PromptManager())
    events = []
    async for evt in a.run_stream(messages=[{"role": "user", "content": "summarize"}], context={"overrides": {}}):
        events.append(evt.get("event"))
    assert "verdict" in events
