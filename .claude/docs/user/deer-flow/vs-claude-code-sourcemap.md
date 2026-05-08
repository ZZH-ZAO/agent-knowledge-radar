# DeerFlow 与 claude-code-sourcemap 对比分析

## Summary

- Project name: DeerFlow / claude-code-sourcemap
- Project path: `D:\deer-flow` / `D:\claude-code-sourcemap`
- Document type: user
- Purpose: 对比 DeerFlow 与 claude-code-sourcemap 在 Agent runtime、Prompt、Tool Calling、Workflow、Memory、Sandbox、Subagent 与产品分层上的异同，并进一步讲清 DeerFlow 自己的 Harness 与 App 分层到底意味着什么

## 一、先给结论：这两个项目看起来都像“Agent 底座”，但它们想解决的问题并不完全一样

如果只看表面，你会觉得这两个项目很像：

- 都不是单一业务 Agent
- 都很重 runtime
- 都强调工具、状态、流程、上下文控制
- 都不是“一个 prompt + 几个 function calling”那么简单

但如果更深一层看，它们的设计重心其实不同。

### `claude-code-sourcemap` 更像什么

它更像：

> 一个围绕 coding agent 主循环而展开的“内核级运行机制样本”。

它最值得学的是：

- 单轮 query loop 怎么跑
- tool use 如何嵌回推理
- 会话如何 compact
- 多 Agent 是怎么协调
- memory 插入点在哪

也就是说，它更像在回答：

- 一个 serious coding agent 的“发动机”到底怎么工作

### `deer-flow` 更像什么

它更像：

> 一个可被别人复用、改造、部署和扩展的“Agent Harness”。

它最值得学的是：

- 如何把 runtime 做成可插拔系统
- 如何把 skills / MCP / sandbox / memory / subagent 统一纳入底座
- 如何让 runtime 与参考产品 App 分层

也就是说，它更像在回答：

- 如果我要给别人一套通用 Agent 底座，我应该怎样设计

所以一句话概括：

- `claude-code-sourcemap` 更偏 runtime engine study
- `deer-flow` 更偏 runtime platform substrate

## 二、最核心的结构区别：一个更像“引擎样本”，一个更像“底盘平台”

这是理解两者差异最重要的一点。

### 1. `claude-code-sourcemap` 的核心价值是“内核运行机制”

它的强项是：

- loop 很清楚
- 状态切分很细
- prompt 与 tool interaction 耦合得很紧
- compact、memory extraction、multi-agent 都围绕执行内核展开

这说明它的目标很集中：

- 把 agent engine 本身做扎实

### 2. `deer-flow` 的核心价值是“可扩展运行底座”

它的强项是：

- 能力模块多而且分层清楚
- 模型、skills、MCP、sandbox、memory、subagent 都可配置
- runtime 和 app 分开
- 更像一套可供别人二次开发的基础设施

这说明它的目标更外扩：

- 不是只把一个 agent 做强
- 而是把“做很多 agent / agent app 的底盘”做出来

### 3. 为什么会形成这种差异

因为这两个项目的目标函数不同。

`claude-code-sourcemap` 更关心：

- 这台 agent 现在怎么跑得更稳

`deer-flow` 更关心：

- 未来别人怎么基于这套东西搭不同系统

所以前者更像“发动机剖面图”，后者更像“整车平台架构”。

## 三、Prompt 设计对比：一个更偏执行内核约束，一个更偏运行时治理协议

### 1. `claude-code-sourcemap` 的 Prompt 更像 engine policy

它更强调：

- 当前回合如何执行
- 何时该用工具
- 何时该停
- 如何处理 memory、workflow 和 multi-agent

Prompt 的核心价值是：

- 让 Agent loop 稳定运转

### 2. `deer-flow` 的 Prompt 更像 runtime governance

DeerFlow 的 prompt 明显承担更多系统治理职责：

- clarification first
- skills progressive loading
- subagent batching policy
- citation 规范
- working directory 语义
- outputs 交付规范
- memory 注入

它不是只在告诉模型“怎么回答”，而是在告诉模型：

- 你在怎样一个操作系统里工作

### 3. 两种设计分别适合什么目标

如果你的目标是：

- 深度优化一个核心 Agent 的执行质量

那么 `claude-code-sourcemap` 这类 prompt 设计更适合。

如果你的目标是：

- 让很多任务、很多能力、很多扩展方式都能在同一个底座里被统一约束

那么 DeerFlow 这种 prompt 治理层会更适合。

## 四、Tool Calling 对比：一个强调 loop 内工具协作，一个强调能力生态分层

### 1. `claude-code-sourcemap` 的 tool 思维

它更像：

- tool 是 agent loop 的执行手臂
- 重点是模型与工具之间的回路闭合

它最值得看的是：

- tool result 怎么回流到推理
- query loop 怎么在多次工具调用后继续稳定收敛

### 2. `deer-flow` 的 tool 思维

它明显不是只把 tool 当 function call。

它把能力拆成三层：

- built-in tools
- skills
- MCP

这意味着 DeerFlow 的问题意识是：

- 真正的 Agent 能力不只是“多几个函数”
- 还包括任务知识模块和外部能力接入协议

### 3. 哪种更强

不能简单说谁更强，而是强在不同层。

`claude-code-sourcemap` 强在：

- tool loop 的执行内核

`deer-flow` 强在：

- tool ecosystem 的平台组织方式

## 五、Workflow 编排对比：一个重“执行链条”，一个重“能力中间层”

### 1. `claude-code-sourcemap` 的 workflow 更像主循环编排

它的 workflow 重点在：

- 单轮 query loop
- session compact
- stop hooks
- post-compact cleanup
- background memory extraction
- multi-agent coordinator / workers

也就是说，它在研究：

- 一个 Agent 如何持续跑下去

### 2. `deer-flow` 的 workflow 更像运行时分层编排

它的 workflow 至少分成：

- middleware workflow
- subagent workflow
- run manager workflow
- app / gateway workflow

它在研究：

- 一个复杂 Agent 平台里，各层分别承担什么职责

### 3. 这意味着什么

`claude-code-sourcemap` 适合学：

- agent engine 内部流程

`deer-flow` 适合学：

- agent platform 分层流程

## 六、Memory 对比：一个强调会话过程中的内存控制，一个强调长期记忆系统

### 1. `claude-code-sourcemap` 的 memory 更偏运行态上下文管理

它更强调：

- 何时 compact
- 何时提取 memory
- 何时 dream / summary
- 如何维持长对话可继续

它关注的是：

- 上下文窗口里的记忆管理

### 2. `deer-flow` 的 memory 更偏长期记忆工程

DeerFlow 明显做了更完整的长期记忆结构：

- user context
- history
- facts
- correction / reinforcement
- async debounce queue
- memory injection token budget

它关注的是：

- 用户与系统长期关系如何沉淀

### 3. 两者的适用场景

如果你要优化：

- 长对话 / 长执行过程中的上下文稳定性

`claude-code-sourcemap` 的 memory 视角更适合。

如果你要优化：

- 多次会话之间的长期个性化和经验沉淀

DeerFlow 的 memory 视角更适合。

## 七、Subagent 对比：一个更像多 Agent 协同机制，一个更像受管控执行单元

### 1. `claude-code-sourcemap` 的多 Agent 更偏 orchestration logic

重点是：

- coordinator
- workers
- mailbox / notification / task state

它更像在研究：

- 多 Agent 如何协作解决问题

### 2. `deer-flow` 的 subagent 更偏 execution infrastructure

对应实现里能看到：

- executor
- thread pool
- timeout
- cancellation
- polling
- status
- trace_id

这意味着它不只是有子代理概念，而是把子代理当成正式的执行资源。

### 3. 这两种思路的本质区别

`claude-code-sourcemap` 更强调：

- 多 Agent 的“协同逻辑”

`deer-flow` 更强调：

- 多 Agent 的“运行管理”

## 八、Sandbox 与执行环境：DeerFlow 明显更强

这是两者差异非常明显的一层。

### `claude-code-sourcemap`

它当然也重视工具和执行，但重点不是把“执行环境抽象层”单独做强。

### `deer-flow`

它明确有：

- sandbox provider abstraction
- local / aio sandbox
- 虚拟路径语义
- 执行环境生命周期
- host bash 风险边界

这说明 DeerFlow 的目标更像：

- 做一个真正的 Agent execution substrate

如果你以后要做：

- 文件操作很多
- shell 操作很多
- 多任务隔离很多

DeerFlow 这部分非常值得借鉴。

## 九、DeerFlow 自己最重要的概念：Harness 与 App 分层到底是什么意思

这是 DeerFlow 特别值得学的一点，也很容易被看干巴巴。

我把它用最直白的方式解释一下。

### 1. Harness 是什么

Harness 可以理解成：

> 一套 Agent 运行时底座。

它负责的是：

- agent 怎么创建
- 工具怎么挂载
- skill 怎么发现和注入
- MCP 怎么接入
- memory 怎么更新和注入
- subagent 怎么执行
- sandbox 怎么隔离
- run 怎么管理

换句话说，Harness 回答的是：

- 这套 Agent 系统怎么运转

### 2. App 是什么

App 可以理解成：

> 把这套底座包装成一个用户真正能打开来用的产品。

它负责的是：

- 前端工作台
- threads
- artifacts
- skills 管理页面
- MCP 配置页面
- 上传与展示流程
- 部署、反代、gateway API

换句话说，App 回答的是：

- 用户怎么用这套系统

### 3. 为什么这种分层很重要

很多 Agent 项目最大的问题是：

- runtime 和 product 写死在一起

这样做短期快，但长期问题很多：

- 换一个前端很难
- 嵌入别的系统很难
- 抽 SDK 很难
- 复用能力很难

DeerFlow 通过 Harness / App 分层，解决的是：

- 运行底座可以复用
- 参考产品可以演示最佳实践
- 别人可以只拿 Harness，也可以整套拿 App

### 4. 为什么这比一般“有个前后端”更高级

因为这里不是普通意义的前后端分离。

它是：

- runtime substrate
- reference product surface

的分离。

也就是说，DeerFlow 不只是分成了“前端”和“后端”，而是分成了：

- 平台底盘
- 产品表达

这是一种更有平台思维的设计。

## 十、如果我要做 Agent 项目，什么时候该参考谁

### 1. 优先参考 `claude-code-sourcemap`

当你的问题是：

- Agent 单轮 loop 怎么设计
- tool use 如何回流推理
- session compact 怎么做
- memory 插入点怎么找
- 多 Agent 协调逻辑怎么组织

### 2. 优先参考 `deer-flow`

当你的问题是：

- 我想做一套通用 Agent 底座
- skills、MCP、sandbox、memory 怎么分层
- 如何做可配置、自托管、可扩展 runtime
- runtime 与 app 应该怎么拆
- 子代理如何工程化执行

### 3. 两者一起参考

最好的方式其实不是二选一，而是：

- 用 `claude-code-sourcemap` 学“运行内核”
- 用 `deer-flow` 学“平台底盘”

这两个合起来，才更像一个完整的 Agent 工程知识图谱。

## 十一、最后用一句话记住这组对比

如果只用一句话记住它，我建议记成这样：

> `claude-code-sourcemap` 更像让你看清 Agent 发动机怎么转，`deer-flow` 更像让你看清整套 Agent 底盘怎么搭，而 DeerFlow 的 Harness / App 分层，则是在告诉你怎样把底盘和整车分开设计。
