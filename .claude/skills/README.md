# Skill Library Map

## Summary

- Project name: workbench skill library
- Project path: `D:\claude-code-sourcemap\.claude\skills`
- Document type: internal skill index
- Purpose: give a stable entry point for choosing the right skill, understanding scope boundaries, and knowing how skills relate to docs, memory, and sessions

## How To Use This Folder

This folder is the method layer of the workbench.

Use `skills/` for:

- reusable work procedures
- task selection guidance
- default execution patterns
- capability-specific playbooks

Do not use `skills/` for:

- case-specific conclusions
- stable cross-case heuristics
- session history
- polished long-form case studies

Those belong in:

- `docs/`
- `memory/`
- `sessions/`

## Core Execution Skill

### `autonomous-delivery-default`

Use when:

- the user wants continuous execution
- the task should keep moving with minimal back-and-forth
- each meaningful phase should leave behind a report entry

Best paired with:

- `../memory/autonomous-execution-preference.md`
- `../docs/user/shared/development-phase-report-template.md`

## Core Agent Research Skills

### `agent-research-workbench`

Use when:

- the task spans review, design, and roadmap
- multiple Agent projects are being compared
- case-study findings need to be turned into reusable guidance

Routes into:

- `agent-architecture-review`
- `agent-platform-design`
- `agent-feature-roadmap`

### `agent-architecture-review`

Use when:

- the main question is what a current Agent system really is
- the runtime spine must be identified from source code
- architecture maturity and tradeoffs need to be judged

Typical companion materials:

- `../docs/user/shared/super-agent-harness-design-template.md`
- `../docs/user/shared/sdk-wrapped-agent-runtime-template.md`

### `agent-platform-design`

Use when:

- the task is how to design a new Agent platform or runtime
- the main need is architecture advice rather than current-state review
- runtime, tools, memory, and workflow need to be designed together

Typical companion materials:

- `../docs/user/shared/productized-agent-platform-template.md`
- `../docs/user/shared/super-agent-harness-design-template.md`

### `agent-feature-roadmap`

Use when:

- the question is what to build next
- the project already exists and needs sequencing
- priorities should be bottleneck-driven rather than wishlist-driven

Typical companion materials:

- `../docs/user/shared/agent-project-classification-map.md`

## Secondary Skills

### `refactoring-guided-review`

Use when:

- the user wants review or refactoring guided by explicit refactoring principles
- the task is code-smell identification plus small-step cleanup
- the work is local code quality, not Agent system architecture

Typical companion materials:

- `../docs/agent/shared/refactoring-review-playbook.md`
- `../docs/user/shared/refactoring-smell-to-action-cheatsheet.md`

## Selection Heuristic

Use this order when choosing:

1. If the user asked for continuous execution style, activate `autonomous-delivery-default`.
2. If the task spans multiple Agent research modes, start with `agent-research-workbench`.
3. If the task is about understanding an existing system, use `agent-architecture-review`.
4. If the task is about designing a system, use `agent-platform-design`.
5. If the task is about priorities and sequencing, use `agent-feature-roadmap`.
6. If the task is about code cleanup or smell-based review, use `refactoring-guided-review`.

## Skill Update Rule

When a new case finishes, ask:

1. Did it change how a class of work should be done?
2. Is the lesson procedural rather than only descriptive?
3. Does it belong in a skill instead of only in docs or memory?

If yes:

- record the observation in `sessions/` first
- promote stable procedural lessons into the relevant skill
- update this index if the skill inventory or routing guidance changed
