---
name: agent-platform-design
description: Use when designing or advising on a new Agent platform, coding agent, or LLM product architecture. Apply this skill when the user wants concrete recommendations for runtime design, prompt structure, tools, memory, workflow, RAG, multi-agent patterns, rollout strategy, or platform evolution.
---

# Agent Platform Design

Use this skill when the task is to design an Agent system or give concrete architecture advice, especially for coding agents and long-running assistants.
如果用户想让你“设计一个 Agent 系统”或者“给 Agent 平台提方案”，就用这个 skill。

For detailed design templates, read:

- `references/design-template.md`
- `references/stage-guide.md`

## Best For

- greenfield Agent platform design
- redesigning an existing runtime into a more structured system
- deciding how much complexity is justified at the current stage
- advising on tools, memory, workflow, and rollout architecture together

## Not For

- codebase-first review where the current system is still poorly understood
- roadmap questions that mainly ask what to build next
- isolated prompt tuning tasks
- narrow implementation review of a single module

## Common Companion Assets

- `../agent-research-workbench/SKILL.md`
- `../agent-architecture-review/SKILL.md`
- `../agent-feature-roadmap/SKILL.md`
- `../../docs/user/shared/productized-agent-platform-template.md`
- `../../docs/user/shared/super-agent-harness-design-template.md`
- `../../docs/user/shared/sdk-wrapped-agent-runtime-template.md`
- `../../memory/memory-operating-model.md`

## Related Cases

- `claude-code`
- `deer-flow`
- `arcreel`
- `hermes-agent`
- `sample-agentic-maintenance-assistant`

## Design Principle

Do not start from “which model should we use”.
Start from:

- what kind of work the Agent must sustain
- what execution loop is needed
- what state must survive
- what side effects must be governed
- how the system should evolve over time

中文理解：

- 不要先纠结模型型号
- 先想系统要持续完成什么工作
- 再想执行循环、状态、工具副作用、长期演进怎么承接

## Design Sequence

1. Clarify the target system type.
   Choose whether the project is mainly:
   - single-turn assistant
   - tool-using coding agent
   - long-session agent
   - multi-agent coordinator
   - platform with remote, team, or background capabilities

2. Design the runtime before the features.
   Define:
   - request entry
   - query loop
   - tool execution path
   - result reinjection
   - turn-end hooks
   - persistence and recovery

3. Design prompt as a context supply system.
   Separate:
   - stable rules
   - dynamic runtime sections
   - temporary attachments or reminders

4. Design tools as a governed runtime.
   Include:
   - schemas
   - permissions
   - concurrency rules
   - side-effect boundaries
   - result protocol

5. Design workflow by time scale.
   At minimum consider:
   - single-turn orchestration
   - session-level management
   - background jobs
   - multi-agent coordination

6. Design memory and retrieval intentionally.
   Separate:
   - short-term working memory
   - session compaction memory
   - persistent preferences or project knowledge
   - external retrieval

7. Design evolution and operations.
   Consider:
   - feature flags
   - runtime gating
   - telemetry
   - cache and cost
   - safe rollout

这一步很重要，因为很多 Agent 项目不是死在“功能不会做”，而是死在“做出来之后不能稳地演进”。

## Recommendation Style

When advising, always say:

- what to implement now
- what can wait
- what is overkill at this stage
- what new signals would justify adding more machinery later

中文理解：

- 现在该做什么
- 哪些先别做
- 什么时候值得升级复杂度

## Maturity Ladder

Use this default maturity ladder:

### Stage 1

Build:

- one query loop
- a small prompt system
- a small tool runtime
- basic turn-end hooks

Avoid:

- heavy multi-agent
- heavy vector RAG
- complex remote control

这是“先把底盘站住”的阶段。

### Stage 2

Add:

- compaction
- persistent memory
- retrieval layering
- safer permissions
- cache-aware prompt design

### Stage 3

Add:

- multi-agent coordination
- background task systems
- team memory
- remote or distributed execution
- feature flag and observability systems

这是“平台化”阶段，不是所有项目都一上来就需要。

## Decision Heuristics

If the user is unsure what to prioritize, prefer:

1. runtime stability
2. tool safety
3. context quality
4. long-session control
5. memory quality
6. multi-agent expansion

If the project is failing, diagnose in this order:

1. broken execution loop
2. uncontrolled tool side effects
3. unstable prompt/context supply
4. missing session governance
5. weak retrieval or memory
6. overcomplicated agent topology

## Output Template

Use a structure close to this:

### System Target

- what kind of Agent product this is
- what work it must sustain
- what complexity level is justified now

### Recommended Architecture

- runtime spine
- prompt/context strategy
- tool runtime strategy
- workflow layers
- memory and retrieval layers
- multi-agent stance

### What To Build Now

- the smallest architecture that can succeed

### What To Delay

- advanced capabilities that are not justified yet

### Upgrade Triggers

- concrete signals that mean the next layer of complexity should be added

## Common Mistakes

- Starting from model choice instead of runtime shape.
- Recommending multi-agent before single-agent stability.
- Recommending vector RAG before retrieval categories are understood.
- Treating memory as “store more history”.
- Designing prompt as one giant text blob with no cache or debugging strategy.
- Proposing platform features without a stable execution spine.

## Skill Feedback Loop

After a design task, check whether the work produced:

- a new stage boundary worth adding to the maturity ladder
- a better default sequence for runtime, memory, or workflow evolution
- a clearer heuristic for when a platform feature is overkill
- a reusable architecture pattern that belongs in companion templates

Keep case-specific advice in `docs/` or `sessions/` first.
Update this skill only when the lesson changes the default design method across projects.
