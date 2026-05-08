# Super Agent Harness 设计模板

## Summary

- Project name: Super Agent Harness design template
- Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared`
- Document type: shared template
- Purpose: 为以后分析或设计通用 Agent Runtime / Harness / Reference App 项目提供统一思考模板，避免只停留在功能罗列层

## 一、这个模板是用来分析什么项目的

这个模板适合分析下面这类项目：

- 通用 Agent runtime
- super agent harness
- agent substrate
- reference app built on runtime
- 自托管 Agent 平台底座

它不主要适合：

- 单一行业工作流 Agent
- 单个业务闭环产品
- 纯 RAG 系统

因为这类项目的关键问题通常不是：

- 这个业务流程怎么走

而是：

- 这套 Agent 底座怎样承载很多能力和很多工作流

## 二、先问四个根问题

在分析任何 super agent harness 之前，先回答这四个问题。

### 1. 它到底在卖什么

常见答案可能是：

- Agent engine
- Agent runtime
- Agent harness
- Agent platform
- Agent app

一定要区分清楚：

- 它是“运行底座”
- 还是“建立在底座之上的产品”
- 或者两者都有，但做了分层

### 2. 它最强的创新层在哪

常见可能在：

- runtime loop
- middleware system
- tools / skills / MCP
- sandbox
- memory
- subagent orchestration
- app layer

不要平均用力。一定要判断：

- 真正最有价值的是哪一层

### 3. 它围绕什么目标做这些设计

每个做法都要追问：

- 这样设计是在解决什么问题
- 为什么不用更简单的方案

### 4. 它更适合被当成什么参考

例如：

- 内核参考
- 底座参考
- 平台参考
- 产品参考

## 三、建议的分层分析框架

分析时建议至少按下面八层去看。

### 1. Product Layer

看什么：

- 是否有 reference app
- 是否有工作台、threads、artifacts、settings、管理面
- runtime 和 product 是否分层

关键问题：

- 用户看到的是产品，还是只是 runtime API

### 2. Runtime Core Layer

看什么：

- lead agent / main agent 怎么创建
- state schema 是什么
- loop 是怎么构成的
- config 怎样进入 runtime

关键问题：

- 这套系统的“发动机”在哪里

### 3. Prompt Governance Layer

看什么：

- prompt 在塑造人格，还是在塑造运行规则
- 是否承担澄清、文件语义、技能加载、引用规范、输出协议等职责

关键问题：

- prompt 是写作模板，还是运行时治理层

### 4. Middleware / Hook Layer

看什么：

- 有没有 middleware chain
- 哪些能力被做成中间层
- 顺序是否重要

关键问题：

- 系统行为是分层插入的，还是硬写在主 loop 里

### 5. Capability Ecology Layer

看什么：

- built-in tools
- skills
- MCP
- plugin / extension

关键问题：

- 能力是“函数集合”，还是“生态分层”

### 6. Execution Environment Layer

看什么：

- sandbox abstraction
- local / remote / container 模式
- 文件路径语义
- 安全边界

关键问题：

- Agent 只是在说，还是有真正可管理的执行环境

### 7. Memory Layer

看什么：

- session memory
- long-term memory
- structured facts
- update queue
- injection policy

关键问题：

- 系统到底把什么当成“值得长期记住的内容”

### 8. Subagent / Workflow Layer

看什么：

- subagent 是否只是 prompt trick
- 是否有正式执行基础设施
- timeout / cancellation / polling / status / trace 是否完备

关键问题：

- 多 Agent 是概念，还是工程系统

## 四、每一层都要追问的五个问题

对每一层都用这五个问题追问，会比单纯列模块有价值很多。

### 1. 这一层的目标是什么

不要只说“它有 memory”。
要说：

- 它为什么要有这层
- 这层是为了降低什么风险、提高什么能力

### 2. 它是怎么实现的

要尽量落到：

- 关键文件
- 关键组件
- 关键数据结构

### 3. 为什么这种做法更好

一定要和替代方案比较。

例如：

- 为什么用 middleware，不直接写死在主逻辑里
- 为什么用 skill，不直接堆 prompt
- 为什么要有 run manager，不直接每次都新跑

### 4. 它适合什么新场景

这一层能支持未来什么扩展。

例如：

- skills 层可以支持第三方能力包
- sandbox 层可以支持更多隔离环境
- memory 层可以支持长期个性化

### 5. 它在哪些场景会显得不够

任何做法都有边界。

例如：

- prompt 太重会难维护
- middleware 太多会难调试
- sandbox 太复杂会提高部署门槛

## 五、推荐输出结构

写分析文档时，推荐按下面结构组织：

1. 先给结论：这个项目到底是什么
2. 它真正解决的核心问题是什么
3. 系统分层
4. Prompt 设计
5. Tool / Skill / MCP / Plugin
6. Workflow 编排
7. Memory
8. Sandbox / Execution
9. 最值得学的亮点
10. 边界与不足
11. 适合作为哪类项目参考
12. 一句话总结

## 六、和其他模板怎么区分

这个模板与其他案例模板的关系可以这样理解：

- `industrial-agent-design-template`
  更适合行业工作流 Agent
- `productized-agent-platform-template`
  更适合产品化 Agent 平台
- `sdk-wrapped-agent-runtime-template`
  更适合“在已有 SDK 上包一层应用 runtime”
- `super-agent-harness-design-template`
  更适合“通用 Agent 底座 / Harness / Runtime substrate”

## 七、最后一句话怎么记

如果只用一句话记住这个模板，我建议记成这样：

> 分析 Super Agent Harness 时，最重要的不是它“有什么功能”，而是它把 Prompt、Runtime、Middleware、Skills、MCP、Memory、Sandbox、Subagent 和 App 分层成了怎样一套可复用的底座。
