# Red teaming the AI tutor

Adversarial red teaming with [promptfoo](https://www.promptfoo.dev/docs/red-team/),
complementing the existing `evals/` suite (promptfoo eval, `safety_evaluation.py`
adversarial simulator, `verifier_eval.py`). Where those measure accuracy and safety on
curated sets, this generates *attacks* - jailbreaks, prompt injection, PII extraction, and
system-prompt leaks - and reports which get through.

## Targets

Both target options are local and free:

1. **Ollama model (default).** In `MODE=local` the tutor routes chat to Ollama, so the base
   model is a fair first target. Runs today with just Ollama up.
2. **Live `/chat` endpoint (commented in the config).** Red-teams the full application -
   retrieval, the Verifier gate, and content-safety filters - which is the point of
   red-teaming a RAG app rather than a bare model. Start the backend (`MODE=local`, so it
   is Ollama-backed) and tune the `body` / `transformResponse` in `promptfooconfig.yaml` to
   the `/chat` SSE contract, then uncomment target 2.

## What it probes

`harmful:*` and `pii:*` (content/PII), `prompt-extraction` (system-prompt leak),
`hijacking` (off-task), and `hallucination` (uncited claims the Verifier should reject),
driven by `jailbreak`, `jailbreak:composite`, and `prompt-injection` strategies.

## Prerequisites

- **Node.js** (promptfoo runs via `npx`).
- **Ollama** running with a chat model pulled:

  ```bash
  ollama serve
  ollama pull llama3.1        # or any chat model; update the target id to match
  ```

- For target 2 only: the backend running locally in `MODE=local` (see the root CLAUDE.md).

## Run

```bash
cd evals/redteam
npx promptfoo@latest redteam run
npx promptfoo@latest redteam report
```

## Notes

- Generated artifacts (`redteam.yaml`, `output.json`, `results/`) are git-ignored - they
  hold machine-generated adversarial prompts and outputs.
- This is research tooling for evaluating your own deployment; it is not a certified safety
  audit. Do not use it against systems you do not own.
