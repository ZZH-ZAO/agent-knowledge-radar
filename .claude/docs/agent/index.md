# Agent Case Library Notes

## Summary

- Project name: Agent research case library
- Project path: `D:\claude-code-sourcemap\.claude\docs`
- Document type: agent
- Purpose: provide compact retrieval notes for selecting the right historical project case when analyzing or designing future Agent systems

## Case Selection Heuristic

### `claude-code-sourcemap`

- Primary label: `runtime-first`
- Core value:
  - study the inner execution engine of a coding agent
- Strong layers:
  - prompt layering
  - query loop
  - tool calling
  - session orchestration
  - memory insertion points
  - multi-agent core routing
- Reuse when:
  - reviewing runtime integrity
  - designing model-tool-state loops
  - judging whether a project has a real agent control plane

### `claude-code`

- Primary label: `platform-expansion`
- Core value:
  - study how a runtime becomes a broader platform and product surface
- Strong layers:
  - feature gating
  - product controls
  - observability
  - persistent agent direction
  - team memory direction
- Reuse when:
  - reviewing platform maturity
  - proposing advanced capability rollout
  - comparing core execution versus system productization

### `career-ops`

- Primary label: `vertical-workflow`
- Core value:
  - study a domain workflow system implemented on top of agent hosts
- Strong layers:
  - domain prompt procedure
  - workflow orchestration
  - output contracts
  - batch worker design
  - human review checkpoints
- Reuse when:
  - analyzing domain-specific agents
  - designing business workflow automation
  - deciding how much to encode in runtime versus procedure

### `fault-diagnosis`

- Primary label: `vertical-workflow`
- Core value:
  - study a data-driven industrial diagnosis agent built around tools, evidence, and report outputs
- Strong layers:
  - SOP-style prompt control
  - business-tool orchestration
  - specialized sub-agent delegation
  - checkpointed session memory
  - report artifact generation
  - practical KB retrieval
- Reuse when:
  - analyzing industrial or maintenance agents
  - designing workflows that must emit charts/reports
  - comparing domain procedure systems against general-purpose runtimes

### `ArcReel`

- Primary label: `platform-expansion`
- Core value:
  - study how an Agent workflow is embedded into a full creative production platform
- Strong layers:
  - SDK runtime wrapping
  - session normalization and reconnect
  - orchestrator-skill workflow control
  - async queue/worker execution
  - multi-provider backend abstraction
  - product surfaces around agent behavior
- Reuse when:
  - analyzing serious Agent products
  - designing platforms with long-running generation jobs
  - comparing runtime-only systems against productized workflow platforms

### `repomind`

- Primary label: `vertical-workflow`
- Core value:
  - study a repository-intelligence product that combines agentic CAG, GitHub evidence tools, and verification-first security flows
- Strong layers:
  - unified repo query pipeline
  - toolized GitHub live snapshots
  - structured process-event streaming
  - multi-layer cache and budget controls
  - scan verification / false-positive control
  - run-state persistence
- Reuse when:
  - analyzing repo-chat or code-intelligence products
  - designing evidence-backed security/code analysis agents
  - comparing classic RAG systems against file-selection CAG systems

### `deer-flow`

- Primary label: `runtime-first`
- Core value:
  - study a super-agent harness that separates reusable runtime foundation from the reference application
- Strong layers:
  - middleware-first runtime composition
  - prompt as runtime-governance layer
  - skills / tools / MCP ecology
  - structured long-term memory
  - formal subagent execution system
  - sandbox abstraction
- Reuse when:
  - analyzing general-purpose agent runtimes
  - designing self-hosted agent platforms
  - comparing runtime substrates against workflow-specific agents

### `hermes-agent`

- Primary label: `long-running-agent`
- Core value:
  - study a memory-first agent workbench that unifies CLI, messaging, scheduling, skills, remote environments, and research/eval hooks
- Strong layers:
  - persistent sessions and search
  - pluggable memory
  - skills as durable assets
  - multi-surface runtime reuse
  - cron automation
  - research-ready trajectory plumbing
- Reuse when:
  - designing long-running personal or team agents
  - comparing chat-first agents against persistent agent workbenches
  - studying systems that want both real usage and training/eval feedback loops

### `cekai-auto-prd-test-agent`

- Primary label: `vertical-workflow`
- Core value:
  - study a testing workflow product built around PRD understanding, retrieval, structured generation, human revision, and AI evaluation
- Strong layers:
  - prompt-based procedure control
  - UI-centric orchestration
  - RAG for generation constraint
  - evaluator / critic path
  - historical case archival
- Reuse when:
  - analyzing testing-agent products
  - comparing workflow apps against formal tool-calling runtimes
  - designing structured artifact generation systems with review loops

### `agentset`

- Primary label: `platform-expansion`
- Core value:
  - study a production-oriented RAG / agent platform
- Strong layers:
  - ingestion / indexing as platform capability
  - eval / benchmark orientation
  - API + hosting + multi-tenancy
- Reuse when:
  - analyzing RAG platforms
  - designing hosted retrieval products

### `ms-agent`

- Primary label: `runtime-first`
- Core value:
  - study a broad Agent framework with strong MCP emphasis and many reference projects
- Strong layers:
  - MCP integration
  - skills and memory
  - context compression
  - framework + reference-app expansion
- Reuse when:
  - analyzing general-purpose agent frameworks
  - comparing MCP-enabled runtimes

### `langgraph-mcp-agents`

- Primary label: `tool-runtime`
- Core value:
  - study a lightweight MCP workbench built with LangGraph and Streamlit
- Strong layers:
  - MCP tool management UX
  - Streamlit workbench
  - rapid demo / learning architecture
- Reuse when:
  - prototyping MCP workbenches
  - teaching LangGraph + MCP integration

### `promptfoo`

- Primary label: `quality-first`
- Core value:
  - study eval, red-team, and benchmark systems for LLM / Agent apps
- Strong layers:
  - CI/CD quality integration
  - red teaming
  - AI testing governance
- Reuse when:
  - designing bad-case and benchmark systems
  - adding evaluation discipline to agent products

### `giskard`

- Primary label: `quality-first`
- Core value:
  - study multi-turn evaluation and RAG testing for agentic systems
- Strong layers:
  - scenario API
  - groundedness / conformity checks
  - RAG eval
- Reuse when:
  - testing multi-turn agents
  - evaluating retrieval-backed systems

### `adk-python`

- Primary label: `runtime-first`
- Core value:
  - study a Google official code-first Agent framework
- Strong layers:
  - tools and MCP/OpenAPI support
  - multi-agent hierarchy
  - eval plus deployment integration
- Reuse when:
  - comparing official Agent frameworks
  - designing code-first runtime substrates

### `sample-agentic-maintenance-assistant`

- Primary label: `vertical-workflow`
- Core value:
  - study a realistic industrial AI maintenance assistant with asset context, ML, RAG, auth, and MCP
- Strong layers:
  - asset-model context
  - industrial workbench
  - ML + RAG + agent combination
  - MCP in a vertical product sample
- Reuse when:
  - analyzing industrial AI products
  - comparing diagnosis and maintenance assistant systems

### `QAagent`

- Primary label: `testing-agent`
- Core value:
  - study research-style multi-agent test generation via intermediate pseudocode
- Strong layers:
  - multi-agent decomposition
  - intermediate reasoning representation
  - coverage-oriented evaluation
- Reuse when:
  - analyzing research prototypes for testing agents
  - designing intermediate representations before final test-case generation

### `awesome-design-md`

- Primary label: `team-knowledge`
- Core value:
  - study how textual design guidance becomes a reusable control layer for AI-generated frontend work
- Strong layers:
  - `DESIGN.md` as repository asset
  - style-case library organization
  - implementation-oriented visual constraints
  - frontend consistency control for coding agents
- Reuse when:
  - improving consistency of Agent-generated UI
  - building internal style-template libraries
  - adding a design-guidance layer without building a full design system

### `fireworks-tech-graph`

- Primary label: `team-knowledge`
- Core value:
  - study how technical-diagram generation can be packaged as a reusable skill with style rules, semantic vocabulary, validation, and regression fixtures
- Strong layers:
  - diagram type taxonomy
  - visual style system
  - semantic shape/arrow encoding
  - SVG validation/export workflow
  - fixture-driven quality control
- Reuse when:
  - adding architecture/flow/UML diagram generation to an Agent workflow
  - standardizing technical-visual outputs across projects
  - building documentation-support skills rather than core runtimes

### `computer-fundamentals`

- Primary label: `team-knowledge`
- Core value:
  - provide a stable local taxonomy for foundational computer science knowledge
- Strong layers:
  - interview-oriented concept organization
  - contrast-based explanation scaffolding
  - reusable routing across data structures, networking, OS, and computer organization
- Reuse when:
  - answering CS fundamentals questions
  - building interview prep notes
  - grounding future book and website ingestion into one stable structure

## Reusable Classification Labels

- `runtime-first`
- `platform-expansion`
- `vertical-workflow`
- `team-knowledge`
- `persistent-agent`
- `memory-first`
- `tool-runtime`
- `RAG-first`

## Required Metadata For New Case Docs

- Project name
- Project path
- Document type
- Purpose
- Primary label
- Strongest layers
- Main design tradeoff
- Recommended reuse scenarios

## Folder Rule

Project-specific condensed notes should be stored under:

- `agent/<project-name>/`

Shared condensed notes should be stored under:

- `agent/shared/`

## Shared Agent Playbooks

### `testing-agent-review-playbook.md`

- Use when:
  - analyzing PRD-to-test-case systems
  - reviewing testing copilots or testing workflow Agents
  - comparing a testing project against retrieval, evidence, evaluation, memory, bad-case, and governance best practices

### `refactoring-review-playbook.md`

- Use when:
  - reviewing legacy code or AI-generated code with a refactoring mindset
  - naming code smells before proposing structural changes
  - converting vague rewrite advice into small behavior-preserving refactoring steps
