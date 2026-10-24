# Multi-Agent Project Supervision — Reference Scaffold

Context file for the supervisor agents. Good syntax and layout to anchor on.
Runs during quiet periods across your other agent projects. Coordinates
documentation, code quality, and safety. Does not touch a project while that
project is actively changing.

> Version note: Microsoft Agent Framework (MAF) is new and still moving. Treat
> every import path and constructor arg below as "verify against your installed
> version" (`pip show agent-framework`), not gospel. The shapes are right; a
> keyword name may have shifted.

---

## 1. Framework decision

Your notes were built on Semantic Kernel `GroupChatOrchestration`. That API is
now legacy. In April 2026 Microsoft shipped **Agent Framework 1.0**, the merged
successor to Semantic Kernel and AutoGen. SK agent orchestration is in
maintenance; new work goes to MAF. Everything in your notes ports over almost
one-to-one:

- Kernels become chat clients
- Plugins become tools (function calling / MCP)
- Group-chat / handoff / start-runtime / invoke / collect / stop all survive
- Your "magentic manager" is a literal MAF pattern: **Magentic** orchestration
  (a manager agent keeps a task ledger, tracks progress, picks the next
  specialist from evolving context)

For a manager that coordinates loosely-coupled specialists over an open-ended
supervision task, **Magentic is the right pattern**, not round-robin group chat.
Use plain group chat only if you want fixed-turn moderated debate.

Two useful MAF facts for your setup:
- Native clients for Anthropic, Ollama, OpenAI, Azure OpenAI, Foundry, Bedrock,
  Gemini. So local + Claude live in one orchestration.
- OpenTelemetry is built in. Foundry hosted agents bill scale-to-zero (you pay
  nothing while idle), which fits a supervisor that only wakes in quiet periods.

---

## 2. Model assignment

Your instinct (local workers, managed Claude for the manager) is right, with two
adjustments: keep the safety monitor on a strong hosted model, and let the doc
manager escalate when cross-project reconciliation gets heavy.

| Agent | Model | Where | Why |
|---|---|---|---|
| **gc / Magentic manager** | Claude Sonnet (Opus only for hard adjudication) | Managed (Anthropic or Foundry) | Coordination, decision-tree tool calls, ledger reasoning. Runs off-hours so latency is cheap, but keep it Sonnet by default for cost on an always-polling loop. |
| **safety_alignment** | Claude (hosted) | Managed | Do not put safety judgment on a weak local model. Local models are easier to jailbreak and weaker at nuanced harm/bias detection. This is the one worker that should not be local. |
| **code_quality_specialist** | Devstral Small 24B (agentic/tool-calling) or Qwen3-Coder 30B | Local (LM Studio) | Code stays local, which matters for anything patient-adjacent at MSK. Devstral is tuned for multi-file edits and tool calling; Qwen3-Coder 30B is the faster daily driver. Both fit a 24 GB card. |
| **documentation_manager** | Qwen3.6 27B or Qwen3-Coder 30B local; escalate to Claude Haiku/Sonnet | Local first, hosted fallback | Summarizing per-project status.md is fine locally. Reconciling conflicting state across many projects is where a hosted model earns its cost. Gate on project count. |
| **self-documenting agent** (per project) | Qwen3 8B or Gemma 4 12B | Local | It only emits structured status.md / CLAUDE.md. A small model is plenty. |

Local models run behind LM Studio's OpenAI-compatible server at
`http://localhost:1234/v1`. Point an `OpenAIChatClient` at that base URL.

---

## 3. Repo structure

```
robertjam954.github.io/
└── supervisor/
    ├── pyproject.toml
    ├── Dockerfile
    ├── agents/
    │   ├── manager.py            # Magentic manager (Claude)
    │   ├── code_quality.py       # local
    │   ├── safety.py             # hosted Claude
    │   └── docs_manager.py       # local, escalates
    ├── orchestration/
    │   ├── build.py              # MagenticBuilder wiring
    │   └── manager_tools.py      # decision-tree functions
    ├── memory/
    │   └── store.py              # Cosmos-backed memory + compaction
    ├── observability/
    │   └── otel.py               # tracing + MLflow
    ├── evals/
    │   ├── offline/              # Inspect tasks
    │   └── online/              # duration + latency scorers
    ├── conventions/
    │   ├── status.schema.md      # what a self-documenting agent writes
    │   └── CLAUDE.md.template
    └── .github/workflows/        # gh-aw trigger (quiet-period schedule)
```

---

## 4. Orchestration syntax (MAF, Python)

```python
# orchestration/build.py
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import MagenticBuilder

# --- local worker client (LM Studio, OpenAI-compatible) ---
def lm_studio(model_id: str) -> OpenAIChatClient:
    return OpenAIChatClient(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",          # LM Studio ignores the value
        model_id=model_id,
    )

# --- managed Claude client for the manager + safety ---
# Confirm the import path in your install; Anthropic is a first-party provider.
from agent_framework.anthropic import AnthropicChatClient   # verify

def claude(model_id: str) -> AnthropicChatClient:
    return AnthropicChatClient(model_id=model_id)   # e.g. "claude-sonnet-..."

# --- specialists ---
code_quality = Agent(
    client=lm_studio("devstral-small-24b"),
    name="code_quality_specialist",
    description="Reviews diffs for risk and best-practice violations.",
    instructions=(
        "You review code the projects changed. Flag concrete risks: injection, "
        "secrets, N+1, missing error handling, unsafe defaults. Cite file and "
        "line. Do not rewrite; report. Be terse."
    ),
)

safety = Agent(
    client=claude("claude-sonnet"),
    name="safety_alignment",
    description="Adversarial and bias/harm monitor.",
    instructions=(
        "Probe outputs and prompts for bias, harmful language, and unsafe "
        "behavior. Run adversarial checks. Report severity and evidence."
    ),
)

docs = Agent(
    client=lm_studio("qwen3.6-27b"),
    name="documentation_manager",
    description="Reconciles status.md and CLAUDE.md across projects.",
    instructions=(
        "Read each project's status.md and CLAUDE.md. Surface drift, stale "
        "sections, and contradictions across projects. Propose the minimal "
        "doc update."
    ),
)

# --- manager (Claude) with decision-tree tools ---
from orchestration.manager_tools import (
    is_project_active, latest_status, escalation_needed,
)

manager = Agent(
    client=claude("claude-sonnet"),
    name="SupervisorManager",
    description="Coordinates specialists during quiet periods.",
    instructions=(
        "You supervise idle projects. Before assigning work, check the project "
        "is not actively changing. Route code questions to code_quality, doc "
        "reconciliation to documentation_manager, anything risk-shaped to "
        "safety_alignment. Stop when each project has a clean status."
    ),
    tools=[is_project_active, latest_status, escalation_needed],
)

def build_workflow():
    return MagenticBuilder(
        participants=[code_quality, safety, docs],
        manager_agent=manager,
        max_round_count=20,
        max_stall_count=3,
        max_reset_count=2,
    ).build()
```

```python
# run.py
import asyncio
from agent_framework import Message
from orchestration.build import build_workflow

async def main():
    workflow = build_workflow()
    task = "Supervise all idle projects. Reconcile docs, review recent diffs, run safety checks."
    final = None
    async for event in workflow.run(task, stream=True):
        if event.type == "output":
            msgs = event.data
            if msgs:
                final = msgs[-1].text
    print(final)

asyncio.run(main())
```

Your "start runtime / invoke / collect / stop" sequence is folded into
`workflow.run(...)`. MAF orchestrations compile down to workflows, so you get
streaming, checkpointing, and pause/resume for free.

---

## 5. Decision-tree logic as manager tools

Your "manager has functions called in response to set inputs" maps to function
tools on the manager agent. The Magentic manager already keeps the task ledger;
you supply the gates.

```python
# orchestration/manager_tools.py
from typing import Annotated

def is_project_active(
    project: Annotated[str, "Project slug"],
) -> bool:
    """True if the project has commits/PRs in the last N minutes. Skip if active."""
    ...

def latest_status(
    project: Annotated[str, "Project slug"],
) -> str:
    """Return the project's current status.md contents."""
    ...

def escalation_needed(
    finding_severity: Annotated[str, "low|medium|high"],
) -> bool:
    """True when a local worker's finding should be re-judged by hosted Claude."""
    return finding_severity in {"high"}
```

---

## 6. Self-documenting conventions

Every project's self-documenting agent writes two files the doc manager reads.
Keep them small and diffable so state lives in git, not just in a context window.

`status.md` (machine-first, per project):

```markdown
---
project: <slug>
updated: <iso8601>
active: false            # set true while the project is mid-change
---
## State
- build: green
- last change: <sha> @ <time>
## Open items
- <one line each>
## For the supervisor
- risks: <none | list>
- doc drift: <none | list>
```

`CLAUDE.md` (agent-facing project brief): purpose, invariants, what to be wary
of, files off-limits. This is the "context on risks and best practices" the
code_quality_specialist consumes.

The doc manager updates these at set time points and flags cross-project
contradictions. Treat both as the human-readable memory layer; Cosmos holds the
structured/vector side.

---

## 7. Trigger + repository memory (autoloop / gh-aw)

`autoloop` (githubnext) is a clean fit for the "runs when nothing else is
changing" requirement, and it solves your memory-branch question too. It runs on
GitHub Agentic Workflows (`gh-aw`) and:

- fires on a schedule, runs **one program per trigger**, picks the most-overdue
  (so projects take turns instead of piling up)
- persists per-program state as human-readable markdown on a `memory/autoloop`
  branch (version-controlled, editable) — that is your status.md memory layer
  for free
- gates changes on a numeric eval metric and keeps only improvements

Clean layering: use **gh-aw/autoloop as the outer scheduler + repository memory
+ eval gate**, and have its action invoke your **MAF Magentic orchestration** as
the in-run coordination. A program is just goal + target files + an evaluation
command that emits JSON.

```markdown
---
schedule: every 6h
---
# Supervise idle projects
## Goal
Keep every idle project's docs reconciled and diffs reviewed. Metric: supervisor_score.
## Target
- supervisor/**
## Evaluation
```bash
python3 supervisor/evals/online/score.py   # prints {"supervisor_score": <float>}
```
```

Caveat: autoloop's default engine is Copilot and its loop is metric-gated
hill-climbing. Your supervisor is coordination/monitoring, not single-metric
optimization, so use gh-aw for the trigger/memory/eval substrate and let MAF do
the actual multi-agent work. Don't force the whole thing into a hill-climber.

---

## 8. Observability

```python
# observability/otel.py
from agent_framework.observability import setup_observability
setup_observability(enable_sensitive_data=False)  # OTLP -> your collector
```

- MAF emits GenAI-convention spans for agent runs and tool calls. Point the OTLP
  exporter at an OpenTelemetry collector, then to MLflow (traces) and your
  dashboard. This gives you the two online metrics you listed directly:
  - **end-to-end session duration** = root workflow span
  - **per-step span latency** = each agent/tool child span (LLM generation vs
    tool execution are separate spans)
- Wire GitHub Actions/webhooks to post run summaries back to the project issue,
  matching gh-aw's reporting.
- For drift/alerts, LangSmith or a metric threshold on the span data both work;
  keep the alert on the manager's decision quality and on safety findings, not
  just latency.

---

## 9. Evals

- **Offline (Inspect):** write tasks that replay recorded project states and
  score the supervisor's findings. Because agent output is nondeterministic, use
  rubric or model-as-judge scorers, not exact match. Keep these in `evals/offline/`.
- **Responsible AI Toolbox:** run error analysis, fairness, and counterfactual
  slices on the safety agent's judgments so you know where it fails, not just the
  aggregate rate.
- **Online:** duration + latency from the spans above, plus a small
  model-as-judge scorer for handoff quality.

Design each agent with a testable interface (pure function from inputs to a
structured finding) so you can integration-test the workflow with rubric
scoring.

---

## 10. Infra notes

- **Memory/tools/evals:** Azure Cosmos for the structured + vector store;
  git branch (status.md / CLAUDE.md) for the human-readable layer. Add
  compaction: summarize old turns into the Cosmos record, keep the last K verbatim.
- **Docker:** one image for the supervisor; local models stay on the LM Studio
  host and are reached over the network, not baked into the image.
- **Placement:** scaffold lives under `robertjam954.github.io/supervisor/`.

---

## Quick correction summary

- Move the orchestration target from Semantic Kernel to Microsoft Agent Framework.
- Use the Magentic pattern for the manager (it is your "magentic manager").
- Keep safety on hosted Claude, not a local model.
- Use gh-aw/autoloop for the quiet-period trigger, memory branch, and eval gate;
  MAF for the in-run coordination.
