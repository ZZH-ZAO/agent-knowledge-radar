# Session Archive Workflow

## Summary

- Project name: session archive workflow
- Project path: `D:\claude-code-sourcemap\.claude\sessions`
- Document type: internal workbench workflow
- Purpose: define the minimum workflow for keeping session records, formal docs, and the session index in sync

## Why This Exists

The session archive is only useful if it stays connected to the formal documentation flow.

This workflow makes sure a task does not leave behind:

- only `docs/` with no historical process record
- only `entries/*.json` with no formal output
- only an entry file without updating `index.json`

## Minimum Workflow For A New Case

When a new project analysis or design task is completed:

1. Create or update the formal docs in `.claude/docs/`
2. Create one session record in `.claude/sessions/entries/`
3. Ensure the session record points to the final docs via `derived_docs`
4. Register the session entry into `.claude/sessions/index.json`

## Entry File Naming

Recommended pattern:

- `YYYY-MM-DD-project-slug-task-slug.json`

Example:

- `2026-04-22-hermes-agent-analysis.json`

## Required Entry Fields

The entry must contain:

- `id`
- `created_at`
- `project`
- `task_type`
- `title`
- `summary`
- `status`

Strongly recommended:

- `keywords`
- `related_cases`
- `source_paths`
- `derived_docs`
- `phase_report`
- `skill_promotions`
- `memory_promotions`
- `doc_promotions`
- `promotion_review`
- `followup_actions`

## Registering An Entry

After creating the entry file, run:

```powershell
python .\scripts\register_session.py .\.claude\sessions\entries\2026-04-22-hermes-agent-analysis.json
```

This will:

- validate the entry
- add or update the matching index record
- keep `index.json` sorted by `created_at`

## Promotion Check

Before registering a session as fully archived, explicitly check whether the case should promote anything into:

- `skills/`
- `memory/`
- `docs/`

Use these fields when relevant:

- `phase_report`
  - points to the development report or implementation report for the task
- `skill_promotions`
  - records what reusable procedural lessons were promoted into skills
- `memory_promotions`
  - records what stable heuristics were promoted into memory
- `doc_promotions`
  - records what reusable artifacts were promoted into docs or shared templates
- `promotion_review`
  - records that `skills/`, `memory/`, and `docs/` were all explicitly checked
  - should include `skills_checked`, `memory_checked`, `docs_checked`, and `decision`
  - is especially important when no promotion list is populated, because it proves the review was done deliberately
- `followup_actions`
  - records what still needs to happen after archiving
  - can be stored as plain strings or structured objects with `action`, `status`, `owner`, and `notes`

If nothing is promoted, that is acceptable.
The important part is that the decision is made explicitly rather than silently skipped.
The default registration script now validates this by requiring either non-empty promotion lists or a populated `promotion_review`.

## Search After Registration

After registration, the entry should be discoverable through:

```powershell
python .\scripts\session_search.py --project hermes-agent
python .\scripts\session_search.py --text workbench
python .\scripts\followup_actions.py
python .\scripts\session_archive_audit.py
```

To inspect unfinished or still-relevant follow-up actions, run:

```powershell
python .\scripts\followup_actions.py
python .\scripts\followup_actions.py --project hermes-agent
python .\scripts\followup_actions.py --text memory
python .\scripts\followup_actions.py --status pending
python .\scripts\followup_actions.py --status needs-confirmation
python .\scripts\followup_actions.py --verbose
python .\scripts\followup_actions.py --write-root-md
python .\scripts\session_archive_audit.py --only-issues
python .\scripts\export_root_overviews.py
```

## Completion Checklist

Before considering a case fully archived, verify:

- `user/` doc exists when needed
- `agent/` doc exists when needed
- session entry exists
- `derived_docs` points at the final doc outputs
- `phase_report` is linked when the task had meaningful implementation phases
- promotion fields are filled if the case changed `skills/`, `memory/`, or shared `docs/`
- `promotion_review` confirms the archive explicitly checked `skills/`, `memory/`, and `docs/`
- `index.json` contains the session
- `session_search.py` can find it
- `session_archive_audit.py` reports the archive as clean

## Scope Boundary

Use the session archive for:

- historical work process
- brief task summaries
- retrieval-friendly links between work and outputs

Do not use it for:

- full analysis writeups
- stable principles
- skill bodies

Those still belong in:

- `.claude/docs/`
- `.claude/memory/`
- `.claude/skills/`

For the detailed boundary between these layers, see:

- `.claude/memory/memory-operating-model.md`
