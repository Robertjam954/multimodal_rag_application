"""Batch evaluation of the tutor agent against the three Foundry built-in evaluators.

Flow:
1. Read AI-engineering test questions from `eval_questions.jsonl`.
2. Run each through `tutor_agent.chat_turn` locally (with tools + memory).
3. Submit the (query, response) pairs to `openai_client.evals` as a `completions` data
   source so the built-in evaluators score the precomputed answers.
4. Poll until the run finishes, print per-question pass/fail + scores.

Built-in evaluators used:
- builtin.violence       safety  (0-7 severity)
- builtin.fluency        quality (1-5)
- builtin.task_adherence quality (1-5) - did the answer address the query

Run:
    python -m agents.run_eval
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

QUESTIONS_PATH = Path(__file__).parent / "eval_questions.jsonl"


def _load_questions() -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    for line in QUESTIONS_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        questions.append(json.loads(line))
    return questions


async def _run_agent_on_all(questions: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Execute the tutor agent locally on each question and collect (query, response) pairs."""
    from agents.tutor_agent import chat_turn

    session_id = f"eval-{uuid.uuid4().hex[:8]}"
    pairs: list[dict[str, Any]] = []
    for i, q in enumerate(questions, 1):
        query = q["query"]
        print(f"[{i}/{len(questions)}] {query}")
        t0 = time.time()
        result = await chat_turn(query, session_id=f"{session_id}-{i}")
        dur = int((time.time() - t0) * 1000)
        tool_names = [tc["tool"] for tc in result.tool_calls]
        print(f"   -> tools_called={tool_names}  duration={dur}ms  answer_chars={len(result.answer)}")
        pairs.append(
            {
                "item": {
                    "query": query,
                    "response": result.answer,
                }
            }
        )
    return pairs


def _build_project_client():
    """Construct the AIProjectClient against the Foundry project endpoint."""
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        raise RuntimeError("AZURE_AI_PROJECT_ENDPOINT is not set")
    return AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())


def _testing_criteria(judge_deployment: str) -> list[dict[str, Any]]:
    return [
        {
            "type": "azure_ai_evaluator",
            "name": "violence_detection",
            "evaluator_name": "builtin.violence",
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "fluency",
            "evaluator_name": "builtin.fluency",
            "initialization_parameters": {"deployment_name": judge_deployment},
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "task_adherence",
            "evaluator_name": "builtin.task_adherence",
            "initialization_parameters": {"deployment_name": judge_deployment},
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
    ]


def _data_source(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "type": "completions",
        "source": {
            "type": "file_content",
            "content": pairs,
        },
        "input_messages": {
            "type": "template",
            "template": [
                {
                    "type": "message",
                    "role": "user",
                    "content": {"type": "input_text", "text": "{{item.query}}"},
                }
            ],
        },
        # The "model" field is required but no completions are generated for this data source
        # shape - we're feeding precomputed responses. Use the chat deployment as a no-op.
        "model": os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "grok-4-20-reasoning"),
    }


def _as_dict(obj: Any) -> dict[str, Any]:
    """SDK objects are Pydantic models; fall back to dict-like or attribute access."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return obj
    return {k: getattr(obj, k) for k in dir(obj) if not k.startswith("_") and not callable(getattr(obj, k))}


def _print_results(output_items: list[Any]) -> None:
    print(f"\n=== Per-question results ({len(output_items)}) ===")
    for i, oi in enumerate(output_items, 1):
        sample = _as_dict(getattr(oi, "sample", None) or {})
        # Foundry's Sample carries the input under various shapes; query may live in `query`
        # (custom item field) or under `input[*].content[*].text`.
        query = sample.get("query") or sample.get("input_text") or "(query not in sample)"
        if not query or query == "(query not in sample)":
            inputs = sample.get("input") or []
            for msg in inputs:
                msg_d = _as_dict(msg)
                for c in msg_d.get("content", []) or []:
                    c_d = _as_dict(c)
                    if c_d.get("text"):
                        query = c_d["text"]
                        break
                if query and query != "(query not in sample)":
                    break
        print(f"\n[{i}] {query[:120]}")
        for r in getattr(oi, "results", []) or []:
            r = _as_dict(r)
            name = r.get("name", "?")
            passed = r.get("passed")
            score = r.get("score")
            reason = (r.get("reason") or r.get("explanation") or "").strip()
            tag = "PASS" if passed else "FAIL"
            base = f"   {tag:4}  {name:20}  score={score}"
            if reason:
                base += f"  reason={reason[:120]}"
            print(base)


async def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    questions = _load_questions()
    if not questions:
        print("No questions in eval_questions.jsonl - aborting", file=sys.stderr)
        return 1

    print(f"Running agent on {len(questions)} question(s)...\n")
    pairs = await _run_agent_on_all(questions)

    project_client = _build_project_client()
    try:
        openai_client = project_client.get_openai_client()
        judge_deployment = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "grok-4-20-reasoning")

        print(f"\nCreating evaluation object (judge model: {judge_deployment})...")
        eval_object = openai_client.evals.create(
            name="Tutor Agent Eval",
            data_source_config={
                "type": "custom",
                "item_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "response": {"type": "string"},
                    },
                    "required": ["query", "response"],
                },
                "include_sample_schema": False,
            },
            testing_criteria=_testing_criteria(judge_deployment),
        )
        print(f"   eval_id={eval_object.id}")

        print("Submitting run...")
        run = openai_client.evals.runs.create(
            eval_id=eval_object.id,
            name=f"Tutor Eval Run {uuid.uuid4().hex[:6]}",
            data_source=_data_source(pairs),
        )
        print(f"   run_id={run.id}")

        while run.status not in {"completed", "failed", "canceled"}:
            print(f"   status={run.status}")
            time.sleep(5)
            run = openai_client.evals.runs.retrieve(run_id=run.id, eval_id=eval_object.id)

        print(f"\nFinal status: {run.status}")
        if run.status != "completed":
            print(f"Run did not complete cleanly. Full run object: {run}")
            return 2

        print(f"Result counts: {run.result_counts}")
        output_items = list(
            openai_client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id)
        )
        _print_results(output_items)

        report_url = getattr(run, "report_url", None)
        if report_url:
            print(f"\nReport URL: {report_url}")

        # Cleanup so we don't leave eval objects behind.
        try:
            openai_client.evals.delete(eval_id=eval_object.id)
        except Exception:
            logger.exception("eval cleanup failed (non-fatal)")

        return 0
    finally:
        project_client.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
