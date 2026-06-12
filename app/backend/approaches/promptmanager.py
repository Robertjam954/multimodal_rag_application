"""Jinja2 prompt loader. Caches templates by name; renders with context dict."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

PROMPT_DIR = Path(__file__).parent / "prompts"


class PromptManager:
    def __init__(self, prompt_dir: Path | None = None) -> None:
        self.prompt_dir = prompt_dir or PROMPT_DIR
        self.env = Environment(
            loader=FileSystemLoader(str(self.prompt_dir)),
            autoescape=select_autoescape(enabled_extensions=()),
            keep_trailing_newline=True,
        )

    def render(self, name: str, **context: Any) -> str:
        return self.env.get_template(name).render(**context)

    def load_json(self, name: str) -> dict[str, Any] | list[Any]:
        with (self.prompt_dir / name).open("r") as f:
            return json.load(f)
