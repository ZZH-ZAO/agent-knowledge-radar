# Agent Project Classification Map Notes

## Summary

- Project name: Agent project classification map
- Project path: `D:\claude-code-sourcemap\.claude\docs\agent\shared`
- Document type: agent
- Purpose: provide a compact routing map for classifying new Agent projects before choosing comparison cases and analysis depth

## Core Rule

Do not analyze new Agent projects as a flat list of features.
First classify the project type, then compare it to the right historical case.

## Primary Project Types

### `runtime-first`

- Core question:
  - how does the agent execution engine run?
- Strong signals:
  - query/tool loop
  - session state
  - compaction / context control
  - multi-agent core routing
- Best current reference:
  - `claude-code-sourcemap`

### `platform-expansion`

- Core question:
  - how does a working runtime become a product/platform?
- Strong signals:
  - capability gating
  - observability
  - product control surfaces
  - platformized feature rollout
- Best current references:
  - `claude-code`
  - `arcreel`

### `vertical-workflow`

- Core question:
  - how is a domain workflow encoded as an Agent system?
- Strong signals:
  - SOP-like prompts
  - domain tools
  - review checkpoints
  - structured outputs / reports
- Best current references:
  - `career-ops`
  - `fault-diagnosis`
  - `repomind`

### `tool-runtime`

- Core question:
  - how are tools/skills/MCP/providers organized into a capability layer?
- Strong signals:
  - tool layering
  - skill system
  - MCP / plugin / provider adapters
  - execution environment integration
- Best current references:
  - `deer-flow`
  - `repomind`

### `memory-first`

- Core question:
  - what should be remembered, how, and when injected?
- Strong signals:
  - explicit memory schema
  - extraction/update pipeline
  - long-term personalization or correction memory
- Best current references:
  - `deer-flow`
  - `claude-code-sourcemap`

### `RAG-first` / `evidence-first`

- Core question:
  - where does reliable external evidence come from?
- Strong signals:
  - retrieval layer
  - evidence/citation rules
  - data/knowledge snapshots
  - context construction emphasis
- Best current references:
  - `repomind`
  - `fault-diagnosis`

## Current Case Routing

### `claude-code-sourcemap`

- Primary:
  - `runtime-first`
- Secondary:
  - `memory-first`
  - `tool-runtime`
- Use when:
  - engine / loop / compaction / coordination is the main question

### `claude-code`

- Primary:
  - `platform-expansion`
- Secondary:
  - `persistent-agent`
  - `team-knowledge`
- Use when:
  - platform maturity / governance / capability rollout is the main question

### `career-ops`

- Primary:
  - `vertical-workflow`
- Use when:
  - business workflow encoding is the main question

### `fault-diagnosis`

- Primary:
  - `vertical-workflow`
- Secondary:
  - `evidence-first`
- Use when:
  - industrial workflow + reports + evidence chain is the main question

### `arcreel`

- Primary:
  - `platform-expansion`
- Secondary:
  - `vertical-workflow`
  - `sdk-wrapped-runtime`
- Use when:
  - productized creative workspace/platform is the main question

### `repomind`

- Primary:
  - `vertical-workflow`
- Secondary:
  - `tool-runtime`
  - `evidence-first`
- Use when:
  - repo intelligence / GitHub evidence / verification-first scan flow is the main question

### `deer-flow`

- Primary:
  - `runtime-first`
- Secondary:
  - `tool-runtime`
  - `memory-first`
  - `platform-expansion`
- Use when:
  - harness/runtime substrate / skills+mcp+sandbox+subagents is the main question

## Fast Triage Workflow For New Projects

1. Identify the primary type:
   - engine, harness, platform, vertical workflow, memory-heavy, or evidence-heavy?
2. Identify the strongest layer:
   - prompt, tool runtime, workflow, memory, sandbox, product surface?
3. Pick the closest case:
   - `claude-code-sourcemap`, `deer-flow`, `claude-code`, `career-ops`, `fault-diagnosis`, `arcreel`, or `repomind`
4. State explicitly:
   - what this new project is
   - what it is not
   - which historical case is the best comparison

## Important Anti-Pattern

Do not say:

- "this project has prompts, tools, memory, and workflows"

That is too generic.

Instead say:

- which layer carries the real innovation
- which category the project belongs to
- which case is the right comparison baseline
