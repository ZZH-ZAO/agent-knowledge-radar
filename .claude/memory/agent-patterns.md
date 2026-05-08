# Agent Patterns

This file captures reusable architecture patterns observed from the analyzed projects.
这个文件记录的是从多个 Agent 项目里提炼出来、以后可以反复复用的架构模式。

## Pattern 1: Runtime-First Agent

Characteristics:

- strong query loop
- 强 query loop
- structured prompt supply
- 结构化 prompt/context 供给
- tool orchestration as runtime
- 把 tool orchestration 当成运行时
- layered workflow and memory
- 分层 workflow 和 memory

Best for:

- coding agents
- coding agent
- long-session assistants
- 长会话 assistant
- teams building a serious Agent core
- 想做严肃 Agent 内核的团队

Main lesson:

- get the execution spine right before expanding features
- 先把执行脊梁搭对，再扩 feature

## Pattern 2: Platform-Expansion Agent

Characteristics:

- feature-flag-heavy evolution
- 强 feature flag 演进
- runtime gates and staged rollout
- 运行时门控和分阶段发布
- many optional capabilities
- 很多可选能力并存
- remote, team, or persistent agent experiments
- 远程、团队、常驻 Agent 试验方向

Best for:

- productized agent platforms
- 产品化 Agent 平台
- teams exploring many capabilities in parallel
- 并行探索很多能力的团队
- systems that need rollout safety and experimentation
- 需要灰度和实验安全的系统

Main lesson:

- treat the Agent as an evolvable platform, not just a single workflow
- 把 Agent 当成可演进平台，而不是单一工作流

## Pattern 3: Team-Knowledge Agent

Characteristics:

- memory treated as shared project knowledge
- memory 被当成共享项目知识
- sync, conflict control, secret scanning, path safety
- 同步、冲突控制、secret scanning、路径安全
- knowledge lives beyond a single user or session
- 知识超出单一用户和单次会话

Best for:

- enterprise assistants
- 企业 assistant
- repository or team copilots
- 仓库级或团队级 copilot
- long-lived project agents
- 长期运行的项目 Agent

Main lesson:

- memory becomes infrastructure once multiple people rely on it
- 一旦多人依赖 memory，它就变成基础设施

## Pattern 4: Persistent or Proactive Agent

Characteristics:

- background activity
- 背景活动
- tick or wake mechanisms
- tick / wake 机制
- sleep or pacing controls
- sleep / 节奏控制
- ability to continue without immediate user input
- 没有即时用户输入也能继续工作

Best for:

- monitoring
- 监控型场景
- long-running workflows
- 长任务工作流
- assistant modes that remain active across time
- 跨时间持续活跃的 assistant 模式

Main lesson:

- autonomy is a pacing and safety design problem, not just a capability problem
- 自主性首先是节奏控制和安全设计问题，不只是能力问题
