"""Runs the eval harness: send each ground-truth question to the backend, score answers."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

import httpx


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="evals/evaluate_config.json")
    p.add_argument("--numquestions", type=int, default=None)
    args = p.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    target = cfg["target_url"]
    gt_path = Path(cfg["ground_truth"])
    out_dir = Path(cfg["results_dir"]) / "run"
    out_dir.mkdir(parents=True, exist_ok=True)

    questions = [json.loads(l) for l in gt_path.read_text().splitlines() if l.strip()]
    if args.numquestions:
        questions = questions[: args.numquestions]

    out_file = out_dir / "predictions.jsonl"
    async with httpx.AsyncClient(timeout=60) as c:
        with out_file.open("w") as f:
            for q in questions:
                resp = await c.post(target, json={"messages": [{"role": "user", "content": q["question"]}]})
                pred = resp.json() if resp.status_code == 200 else {"error": resp.status_code}
                f.write(json.dumps({"id": q["id"], "question": q["question"], "prediction": pred}) + "\n")
    print(f"wrote {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
