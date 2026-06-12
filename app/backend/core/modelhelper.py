"""Model name -> tokens-per-dollar table for cost estimates."""
from __future__ import annotations

# USD per 1M tokens (rough placeholders; refresh quarterly)
PRICES_PER_M = {
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "o3-mini": {"input": 1.10, "output": 4.40},
    "text-embedding-3-large": {"input": 0.13, "output": 0.0},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
}


def estimate_cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICES_PER_M.get(model, PRICES_PER_M["gpt-4.1-mini"])
    return (input_tokens / 1_000_000) * p["input"] + (output_tokens / 1_000_000) * p["output"]
