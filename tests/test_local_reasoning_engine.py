from __future__ import annotations

import sys
import types

import local_reasoning_engine
import local_reasoning_server
import pytest


def install_fake_vertex(monkeypatch):
    calls: dict[str, object] = {}
    vertexai_module = types.ModuleType("vertexai")

    def fake_init(*, project: str, location: str) -> None:
        calls["init"] = {"project": project, "location": location}

    class FakeLangchainAgent:
        def __init__(self, *, model, tools, instructions):
            calls["agent"] = {
                "model": model,
                "tools": tools,
                "instructions": instructions,
            }

        def query(self, *, input):
            calls["query"] = input
            return {"input": input, "tool_count": len(calls["agent"]["tools"])}

    vertexai_module.init = fake_init
    preview_module = types.ModuleType("vertexai.preview")
    reasoning_engines_module = types.ModuleType("vertexai.preview.reasoning_engines")
    reasoning_engines_module.LangchainAgent = FakeLangchainAgent
    preview_module.reasoning_engines = reasoning_engines_module

    monkeypatch.setitem(sys.modules, "vertexai", vertexai_module)
    monkeypatch.setitem(sys.modules, "vertexai.preview", preview_module)
    monkeypatch.setitem(sys.modules, "vertexai.preview.reasoning_engines", reasoning_engines_module)
    return calls


def test_resolve_local_config_from_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "demo-project")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "europe-west4")

    config = local_reasoning_engine.resolve_local_config()

    assert config.project_id == "demo-project"
    assert config.location == "europe-west4"
    assert config.model == local_reasoning_engine.DEFAULT_MODEL


def test_build_local_orchestrator_initializes_vertex(monkeypatch):
    calls = install_fake_vertex(monkeypatch)
    config = local_reasoning_engine.LocalReasoningConfig(project_id="demo-project")

    orchestrator = local_reasoning_engine.build_local_orchestrator(config)
    result = orchestrator.query(input="hello world")

    assert calls["init"] == {"project": "demo-project", "location": local_reasoning_engine.DEFAULT_LOCATION}
    assert calls["agent"]["model"] == local_reasoning_engine.DEFAULT_MODEL
    assert len(calls["agent"]["tools"]) == 2
    assert result == {"input": "hello world", "tool_count": 2}


def test_query_local_orchestrator_with_explicit_orchestrator():
    class StubOrchestrator:
        def query(self, *, input):
            return f"echo:{input}"

    result = local_reasoning_engine.query_local_orchestrator(
        "How many units are in stock?",
        orchestrator=StubOrchestrator(),
    )

    assert result == "echo:How many units are in stock?"


@pytest.mark.asyncio
async def test_local_reasoning_server_predict(monkeypatch):
    monkeypatch.setattr(local_reasoning_server, "query_local_orchestrator", lambda prompt: {"echo": prompt})
    client = local_reasoning_server.app.test_client()

    response = await client.post("/predict", json={"input": "test prompt"})

    assert response.status_code == 200
    assert await response.get_json() == {"status": "success", "output": {"echo": "test prompt"}}


@pytest.mark.asyncio
async def test_local_reasoning_server_rejects_missing_json():
    client = local_reasoning_server.app.test_client()

    response = await client.post("/predict")

    assert response.status_code == 400
    payload = await response.get_json()
    assert payload["status"] == "error"
