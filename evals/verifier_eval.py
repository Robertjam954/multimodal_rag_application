"""Evaluate the Verifier against a golden set of (claim, evidence, label) triples."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "backend"))

from agents.verifier import verify_claim  # noqa: E402
from approaches.approach import Citation, Claim, DataPoints  # noqa: E402


async def main() -> int:
    golden = Path(__file__).parent / "verifier_golden.jsonl"
    correct = total = 0
    for line in golden.read_text().splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        dp = DataPoints(citations=[Citation(id=e["id"], source_file=e.get("source_file", "f"), content_snippet=e["text"]) for e in case["evidence"]])
        v = await verify_claim(Claim(sentence=case["claim"], citation_ids=[e["id"] for e in case["evidence"]]), dp)
        if v.label == case["expected_label"]:
            correct += 1
        total += 1
    print(f"verifier accuracy: {correct}/{total} = {correct / max(total, 1):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
