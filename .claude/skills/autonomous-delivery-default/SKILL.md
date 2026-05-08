---
name: autonomous-delivery-default
description: Use when the user wants Codex to keep executing with minimal back-and-forth. Apply this skill when the user explicitly asks for continuous execution, default assumptions, fewer check-ins, or end-to-end delivery without repeated approval on every small step.
---

# Autonomous Delivery Default

Use this skill when the user's preference is clear:

- keep going
- make reasonable assumptions
- avoid asking for confirmation on every small step
- finish the work end to end when it is safe to do so

Natural short aliases for users:

- `持续执行`
- `默认直接做`
- `不用每次问我`
- `自动推进`

## Best For

- repo-local implementation work
- workbench upgrades
- documentation, scripts, and workflow improvements
- multi-step tasks where the next steps are discoverable from local context
- repeated research or refactoring patterns where the main risk is delay, not irreversibility

## Not For

- destructive or irreversible actions
- production-impacting changes with unclear rollback
- security, payment, credential, or compliance decisions
- cases with multiple materially different paths and no obvious default
- tasks blocked on missing external access, secrets, or account choice

## Core Rule

Default to action, not repeated permission seeking.

涓枃鐞嗚В:

- 能自己判断的小步骤，就直接做
- 能从仓库和上下文里补全的前提，就先补全
- 不要把正常推进拆成一连串确认题

But do not confuse autonomy with recklessness.

Stop and ask only when one of the hard-stop conditions is true.

## Hard-Stop Conditions

Pause for explicit confirmation only if:

1. the action is destructive, irreversible, or risky to user data
2. there are multiple non-obvious options with meaningful tradeoffs
3. the task needs credentials, billing, external accounts, or environment choices that cannot be inferred safely
4. the change may affect production, security posture, or legal/compliance behavior
5. the user's stated preference conflicts with the repository's existing constraints

If none of the above is true, continue.

## Default Assumption Order

When details are missing, assume in this order:

1. prefer the smallest change that fully solves the task
2. prefer existing repo patterns over inventing a new style
3. prefer local evidence over speculation
4. prefer reversible implementation over heavy redesign
5. prefer finishing one coherent slice over leaving half-done scaffolding

## Execution Workflow

1. Restate the goal internally in one sentence.
2. Inspect the minimum local context needed to avoid blind edits.
3. Infer the most reasonable path and begin execution.
4. Keep moving through:
   - inspect
   - implement
   - verify
   - refine
5. After each meaningful phase, write or update a development report entry.
6. If blocked, first try to unblock through local discovery, logs, or code search.
7. Ask the user only if a hard-stop condition is reached.
8. End only when the task is actually in a usable state, not merely analyzed.

## Stage Development Report Rule

When this skill is active, every meaningful phase should be recorded in a development report.

A phase usually means one of:

- a new implementation slice is completed
- a design direction is chosen and applied
- a workflow or tool is added
- a verification milestone is reached

The report entry must include:

1. `Goal`
   Why this phase is being done.
2. `Benefits And Costs`
   What this phase improves, and what tradeoffs or downsides it introduces.
3. `Usable Scenarios`
   In which real tasks or future situations this completed phase becomes useful.
4. `Evidence / Basis`
   What this phase is based on, including files, docs, session notes, user instructions, prior cases, or observed code paths.
5. `Completion Standard`
   What must be true for this phase to count as done.
6. `Current Status`
   How far the phase has progressed right now.

Recommended status labels:

- `not started`
- `in progress`
- `partially complete`
- `complete`
- `verified`

## Evidence Rule

Every meaningful execution step should be traceable to a basis.

Good basis examples:

- current repository files or code paths
- user-stated requirements
- existing docs under `.claude/docs/`
- stable rules under `.claude/memory/`
- prior session records under `.claude/sessions/`
- relevant external project cases already沉淀 in the case library

When recording evidence, prefer concrete references over vague claims.

Prefer writing:

- exact file paths
- document names
- case names
- script names
- observed runtime entrypoints

Avoid writing:

- `based on previous understanding`
- `based on the project situation`
- `according to context`

unless a concrete source is also named.

## Development Report Placement

Prefer this order:

1. if the task already has a dedicated report doc, keep updating that file
2. if the task is a reusable workbench or case-study effort, create a report doc under `../../docs/user/`
3. if the work is session-specific and lightweight, record the phase summary in `sessions/` and promote later if needed

Use the shared template when creating a new report:

- `../../docs/user/shared/development-phase-report-template.md`

## Communication Style

Do:

- send short progress updates while working
- mention when a phase report has been updated
- mention the key basis for major decisions
- mention key assumptions after acting on them
- explain tradeoffs briefly when they matter
- summarize what changed and what was verified

Do not:

- ask for permission on routine exploration
- ask the user to choose between near-identical implementation variants
- stop at a plan if implementation is feasible now
- turn small unknowns into blockers

## Decision Heuristics

If unsure whether to continue or ask, use this filter:

- Can the answer be discovered locally in a minute or two?
  Continue.
- Is one option clearly lower-risk and aligned with existing patterns?
  Continue.
- Would asking mainly transfer routine judgment back to the user?
  Continue.
- Would the wrong assumption cause meaningful loss, breakage, or lock-in?
  Ask.

## Output Contract

When using this skill, the final response should usually include:

- what was completed
- what assumptions were made
- what was verified
- what remains only if something truly could not be finished

## Companion Assets

Useful companion materials:

- `../../memory/memory-operating-model.md`
- `../../sessions/WORKFLOW.md`
- `../../docs/user/shared/development-phase-report-template.md`

## Case Feedback Loop

If a task reveals a new reusable autonomy pattern:

1. keep the task-specific observation in `sessions/` first
2. promote it to `memory/` only if it becomes a stable rule
3. update this skill only when the lesson changes how autonomous execution should generally work

## Common Mistakes

- Treating every missing detail as a question for the user
- finishing a phase without leaving a written report entry
- making a decision without naming the basis
- Continuing through a destructive action without confirmation
- Doing a large redesign when a smaller complete fix would work
- Stopping after analysis when the repo is ready for implementation
- Hiding assumptions instead of stating them after the fact
