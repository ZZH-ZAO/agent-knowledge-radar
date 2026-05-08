# Session Archive

## Summary

- Project name: current workbench session archive
- Project path: `D:\claude-code-sourcemap\.claude\sessions`
- Document type: internal workbench guide
- Purpose: store lightweight historical work records that sit between transient task execution and formal long-term documentation

## What This Folder Is

This folder is the workbench's historical process layer.

It is not a replacement for:

- `.claude/docs/`
- `.claude/memory/`
- `.claude/skills/`

Instead, it fills the gap between them.

Use it to store:

- brief records of completed research or design tasks
- intermediate architectural judgments worth retrieving later
- mappings between a task and the final docs it produced
- candidate insights that are not yet stable enough for `memory/`

## What Goes Here

Each session record should be small, structured, and retrieval-friendly.

Recommended fields:

- `id`
- `created_at`
- `project`
- `task_type`
- `title`
- `summary`
- `keywords`
- `related_cases`
- `source_paths`
- `derived_docs`
- `status`

## What Does Not Go Here

Do not use this folder for:

- full lecture-style analysis docs
- stable long-term principles
- reusable skill instructions
- large raw transcripts

Those belong in:

- `.claude/docs/`
- `.claude/memory/`
- `.claude/skills/`

## File Layout

- `index.json`
  Master lightweight index of all session entries.
- `templates/session-entry.template.json`
  Template for creating a new session entry.
- `WORKFLOW.md`
  Minimum operating workflow for keeping entries, docs, and the index aligned.
- `entries/`
  Individual session records, one JSON file per entry.

## Operating Model

Think of the workbench knowledge layers like this:

- `sessions/` = historical work process
- `docs/` = formalized long-term case assets
- `memory/` = stable judgment rules
- `skills/` = reusable methods

## Current Stage

This folder is Phase 1 of the workbench upgrade plan:

- first create a stable archive structure
- then add lightweight search and retrieval
- then connect the archive into the formal documentation workflow

## Search

Phase 2 starts with a lightweight local search script:

```powershell
python .\scripts\session_search.py --project hermes-agent
python .\scripts\session_search.py --keyword memory-first
python .\scripts\session_search.py --text workbench --verbose
```

The script reads `index.json` only, so keeping the index concise and updated matters.

## Registration

After creating or updating an entry file, register it into the index with:

```powershell
python .\scripts\register_session.py .\.claude\sessions\entries\2026-04-22-hermes-agent-analysis.json
```

See `WORKFLOW.md` for the end-to-end archive process.
