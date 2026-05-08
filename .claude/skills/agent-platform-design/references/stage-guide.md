# Stage Guide

Use this when deciding how much architecture is justified.

## Stage 1: Core Runtime

Build:

- one strong query loop
- prompt structure
- tool permissions
- basic session handling

Avoid:

- heavy multi-agent
- heavy remote systems
- heavy RAG infrastructure

## Stage 2: Long-Session Reliability

Add:

- compaction
- memory writing/recall
- retrieval categories
- better observability

## Stage 3: Platform Expansion

Add:

- multi-agent coordination
- background jobs
- feature gates
- team memory
- remote control

## Rule of Thumb

If the system still fails basic tasks, stay at Stage 1.
If it succeeds but becomes unstable over time, move into Stage 2.
If the core is stable and product scope is widening, move into Stage 3.
