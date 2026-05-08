# Shared Templates Folder

## Summary

- Project name: shared agent design templates
- Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared`
- Document type: user folder guide
- Purpose: help a human reader quickly find reusable cross-project templates and methods without confusing them with any single project case

## 这是什么

这个目录放的不是某一个具体项目的案例分析，而是跨项目都能复用的模板、方法论和设计框架。

如果说：

- `user/<project-name>/` 负责“看懂某一个项目”

那么这里负责的就是：

- “把多个项目里提炼出来的方法真正沉淀成可直接套用的模板”

## 当前模板一览

### 1. `industrial-agent-design-template.md`

适合场景：

- 工业 Agent
- 诊断 Agent
- 巡检 Agent
- 运维 / 维护类垂直 Agent

它主要回答：

- 工业 Agent 应该怎样分层
- prompt、tool、RAG、memory、audit 应该围绕什么目标设计
- 为什么工业 Agent 的重点是证据、流程和交付物

推荐什么时候看：

- 当你在设计工业或重流程垂直 Agent 时

### 2. `productized-agent-platform-template.md`

适合场景：

- Agent 工作台
- 多供应商 AI 平台
- 创作平台
- 平台化 Agent 产品

它主要回答：

- 一个产品化 Agent 平台应该有哪些层
- Agent 怎样和项目状态、任务系统、配置系统、产品表面协同
- 为什么产品化 Agent 不能只做聊天框

推荐什么时候看：

- 当你在设计完整 Agent 产品或工作台时

### 3. `sdk-wrapped-agent-runtime-template.md`

适合场景：

- 基于 Claude Agent SDK、OpenAI Agents SDK、或其他 Agent SDK 做产品
- 需要 session / reconnect / interrupt / snapshot / projector 的系统

它主要回答：

- 为什么需要在 SDK 之上再包一层应用级 runtime
- session manager、stream projector、turn normalization 这些组件分别负责什么
- 什么情况下必须做 SDK wrapping

推荐什么时候看：

- 当你不是在做 demo，而是在做真正会给用户使用的 Agent 产品时

### 4. `super-agent-harness-design-template.md`

适合场景：

- 通用 Agent runtime
- super agent harness
- Agent 底座 / substrate
- runtime 与 reference app 分层项目

它主要回答：

- 如何分析一个通用 Agent 底座，而不是只列功能
- Prompt、middleware、skills、MCP、memory、sandbox、subagent 各自在哪一层做什么
- Harness 与 App 分层为什么重要

推荐什么时候看：

- 当你想做一套可复用的 Agent 运行时底座
- 当你要分析 DeerFlow 这类 harness 型项目

### 5. `agent-project-classification-map.md`

适合场景：

- 想建立 Agent 项目整体认知地图
- 想先判断一个项目属于哪一类再深入分析
- 想设计自己的学习路径

它主要回答：

- 当前常见 Agent 项目可以分成哪几大类
- 每一类项目最该学什么
- 新项目应该优先和哪个历史案例对比

推荐什么时候看：

- 当你开始看新的 Agent 项目之前
- 当你觉得案例越来越多、需要一张总图来整理思路时

## 推荐阅读方式

### 如果你正在做工业 Agent

优先看：

1. `industrial-agent-design-template.md`
2. 对照 `fault-diagnosis/` 案例目录

### 如果你正在做平台化 Agent 产品

优先看：

1. `productized-agent-platform-template.md`
2. 对照 `arcreel/` 或 `claude-code/` 案例目录

### 如果你正在做 SDK 包装型 runtime

优先看：

1. `sdk-wrapped-agent-runtime-template.md`
2. 对照 `arcreel/` 案例目录

### 如果你正在做通用 Agent Harness

优先看：

1. `super-agent-harness-design-template.md`
2. 对照 `deer-flow/` 案例目录

### 如果你想先建立 Agent 学习地图

优先看：

1. `agent-project-classification-map.md`
2. 再按地图选择对应案例和模板

## 使用原则

这里的模板不应该孤立使用，最好总是配合至少一个真实案例一起看。

推荐搭配方式：

- 工业模板 + `fault-diagnosis`
- 平台模板 + `ArcReel`
- SDK runtime 模板 + `ArcReel`
- Harness 模板 + `deer-flow`
- 分类总图 + 任意案例目录

这样你既能看到抽象方法，也能看到真实落地方式。

## 一句话记忆

`shared/` 负责沉淀“跨项目可复用的方法”，而具体项目目录负责沉淀“这些方法在真实项目里是怎么长出来的”。
