# Hermes Agent、DeerFlow 与 claude-code 对比分析

## Summary

- Project name: Hermes Agent / DeerFlow / claude-code
- Project path: `D:\hermes-agent` / `D:\deer-flow` / `D:\claude-code`
- Document type: `user`
- Purpose: explain the difference between a long-running agent workbench, a general-purpose harness, and a platform-expansion agent system, so future design choices can be made at the right abstraction layer

## 一、先给总图：这三个项目分别代表三种不同重心

如果把这三个项目放在一张图上理解，我会这样看：

- `deer-flow`
  更像 `general-purpose Agent harness`
- `claude-code`
  更像 `platform-expansion Agent product`
- `hermes-agent`
  更像 `long-running Agent workbench`

这不是高低之分，而是它们在回答不同问题。

### `deer-flow` 在回答什么

它最像在回答：

> 如果我要做一套通用、可扩展、可自托管的 Agent runtime / harness，该怎么把 prompt、middleware、skills、MCP、sandbox、subagent 组织起来？

### `claude-code` 在回答什么

它最像在回答：

> 当一个 Agent runtime 已经能跑之后，怎样把它做成一个可灰度、可治理、可观测、可远控、可持续演进的平台产品？

### `hermes-agent` 在回答什么

它最像在回答：

> 如果 Agent 不是一次性对话器，而是一个长期存在、跨入口运行、会积累记忆和技能、还能被时间驱动和研究系统复用的工作体，该怎么设计？

所以一句话概括就是：

- `deer-flow` 教你怎么搭底盘
- `claude-code` 教你怎么把底盘长成平台产品
- `hermes-agent` 教你怎么让 Agent 长期活着并持续积累

## 二、从系统目标看：三者解决的核心问题不一样

### 1. `deer-flow` 的目标最偏“通用底座”

它最关心的是：

- runtime 怎样分层
- middleware 怎样插拔
- skills / MCP / sandbox / subagent 怎样进入统一生态
- harness 和 app 怎样拆开

它解决的是“通用 Agent substrate”的问题。

### 2. `claude-code` 的目标最偏“平台演进”

它最关心的是：

- feature flag 和 rollout
- observability
- persistent / proactive direction
- remote control
- team memory
- 能力治理和 kill-switch

它解决的是“能跑的 Agent 怎么继续长成功能密集的平台”的问题。

### 3. `hermes-agent` 的目标最偏“长期运行”

它最关心的是：

- session 怎样持久化
- memory 与 session search 怎样闭环
- skill 怎样从经验中持续积累
- Agent 怎样同时活在 CLI、gateway、TUI、编辑器里
- cron 和远程环境怎样把 Agent 从被动响应推进到长期工作
- 同一运行底座怎样兼顾真实使用和 trajectory / RL 训练

它解决的是“Agent 如何成为长期存在的工作台”的问题。

## 三、架构气质对比：谁更像 engine，谁更像 harness，谁更像 workbench

### `deer-flow`

架构气质最强的是：

- formal runtime layering
- harness / app separation
- middleware-first composition
- capabilities as pluggable ecosystem

它的味道很像“面向很多未来 Agent 的通用底座”。

### `claude-code`

架构气质最强的是：

- governed runtime evolution
- feature gating
- product controls
- remote / persistent / team-oriented expansion

它的味道很像“有真实产品压力的平台分支”。

### `hermes-agent`

架构气质最强的是：

- one substrate, many surfaces
- memory-first persistence
- skill accumulation
- scheduling + remote environments
- research-ready tooling

它的味道更像“真正每天会被用、会活很久、还能不断沉淀的 Agent 工作台”。

## 四、Prompt 与能力组织：三者各自强调什么

### `deer-flow`

Prompt 更像：

- runtime governance protocol

它关心：

- clarification first
- skill progressive loading
- subagent policy
- citation discipline
- outputs / workspace semantics

### `claude-code`

Prompt 更像：

- platform capability policy

它关心：

- 哪些功能应该开放
- 如何按模式和用户条件 gate
- 高风险能力怎样 fail-closed
- 实验 feature 如何不污染主路径

### `hermes-agent`

Prompt 和能力组织更像：

- long-running operational policy

它关心：

- memory context 怎么注入
- session search 怎么参与 recall
- skill 怎样成为可调用、可持续增长的程序性资产
- 跨平台入口怎么共享 slash commands 和同一底座

所以如果你想学：

- 通用 runtime governance，看 `deer-flow`
- 平台能力治理，看 `claude-code`
- 长期运行 + 记忆/技能闭环，看 `hermes-agent`

## 五、Memory 视角对比：这是三者差异最大的一块

### `deer-flow`

Memory 更偏：

- 结构化长期记忆系统
- runtime 中的长期 facts / user context / async memory update

它关心的是怎样把 memory 放进通用 Agent runtime。

### `claude-code`

Memory 更偏：

- persistent direction
- team-shared knowledge
- platform-level memory governance

它关心的是当 memory 进入团队与平台层面后，怎样治理冲突、同步和安全。

### `hermes-agent`

Memory 更偏：

- 长期 personal / cross-session operating memory
- transcript search + memory provider 双轨协同
- MEMORY.md / USER.md + provider architecture + FTS5 search + profile continuity

它关心的是让 Agent 在多次真实使用中“越来越像一个持续存在的助手”。

如果把这三者压缩成一句话：

- `deer-flow` 更像“怎么把长期记忆接进 runtime”
- `claude-code` 更像“长期记忆怎样升级成平台/团队资产”
- `hermes-agent` 更像“长期记忆怎样真正服务一个每天都在运行的助手”

## 六、入口层对比：Hermes Agent 最不一样

三者都不算简单聊天壳子，但入口层重心很不同。

### `deer-flow`

更强调：

- harness 与 app 的职责拆分
- 前后端与 gateway 的系统化分层

### `claude-code`

更强调：

- 平台 feature surface
- remote control / bridge / multi-instance direction

### `hermes-agent`

更强调：

- CLI
- messaging gateway
- Ink TUI
- ACP editor integration

而且它们尽量共用同一 agent substrate。

这使得 Hermes 更像“同一个 Agent 活在很多入口里”，而不是“同一个仓库里有很多不同产品”。

这也是它特别适合参考“多入口长期助手”的原因。

## 七、调度与长期运行：Hermes Agent 在这里最突出

这块是 `hermes-agent` 最鲜明的独特价值。

### `deer-flow`

更偏“runtime 能承载复杂任务与多能力生态”。

### `claude-code`

更偏“平台继续长 persistent / proactive / remote 功能”。

### `hermes-agent`

则已经把下面这些东西更明确地放在系统正中央：

- cron scheduler
- platform delivery
- remote / persistent terminal environments
- cross-session continuity
- memory + skills 累积

这意味着它不是只探索“Agent 未来可能主动”，而是已经在搭：

- 时间驱动的 Agent
- 云端常驻的 Agent
- 会积累工作方法的 Agent

如果你未来想做的不是“更强对话”，而是“更像工作体的 Agent”，Hermes 的参考价值会非常高。

## 八、研究取向对比：Hermes Agent 也比另外两者更统一

### `deer-flow`

强在 runtime/harness 抽象与 reference app 设计。

### `claude-code`

强在平台 feature 演进和产品治理。

### `hermes-agent`

独特之处在于：

- `batch_runner.py`
- `trajectory_compressor.py`
- `environments/`
- `tinker-atropos/`

说明它把“真实使用 runtime”和“训练/eval 数据生成”放在了一套连续面里。

这对研究团队尤其有价值，因为很多系统会把：

- 线上工作台
- 线下数据生成
- RL / eval 环境

拆成完全不同的工程世界，而 Hermes 更像试图把它们连起来。

## 九、如果你以后要借鉴，分别最该学什么

### 最该从 `deer-flow` 学的

- 通用 Agent harness 怎样分层
- middleware-first runtime 怎样设计
- skills / MCP / sandbox / subagent 怎样形成统一底座

### 最该从 `claude-code` 学的

- feature gating / rollout / kill-switch
- 观测性和平台治理
- persistent / remote / team memory 这些能力如何被稳妥引入

### 最该从 `hermes-agent` 学的

- 怎样把 Agent 做成长期运行型工作台
- memory、session search、skills、cron 怎样形成长期闭环
- 多入口怎样共用一个 Agent substrate
- 如何把真实产品使用与 trajectory / RL 研究路径接在一起

## 十、最后一句总结

如果只记一句话，我会建议记这个：

> `deer-flow` 更像通用 Agent harness，`claude-code` 更像平台化 Agent 产品试验场，而 `hermes-agent` 最像一个真正会长期运行、跨入口存在、不断积累记忆与技能的 Agent 工作台。
