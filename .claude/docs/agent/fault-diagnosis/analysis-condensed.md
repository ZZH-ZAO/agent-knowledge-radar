# fault-diagnosis Analysis Notes

## Summary

- Project name: fault-diagnosis
- Project path: `D:\fault-diagnosis`
- Document type: agent
- Purpose: provide condensed reusable notes for analyzing future industrial or vertical Agent systems against this project

## Classification

- Primary label: `vertical-workflow`
- Secondary label: `tool-runtime`
- Secondary label: `RAG-assisted`

## Core Identity

Industrial fault-diagnosis Agent system built as a vertical workflow service, not a general-purpose Agent runtime.

Main value:

- encode industrial diagnosis SOP into prompt + tools + report outputs
- combine data query, model inference, knowledge retrieval, visualization, and report generation
- provide transparent execution via SSE and todo/task state

## Strongest Layers

### Prompt / procedure layer

- system prompt acts as workflow policy
- includes tool routing, constraints, answer format, uncertainty rules
- dynamic prompt adapts by user identity

### Tool layer

- tools directly map to business actions:
  - SQL query
  - dataframe extraction
  - chart generation
  - KB query
  - web search
  - markdown/html report output
  - sub-agent diagnosis

### Workflow layer

- workflow-first design
- typical path:
  - get time
  - write todos
  - run diagnosis sub-agent
  - enrich with KB or search
  - save report

### Session memory layer

- PostgreSQL checkpoint persistence
- summarization middleware
- todo state exposure
- history retrieval APIs

## Important Implementation Signals

- `app.py`
  - FastAPI app
  - creates main agent
  - wires checkpointer with Postgres fallback to memory
- `middleware.py`
  - `TodoListMiddleware`
  - identity-aware dynamic prompt
  - `SummarizationMiddleware`
- `streaming.py`
  - SSE event protocol:
    - `chat_start`
    - `token`
    - `tool_start`
    - `tool_end`
    - `chat_complete`
    - `server_error`
- `knowledge_base.py`
  - PDF -> chunks -> Ollama embeddings -> FAISS
- `tools/subagent/`
  - specialized fault diagnosis sub-agent around external ML API + chart generation

## Multi-Layer Orchestration

### Single-turn loop

- model -> tool use -> tool result -> continue reasoning

### Session-level orchestration

- checkpoint persistence
- summarization for context control
- history recovery

### Task-level orchestration

- todo middleware + workflow prompt
- task status is visible to frontend

### Multi-agent orchestration

- coordinator pattern is minimal and domain-specific
- main agent delegates specialized diagnosis to one sub-agent
- not a generic swarm system

## RAG Notes

RAG goal is narrow and practical:

- retrieve fault-code meaning
- retrieve manual/process knowledge
- supplement diagnosis, not replace runtime data analysis

Current maturity:

- basic FAISS retriever
- no rerank
- no layered indexes
- no explicit evidence synthesis stage

## Memory Notes

Memory here is mostly session memory, not learning memory.

Present:

- checkpoint memory
- summarized context memory
- todo/task progress memory

Missing:

- durable case memory
- extracted lessons from historical diagnosis reports
- memory feedback loop into future diagnosis

## Reusable Lessons

### What to copy

- use prompt as SOP, not persona decoration
- make tools match real business workflow stages
- expose execution transparency with stream events and task state
- output artifacts, not just chat text

### What to watch

- `globals()` state sharing between tools is fragile
- heavy dependency chain increases operational risk
- prompt-heavy control becomes harder to maintain as workflows diversify
- RAG quality may degrade as corpus size grows

## Best Reuse Scenarios

- industrial agent systems
- diagnostics / inspection / maintenance workflows
- business workflows that must produce reports or auditable artifacts
- vertical agent systems where trust comes from process transparency

## Compare Against This Case When Asking

- how to build a data-driven vertical agent workflow
- how to combine runtime data + KB + external model inference
- how to make an agent produce charts and reports as deliverables
- how to use session memory and SSE transparency in a domain system
