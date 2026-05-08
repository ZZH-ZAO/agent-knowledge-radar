---
name: agent-feature-roadmap
description: Use when deciding what an Agent project should build next. Apply this skill when the user wants a roadmap, prioritization advice, maturity assessment, feature sequencing, or guidance on when to add memory, RAG, multi-agent, remote control, observability, or platform features.
---

# Agent Feature Roadmap

Use this skill when the user needs prioritization, sequencing, or roadmap advice for an Agent project.
如果用户在问“下一步该补什么”“这个项目该怎么排路线图”，就用这个 skill。

For detailed roadmap templates, read:

- `references/roadmap-template.md`
- `references/trigger-signals.md`

## Best For

- deciding the next 1 to 3 build priorities
- maturity assessment of an existing Agent project
- sequencing memory, retrieval, multi-agent, and platform features
- making a roadmap from observed bottlenecks instead of feature desire

## Not For

- deep architecture explanation without a prioritization question
- greenfield system design from scratch
- implementation details of one local feature
- feature comparison with no recommendation goal

## Common Companion Assets

- `../agent-research-workbench/SKILL.md`
- `../agent-architecture-review/SKILL.md`
- `../agent-platform-design/SKILL.md`
- `../../docs/user/shared/agent-project-classification-map.md`
- `../../memory/memory-operating-model.md`

## Related Cases

- `hermes-agent`
- `claude-code`
- `fault-diagnosis`
- `arcreel`
- `repomind`

## Core Rule

Do not recommend the most advanced feature first.
Recommend the next feature that matches the project's current bottleneck.

中文理解：

- 不要推荐最酷的
- 要推荐最对当前瓶颈的

## Bottleneck-Based Roadmapping

Diagnose the project first.
Common bottlenecks:

- the Agent cannot reliably finish a single task
- tool use is unsafe or inconsistent
- long sessions degrade badly
- useful knowledge is not being retrieved
- the system forgets stable preferences or project facts
- the team wants parallelism but result integration is weak
- the product is growing features without rollout control

这些才是路线图真正应该围绕的东西，而不是功能愿望单。

## Roadmap Order

Default upgrade sequence:

1. solid query loop
2. prompt and context structure
3. tool runtime and permissions
4. session compaction and turn-end hooks
5. memory and retrieval layers
6. multi-agent coordination
7. platform features such as remote control, team memory, feature gating, telemetry

## When To Add Specific Features

### Add Memory When

- the same user preferences repeat
- project conventions keep getting re-explained
- long tasks span multiple sessions

### Add RAG When

- relevant facts live outside current context
- external documents or rules matter
- simple file search is no longer enough

### Add Multi-Agent When

- work naturally splits into independent subproblems
- a coordinator can own final synthesis
- one agent is overloaded with search or verification work

### Add Feature Flags and Runtime Gates When

- the project is exploring multiple high-risk features
- not all users should see all capabilities
- rollback and staged rollout matter

### Add Team Memory or Remote Control When

- the system is moving from solo use to team workflows
- sessions must continue across devices or surfaces
- multiple execution instances must cooperate

中文理解：

- 进入团队协作
- 需要跨端继续会话
- 需要多个实例协作

这时才值得考虑 team memory、remote control、pipes 这类更重的能力。

## What To Avoid

Do not recommend:

- vector databases before retrieval categories are understood
- multi-agent before single-agent stability
- autonomous modes before safety and pacing controls
- broad feature expansion without observability or gating

这几条本质上是在防止“技术上很兴奋，但工程上很失控”。

## Output Format

Produce:

1. current maturity assessment
2. top 3 bottlenecks
3. next 3 build priorities
4. what not to build yet
5. what signals would trigger the next layer of complexity

## Roadmap Template

Use a structure close to this:

### Current Stage

- runtime stage
- tooling stage
- memory/retrieval stage
- platform stage

### Top Bottlenecks

- 3 most important current constraints

### Recommended Next Steps

- priority 1 with reason
- priority 2 with reason
- priority 3 with reason

### Explicit “Not Yet”

- features that sound attractive but are premature

### Trigger Signals

- what evidence would justify adding multi-agent, team memory, remote control, observability, or heavier retrieval

## Common Mistakes

- Writing a wishlist instead of a bottleneck-driven roadmap.
- Recommending the most advanced feature because it sounds impressive.
- Ignoring operational maturity like rollout gates, telemetry, and safety.
- Adding memory, RAG, and multi-agent all at once without knowing which problem each solves.
- Failing to say what should wait.

## Skill Feedback Loop

After a roadmap task, check whether the case exposed:

- a new bottleneck pattern that recurs across projects
- a missing trigger signal for adding memory, RAG, or multi-agent
- a better default `not yet` rule
- a clearer maturity marker for platformization

Keep case-specific sequencing in the case docs first.
Update this skill only when the lesson changes roadmap heuristics beyond that one project.
