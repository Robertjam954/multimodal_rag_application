---
# supervisor/.github/workflows/morning-todos.md
# Compile: gh aw compile morning-todos
on:
  schedule:
    - cron: "0 7 * * *"
      timezone: America/New_York   # real 7am ET, DST handled by the compiler
  workflow_dispatch:               # manual reruns
engine: claude                     # the managed gc manager (needs ANTHROPIC_API_KEY secret)
permissions:
  contents: read
  issues: read
tools:
  repo-memory:
    branch-name: memory/supervisor-docs   # where the 6am refresh pushed status.md/CLAUDE.md
  github:
    toolsets: [issues, pull_requests]
safe-outputs:
  create-issue:
    title-prefix: "[todos] "
    labels: [todos, supervisor]
---

# 7am todo compile

You are the gc manager for the supervisor folder. Compile the active todos
across every subproject.

## Freshness gate (do this first)
Each subproject's `status.md` in repo memory has an `updated` field. Before
compiling, check every one:
- If `updated` is not from today, or the file is missing, the 6am refresh did
  not complete for that subproject. List it under a **STALE** heading and do
  **not** invent or infer its todos. Report last-known `updated` date.
- Only compile todos for subprojects whose docs are fresh today.

## Compile
1. Read each fresh subproject's `status.md` "Open items" and the "be wary of"
   notes from its `CLAUDE.md`.
2. Read open issues and open PRs for in-flight work not yet in the docs.
3. Carry forward unfinished items from the most recent `[todos]` issue; mark an
   item done if its issue or PR has since closed.
4. Group todos by subproject. Flag anything stale (untouched > 5 days) and
   anything that blocks another subproject.
5. Emit one dated digest issue: fresh subprojects grouped with their todos, a
   STALE section for any that missed the 6am refresh, and a short "blocked /
   cross-project" section at the top.

Keep it terse. This is a scannable morning digest, not a report.
