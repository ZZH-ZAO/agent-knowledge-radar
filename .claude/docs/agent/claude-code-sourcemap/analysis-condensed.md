# Claude Code Sourcemap Condensed Notes

## Project Summary

- Project name: `claude-code-sourcemap`
- Project path: `D:\claude-code-sourcemap`
- Document type: `agent`
- Purpose: compressed notes for future agent reuse and fast architectural recall

## System Type

- serious Agent runtime sample
- best treated as a Claude Code core-architecture study object

## Real Center

- the center is the query loop, not the raw model API
- all major subsystems hang off the loop:
  - prompt/context
  - tool runtime
  - compaction
  - memory
  - multi-agent execution

## Strongest Design Areas

### 1. Runtime Spine

- entrypoint
- session engine
- query loop
- result reinjection
- stop hooks

### 2. Prompt as context supply system

- stable rules vs dynamic sections vs attachments
- cache-aware structure
- debuggable prompt composition

### 3. Tool runtime maturity

- schema
- orchestration
- permissions
- concurrency
- side-effect governance
- MCP integration

### 4. Workflow by time scale

- single turn
- session level
- background tasks
- multi-agent

### 5. Memory and retrieval layering

- rule retrieval
- memory recall
- tool retrieval
- external retrieval
- short/session/persistent memory distinctions

### 6. Multi-agent responsibility design

- main agent
- forked agent
- subagent
- coordinator
- swarm/teammates

## Main Reusable Lessons

- Treat agents as runtimes, not prompts with tools
- The query loop is the real architectural center
- Prompt engineering should be treated as context-system design
- Tool calling should be treated as side-effect governance
- Workflow must be modeled across multiple time scales
- Memory should be layered, not reduced to chat history

## Best Use As A Reference

- runtime-first agent architecture
- coding-agent core design
- architecture review benchmark
