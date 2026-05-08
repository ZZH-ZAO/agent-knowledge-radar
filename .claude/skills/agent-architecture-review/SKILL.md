---
name: agent-architecture-review
description: Use when reviewing an Agent, AI coding assistant, or LLM application architecture. Apply this skill when the task is to analyze runtime design, prompt system, tool calling, workflow orchestration, memory, RAG, multi-agent coordination, or engineering tradeoffs in a codebase or design doc.
---

# Agent Architecture Review

Use this skill when the user wants a serious architecture review of an Agent or LLM system, not a shallow feature inventory.
如果用户想要的是“真正看懂一个 Agent 项目”，而不是简单列模块，就用这个 skill。

For detailed review templates, read:

- `references/review-template.md`
- `references/layer-questions.md`

## Best For

- deep codebase-based architecture review
- identifying the real runtime spine of an Agent system
- judging whether a project is a true runtime, a workflow app, or a thin wrapper
- extracting transferable design lessons from source code

## Not For

- greenfield platform design without an existing system to inspect
- roadmap-only prioritization questions
- shallow feature inventory requests
- code review tasks focused on local refactoring rather than system architecture

## Common Companion Assets

- `../agent-research-workbench/SKILL.md`
- `../agent-platform-design/SKILL.md`
- `../agent-feature-roadmap/SKILL.md`
- `../../docs/user/shared/super-agent-harness-design-template.md`
- `../../docs/user/shared/sdk-wrapped-agent-runtime-template.md`
- `../../memory/memory-operating-model.md`

## Related Cases

- `deer-flow`
- `claude-code-sourcemap`
- `hermes-agent`
- `ms-agent`
- `adk-python`

## Review Goal

Your job is to answer:

- What kind of system this really is
- What the runtime center is
- Which layers are strong or weak
- Why the current design was likely chosen
- What tradeoffs or missing pieces remain

中文理解：

- 这个系统本质上到底是什么
- 它真正的中心是不是 query loop / runtime
- 哪些层做得成熟，哪些层只是表面上有
- 为什么团队会做出这种设计
- 现在还缺什么，风险在哪里

Do not stop at listing modules.
Always explain each major area in terms of:

- what it is
- why it exists
- how it is implemented
- what problem it solves
- what simpler alternative exists
- where it may break or become heavy

也就是说，不要只说“这个文件负责什么”，而要讲“为什么这样做更合理，以及代价是什么”。

## Review Workflow

1. Find the main execution path first.
   Usually this means locating the entrypoint, session engine, query loop, tool orchestration, and turn-end hooks.

2. Classify the system.
   Decide whether it is mainly:
   - a chat shell
   - a tool-using assistant
   - an Agent runtime
   - a platform for multiple Agents or long-running workflows

3. Review these layers in order:
   - runtime and query loop
   - prompt and context system
   - tool runtime and permissions
   - workflow orchestration across time scales
   - RAG and retrieval strategy
   - memory architecture
   - multi-agent coordination
   - observability, gating, and cost engineering

4. For each layer, identify:
   - the design intent
   - the key implementation points
   - the benefits
   - the hidden risks
   - the maturity level

5. End with judgment, not summary.
   State what this project is genuinely good at, what stage it is in, and what should be improved next.

中文理解：

- 最后一定要下判断
- 不要只做摘要
- 要说出“这个项目现在真正强在哪、处在什么阶段、下一步应该补什么”

## What Good Output Looks Like

Good output reads like a lecture or architecture walkthrough.
好的输出应该像讲稿或架构导读，而不是 PPT 式清单。

Avoid:

- dry bullet dumps
- vague praise
- “this module handles X/Y/Z” without explanation

Prefer:

- “the real center of this system is...”
- “this is stronger than a normal Function Calling demo because...”
- “the tradeoff of doing it this way is...”
- “if the team were earlier-stage, a simpler version would be...”

这些句型的价值在于，它们会逼你讲“设计原因”和“替代方案”。

## Common Evaluation Questions

Use these questions to sharpen the review:

- Is the system centered on a real query loop or just an API wrapper?
- Are prompt rules, dynamic context, and attachments separated?
- Is tool calling treated as a runtime with permissions and side-effect control?
- Does workflow exist at multiple time scales, or only on the happy path?
- Is retrieval actually designed, or is “RAG” just a label?
- Is memory just stored history, or a governed multi-layer system?
- Is multi-agent design about responsibility and result flow, or just spawning workers?
- Are cost, cache, rollout, and observability treated as architecture concerns?

如果这些问题回答不出来，就说明分析还停留在表层。

## Output Structure

Prefer this structure unless the user asks for something else:

1. Overall judgment
2. Layer-by-layer analysis
3. Strongest design ideas worth learning
4. Weak points or future scaling risks
5. Actionable advice for builders

## Output Template

Use a structure close to this:

### Overall Judgment

- what kind of system this really is
- what maturity level it appears to be at

### Runtime Spine

- entrypoint
- session engine
- query loop
- tool reinjection
- turn-end handling

### Layer Analysis

For each major layer:

- what it means here
- how it is implemented
- why this design is stronger than a simpler version
- what tradeoffs remain

### Most Transferable Lessons

- the 3 to 5 ideas another Agent project should copy

### Next Risks or Weaknesses

- scaling risks
- missing governance
- parts that still look demo-level or experimental

## Common Mistakes

- Treating every module equally instead of finding the system center.
- Confusing feature richness with architectural maturity.
- Describing files without explaining causal relationships.
- Calling something “RAG”, “memory”, or “multi-agent” without checking whether the implementation actually supports that claim.
- Ignoring rollout, cost, or observability when the project is clearly platform-level.

## Skill Feedback Loop

After a new case is analyzed, check whether the case reveals:

- a better way to identify the runtime center
- a missing architecture layer in the review order
- a more precise classification heuristic
- a repeatable failure mode worth adding to `Common Mistakes`

Record task-specific observations in `sessions/` first.
Only update this skill when the lesson improves how future architecture reviews should generally be done.
