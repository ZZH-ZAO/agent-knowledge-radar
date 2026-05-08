# DeerFlow、claude-code-sourcemap 与 claude-code 三方对比

## Summary

- Project name: DeerFlow / claude-code-sourcemap / claude-code
- Project path: `D:\deer-flow` / `D:\claude-code-sourcemap`
- Document type: user
- Purpose: 从“运行内核、通用底座、平台产品化”三种层次，对 DeerFlow、claude-code-sourcemap 与 claude-code 做系统对比，帮助建立更完整的 Agent 工程认知框架

## 一、先给总图：这三个项目分别代表 Agent 工程的三种重心

如果把这三个项目放在一条连续谱上，我会这样理解：

- `claude-code-sourcemap`
  更像 `Agent engine`
- `deer-flow`
  更像 `Agent harness`
- `claude-code`
  更像 `Agent platform`

这不是说谁高谁低，而是说它们在回答不同的问题。

### `claude-code-sourcemap` 在回答什么

它最像在回答：

> 一个 serious Agent 的执行内核，到底是怎么运转的？

重点是：

- query loop
- tool use 回流
- session compact
- memory 提取
- 多 Agent 协调

### `deer-flow` 在回答什么

它最像在回答：

> 如果我要给很多 Agent 场景提供一套通用运行底座，我该怎么设计？

重点是：

- harness / app 分层
- middleware-first runtime
- skills / MCP / sandbox / memory / subagent 的统一组织

### `claude-code` 在回答什么

它最像在回答：

> 当一个 Agent runtime 已经能跑以后，怎样把它做成一个可控制、可观察、可治理、可扩展的平台产品？

重点是：

- feature gating
- persistent / proactive direction
- platform surface
- 运营控制面
- 产品级能力投放

所以一句话总结：

- `claude-code-sourcemap` 教你看“发动机”
- `deer-flow` 教你看“底盘”
- `claude-code` 教你看“整车平台和控制系统”

## 二、从架构目标看：三者解决的问题完全不一样

### 1. `claude-code-sourcemap` 的目标最聚焦

它主要解决：

- 一个 coding agent 如何稳定地执行复杂任务

它不是特别关注：

- 平台控制面
- 通用 SDK 外放
- 生态扩展系统

它更像一个高质量内核样本。

### 2. `deer-flow` 的目标最偏通用化

它主要解决：

- 怎样做一个可复用、可配置、可自托管的 Agent Harness

所以它会天然更重：

- extensibility
- runtime composition
- sandbox
- skills
- MCP
- subagent infra

### 3. `claude-code` 的目标最偏平台化

它主要解决：

- 如何把已有 Agent 能力持续扩展成真实产品平台

所以它天然更重：

- 产品表面
- 能力投放节奏
- 风险控制
- 可观测性
- feature lifecycle

## 三、Prompt 设计对比：三者各自承担的职责不同

### `claude-code-sourcemap`

Prompt 更像：

- loop-level execution policy

它关心：

- 当前轮如何思考
- 如何用工具
- 如何继续执行
- 如何在会话和多 Agent 之间衔接

### `deer-flow`

Prompt 更像：

- runtime governance protocol

它关心：

- clarification first
- skill progressive loading
- subagent batching
- citation discipline
- working directory semantics
- outputs 交付语义

### `claude-code`

Prompt 更像：

- productized capability policy

它关心：

- 平台级能力如何被安全、可控地暴露
- 不同模式、功能、权限和方向如何协同

### 可以怎么学

如果你想学：

- Prompt 如何直接参与执行内核
  看 `claude-code-sourcemap`
- Prompt 如何成为运行时治理协议
  看 `deer-flow`
- Prompt 如何服务平台化投放与能力分层
  看 `claude-code`

## 四、Tool Calling 对比：从“执行回路”到“能力生态”再到“平台能力管理”

### `claude-code-sourcemap`

工具更偏：

- execution loop limb

也就是：

- 模型怎么调工具
- 工具结果怎么回流
- loop 怎么闭环

### `deer-flow`

工具更偏：

- capability stack

它把能力拆成：

- built-in tools
- skills
- MCP

这是很典型的 runtime substrate 视角。

### `claude-code`

工具更偏：

- managed platform capability

它更关注：

- 哪些能力要开放
- 怎么控制风险
- 怎么分阶段提供
- 怎么持续演化

### 三者连起来看

你可以把它们理解成：

- `claude-code-sourcemap`: 工具怎样参与执行
- `deer-flow`: 工具怎样组成生态
- `claude-code`: 工具怎样进入平台治理

## 五、Workflow 对比：三种不同层级的编排

### 1. `claude-code-sourcemap` 更偏执行链条编排

强项在：

- query loop
- session compact
- memory extraction
- coordinator / worker

它研究的是：

- Agent 如何持续跑下去

### 2. `deer-flow` 更偏 runtime 分层编排

强项在：

- middleware workflow
- subagent workflow
- run manager
- gateway / app workflow

它研究的是：

- 一个通用 Agent 系统如何分层运行

### 3. `claude-code` 更偏平台级编排

强项在：

- 平台控制流
- feature rollout
- capability gating
- 多能力协同

它研究的是：

- 一个 Agent 平台怎样稳定进化

## 六、Memory 对比：三种不同的记忆观

### `claude-code-sourcemap`

更强调：

- 运行中的上下文控制

关键词是：

- compact
- summarization
- extraction
- session continuity

### `deer-flow`

更强调：

- 结构化长期记忆

关键词是：

- user context
- history
- facts
- correction
- async update queue

### `claude-code`

更强调：

- 平台尺度上的长期方向、团队共享、持久状态

关键词是：

- platform memory direction
- persistent agent
- shared state

### 三者合起来

你可以把 memory 分成三种视角：

- 运行时记忆
- 用户长期记忆
- 平台持久记忆

这三个项目分别把其中一层做得比较突出。

## 七、Subagent / Multi-Agent 对比

### `claude-code-sourcemap`

重点是：

- 多 Agent 协同逻辑

### `deer-flow`

重点是：

- 子代理执行基础设施

包括：

- timeout
- cancellation
- thread pool
- polling
- trace_id

### `claude-code`

重点是：

- 多能力如何成为平台的一部分

也就是不只是“能协作”，还包括：

- 怎么被平台纳管
- 怎么与其他功能协同

## 八、Sandbox / Execution Environment 对比

### `claude-code-sourcemap`

当然也重执行，但不以“执行环境抽象系统”见长。

### `deer-flow`

这一层明显最强。

因为它：

- 明确有 sandbox provider abstraction
- 有 local 与 isolated 模式
- 有固定路径语义
- 有运行生命周期
- 有安全边界说明

### `claude-code`

更可能把执行环境放在平台能力与产品安全框架里考虑，而不是把它单独做成 DeerFlow 那样完整的抽象模块。

## 九、平台化程度对比：谁最像“产品平台”

### `claude-code-sourcemap`

平台化不是它的主目标。

### `deer-flow`

它是：

- 底座 + 参考应用

已经有平台气质，但重点仍然是“通用 runtime + app”

### `claude-code`

它最像真正的平台产品方向。

因为它更关注：

- capability lifecycle
- exposure control
- feature maturity
- product governance

所以如果你问：

- 谁最像 Agent 平台产品？

三者里是 `claude-code`。

如果你问：

- 谁最像 Agent 基础设施底盘？

三者里是 `deer-flow`。

如果你问：

- 谁最像 Agent 执行引擎剖面样本？

三者里是 `claude-code-sourcemap`。

## 十、你以后做架构参考时，应该怎么用这三者

### 场景 1：我要先搞懂 Agent 内核怎么工作

优先看：

- `claude-code-sourcemap`

### 场景 2：我要搭一套可复用、自托管、可扩展的 Agent runtime

优先看：

- `deer-flow`

### 场景 3：我的 runtime 已经能跑，我要把它做成产品平台

优先看：

- `claude-code`

### 场景 4：我要建立完整知识体系

推荐顺序：

1. `claude-code-sourcemap`
   先学引擎
2. `deer-flow`
   再学底盘
3. `claude-code`
   最后学平台

这个顺序最自然，因为它基本对应：

- engine
- substrate
- platform

## 十一、最后用一句话记住这组三角关系

如果只用一句话记住它，我建议记成这样：

> `claude-code-sourcemap` 让你看清 Agent 发动机怎么转，`deer-flow` 让你看清通用 Agent 底盘怎么搭，`claude-code` 则让你看清一个 Agent 系统如何继续长成真正的平台产品。
