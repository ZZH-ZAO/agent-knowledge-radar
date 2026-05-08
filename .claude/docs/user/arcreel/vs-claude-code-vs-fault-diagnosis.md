# ArcReel、claude-code、fault-diagnosis 对比分析

## Summary

- Project name: ArcReel vs claude-code vs fault-diagnosis
- Project path: `D:\ArcReel`, `D:\claude-code`, `D:\fault-diagnosis`
- Document type: user
- Purpose: explain the difference between a productized Agent platform, a platform-expansion coding agent system, and a vertical industrial workflow agent, so future design choices can be made on the right abstraction layer

## 一、先给结论：这三个项目分别代表什么路线

如果要用最短的话概括这三个项目，我会这样分：

- `claude-code`：平台扩展型 Agent 系统
- `fault-diagnosis`：垂直工业工作流 Agent 系统
- `ArcReel`：产品化创作 Agent 平台

它们都不是“简单聊天机器人”，但系统重心完全不同。

### `claude-code`

更像：

- 一个在 Agent runtime 基础上继续平台化、产品化的 coding agent 系统

它最关心的是：

- runtime 能力怎么扩
- 功能怎么 gating
- 持续代理、团队协作、远程控制、观测等能力怎么进入系统

### `fault-diagnosis`

更像：

- 一个面向工业诊断的垂直工作流执行系统

它最关心的是：

- 诊断证据怎么形成
- 数据、知识、图表、报告怎么串成闭环

### `ArcReel`

更像：

- 一个把 Agent 编排嵌入创作工作台的产品平台

它最关心的是：

- Agent 如何服务完整的内容生产工作流
- 多供应商媒体能力如何平台化
- 长耗时生成任务如何工程化

## 二、三者最本质的区别是什么

### 1. `claude-code` 的中心是“Agent 平台能力”

也就是说，它的重心更偏：

- Agent 自身的操作系统
- 能力开放与控制
- 产品功能扩展

### 2. `fault-diagnosis` 的中心是“领域作业流程”

也就是说，它的重心更偏：

- 行业任务闭环
- 证据链
- 产出可信诊断结果

### 3. `ArcReel` 的中心是“产品工作台 + Agent 协同生产”

也就是说，它的重心更偏：

- 产品工作空间
- 项目状态
- 媒体后端平台
- Agent 作为其中的调度与协作层

这三个中心不同，会导致它们的所有工程选择都不一样。

## 三、Prompt 设计重点分别是什么

### `claude-code`

重点更偏：

- 行为边界
- 工具使用规则
- 平台能力约束
- 产品特性控制

它的 prompt 更像 runtime policy。

### `fault-diagnosis`

重点更偏：

- 标准诊断流程
- 工具选择规则
- 输出模板
- 不确定性声明

它的 prompt 更像工业 SOP。

### `ArcReel`

重点更偏：

- 产品身份
- 项目上下文
- 工作流边界
- 路径和工具安全约束

它的 prompt 更像应用级操作约束层。

所以如果总结成一句话：

- `claude-code`：prompt 管平台行为
- `fault-diagnosis`：prompt 管领域流程
- `ArcReel`：prompt 管产品协作上下文

## 四、Workflow 编排思路分别是什么

### `claude-code`

更偏：

- runtime query loop
- session compaction
- multi-agent / coordinator 能力扩展
- 长会话控制

也就是说，它的 workflow 重心更偏 Agent 内核如何运转。

### `fault-diagnosis`

更偏：

- get time
- todo planning
- diagnosis subagent
- KB / search 补证
- report output

也就是说，它的 workflow 重心更偏领域任务流水线。

### `ArcReel`

更偏：

- project stage detection
- orchestrator skill dispatch
- focused subagent
- user confirmation between stages
- async generation queue

也就是说，它的 workflow 重心更偏产品化创作流水线。

## 五、Memory 的差异最值得看什么

### `claude-code`

更适合看：

- 长会话
- 团队级和平台级记忆方向
- 持久代理相关思路

### `fault-diagnosis`

更适合看：

- checkpoint
- todo state
- session continuity

它是执行连续性导向。

### `ArcReel`

更适合看：

- session memory
- project state memory
- platform business memory

ArcReel 特别重要的一点是：

- 它把 memory 从“聊天记忆”扩展成“整个平台状态系统”

这是产品化 Agent 和一般 Agent 项目的巨大差异。

## 六、RAG / 知识层在三者里的角色

### `claude-code`

重点不在典型 RAG，而在 runtime / tool / workflow。

### `fault-diagnosis`

RAG 是重要补证层：

- 手册
- 故障码
- 处理步骤

### `ArcReel`

RAG 不是主轴，重点在：

- 项目状态
- skill instruction
- product context

这说明一个很重要的判断标准：

- 如果核心上下文来自结构化项目状态，RAG 就不一定是主轴
- 如果核心上下文来自文档知识和静态经验，RAG 才更可能成为主轴

## 七、Tool / 执行层最大的区别

### `claude-code`

更偏：

- coding tools
- system/runtime controls
- platform capability surfaces

### `fault-diagnosis`

更偏：

- SQL
- data analysis
- chart generation
- KB retrieval
- report generation

### `ArcReel`

更偏：

- skills / workflow control
- project file operations
- generation backends
- queue / worker execution

也就是说：

- `claude-code` 的工具偏 Agent 平台能力
- `fault-diagnosis` 的工具偏行业证据链
- `ArcReel` 的工具偏产品工作流 + 生成平台能力

## 八、哪一个最适合学“产品化”

如果说“产品化”有不同层次，那么：

### 学 Agent 平台产品化

优先看：

- `claude-code`

因为它更偏 Agent 产品能力扩展。

### 学行业工作流产品化

优先看：

- `fault-diagnosis`

因为它更偏行业任务闭环。

### 学完整工作台产品化

优先看：

- `ArcReel`

因为它真正把 Agent 放进了一个完整工作台体系里。

## 九、以后遇到新项目时应该和谁对比

### 如果新项目主要问题是：

- Agent 内核怎么做强

优先对比：

- `claude-code`

### 如果新项目主要问题是：

- 怎么把某个行业流程做成 Agent

优先对比：

- `fault-diagnosis`

### 如果新项目主要问题是：

- 怎么把 Agent 工作流做成产品平台和工作台

优先对比：

- `ArcReel`

## 十、最后一句话记忆

如果要用一句话记住三者差别，我建议记成这样：

> `claude-code` 教你怎么扩 Agent 平台，`fault-diagnosis` 教你怎么做行业闭环，`ArcReel` 教你怎么把 Agent 变成真正的产品工作台。
