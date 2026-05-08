# Agent Case Library Guide

## Summary

- Project name: Agent research case library
- Project path: `D:\claude-code-sourcemap\.claude\docs`
- Document type: user
- Purpose: help a human reader understand what each accumulated case study is best for, and how to reuse it when studying or designing Agent systems

## How To Read These Cases

These documents are not meant to be a random pile of notes. They form a small teaching library for Agent and LLM engineering.

Each case should answer four questions:

1. What kind of system is this project really building?
2. Which layer is doing the real work: prompt, tool runtime, workflow, memory, RAG, or multi-agent coordination?
3. Why is the project designed this way instead of a simpler alternative?
4. What lessons are portable to another Agent project, and what lessons are only local to this project?

If a case study cannot answer these four questions clearly, it is not mature enough yet.

## Current Cases

### `claude-code-sourcemap`

This is the best case for studying an Agent core runtime.

Why it matters:
- It helps you see that a useful coding agent is not just “an LLM plus a few tools”.
- The real capability comes from the loop between model reasoning, tool invocation, state update, and continued execution.
- It is strong for understanding how prompt system design and workflow orchestration combine into a stable execution engine.

Best learning topics:
- single-turn query loop
- session-level workflow
- auto compaction and context control
- memory extraction placement
- multi-agent coordination basics

Use this case when:
- you want to understand how a serious coding agent is internally structured
- you want to design your own Agent runtime
- you need a reference for “how the engine works”

### `claude-code`

This is the best case for studying how an Agent runtime grows into a product platform.

Why it matters:
- Many teams can build a loop, but fewer teams know how to expose it safely, observe it, gate it, and make it usable across broader scenarios.
- This project is valuable because it is not only about intelligence flow; it is also about operationalizing that intelligence.

Best learning topics:
- feature flags and capability gating
- product surface expansion
- persistent or proactive agent directions
- team memory and shared state ideas
- observability and control surfaces

Use this case when:
- your runtime already works and the next problem is platformization
- you are comparing engine quality versus product completeness
- you want to think about how advanced features should be staged into a system

### `career-ops`

This is the best case for studying a vertical, domain-specific agent workflow system.

Why it matters:
- It shows that not every valuable Agent system needs to be a general-purpose runtime.
- In many business settings, the real value comes from encoding domain procedure, constraints, review steps, and output contracts.

Best learning topics:
- prompt as operating procedure
- workflow-first design
- structured artifacts and handoff contracts
- batching and worker decomposition
- human review in agent pipelines

Use this case when:
- you want to build an industry or function-specific Agent
- you care about repeatability more than maximum autonomy
- you need an example of domain workflow engineering

### `fault-diagnosis`

This is the best case for studying a data-driven industrial diagnosis Agent.

Why it matters:
- It shows how an Agent can be embedded into a real operational workflow rather than only acting as a chat layer.
- It combines structured business data, external ML inference, knowledge retrieval, charts, and report output into one delivery chain.
- It is useful for understanding how domain trust is often built from process transparency and artifacts, not just from the final answer text.

Best learning topics:
- prompt as standard operating procedure
- tool-rich diagnosis workflow
- specialized sub-agent delegation
- checkpointed session memory
- report generation as a first-class product output
- practical RAG in industrial scenarios

Use this case when:
- you want to design an industrial or maintenance Agent
- you need the system to output reports, charts, and traceable evidence
- you want to study how vertical workflow systems differ from general-purpose runtimes

### `ArcReel`

This is the best case for studying a productized Agent platform for creative production.

Why it matters:
- It shows how Agent systems become much more useful when they are embedded into a real workspace, not left as a floating chat interface.
- It wraps Claude Agent SDK with an application runtime layer that handles sessions, reconnect, normalization, interruption, and streaming UI needs.
- It combines workflow orchestration, multi-provider media abstraction, background job execution, and product management concerns in one coherent system.

Best learning topics:
- application runtime on top of an Agent SDK
- orchestrator skill plus focused subagent pattern
- project-state-driven workflow continuation
- queue and worker architecture for long-running generation
- provider abstraction across image, video, and text
- Agent productization beyond pure chat

Use this case when:
- you want to build a serious Agent product rather than a demo
- you need Agent orchestration and heavy background generation to coexist
- you want to study how platform and workflow concerns mix in one Agent system

### `repomind`

This is the best case for studying a repository-intelligence Agent product.

Why it matters:
- It shows that repo chat becomes much more useful once it is organized as a real pipeline instead of a raw LLM call over a code dump.
- It combines file-selection-based code understanding, GitHub live evidence tools, productized streaming, cache/budget control, and security verification into one system.
- It is especially valuable for understanding how an Agent feature becomes a dependable Web product under cost, latency, and trust constraints.

Best learning topics:
- agentic CAG for repository analysis
- GitHub tool calling as evidence gathering
- structured streaming event protocol
- query cache and tenant-aware cache design
- run-state persistence with `ChatRun`
- verification-first security scan workflow

Use this case when:
- you want to build a GitHub repository understanding product
- you need evidence-backed answers rather than pure code summarization
- you want to study how security scanning can be integrated into an Agent product with reporting and feedback loops

### `deer-flow`

This is the best case for studying a super-agent harness.

Why it matters:
- It clearly separates the reusable runtime foundation from the reference application built on top of it.
- It shows how prompt, middleware, skills, MCP, memory, subagents, and sandbox can be organized into one configurable runtime system.
- It is especially useful when the question is no longer "how do I build one agent", but "how do I build an agent substrate others can build on".

Best learning topics:
- harness vs app layering
- middleware-first runtime architecture
- progressive skill loading
- MCP integration as capability extension
- structured long-term memory with async updates
- formal subagent execution infrastructure
- sandbox abstraction and path semantics

Use this case when:
- you want to design a general-purpose Agent runtime
- you want to build a self-hosted Agent platform instead of a single workflow demo
- you want to study how a runtime foundation becomes a reference application

### `cekai-auto-prd-test-agent`

This is the best case for studying a testing-oriented vertical AI workflow product.

Why it matters:
- It shows that many useful “Agent projects” are not really general-purpose agent runtimes, but carefully assembled workflow systems for one business task.
- It combines PRD understanding, local RAG, structured test case generation, human refinement, and AI quality review into one coherent workbench.
- It is especially useful for understanding how Prompt, retrieval, and UI interaction can together replace a heavier runtime architecture in an early-stage product.

Best learning topics:
- prompt as testing SOP
- UI-centric workflow orchestration
- structured test-case artifact generation
- human-in-the-loop refinement
- evaluator / critic pattern
- lightweight retrievable case memory

Use this case when:
- you want to build a testing copilot or test case generation product
- you want to understand the difference between a workflow app and a runtime-first Agent
- you want to study how RAG can constrain structured generation instead of only answering questions

### `agentset`

This is the best case for studying how RAG becomes a platform product.

Why it matters:
- It treats ingestion, indexing, retrieval, evaluation, API, hosting, and multi-tenancy as one system rather than isolated features.
- It is useful for understanding how retrieval applications become developer platforms and hosted products.

Best learning topics:
- RAG as platform capability
- evaluation and benchmark orientation
- API and hosting surfaces
- multi-tenancy

Use this case when:
- you want to analyze or design a RAG platform
- you care about productization beyond a single chat demo

### `ms-agent`

This is the best case for studying a broad general-purpose Agent framework with strong MCP emphasis.

Why it matters:
- It combines MCP, skills, memory, context compression, WebUI, and multiple reference applications into one evolving framework.
- It is valuable for understanding how a framework supports many agent scenarios at once.

Best learning topics:
- MCP in a general-purpose framework
- framework plus reference-app model
- context compression and memory evolution
- broad agent application packaging

Use this case when:
- you want to compare general-purpose agent frameworks
- you want to see how one framework supports research, coding, and other agent applications

### `langgraph-mcp-agents`

This is the best case for studying a lightweight MCP workbench.

Why it matters:
- It makes MCP tools user-manageable through a Streamlit UI rather than hiding everything in backend configuration.
- It is especially useful for quickly understanding how LangGraph, ReAct agents, and MCP can be combined into an interactive workbench.

Best learning topics:
- MCP tool management UX
- Streamlit workbench for agents
- LangGraph + MCP integration
- rapid teaching and validation architecture

Use this case when:
- you want to prototype an MCP-enabled workbench
- you want a highly understandable learning example for MCP

### `promptfoo`

This is the best case for studying AI testing and evaluation discipline.

Why it matters:
- It treats evals, red teaming, vulnerability scanning, and CI/CD checks as core engineering capabilities rather than optional extras.
- It is especially useful when an Agent system is already working functionally, but quality governance is still weak.

Best learning topics:
- eval and benchmark systems
- AI red teaming
- CI/CD integration for AI quality
- quality governance

Use this case when:
- you want to build bad-case and benchmark systems
- you want to make an Agent product more testable and safer

### `giskard`

This is the best case for studying multi-turn Agent evaluation and RAG testing.

Why it matters:
- It focuses on scenarios, groundedness, conformity, and LLM-as-judge checks for agentic systems.
- It is very useful when retrieval-backed agents need more systematic evaluation.

Best learning topics:
- scenario-based evaluation
- multi-turn testing
- groundedness checks
- RAG evaluation

Use this case when:
- you want to test agents, not just inspect outputs manually
- you want to add regression culture to RAG or workflow systems

### `adk-python`

This is the best case for studying a large-company official Agent framework.

Why it matters:
- It shows how Google packages tools, MCP/OpenAPI, multi-agent, eval, and deployment into a code-first framework.
- It is especially useful for understanding how an official framework balances flexibility with engineering control.

Best learning topics:
- code-first agent framework design
- tools and MCP/OpenAPI support
- multi-agent hierarchy
- eval plus deployment

Use this case when:
- you want to compare major official Agent frameworks
- you want a reference for runtime-first Agent substrate design

### `sample-agentic-maintenance-assistant`

This is the best case for studying an industrial AI maintenance assistant sample.

Why it matters:
- It combines asset context, ML-based fault detection, RAG documentation, maps, auth, and MCP into one realistic product sample.
- It is especially relevant for industrial AI and maintenance assistant design.

Best learning topics:
- asset-centered AI architecture
- ML + RAG + Agent collaboration
- industrial AI product workbench
- MCP in a real vertical application

Use this case when:
- you want to study industrial AI products
- you want to compare maintenance assistants against diagnosis workflows

### `awesome-design-md`

This is the best case for studying how design guidance becomes a reusable asset for AI coding.

Why it matters:
- Many coding agents can build working UIs, but they drift badly on taste, consistency, and product feel.
- This project shows a lightweight way to store design direction as `DESIGN.md`, so style stops living only in chat prompts.
- It is useful for understanding how frontend quality can be improved through versioned textual constraints before building a full design system.

Best learning topics:
- `DESIGN.md` as design-control layer
- style-template libraries for AI coding
- converting visual taste into reusable implementation guidance
- keeping Agent-generated UI more consistent over time

Use this case when:
- you want AI-generated frontend work to stop looking random
- you want a reusable starting point for different product styles
- you are exploring how design constraints should enter an Agent coding workflow

### `fireworks-tech-graph`

This is the best case for studying how technical diagram generation becomes a reusable AI skill.

Why it matters:
- Many teams still explain systems with hand-made diagrams or inconsistent screenshots, even when the rest of the workflow is already AI-assisted.
- This project shows how to encode diagram types, layout rules, visual styles, semantic shapes, validation, and export into one reusable skill package.
- It is especially useful for understanding how AI-generated deliverables become dependable only after style rules, validation scripts, and regression fixtures are added.

Best learning topics:
- technical-diagram generation workflow
- style systems for diagrams
- semantic shape and arrow vocabularies
- fixture-driven quality control for AI-generated SVG/PNG outputs

Use this case when:
- you want Agents to generate architecture diagrams, flowcharts, or UML diagrams more reliably
- you want technical documentation to include more standardized visual outputs
- you want to turn “help me draw a diagram” into a stable team capability

### `computer-fundamentals`

This is the best entry for building a reusable computer science fundamentals knowledge base.

Why it matters:
- Foundational CS knowledge is often scattered across books, websites, interview notes, and ad hoc summaries.
- This folder is meant to turn that scattered material into a stable taxonomy that both humans and Agents can reuse.
- It is especially useful when you want explanations to be structured by problem, contrast, common confusion, and engineering relevance instead of raw definition dumps.

Best learning topics:
- data structures
- computer networking
- operating systems
- computer organization

Use this case when:
- you want to accumulate interview-oriented CS knowledge systematically
- you want future Agent answers to stay within your preferred knowledge structure
- you want books and websites to be digested into a stable local knowledge base

## Shared Maps

### `testing-agent-landscape-map.md`

Use this when:
- you want one learning map that connects QAagent, ByteDance--Auto_prd_test_agent, promptfoo, and giskard
- you want to understand the difference between test generation, testing workbench design, AI eval, and multi-turn Agent evaluation

## Which Case Should You Compare A New Project Against

If the new project mainly asks:

- How does the core agent run: compare it to `claude-code-sourcemap`
- How does the agent become a product platform: compare it to `claude-code`
- How does the agent solve a domain workflow end to end: compare it to `career-ops`
- How does the agent execute an industrial diagnosis workflow with data, KB, and reports: compare it to `fault-diagnosis`
- How does the agent become a creative production platform with async jobs and provider abstraction: compare it to `ArcReel`
- How does the agent become a repository-intelligence product with GitHub evidence and verification-first security flows: compare it to `repomind`
- How do we build a general-purpose super-agent harness with skills, MCP, memory, sandbox, and subagents: compare it to `deer-flow`
- How do we build a practical PRD-to-test-case workflow with retrieval, human editing, and AI review: compare it to `cekai-auto-prd-test-agent`
- How do we turn RAG into a hosted platform with ingestion, eval, and multi-tenancy: compare it to `agentset`
- How do we study MCP in a broad general-purpose Agent framework: compare it to `ms-agent`
- How do we rapidly validate LangGraph + MCP + Streamlit workbench ideas: compare it to `langgraph-mcp-agents`
- How do we make an Agent system testable, benchmarked, and safer: compare it to `promptfoo`
- How do we evaluate multi-turn agents and retrieval-backed systems systematically: compare it to `giskard`
- How do we study a major official code-first Agent framework: compare it to `adk-python`
- How do we study a realistic industrial AI maintenance assistant sample: compare it to `sample-agentic-maintenance-assistant`
- How do we make frontend style guidance reusable and durable for coding agents: compare it to `awesome-design-md`
- How do we make technical diagram generation reusable and validated for coding agents: compare it to `fireworks-tech-graph`

## Folder Rule

Project-specific docs should be stored under:

- `user/<project-name>/`

Cross-project reusable templates should be stored under:

- `user/shared/`

## Shared Templates

### `testing-agent-design-template.md`

Use this when:
- you want to analyze a testing-oriented Agent project systematically
- you want a reusable blueprint for PRD-to-test-case, testing copilot, or test knowledge workbench systems
- you want to compare a testing Agent against workflow, retrieval, memory, and quality-closure best practices

### `agent-output-quality-control-template.md`

Use this when:
- you want to design a quality-control layer for Agent outputs rather than only the reasoning/runtime layer
- you need frontend design consistency and technical-visual consistency to become reusable assets
- you want one template that bridges `awesome-design-md` and `fireworks-tech-graph`

### `refactoring-2nd-edition-notes.md`

Use this when:
- you want a reusable reading of Refactoring, 2nd Edition focused on engineering method rather than book summary
- you need a stable lens for code smells, small-step refactoring, and behavior-preserving change
- you want review and AI coding guidance grounded in classic refactoring practice

### `refactoring-smell-to-action-cheatsheet.md`

Use this when:
- you want a quick lookup from a code smell to likely refactoring moves
- you need review wording that is more concrete than “this should be optimized”
- you want to turn classic refactoring ideas into day-to-day coding guidance fast

### `refactoring-review-prompt-templates.md`

Use this when:
- you want ready-to-copy prompt templates for Claude Code, Codex, or similar coding agents
- you want refactoring-minded reviews instead of vague optimization advice
- you want prompt scaffolds for PR review, legacy-code review, AI-generated-code review, or stepwise refactoring planning

## What A Good New Case Should Add

A new case is worth storing only if it contributes at least one of these:

- a new runtime pattern
- a new memory or RAG design
- a new tool orchestration model
- a new multi-agent coordination pattern
- a new domain workflow packaging strategy
- a new productization or governance idea

If it does not add a meaningful pattern, it should probably remain a temporary note instead of entering the long-term library.
