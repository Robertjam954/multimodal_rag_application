#!/usr/bin/env python3
"""Fetch curated Microsoft Learn URLs and save extracted article text to disk.

Standalone (no Azure AI Search / embeddings required) - reuses LearnDocParser so
the saved text matches what `prepdocs --source learn` ingests once the search
index is deployed. Each URL becomes one .md file under --out; failures are
skipped and reported.

  python scripts/fetch_learn.py
  python scripts/fetch_learn.py --urls data/learn/azure_ai_seed.txt --out data/learn/fetched
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

import httpx  # noqa: E402
from prepdocslib.learndocparser import LearnDocParser  # noqa: E402


def read_urls(path: Path) -> list[str]:
    urls: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def out_name(url: str) -> str:
    p = urlparse(url)
    slug = f"{p.netloc}{p.path}".strip("/").replace("/", "_")
    for ch in "?=&":
        slug = slug.replace(ch, "-")
    return (slug or "index")[:180] + ".md"


async def fetch_all(urls: list[str], out_dir: Path, concurrency: int, timeout: float):
    out_dir.mkdir(parents=True, exist_ok=True)
    parser = LearnDocParser()
    sem = asyncio.Semaphore(concurrency)
    ok: list[str] = []
    failed: list[tuple[str, str]] = []

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": "multimodal-rag-app/learn-ingest"},
    ) as http:

        async def one(url: str) -> None:
            async with sem:
                try:
                    r = await http.get(url)
                    r.raise_for_status()
                except Exception as exc:  # noqa: BLE001
                    failed.append((url, str(exc)))
                    print(f"  FAIL  {url} -> {exc}")
                    return
            texts: list[str] = []
            async for page in parser.parse(r.content, url):
                if page.text.strip():
                    texts.append(page.text)
            if not texts:
                failed.append((url, "empty after parse"))
                print(f"  EMPTY {url}")
                return
            dest = out_dir / out_name(url)
            dest.write_text(f"<!-- source: {url} -->\n\n" + "\n\n".join(texts), encoding="utf-8")
            ok.append(url)
            print(f"  OK    {dest.name} ({sum(len(t) for t in texts):,} chars)")

        await asyncio.gather(*(one(u) for u in urls))

    return ok, failed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="data/learn/azure_ai_seed.txt")
    ap.add_argument("--out", default="data/learn/fetched")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=30.0)
    args = ap.parse_args()

    urls = read_urls(Path(args.urls))
    print(f"Fetching {len(urls)} URLs -> {args.out}\n")
    ok, failed = asyncio.run(fetch_all(urls, Path(args.out), args.concurrency, args.timeout))
    print(f"\nDone: {len(ok)} ok, {len(failed)} failed")
    for url, err in failed:
        print(f"  - {url}: {err}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
