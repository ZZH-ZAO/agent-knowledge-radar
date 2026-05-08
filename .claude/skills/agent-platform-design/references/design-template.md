# Design Template

Use this template for proposing a new Agent platform design.

## 1. Product Target

- primary use case
- single-user or team
- request-driven or long-running
- local, remote, or hybrid

## 2. Runtime Spine

- entrypoint
- session engine
- query loop
- tool execution and reinjection
- stop hooks and persistence

## 3. Prompt and Context

- stable rules
- dynamic runtime sections
- attachments / temporary reminders
- cache strategy

## 4. Tool Runtime

- tool schemas
- permissions
- concurrency model
- side-effect governance
- result protocol

## 5. Workflow Layers

- single-turn
- session-level
- background tasks
- multi-agent

## 6. Retrieval and Memory

- retrieval categories
- short-term memory
- session memory
- persistent memory
- consolidation strategy

## 7. Platform Concerns

- feature flags
- telemetry
- cache/cost
- rollout
- security

## 8. Phased Build Plan

- what to build now
- what to defer
- what signals justify the next step
