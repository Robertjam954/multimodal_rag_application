#!/usr/bin/env python3
"""
6am self-doc refresh (local worker).

Walks each subproject folder, skips any that are actively changing, asks the
local LM Studio model to regenerate status.md and CLAUDE.md, stamps `updated`
with today's date, and pushes the docs to the `supervisor-docs` branch that the
7am gc-manager compile reads.

Failure mode by design: if a project's model call fails, its docs are left
untouched, so the old `updated` timestamp stays and the 7am compile flags it
STALE instead of publishing stale todos. Never fake the timestamp.

Run:  python3 refresh_docs.py               (all projects)
      python3 refresh_docs.py --project foo (one)
      python3 refresh_docs.py --dry-run     (no writes, no push)
"""

from __future__ import annotations
import argparse, json, subprocess, sys, time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

# ---------------------------------------------------------------- config
REPO_DIR       = Path.home() / "robertjam954.github.io"   # local clone with the subprojects
PROJECTS_ROOT  = REPO_DIR / "projects"                    # parent of the subproject folders
SUPERVISOR_DIR = "supervisor"                             # exclude the supervisor's own folder
DOCS_BRANCH    = "supervisor-docs"                        # branch the 7am compile reads
DOCS_CHECKOUT  = Path.home() / ".cache" / "supervisor-docs"  # dedicated checkout for that branch
GIT_REMOTE     = "origin"

LM_STUDIO_URL  = "http://localhost:1234/v1/chat/completions"
MODEL_ID       = "qwen3-8b"        # the small local self-doc model
REQUEST_TIMEOUT = 120

TZ             = ZoneInfo("America/New_York")
ACTIVE_WINDOW_SEC = 20 * 60        # skip a project committed to within this window
MAX_README_CHARS  = 4000
MAX_TREE_LINES    = 150
# -----------------------------------------------------------------------


def git(*args: str, cwd: Path = REPO_DIR, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, text=True,
                       capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> {r.stderr.strip()}")
    return r.stdout.strip()


def today_stamp() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def today_date() -> str:
    return datetime.now(TZ).date().isoformat()


def discover_projects() -> list[Path]:
    out = []
    for p in sorted(PROJECTS_ROOT.iterdir()):
        if p.is_dir() and not p.name.startswith(".") and p.name != SUPERVISOR_DIR:
            out.append(p)
    return out


def is_active(proj: Path) -> bool:
    """Active = uncommitted changes, or a commit within the last window."""
    rel = str(proj.relative_to(REPO_DIR))
    if git("status", "--porcelain", "--", rel):
        return True
    ct = git("log", "-1", "--format=%ct", "--", rel, check=False)
    if ct.isdigit():
        return (time.time() - int(ct)) < ACTIVE_WINDOW_SEC
    return False


def gather_context(proj: Path) -> str:
    rel = str(proj.relative_to(REPO_DIR))
    commits = git("log", "-10", "--format=%h %s", "--", rel, check=False)
    tree = "\n".join(git("ls-files", "--", rel, check=False).splitlines()[:MAX_TREE_LINES])
    readme = ""
    for name in ("README.md", "readme.md"):
        f = proj / name
        if f.exists():
            readme = f.read_text(errors="ignore")[:MAX_README_CHARS]
            break
    prev = ""
    prev_f = DOCS_CHECKOUT / "docs" / proj.name / "status.md"
    if prev_f.exists():
        prev = prev_f.read_text(errors="ignore")
    return (
        f"# Project: {proj.name}\n\n"
        f"## Recent commits\n{commits or '(none)'}\n\n"
        f"## Tracked files\n{tree or '(none)'}\n\n"
        f"## README (truncated)\n{readme or '(none)'}\n\n"
        f"## Previous status.md\n{prev or '(none)'}\n"
    )


SYSTEM_PROMPT = (
    "You are a self-documenting agent for one software subproject. From the "
    "context, produce two documents. Return ONLY a JSON object, no prose and no "
    "code fences, with exactly these keys:\n"
    '  "status_body": markdown for status.md WITHOUT frontmatter. Include a '
    '"## State" section (build status, last change) and a "## Open items" '
    "section as a bullet list of concrete, current todos drawn from code TODOs, "
    "unfinished work, and open threads.\n"
    '  "claude_body": markdown for CLAUDE.md with "## Purpose", "## Invariants", '
    'and "## Be wary of" (real risks and gotchas for an agent touching this code).\n'
    "Be concrete and terse. Do not invent facts not supported by the context."
)


def call_model(context: str) -> dict:
    payload = {
        "model": MODEL_ID,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context},
        ],
    }
    r = requests.post(LM_STUDIO_URL, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    text = r.json()["choices"][0]["message"]["content"]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("model did not return JSON")
    obj = json.loads(text[start:end + 1])
    if "status_body" not in obj or "claude_body" not in obj:
        raise ValueError("missing keys in model output")
    return obj


def write_docs(proj: Path, doc: dict) -> None:
    d = DOCS_CHECKOUT / "docs" / proj.name
    d.mkdir(parents=True, exist_ok=True)
    frontmatter = (
        "---\n"
        f"project: {proj.name}\n"
        f"updated: {today_stamp()}\n"
        "active: false\n"
        "---\n\n"
    )
    (d / "status.md").write_text(frontmatter + doc["status_body"].strip() + "\n")
    (d / "CLAUDE.md").write_text(doc["claude_body"].strip() + "\n")


def ensure_docs_checkout() -> None:
    """Make DOCS_CHECKOUT a clone sitting on DOCS_BRANCH, creating the branch if new."""
    if not (DOCS_CHECKOUT / ".git").exists():
        DOCS_CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        url = git("remote", "get-url", GIT_REMOTE)
        git("clone", url, str(DOCS_CHECKOUT), cwd=DOCS_CHECKOUT.parent)
    git("fetch", GIT_REMOTE, cwd=DOCS_CHECKOUT)
    remote_branches = git("branch", "-r", cwd=DOCS_CHECKOUT)
    if f"{GIT_REMOTE}/{DOCS_BRANCH}" in remote_branches:
        git("checkout", "-B", DOCS_BRANCH, f"{GIT_REMOTE}/{DOCS_BRANCH}", cwd=DOCS_CHECKOUT)
        git("reset", "--hard", f"{GIT_REMOTE}/{DOCS_BRANCH}", cwd=DOCS_CHECKOUT)
    else:
        git("checkout", "--orphan", DOCS_BRANCH, cwd=DOCS_CHECKOUT)
        git("rm", "-rf", "--quiet", ".", cwd=DOCS_CHECKOUT, check=False)


def commit_and_push(n: int) -> None:
    git("add", "-A", cwd=DOCS_CHECKOUT)
    if not git("status", "--porcelain", cwd=DOCS_CHECKOUT):
        print("no doc changes to push")
        return
    git("commit", "-m", f"docs: 5:30 refresh {today_date()} ({n} projects)", cwd=DOCS_CHECKOUT)
    git("push", GIT_REMOTE, DOCS_BRANCH, cwd=DOCS_CHECKOUT)
    print(f"pushed {DOCS_BRANCH}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="run one project by folder name")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.dry_run:
        ensure_docs_checkout()

    projects = discover_projects()
    if args.project:
        projects = [p for p in projects if p.name == args.project]
        if not projects:
            sys.exit(f"no such project: {args.project}")

    refreshed, skipped, failed = [], [], []
    for proj in projects:
        if is_active(proj):
            skipped.append(proj.name)
            print(f"skip  {proj.name} (active)")
            continue
        try:
            doc = call_model(gather_context(proj))
            if not args.dry_run:
                write_docs(proj, doc)
            refreshed.append(proj.name)
            print(f"ok    {proj.name}")
        except Exception as e:            # leave this project's docs stale on purpose
            failed.append(proj.name)
            print(f"FAIL  {proj.name}: {e}", file=sys.stderr)

    if not args.dry_run and refreshed:
        commit_and_push(len(refreshed))

    print(f"\nrefreshed={len(refreshed)} skipped={len(skipped)} failed={len(failed)}")
    return 1 if failed else 0   # nonzero surfaces in `systemctl --user status`


if __name__ == "__main__":
    raise SystemExit(main())
