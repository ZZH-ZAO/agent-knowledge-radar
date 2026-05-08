# 产品化 Agent 平台设计模板

## Summary

- Project name: productized-agent-platform-template
- Project path: `D:\claude-code-sourcemap\.claude\docs\user`
- Document type: user
- Purpose: provide a reusable design template for building productized Agent platforms, especially those that combine workflow orchestration, SDK runtime wrapping, async task execution, and multi-provider capabilities

## 一、这份模板适合什么项目

这份模板适合的不是所有 Agent 项目，而是这类项目：

- 你不只是想做一个聊天助手
- 你想做一个完整产品或工作台
- 你的 Agent 要和项目管理、任务系统、文件系统、配置系统、计费系统一起工作
- 你的任务可能很长、很重、需要后台执行

典型场景包括：

- 创作工作台
- Coding Agent 平台
- 设计生成平台
- 运营自动化工作台
- 多供应商 AI 工作空间

如果你做的是一个很轻量、很单点的 Agent，这份模板可能太重；但如果你想做一个真正可长期发展的 Agent 产品，这份模板很有参考价值。

## 二、先不要问“用哪个模型”，先问这六个问题

### 1. 这个系统到底是 Agent 产品，还是带聊天框的普通产品

这两者差别很大。

如果只是普通产品加聊天框，Agent 往往只是边缘功能。

如果是 Agent 产品，Agent 就会影响：

- 工作流
- 状态管理
- 数据结构
- 前端交互
- 后端架构

### 2. 你的核心状态存在聊天里，还是存在项目里

如果核心状态只在聊天历史里，系统会很脆。

成熟产品通常要把关键状态沉淀到：

- project.json
- 数据库
- 文件系统
- 任务系统

### 3. 你的长耗时能力要不要进入后台任务系统

如果回答是“要”，那就不能只靠 Agent 同步调用。

你要提前设计：

- queue
- worker
- cancel
- retry
- progress

### 4. 你是不是要支持多个模型/供应商

如果要，后端抽象必须前置做。

否则业务逻辑会和供应商 SDK 严重耦合。

### 5. 你的 Agent 交互是主界面，还是工作台中的一个面板

这会决定前端设计完全不同。

真正产品化的 Agent，往往不应该独占整个 UI。

### 6. 你的记忆是会话记忆，还是系统状态记忆

很多团队只想到前者，忽略后者。

产品化 Agent 更需要的是后者。

## 三、推荐的八层结构

### 1. 产品界面层

目标：

- 承载聊天、状态、资产、任务、配置、通知

设计建议：

- Agent 聊天界面只是工作台一部分
- 必须结合结构化面板
- 关键状态不要只通过聊天展示

### 2. API / 服务层

目标：

- 把不同业务域拆成明确接口

建议：

- 路由层只做协议和校验
- 业务逻辑进 services
- Agent 相关接口和普通产品接口分开

### 3. 应用级 Agent runtime 层

目标：

- 把底层 SDK 或模型事件转成产品可用会话系统

典型能力：

- session manager
- snapshot
- reconnect
- interrupt
- turn normalization
- stream projector

设计建议：

- 不要直接把底层 SDK 事件暴露给前端
- 一定要做一层应用级封装

### 4. Workflow orchestration 层

目标：

- 把任务拆成阶段
- 决定何时 dispatch skill / subagent / tool

设计建议：

- 工作流状态尽量从项目状态中恢复，而不是只靠聊天上下文
- 阶段切换尽量有确认协议
- subagent 只接收最小必要上下文

### 5. Tool / Skill 执行层

目标：

- 承担 Agent 直接操作能力

设计建议：

- 区分“真正需要 Agent 调用的能力”和“普通后端服务能力”
- Skill 更适合确定性流程
- Subagent 更适合聚焦推理任务

### 6. 后台任务系统层

目标：

- 承载长耗时和重资源任务

设计建议：

- 不要让 Agent 直接同步等待很重的任务
- 引入 queue / worker / lease / cancel / retry
- 进度和任务状态要可查询、可推送

### 7. 平台抽象层

目标：

- 隔离供应商、模型、计费和能力差异

设计建议：

- 为 image / video / text / search 等能力定义统一协议
- 业务逻辑不直接依赖某一家供应商 SDK
- 支持能力声明和兼容性判断

### 8. 系统状态层

目标：

- 保存产品真正的长期状态

至少应包括：

- session state
- project state
- task state
- usage state
- config state
- version state

## 四、产品化 Agent 的 workflow 应该分哪几层

### 1. 单轮 loop

模型、工具、继续推理。

### 2. 会话级 loop

创建、流式输出、恢复、打断、回放。

### 3. 项目级 loop

根据项目状态决定下一步工作阶段。

### 4. 后台任务 loop

任务入队、执行、重试、取消、完成。

### 5. 用户确认 loop

关键节点把结果展示给用户，再确认是否继续。

很多项目的失败点在于：

- 只实现了第一层
- 后面四层都没有真正设计

## 五、产品化 Agent 的 memory 应该怎么理解

不要只把 memory 理解成：

- 对话上下文

更应该拆成：

### 1. Session memory

保存会话过程。

### 2. Project memory

保存项目实体和进度。

### 3. Operational memory

保存任务、错误、调用轨迹、版本。

### 4. Knowledge memory

保存长期可复用知识、案例、规则。

真正成熟的平台，至少前 3 种都要有。

## 六、什么时候需要 SDK runtime wrapping

如果你满足下面任意几条，就建议在 SDK 上再包一层：

- 需要 reconnect
- 需要 snapshot
- 需要前端 patch/delta 更新
- 需要中断恢复
- 需要 pending question
- 需要转成统一 turn schema

换句话说：

- 只要你在做产品，而不是做实验，大概率就需要 wrapping

## 七、什么时候需要 queue / worker

如果任务具有这些特点，就应该上：

- 耗时长
- 外部依赖重
- 容易失败
- 需要并发控制
- 需要取消或恢复

典型如：

- 视频生成
- 批量图像生成
- 大规模文档处理
- 长时间代码任务

## 八、一个可直接套用的产品化 Agent 设计清单

### A. 产品目标

- 这个产品的核心工作对象是什么
- Agent 是主功能还是辅功能
- 最终交付物是什么

### B. 状态模型

- 核心状态存哪里
- 项目状态和会话状态如何区分
- 哪些状态需要长期保存

### C. Runtime

- 会话怎么创建
- 中断怎么处理
- 重连怎么处理
- 流式结果怎么投影给前端

### D. Workflow

- 工作流有哪些阶段
- 阶段如何检测
- 阶段之间是否需要确认
- subagent 负责什么

### E. 执行系统

- 哪些能力直接同步执行
- 哪些能力进入任务系统
- 重试与取消怎么处理

### F. 平台抽象

- 是否支持多供应商
- 供应商能力是否统一抽象
- 计费和能力差异如何处理

### G. 产品表面

- 聊天是否只是一个面板
- 是否有任务面板、资产面板、版本面板
- 是否有配置和观测入口

## 九、基于 ArcReel 得到的关键启发

如果以后你做类似 ArcReel 的系统，我最建议记住的是：

- Agent 不应该孤立存在，应该嵌入产品工作流
- 会话状态不够，项目状态更重要
- 长任务必须脱离同步 Agent 调用
- 供应商抽象越早做，后面越不痛苦
- SDK 之上的应用 runtime 几乎是必需品

## 十、最后一句话记忆

如果用一句话记住产品化 Agent 平台的设计重点，我建议记成这样：

> 产品化 Agent 的关键，不是让模型更像人，而是让 Agent 成为工作台、状态系统、任务系统和平台能力之间的协调层。
