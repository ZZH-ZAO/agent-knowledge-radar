---
name: agent-research-workbench
description: Use when the user wants a full-spectrum Agent project analysis or design session. Apply this skill when the task spans architecture review, platform design advice, roadmap planning, comparison of multiple Agent projects, or turning research findings into reusable guidance.
---

# Agent Research Workbench

Use this skill as the top-level entry when the task is broader than a single review, design proposal, or roadmap.
如果用户要你“系统分析一个 Agent 项目”“对比多个 Agent 项目”“顺便给设计建议和下一步路线”，优先用这个总入口 skill。

For routing help, read:

- `references/routing-guide.md`

## Best For

- full-spectrum analysis that spans review, design, and roadmap
- comparing multiple Agent projects and extracting reusable lessons
- turning case-study findings into workbench guidance
- deciding which sub-skill should lead a complex Agent task

## Not For

- narrow single-purpose tasks that clearly belong to one sub-skill
- local code cleanup or refactoring work
- isolated product requirement writing unrelated to Agent architecture
- tasks where no case comparison or synthesis is needed

## Common Companion Assets

- `../agent-architecture-review/SKILL.md`
- `../agent-platform-design/SKILL.md`
- `../agent-feature-roadmap/SKILL.md`
- `../autonomous-delivery-default/SKILL.md`
- `../../docs/index.md`
- `../../memory/memory-operating-model.md`
- `../../sessions/WORKFLOW.md`

## Related Cases

- `hermes-agent`
- `deer-flow`
- `claude-code`
- `arcreel`
- `repomind`

## What This Skill Does

This skill helps you choose and combine the right sub-skills:

- `agent-architecture-review`
- `agent-platform-design`
- `agent-feature-roadmap`

中文理解：

- 它不是替代那 3 个 skill
- 它是一个总控入口，帮你判断这次任务到底更偏 review、design、roadmap，还是三者组合

## Routing Rules

### Use Architecture Review First When

- the user asks what the current system really is
- the codebase must be understood before recommendations are made
- the user wants deep source-based explanation

### Use Platform Design First When

- the user asks how to build a similar system
- the task is greenfield design
- the user wants architecture recommendations more than current-state analysis

### Use Feature Roadmap First When

- the user asks what to build next
- the project already exists and the question is prioritization
- the user wants maturity assessment or sequencing advice

### Use All Three Together When

- the user wants: understand current system -> extract lessons -> propose future path
- the user wants a comparison between multiple Agent projects
- the user wants reusable guidance for future Agent work

## Recommended Workflow

1. Classify the request.
2. Decide whether review, design, roadmap, or a combination is needed.
3. If codebase-specific, do architecture review first.
4. Convert findings into platform lessons.
5. End with roadmap-style next steps if useful.

中文理解：

最常见的正确顺序是：

1. 先看清当前项目
2. 再提炼能学走的方法
3. 最后再讲下一步怎么做

## Common Output Modes

### Mode 1: Deep Project Analysis

- architecture review as the spine
- design lessons as a secondary layer

### Mode 2: Build-a-Similar-System Guide

- platform design as the spine
- architecture review only as evidence

### Mode 3: What Should We Build Next

- roadmap as the spine
- architecture review used only to justify priorities

### Mode 4: Compare Several Agent Projects

- compare runtime center
- compare prompt/tool/workflow/memory/multi-agent maturity
- compare productization and platform evolution
- extract reusable lessons

## Common Mistakes

- Jumping into recommendations before understanding the current runtime.
- Giving a roadmap without identifying bottlenecks.
- Giving design advice without naming tradeoffs or stage assumptions.
- Comparing projects by feature count instead of architecture and design philosophy.

## Skill Feedback Loop

After a broad research task, check whether it should produce updates to:

- one of the sub-skills
- `docs/index.md`
- shared templates under `docs/user/shared/`
- stable heuristics under `memory/`
- a searchable session record under `sessions/`

Default rule:

- case detail goes to `docs/` and `sessions/` first
- stable heuristics go to `memory/`
- procedural upgrades go to the relevant skill
