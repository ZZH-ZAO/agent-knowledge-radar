# DeerFlow Analysis Notes

## Summary

- Project name: DeerFlow
- Project path: `D:\deer-flow`
- Document type: agent
- Purpose: provide condensed reusable notes for analyzing future super-agent runtime or harness projects against DeerFlow

## Classification

- Primary label: `runtime-first`
- Secondary label: `platform-expansion`
- Secondary label: `tool-runtime`
- Secondary label: `memory-first`

## Core Identity

DeerFlow is a super-agent harness plus reference app.

Important distinction:

- Harness = reusable runtime / Python SDK / agent foundation
- App = best-practice product implementation built on top

Not a narrow vertical workflow system.
Best understood as a configurable agent operating substrate.

## Strongest Layers

### Runtime composition

- `agents/lead_agent/agent.py`
- `make_lead_agent` resolves model, runtime flags, tools, middleware, prompt, state schema
- runtime behavior is driven by config + middleware, not only by prompt

### Middleware-first architecture

- summarization
- todo / plan mode
- token usage
- title generation
- memory
- view image
- deferred tool filter
- subagent limit
- loop detection
- clarification

Reusable lesson:

- treat many agent behaviors as composable middleware hooks instead of stuffing everything into one loop

### Prompt as runtime governance

- `agents/lead_agent/prompt.py`
- prompt responsibilities:
  - clarification-first policy
  - skills progressive-loading contract
  - subagent orchestration policy
  - citation discipline
  - working-directory semantics
  - memory injection
- prompt is less about persona, more about operating rules

### Skills / tools / MCP ecology

- `skills/loader.py`
- `mcp/`
- `tools/`
- three-layer capability model:
  - built-in tools = primitive actions
  - skills = workflow knowledge modules
  - MCP = external capability integration

### Subagent execution system

- `subagents/executor.py`
- `tools/builtins/task_tool.py`
- background execution, timeout, cancellation, polling, trace propagation, tool filtering
- subagents are treated as managed execution units, not simple recursive prompts

### Sandbox abstraction

- `sandbox/`
- `community/aio_sandbox/`
- provider abstraction across local vs isolated/container execution
- fixed virtual path semantics for uploads/workspace/outputs/skills

### Memory system

- `agents/memory/prompt.py`
- `agents/memory/updater.py`
- `agents/memory/queue.py`
- structured long-term memory:
  - user context
  - history
  - facts
- async debounce queue for updates
- correction/reinforcement-aware memory extraction

## Workflow Layers

### Single-turn loop

- model + tools + state update

### Middleware workflow

- request passes through runtime middleware stack before/around agent execution

### Subagent workflow

- lead agent delegates via `task`
- background executor handles status / timeout / cancellation / result collection

### Run management workflow

- `runtime/runs/manager.py`
- run registry, inflight conflict handling, interrupt/rollback strategies, abort events

### Product workflow

- Gateway handles skills, MCP, uploads, artifacts, thread cleanup
- App provides workspace UI on top of runtime

## Memory Notes

Memory is not just prompt history.

Key layers:

- injected memory context in system prompt
- long-term stored memory summaries + facts
- async update queue with debounce
- correction-aware memory facts

Strong lesson:

- memory should capture user profile and stable operating knowledge, not transient session artifacts

## Reusable Lessons

### What to copy

- separate harness from app
- make runtime capabilities middleware-based
- treat skills as progressive-loaded workflow modules
- support MCP as a configuration-driven integration layer
- build formal subagent execution infrastructure
- give sandbox paths stable semantics
- make memory structured and asynchronous

### What to watch

- high complexity and onboarding cost
- prompt policy becomes large and maintenance-heavy
- deep LangGraph/LangChain coupling
- better as a runtime reference than as a domain workflow reference

## Best Reuse Scenarios

- building a general-purpose agent harness
- building a self-hosted agent platform
- designing skill/mcp/sandbox ecosystems
- designing middleware-heavy agent runtimes
- comparing runtime substrate projects against workflow-specific agent systems
