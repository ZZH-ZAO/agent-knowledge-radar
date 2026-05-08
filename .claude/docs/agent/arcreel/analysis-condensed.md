# ArcReel Analysis Notes

## Summary

- Project name: ArcReel
- Project path: `D:\ArcReel`
- Document type: agent
- Purpose: provide condensed reusable notes for analyzing future productized Agent platforms against ArcReel

## Classification

- Primary label: `platform-expansion`
- Secondary label: `vertical-workflow`
- Secondary label: `tool-runtime`

## Core Identity

AI video creation workbench that combines:

- Claude Agent SDK application runtime
- workflow-oriented multi-agent orchestration
- multi-provider media backend platform
- async generation queue and worker system
- productized web workspace

Not a pure runtime-first sample.
Not a simple vertical workflow only.
Best understood as a productized Agent platform for creative production.

## Strongest Layers

### Agent runtime productization

- `server/agent_runtime/` wraps raw SDK behavior
- session lifecycle
- snapshot / reconnect
- turn normalization
- stream projection
- pending user questions
- session interruption and stale session handling

### Workflow orchestration

- README + openspec show orchestrator skill + focused subagent pattern
- project-state detection drives dispatch
- supports resume from arbitrary stage
- confirmation protocol between stages

### Platform backend abstraction

- `lib/image_backends/`, `lib/video_backends/`, `lib/text_backends/`
- provider protocols + registries
- custom provider support
- project/global provider switching

### Async task system

- `GenerationQueue`
- `GenerationWorker`
- lease-based worker ownership
- image/video split lanes
- provider-level pools
- cancel / recover / requeue behavior

### Product system layer

- auth
- config
- usage tracking
- cost estimation
- version history
- archive/export
- project events

## Important Implementation Signals

- `server/app.py`
  - FastAPI shell
  - startup orchestration
  - worker + event service startup
- `server/routers/assistant.py`
  - assistant session API surface
- `server/agent_runtime/service.py`
  - application-level assistant service
- `server/agent_runtime/session_manager.py`
  - SDK session orchestration and permission boundaries
- `server/agent_runtime/stream_projector.py`
  - event -> snapshot/patch/delta projection
- `lib/generation_queue.py`
  - persistent task queue wrapper
- `lib/generation_worker.py`
  - provider-aware background execution

## Workflow Layers

### Single-turn loop

- Claude SDK internal query/tool loop

### Session-level orchestration

- session manager
- transcript adapter
- projector
- reconnect / interrupt

### Project-level orchestration

- workflow stage inferred from `project.json` + filesystem
- not just from chat history

### Background task orchestration

- generation queue + worker
- decouples agent intent from long-running media generation

### Multi-agent orchestration

- orchestrator skill + focused subagents
- minimize context passed to subagents
- stage-confirmation protocol

## Memory Notes

Memory is distributed across three layers:

- session memory
  - assistant transcript + normalized turns
- project memory
  - `project.json`, assets, versions, file state
- platform memory
  - DB-backed tasks, usage, sessions, credentials, providers

This is a key reusable lesson:

- for productized agents, memory is not only “what the model remembers”
- it is the full persistent system state model

## RAG Notes

RAG is not a primary architectural pillar here.

Context mostly comes from:

- project state
- skill instructions
- runtime prompt injection
- SDK environment

Useful comparison point versus projects where vector retrieval is central.

## Reusable Lessons

### What to copy

- build an application runtime layer above the vendor SDK
- keep workflow state in project state, not only chat state
- use provider protocols to isolate business logic from model vendors
- move long-running generation into queue/worker infrastructure
- treat agent UI as one part of a broader product surface

### What to watch

- system complexity is high
- SDK coupling is meaningful
- multi-provider support creates capability mismatch pressure
- knowledge accumulation / RAG is weaker than workflow/platform depth

## Best Reuse Scenarios

- productized coding/creative agent platforms
- heavy async-generation systems
- multi-provider AI workbenches
- projects needing session reconnect + normalized streaming UI
- projects combining agent orchestration with structured app workflows
