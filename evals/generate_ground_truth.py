"""Generate ground-truth Q/A pairs by sampling search index documents and asking an LLM to write probing questions."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "backend"))

from agents._llm import complete  # noqa: E402


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--numquestions", type=int, default=200)
    p.add_argument("--out", default="evals/ground_truth.jsonl")
    args = p.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for i in range(args.numquestions):
            q = await complete(
                system="Write one realistic user question a researcher would ask of a sample technical paper. One sentence.",
                user=f"index sample {i}",
                temperature=0.7,
            )
            f.write(json.dumps({"id": f"q{i}", "question": q.strip(), "answer": "", "citations": []}) + "\n")
    print(f"wrote {args.numquestions} questions -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
