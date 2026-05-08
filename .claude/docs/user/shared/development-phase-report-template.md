# Development Phase Report Template

## Summary

- Document type: shared template
- Purpose: record each meaningful development phase in a way that is reusable, reviewable, and easy to continue later

## When To Use

Use this template when a task spans multiple phases and each phase should leave behind a clear progress record.

Typical use cases:

- workbench upgrades
- multi-step implementation work
- long-running refactors
- research-to-build transitions
- toolchain or workflow construction

## Phase Entry Template

Copy this block for each phase:

```md
## Phase: <phase name>

### Goal

Why this phase exists and what problem it is trying to solve.

### Benefits And Costs

Benefits:

- <benefit 1>
- <benefit 2>

Costs / Tradeoffs:

- <cost or downside 1>
- <cost or downside 2>

### Usable Scenarios

- <scenario 1>
- <scenario 2>
- <scenario 3>

### Evidence / Basis

- <user requirement or instruction>
- <file / doc / script / code path reference>
- <case study / memory / session reference>

### Completion Standard

- <condition 1>
- <condition 2>
- <condition 3>

### Current Status

- Status: `<not started | in progress | partially complete | complete | verified>`
- Progress: <what is already done>
- Remaining: <what is still left>
```

## Writing Rule

Do not wait until the whole project is over.

Update the report at the end of each meaningful phase so future work can resume from a real checkpoint rather than memory.
