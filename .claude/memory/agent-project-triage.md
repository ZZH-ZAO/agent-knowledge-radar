# Agent Project Triage Checklist

## Purpose

Use this checklist before deeply analyzing a new Agent project.

Goal:

- classify the project correctly
- avoid flat feature-dump analysis
- choose the right historical comparison case
- focus on the layer that carries the real innovation

## Step 1: Identify The Primary Type

Ask:

- Is this mainly a `runtime-first` project?
- Is this mainly a `platform-expansion` project?
- Is this mainly a `vertical-workflow` project?
- Is this mainly a `tool-runtime` project?
- Is this mainly a `memory-first` project?
- Is this mainly an `evidence-first` / `RAG-first` project?

Rule:

- pick one primary type first
- add secondary labels only after the main identity is clear

## Step 2: State What The Project Really Is

Write one sentence in this form:

- "This project is best understood as ..."

Also write:

- what it is not

Examples:

- not a general-purpose runtime
- not mainly a product platform
- not mainly a classic vector RAG system

## Step 3: Find The Strongest Layer

Ask which layer carries the real value:

- prompt design
- tool calling
- workflow orchestration
- session/run state
- memory
- sandbox/execution
- subagent coordination
- product surface
- evidence / retrieval layer

Rule:

- do not say "everything matters equally"
- force-rank the top 1-2 layers

## Step 4: Choose The Best Comparison Case

Use this routing:

- `claude-code-sourcemap`
  - when engine / loop / compaction / coordination is the main question
- `deer-flow`
  - when harness / skills / MCP / sandbox / subagent substrate is the main question
- `claude-code`
  - when platform maturity / governance / capability rollout is the main question
- `career-ops`
  - when domain workflow packaging is the main question
- `fault-diagnosis`
  - when industrial evidence workflow / reports / charts is the main question
- `arcreel`
  - when productized workspace / creative platform / sdk-wrapped runtime is the main question
- `repomind`
  - when repo intelligence / GitHub evidence / verification-first security flow is the main question

## Step 5: Ask Why This Design Exists

For each major design choice, ask:

- what problem is this solving?
- why is this better than a simpler alternative?
- what future scenario does this design make easier?
- what new weakness or complexity does this design introduce?

## Step 6: Check For Common Misclassification Errors

Do not confuse:

- runtime-first with platform-expansion
- vertical workflow with general runtime
- tool-rich system with true harness
- memory injection with real memory system
- evidence use with full RAG architecture
- multi-agent mention with real subagent infrastructure

## Step 7: Produce The Final Analysis Shape

The final analysis should clearly answer:

1. what kind of project this is
2. what problem it is actually solving
3. what layer is strongest
4. why it is designed this way
5. what it is good to learn from
6. where it is weak or bounded

## Preferred Output Style

When writing user-facing docs:

- explain, do not just list
- define key terms
- compare against alternatives
- discuss tradeoffs and future scenarios

When writing agent-facing notes:

- compress into classification, strongest layers, reuse scenarios, and warnings

## Anti-Pattern To Avoid

Do not write analysis like:

- "This project has prompts, tools, workflows, memory, and RAG"

That says almost nothing.

Instead write:

- which one is primary
- how it is implemented
- why that layer matters most
- what historical case it should be compared against
