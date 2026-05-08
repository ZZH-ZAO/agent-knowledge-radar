# Agent Case Library Index

## Summary

- Project name: Agent research case library
- Project path: `D:\claude-code-sourcemap\.claude\docs`
- Document type: shared index
- Purpose: provide a stable entry point for all accumulated Agent project analyses, comparisons, and reusable design lessons

## What This Folder Is

This folder is the long-term case library for Agent and LLM engineering research.

It has two audiences:

- `user/`: detailed, lecture-style documents for learning and review
- `agent/`: compressed, reusable notes for future agent analysis and design work

Every case study should start with a summary block that clearly states:

- Project name
- Project path
- Document type
- Purpose

## How To Use This Case Library

When a new project needs analysis, the recommended workflow is:

1. Analyze the project as a system, not just as a feature list.
2. Identify what layer it is strongest in: runtime, platform, workflow, memory, RAG, or multi-agent coordination.
3. Extract reusable lessons rather than only describing implementation details.
4. Persist both outputs:
   - a user-facing deep explanation in `user/`
   - an agent-facing condensed reference in `agent/`

## Case Map

### `claude-code-sourcemap`

- Classification: runtime-first Agent core study
- Best for learning:
  - query loop
  - prompt system layering
  - tool calling runtime
  - workflow orchestration
  - memory placement
  - multi-agent core coordination
- When to use as a reference:
  - when reviewing a serious coding agent runtime
  - when designing the internal control loop of an agent
  - when evaluating whether a project is more than a thin wrapper around an API

User doc:
- `user/claude-code-sourcemap/analysis.md`
- `user/claude-code-sourcemap/workbench-development-report.md`

Agent doc:
- `agent/claude-code-sourcemap/analysis-condensed.md`

Supporting assets:
- `.claude/skills/README.md`
- `.claude/sessions/WORKFLOW.md`
- `.claude/memory/memory-operating-model.md`

### `claude-code`

- Classification: platform-expansion and productization study
- Best for learning:
  - capability gating
  - feature flags
  - observability
  - persistent and proactive agent directions
  - team memory and remote control ideas
- When to use as a reference:
  - when a runtime is already working and the next step is becoming a platform
  - when deciding how to expose advanced features without collapsing usability
  - when comparing core runtime versus product system design

User doc:
- `user/claude-code/analysis.md`

Agent doc:
- `agent/claude-code/analysis-condensed.md`

### `career-ops`

- Classification: vertical workflow system built on agent hosts
- Best for learning:
  - domain operating procedure encoded in prompts
  - workflow-first orchestration
  - structured output contracts
  - multi-worker batch task design
  - pragmatic human-in-the-loop delivery
- When to use as a reference:
  - when analyzing a domain agent rather than a general-purpose runtime
  - when designing agent workflows for a business process
  - when deciding how much autonomy should live in runtime versus prompt procedure

User doc:
- `user/career-ops/analysis.md`

Agent doc:
- `agent/career-ops/analysis-condensed.md`

### `fault-diagnosis`

- Classification: vertical workflow system for industrial diagnosis
- Best for learning:
  - prompt as industrial SOP
  - tool-driven diagnosis workflow
  - sub-agent for specialized analysis
  - session memory with checkpoints and summaries
  - report generation as final artifact
  - RAG as supporting evidence, not primary engine
- When to use as a reference:
  - when designing industrial or operations-focused agents
  - when combining business data, model inference, and knowledge retrieval
  - when the target system must produce auditable reports rather than only chat answers

User doc:
- `user/fault-diagnosis/analysis.md`

Agent doc:
- `agent/fault-diagnosis/analysis-condensed.md`

Supporting docs:
- `user/fault-diagnosis/vs-career-ops-comparison.md`
- `user/shared/industrial-agent-design-template.md`
- `user/fault-diagnosis/industrial-agent-roadmap.md`
- `user/fault-diagnosis/technical-upgrade-plan.md`

### `ArcReel`

- Classification: productized creative Agent platform
- Best for learning:
  - application runtime on top of Claude Agent SDK
  - workflow orchestration via skill + focused subagents
  - project-state-driven continuation and resume
  - multi-provider media backend abstraction
  - async generation queue and worker system
  - Agent as one layer inside a full product workbench
- When to use as a reference:
  - when building a serious Agent product rather than a chat demo
  - when combining agent orchestration with long-running generation jobs
  - when designing a multi-provider AI platform with product surfaces

User doc:
- `user/arcreel/analysis.md`
- `user/arcreel/vs-claude-code-vs-fault-diagnosis.md`
- `user/shared/productized-agent-platform-template.md`

Agent doc:
- `agent/arcreel/analysis-condensed.md`

Supporting docs:
- `user/arcreel/vs-claude-code-vs-fault-diagnosis.md`
- `user/shared/productized-agent-platform-template.md`
- `user/arcreel/platform-roadmap.md`
- `user/shared/sdk-wrapped-agent-runtime-template.md`

### `repomind`

- Classification: repository-intelligence and verification-first security Agent product
- Best for learning:
  - agentic CAG for codebase understanding
  - GitHub live evidence tool layer
  - structured streaming event protocol
  - run-state persistence for long answers
  - cache/budget/isolation design in an Agent product
  - verification-first security scanning and reporting workflow
- When to use as a reference:
  - when building a repo chat or code intelligence product
  - when deciding between vector RAG and file-selection-based context assembly
  - when adding security scanning, false-positive control, and result lifecycle management to an Agent system

User doc:
- `user/repomind/analysis.md`

Agent doc:
- `agent/repomind/analysis-condensed.md`

### `deer-flow`

- Classification: super-agent harness and reference-app runtime platform
- Best for learning:
  - harness vs app layering
  - middleware-first runtime architecture
  - prompt as runtime governance
  - skills and MCP as extensibility layers
  - structured long-term memory
  - formal subagent execution
  - sandbox abstraction
- When to use as a reference:
  - when building a general-purpose Agent runtime rather than a single vertical workflow
  - when designing a self-hosted Agent platform
  - when studying how runtime foundations become reference applications

User doc:
- `user/deer-flow/analysis.md`
- `user/deer-flow/vs-claude-code-sourcemap.md`
- `user/deer-flow/vs-claude-code-sourcemap-vs-claude-code.md`

Agent doc:
- `agent/deer-flow/analysis-condensed.md`

### `hermes-agent`

- Classification: long-running and memory-first general-purpose Agent workbench
- Best for learning:
  - long-lived agent design
  - session persistence and FTS search
  - skills as reusable procedural assets
  - CLI + gateway + TUI + editor multi-surface architecture
  - cron-driven automation
  - research/runtime unification
- When to use as a reference:
  - when designing an agent that should persist across sessions and interfaces
  - when combining personal assistant behavior with tool/runtime extensibility
  - when exploring how product use and RL/eval data generation can share one system

User doc:
- `user/hermes-agent/analysis.md`
- `user/hermes-agent/vs-deer-flow-vs-claude-code.md`
- `user/hermes-agent/what-to-borrow-for-this-workbench.md`
- `user/hermes-agent/workbench-upgrade-plan.md`

Agent doc:
- `agent/hermes-agent/analysis-condensed.md`

### `cekai-auto-prd-test-agent`

- Classification: vertical testing workflow and RAG-assisted generation workbench
- Best for learning:
  - prompt as testing SOP
  - UI-centric workflow orchestration
  - PRD-to-test-case structured generation
  - human-in-the-loop refinement loop
  - AI evaluator / critic pattern
  - lightweight local RAG with historical case recall
- When to use as a reference:
  - when analyzing testing-focused AI products
  - when designing a domain workflow around structured artifact generation
  - when judging the boundary between “LLM workflow app” and “true Agent runtime”

User doc:
- `user/cekai-auto-prd-test-agent/analysis.md`

Agent doc:
- `agent/cekai-auto-prd-test-agent/analysis-condensed.md`

### `agentset`

- Classification: production-oriented RAG / agent platform
- Best for learning:
  - ingestion and indexing as platform capability
  - evaluation / benchmark orientation
  - API + hosting + multi-tenancy productization
  - RAG system packaging beyond a single demo
- When to use as a reference:
  - when analyzing RAG platforms
  - when designing hosted knowledge workbench systems
  - when comparing workflow apps against platformized retrieval products

User doc:
- `user/agentset/analysis.md`

Agent doc:
- `agent/agentset/analysis-condensed.md`

### `ms-agent`

- Classification: general-purpose Agent framework with MCP-heavy expansion
- Best for learning:
  - MCP in a general-purpose framework
  - skills / memory / context compression evolution
  - framework + reference-app development model
  - broad agent application surface design
- When to use as a reference:
  - when analyzing general-purpose Agent frameworks
  - when studying how one framework supports many vertical projects
  - when comparing MCP-enabled frameworks

User doc:
- `user/ms-agent/analysis.md`

Agent doc:
- `agent/ms-agent/analysis-condensed.md`

### `langgraph-mcp-agents`

- Classification: MCP workbench and learning-oriented tool runtime
- Best for learning:
  - LangGraph + MCP integration
  - Streamlit tool workbench design
  - dynamic MCP tool management UX
  - fast demo / validation architecture
- When to use as a reference:
  - when prototyping an MCP-enabled workbench
  - when teaching MCP interaction patterns
  - when evaluating how tools become front-end manageable

User doc:
- `user/langgraph-mcp-agents/analysis.md`

Agent doc:
- `agent/langgraph-mcp-agents/analysis-condensed.md`

### `promptfoo`

- Classification: AI testing, eval, and red-team platform
- Best for learning:
  - evals and benchmark systems
  - red teaming and vulnerability scanning
  - CI/CD integration for AI quality
  - quality governance of LLM / Agent apps
- When to use as a reference:
  - when designing bad-case and benchmark systems
  - when adding testing discipline to Agent products

User doc:
- `user/promptfoo/analysis.md`

Agent doc:
- `agent/promptfoo/analysis-condensed.md`

### `giskard`

- Classification: agent evaluation and RAG testing framework
- Best for learning:
  - multi-turn testing
  - scenario-based evals
  - groundedness and conformity checks
  - RAG evaluation
- When to use as a reference:
  - when testing agents and retrieval-backed systems
  - when building regression and evaluation workflows

User doc:
- `user/giskard/analysis.md`

Agent doc:
- `agent/giskard/analysis-condensed.md`

### `adk-python`

- Classification: official general-purpose Agent framework
- Best for learning:
  - code-first agent engineering
  - tools and MCP/OpenAPI support
  - multi-agent hierarchy
  - eval plus deployment integration
- When to use as a reference:
  - when analyzing official Agent frameworks
  - when comparing runtime-first substrates

User doc:
- `user/adk-python/analysis.md`

Agent doc:
- `agent/adk-python/analysis-condensed.md`

### `sample-agentic-maintenance-assistant`

- Classification: industrial AI maintenance assistant product sample
- Best for learning:
  - asset-model context
  - ML + RAG + agent collaboration
  - industrial product workbench design
  - MCP in a real maintenance workflow
  - auth and system integration in industrial AI
- When to use as a reference:
  - when studying industrial AI products
  - when comparing diagnosis and maintenance assistant systems
  - when designing asset-centered AI workflows

User doc:
- `user/sample-agentic-maintenance-assistant/analysis.md`

Agent doc:
- `agent/sample-agentic-maintenance-assistant/analysis-condensed.md`

### `awesome-design-md`

- Classification: design-control knowledge asset for AI coding workflows
- Best for learning:
  - `DESIGN.md` as a persistent design constraint layer
  - style-case library design for AI-assisted frontend generation
  - how to turn vague UI taste into reusable repository guidance
  - how to improve consistency of Agent-generated frontend output
- When to use as a reference:
  - when AI-generated UI is functional but visually inconsistent
  - when building a reusable frontend style template library
  - when adding a design-control layer to coding-agent workflows

User doc:
- `user/awesome-design-md/analysis.md`

Agent doc:
- `agent/awesome-design-md/analysis-condensed.md`

### `awesome-ai-research-writing`

- Classification: team-knowledge and research-writing asset library
- Best for learning:
  - prompt packaging as reusable knowledge assets
  - scenario-first routing for writing tasks
  - skill onboarding and adoption guidance
  - explicit input/output expectation design
- When to use as a reference:
  - when a repository is mainly curated know-how rather than runtime code
  - when packaging prompt/skill assets for one concrete workflow
  - when improving how a workbench exposes reusable assets to normal users

User doc:
- `user/awesome-ai-research-writing/analysis.md`
- `user/awesome-ai-research-writing/what-to-borrow-for-this-workbench.md`

Agent doc:
- `agent/awesome-ai-research-writing/analysis-condensed.md`

### `browser-harness`

- Classification: tool-runtime and thin browser execution substrate
- Best for learning:
  - CDP-first browser control
  - thin helper/daemon substrate design
  - self-healing helper growth during live use
  - interaction-skill vs domain-skill separation
- When to use as a reference:
  - when building a browser action substrate rather than a full platform
  - when deciding how much browser capability should be built in advance versus learned and written back
  - when separating reusable UI mechanics from site-specific knowledge

User doc:
- `user/browser-harness/analysis.md`
- `user/browser-harness/what-to-borrow-for-this-workbench.md`

Agent doc:
- `agent/browser-harness/analysis-condensed.md`

### `fireworks-tech-graph`

- Classification: visualization skill and technical-documentation support asset
- Best for learning:
  - technical diagram generation as a reusable Agent skill
  - diagram style systems and semantic shape vocabularies
  - SVG validation/export workflow design
  - fixture-driven quality control for AI-generated artifacts
- When to use as a reference:
  - when adding architecture/flow/UML diagram generation to an AI coding workflow
  - when standardizing technical-visual deliverables across a team
  - when turning diagram generation from ad hoc prompting into a repeatable capability

User doc:
- `user/fireworks-tech-graph/analysis.md`

Agent doc:
- `agent/fireworks-tech-graph/analysis-condensed.md`

### `QAagent`

- Classification: research-style multi-agent testing prototype
- Best for learning:
  - intermediate reasoning representation for test generation
  - multi-agent decomposition
  - coverage-oriented thinking
- When to use as a reference:
  - when studying how multi-agent can improve test generation
  - when designing intermediate layers before final test-case output

User doc:
- `user/qaagent/analysis.md`

Agent doc:
- `agent/qaagent/analysis-condensed.md`

## Comparison Guide

Use `claude-code-sourcemap` when the main question is:

- How does the agent think, call tools, and continue a task loop?

Use `claude-code` when the main question is:

- How does a working agent evolve into a platform with controls, gating, and product surfaces?

Use `career-ops` when the main question is:

- How do we turn agent capability into a repeatable domain workflow with clear outputs?

Use `fault-diagnosis` when the main question is:

- How do we turn an industrial diagnosis process into a tool-rich, data-driven Agent workflow with charts and reports?

Use `ArcReel` when the main question is:

- How do we turn an Agent workflow into a full creative production platform with SDK runtime wrapping, provider abstraction, and async job orchestration?

Use `repomind` when the main question is:

- How do we turn repository understanding, GitHub evidence gathering, and security verification into a productized Agent workflow?

Use `deer-flow` when the main question is:

- How do we build a configurable super-agent harness with middleware, skills, MCP, memory, sandbox, and subagents?

Use `cekai-auto-prd-test-agent` when the main question is:

- How do we turn PRD understanding, retrieval, structured generation, human refinement, and AI review into a practical testing workflow product?

Use `awesome-design-md` when the main question is:

- How do we turn frontend style guidance into a reusable repository asset that coding agents can follow?

Use `awesome-ai-research-writing` when the main question is:

- How do we turn prompts, skill instructions, and workflow know-how into a low-friction reusable knowledge product?

Use `browser-harness` when the main question is:

- How do we build a very thin browser-control harness that learns reusable interaction and domain patterns over time?

Use `fireworks-tech-graph` when the main question is:

- How do we turn technical diagram generation into a reusable, validated Agent capability rather than a one-off drawing task?

## Recommended Labels For Future Cases

When adding a new project, assign one primary label first:

- `runtime-first`
- `platform-expansion`
- `vertical-workflow`
- `team-knowledge`
- `persistent-agent`
- `memory-first`
- `tool-runtime`
- `RAG-first`

Then record:

- what problem the project is actually solving
- what layer contains the real innovation
- what design tradeoff it makes
- what kinds of future projects should borrow from it
