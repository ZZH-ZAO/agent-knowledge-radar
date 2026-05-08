# Memory Operating Model

## Summary

- Project name: current workbench memory operating model
- Project path: `D:\claude-code-sourcemap\.claude\memory`
- Document type: memory
- Purpose: define how the workbench should separate stable memory, session history, and formal documentation so knowledge does not collapse into one layer

## Why This Exists

As the workbench accumulates more case studies, it now has four different places where information can live:

- `.claude/skills/`
- `.claude/memory/`
- `.claude/sessions/`
- `.claude/docs/`

Without a clear operating model, information tends to drift into the wrong layer:

- temporary observations get written into stable memory
- formal conclusions are left only in session records
- reusable methods get buried in docs instead of skills

This file defines the intended boundary.

## The Four Knowledge Layers

### 1. `skills/`

Use for:

- how to do a class of tasks
- reusable work procedures
- step-by-step methods
- stable execution playbooks

Examples:

- architecture review workflow
- roadmap design workflow
- comparison workflow

Rule:

- if the knowledge is mainly procedural, it probably belongs in `skills/`

### 2. `memory/`

Use for:

- stable design principles
- durable evaluation heuristics
- project-selection and triage rules
- judgments that should remain true across many tasks

Examples:

- Agent should be understood as a runtime system, not just prompt + tools
- MCP should be introduced for capability-boundary reasons, not novelty
- memory is governed layered knowledge, not chat history

Rule:

- if the knowledge should still be true months later across many future cases, it probably belongs in `memory/`

### 3. `sessions/`

Use for:

- historical work process
- temporary but important intermediate judgments
- what was learned during a specific task
- mappings between a task and the formal docs it produced

Examples:

- “During the Hermes analysis, the most transferable idea was session search”
- “This case was compared mainly against deer-flow and claude-code”
- “These four docs were derived from this analysis session”

Rule:

- if the knowledge is tied to one concrete task or investigation, it probably belongs in `sessions/`

### 4. `docs/`

Use for:

- formalized case studies
- reusable long-form explanations
- final user-facing or agent-facing research assets
- templates and cross-project syntheses

Examples:

- case analysis docs
- comparison docs
- shared templates
- condensed retrieval notes

Rule:

- if the knowledge is polished enough to be intentionally reused as a durable reference artifact, it probably belongs in `docs/`

## Stable Memory vs Session Memory

This is the most important distinction in the current upgrade.

### Stable memory

Stable memory is for:

- enduring principles
- repeated heuristics
- cross-case judgments
- rules that should influence many future tasks

Good examples:

- “Tool calling is a side-effect governance problem”
- “Prefer explicit state boundaries over hidden implicit behavior”
- “Introduce MCP only when scale and heterogeneity justify it”

Bad examples:

- “The Hermes project seems more interesting than I expected”
- “This specific comparison felt weak in section 4”
- “I might later want to compare this to ArcReel”

Those are not stable memory. They are session-level observations.

### Session memory

Session memory is for:

- what mattered in one concrete task
- what was newly discovered but not yet proven stable
- what should remain searchable later even if it never becomes a formal doc

Good examples:

- “Hermes is best classified as long-running-agent + memory-first”
- “The strongest source files were run_agent.py, hermes_state.py, and mcp_tool.py”
- “This task produced one analysis doc and two comparison/borrowing docs”

## Docs vs Sessions

Another common failure mode is confusing final docs with archive entries.

### A session entry should be

- short
- structured
- retrieval-friendly
- linked to the real outputs

### A formal doc should be

- complete enough to read on its own
- explanatory, not just index-like
- intended for durable reuse

In practice:

- `sessions/` says what happened
- `docs/` explains what it means

## Promotion Rules

Use these promotion rules when deciding where a piece of knowledge should go.

### Promote from `sessions/` to `docs/` when

- the result is useful beyond the original task
- the explanation needs full narrative detail
- the content should be intentionally reusable by future readers or agents

### Promote from `sessions/` to `memory/` when

- the observation has become a stable rule
- it applies across multiple projects
- it should influence future judgment by default

### Promote from `docs/` to `skills/` when

- the key reusable value is procedural
- the lesson is really “how to do this class of work”
- future tasks would benefit from following the method directly

## Decision Checklist

When new information appears, ask:

1. Is this mainly a method?
   If yes, prefer `skills/`.
2. Is this mainly a stable principle or heuristic?
   If yes, prefer `memory/`.
3. Is this mainly tied to one concrete task or investigation?
   If yes, prefer `sessions/`.
4. Is this a polished reusable artifact?
   If yes, prefer `docs/`.

If the answer is “somewhere between”:

- start in `sessions/`
- promote later only after the value becomes clearer

That default is important because it keeps stable memory clean.

## Anti-Patterns

Avoid these patterns:

- writing temporary observations directly into `.claude/memory/`
- leaving durable conclusions only inside session records
- hiding reusable methods inside long case-study prose
- using `docs/` as a dumping ground for unstructured notes

## Recommended Default Flow

For a normal case-study task, the preferred flow is:

1. Do the work
2. Write the formal case docs in `.claude/docs/`
3. Write one concise session record in `.claude/sessions/entries/`
4. Register it into `.claude/sessions/index.json`
5. Only if a new judgment is truly stable, update `.claude/memory/`
6. Only if a new method is clearly reusable, update `.claude/skills/`

## One-Sentence Rule

If uncertain, use this default:

> New information should enter `sessions/` first, and only later be promoted into `memory/`, `docs/`, or `skills/` once its long-term role is clear.
