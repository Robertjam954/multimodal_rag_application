"""Lists files from local FS or ADLS Gen2 paths."""
from __future__ import annotations

import dataclasses
import hashlib
from pathlib import Path
from typing import AsyncIterator


@dataclasses.dataclass
class File:
    path: Path
    data: bytes
    md5: str

    @classmethod
    def from_path(cls, path: Path) -> "File":
        data = path.read_bytes()
        return cls(path=path, data=data, md5=hashlib.md5(data).hexdigest())


async def list_local(root: Path, pattern: str = "**/*") -> AsyncIterator[File]:
    for p in root.glob(pattern):
        if p.is_file():
            yield File.from_path(p)
