# DeerFlow 项目分析

## Summary

- Project name: DeerFlow
- Project path: `D:\deer-flow`
- Document type: user
- Purpose: 系统分析 DeerFlow 作为一个“Super Agent Harness + Reference App”项目，如何在 Agent runtime、Prompt、Tool Calling、Skills、MCP、Memory、Sandbox、Subagent 与产品工作台之间完成分层与协同

## 一、先给结论：DeerFlow 到底是什么

DeerFlow 不是一个单功能垂直 Agent，也不是一个只会跑 Deep Research 的工作流脚本。

它更准确的定位是：

> 一个面向长任务、多工具、多子代理、多运行环境的通用 Super Agent Harness，并且同时给出了一套建立在这个底座之上的参考应用。

它自己官方文档已经把这个区别讲得很清楚：

- `Harness`
  是运行时底座、Python SDK、可复用核心能力
- `App`
  是基于 Harness 搭出来的最佳实践产品实现

这意味着 DeerFlow 最值得学的地方，不是某一个具体业务流程，而是：

- 如何把 Agent 做成一个“可编排运行时”
- 如何把产品层和 runtime 层明确分开
- 如何让 skill、memory、sandbox、MCP、subagent 成为可插拔能力

如果把它放进案例库，我会这样给它分类：

- 主标签：`runtime-first`
- 次标签：`platform-expansion`
- 次标签：`tool-runtime`
- 次标签：`memory-first`

它和 `claude-code-sourcemap` 的共同点是都非常重 runtime。

但 DeerFlow 更进一步的地方在于：

- 它想做的是一个“通用 Agent Harness”
- 不只面向 coding 场景
- 不只面向单一宿主
- 更强调可配置、可自托管、可插拔、可扩展生态

## 二、它真正解决的核心问题是什么

DeerFlow 真正解决的问题不是“模型怎么多回答一点”，而是：

- 当一个 Agent 需要长期运行、做复杂任务、调很多工具时，底座应该怎样组织
- 当系统里有 skill、MCP、sandbox、subagent、memory、file system 时，谁负责注入、谁负责管理、谁负责隔离
- 当要把 Agent 做成真正能部署的应用时，线程、artifact、stream、run、gateway、前端界面怎么协同
- 当开发者想自己扩展能力时，怎样做到少改核心代码也能加新 skill、新模型、新 MCP server、新 channel

所以 DeerFlow 的目标不是“做一套固定工作流”，而是：

> 做一套能承载很多工作流、很多模型、很多工具组合方式的 Agent 运行底座。

这和 `fault-diagnosis`、`career-ops` 这类项目明显不同：

- 那些项目更重“业务流程怎么编码”
- DeerFlow 更重“任何业务流程可以依赖什么运行骨架”

## 三、系统分层：DeerFlow 至少有六层

### 1. 产品入口层：Nginx + Frontend + Gateway + LangGraph Server

对应实现和文档：

- `backend/docs/ARCHITECTURE.md`
- `frontend/`
- `backend/app/gateway/`

DeerFlow 的产品入口不是单体，而是分成了几层：

- Nginx
  做统一反向代理入口
- Frontend
  做 DeerFlow App 的工作台界面
- Gateway API
  做 REST 管理面，例如模型、技能、MCP、上传、artifact、thread cleanup
- LangGraph Server
  做真正的 agent runtime

为什么这样分层更好：

- Agent runtime 和产品管理面不是一回事
- 前者更关注线程、流、状态、推理
- 后者更关注配置、资源、文件、生态管理

这是一种很成熟的系统设计：

- 把“会跑 Agent”与“可作为产品管理和交付”拆开

### 2. Runtime 核心层：Lead Agent + Middleware Chain

对应实现：

- `backend/packages/harness/deerflow/agents/lead_agent/agent.py`
- `backend/packages/harness/deerflow/agents/lead_agent/prompt.py`

这是 DeerFlow 最核心的一层。

它的主入口是 `make_lead_agent`，做的事情包括：

- 解析运行时配置
- 决定模型
- 决定是否 thinking mode
- 决定是否 plan mode
- 决定是否启用 subagent
- 构建 middleware 链
- 绑定工具
- 拼装 system prompt

最值得注意的是它不是把所有逻辑写进 agent body，而是高度依赖 middleware。

middleware 链里可以看到这些能力：

- summarization
- todo
- token usage
- title
- memory
- view image
- deferred tool filter
- subagent limit
- loop detection
- clarification

这反映出 DeerFlow 的设计哲学：

> Agent 不是一个 prompt + tool 的单层体，而是一条按职责拆开的可插拔处理链。

为什么这种结构更好：

- 新能力更容易插入
- 某些能力可以按模式启停
- 更适合大型项目长期演进

这也有代价：

- 中间件多了以后，整体调试复杂度会上升
- 很容易出现“某个行为到底是哪层做的”理解门槛

## 四、Prompt 设计：DeerFlow 的 Prompt 不是在塑造人格，而是在塑造运行规则

对应实现：

- `backend/packages/harness/deerflow/agents/lead_agent/prompt.py`

DeerFlow 的 system prompt 很长，但它的功能非常清晰，不是为了文学性，而是为了 runtime governance。

我会把它分成六块理解。

### 1. 角色层

Prompt 明确说明：

- 你是一个 super agent
- 你可以有 agent-specific soul
- 你可能带 memory context

这意味着 DeerFlow 支持：

- 默认 lead agent
- 自定义 agent persona
- 按 agent_name 注入不同 soul 和 memory

### 2. Clarification First 规则层

它把“先澄清再执行”写成了非常强的硬规则。

例如：

- 信息缺失要先问
- 需求歧义要先问
- 存在多种实现路径要先问
- 有破坏性操作要先确认

为什么这样做好：

- 通用 Agent runtime 最怕“自作主张”
- 对真实用户任务来说，错方向比慢一步更糟

### 3. Skill 注入层

Prompt 会动态注入当前可用 skills，并要求：

- 任务命中 skill 时先读 `SKILL.md`
- 按 progressive loading 模式读引用资源

这说明 DeerFlow 把 skill 当成：

- 一种可动态装配的“任务知识模块”

而不是死写在代码里的规则。

### 4. Subagent 编排层

Prompt 会在启用 subagent 时注入完整的 subagent policy：

- 什么时候该拆任务
- 什么时候不该拆
- 每轮最多多少个 task call
- 如果任务超过并发上限应该怎么分 batch

这很关键，因为多 Agent 不是“能调 task 就算完成”，而是要告诉模型：

- 什么情况下拆
- 拆多少
- 怎么分批
- 怎么收敛

### 5. Citation 与 Research 输出层

Prompt 强制要求：

- 用 web search 时要带 citation
- 研究类输出要带 sources section

这说明 DeerFlow 对 research 场景的理解已经不只是“查了就行”，而是开始关注：

- 证据可追溯
- 输出可复查

### 6. Working Directory 与文件交付层

Prompt 明确规定了：

- uploads
- workspace
- outputs

分别是什么用途。

这意味着它不是只把工具给模型，而是把“文件工作空间语义”也给模型了。

这会显著提升 Agent 的稳定性，因为模型知道：

- 临时工作放哪里
- 用户上传的东西在哪里
- 最终交付物必须放哪里

## 五、Tool Calling / Skill / MCP：DeerFlow 的真正亮点是能力层做成了统一生态

对应实现：

- `backend/packages/harness/deerflow/tools/`
- `backend/packages/harness/deerflow/skills/`
- `backend/packages/harness/deerflow/mcp/`

DeerFlow 最强的地方之一，是它没有把“能力”只理解成函数调用，而是分成了三层。

### 1. Built-in Tools

这是最基础的一层，包含：

- 文件读写
- bash
- view_image
- clarification
- present_file
- task
- tool_search

这些工具构成 Agent 的基本行动能力。

### 2. Skills

skill 不是工具，而是能力说明书。

`skills/loader.py` 里可以看到它会：

- 扫描 `skills/public` 与 `skills/custom`
- 解析 `SKILL.md`
- 读取 enabled 状态
- 让 prompt 动态暴露这些 skill

这意味着 DeerFlow 把 skill 做成了：

- 可加载
- 可启停
- 可公开/可自定义
- 可通过文档和资源渐进注入

为什么这样更好：

- 很多复杂任务不是少一个工具，而是少一套操作范式
- skill 恰好用来承载“这类任务应该怎么做”

### 3. MCP Servers

DeerFlow 支持从 `extensions_config.json` 加载 MCP。

这意味着外部能力接入不是硬编码，而是配置化。

支持的意义很大：

- 让 DeerFlow 可以接数据库、浏览器、GitHub、搜索、内部系统
- 保持核心 runtime 不必知道每个集成细节

从工程角度看，这比“自己把所有外部工具写死在代码里”更可持续。

## 六、Workflow 编排：DeerFlow 至少发生在五个层面

### 1. 单轮 Agent Loop

这是最基础的一层：

- 模型读取 prompt 和状态
- 调用工具
- 继续推理

这层和多数 Agent runtime 类似。

### 2. Middleware Workflow

这是 DeerFlow 非常有代表性的一层。

一轮请求进来，不是直接交给模型，而是先过 middleware pipeline：

- thread data
- uploads
- sandbox
- summarization
- todo
- title
- memory
- view image
- clarification

这说明 DeerFlow 把许多“传统上散落在业务代码里的行为”标准化成了 workflow hook。

### 3. Subagent Workflow

对应实现：

- `subagents/executor.py`
- `tools/builtins/task_tool.py`

这层很值得学。

它不是简单调用子 Agent，而是：

- 有独立配置
- 可继承或切换模型
- 可过滤工具
- 有自己的执行线程池
- 有 timeout
- 有 status
- 有 polling
- 有 cancellation
- 有 trace_id

也就是说，DeerFlow 的 subagent 已经不是一个 prompt trick，而是一个正式的执行子系统。

### 4. Run 管理层

对应实现：

- `runtime/runs/manager.py`

这一层解决的问题是：

- 一个 thread 上同时能不能跑多个 run
- 多任务策略是 reject、interrupt 还是 rollback
- 用户断开后 run 如何处理

这说明 DeerFlow 不只关注“能不能跑”，也关注：

- run lifecycle
- run cancellation
- multitask policy

这对产品化 Agent 很重要。

### 5. App / Gateway Workflow

DeerFlow App 还围绕 runtime 做了一层产品工作流，例如：

- skills 管理
- 模型管理
- MCP 配置
- artifact 提供
- thread cleanup

这让 DeerFlow 从 runtime 升级成了可操作系统。

## 七、Memory：DeerFlow 的 memory 是认真做过的一层

对应实现：

- `agents/memory/prompt.py`
- `agents/memory/updater.py`
- `agents/memory/queue.py`

这一层很值得专门讲，因为 DeerFlow 明显不满足于“把聊天历史直接塞 prompt”。

### 1. Memory 不是即时上下文，而是长期记忆

它会把 memory 分成：

- user context
- history
- facts

而不是只存一串对话。

### 2. Memory 更新是异步队列式的

`queue.py` 里可以看到：

- 有 debounce
- 同线程更新会合并
- 后台批量处理

为什么这样更好：

- 避免每轮都同步更新 memory，拖慢主流程
- 减少重复写
- 更适合高频对话

### 3. Memory 更新不是简单摘要，而是结构化反思

`MEMORY_UPDATE_PROMPT` 要求模型识别：

- 用户背景
- 当前关注点
- 长期历史
- fact
- correction
- reinforcement

特别值得注意的是 correction 机制：

- 如果模型之前错了
- 或用户明确纠正了方向
- 它会尝试把“正确做法”沉淀成 memory fact

这很有启发性，因为它说明 memory 不只是“记住用户是谁”，还可以记住：

- 以后不要再犯什么错

### 4. 它也明确排除无价值记忆

例如：

- 文件上传事件不应该进入长期记忆

这说明 DeerFlow 在做 memory hygiene，也就是：

- 不是所有上下文都值得记

## 八、Sandbox：这是 DeerFlow 把 Agent 从聊天提升为执行系统的关键

对应实现：

- `sandbox/middleware.py`
- `sandbox/`
- `community/aio_sandbox/`

DeerFlow 的 sandbox 设计很成熟，因为它不只提供一个 bash tool，而是把执行环境单独抽象出来。

### 1. 它有 provider abstraction

至少有：

- `LocalSandboxProvider`
- `AioSandboxProvider`

这样做的目标是：

- 开发时可以本地运行
- 生产时可以走更隔离的容器/远端执行

### 2. 它把路径语义也固定了

例如：

- `/mnt/user-data/workspace`
- `/mnt/user-data/uploads`
- `/mnt/user-data/outputs`
- `/mnt/skills`

这会让 Agent 的文件操作更稳定，也更便于不同 provider 对齐行为。

### 3. 它把安全边界当成显式设计问题

README 和架构文档都反复强调：

- 本地 bash 默认不安全
- 生产建议隔离执行
- 不正确部署会带来明显安全风险

这一点比很多 Agent 项目成熟，因为很多项目默认把“能执行命令”当卖点，但 DeerFlow 会明确告诉你：

- 这是高权限能力
- 不加边界很危险

## 九、DeerFlow 最值得学的亮点

### 1. Harness 与 App 分层非常清楚

这是它最关键的设计亮点之一。

很多项目要么只有 runtime，没有产品；
要么只有产品，没有清晰底座。

DeerFlow 同时给出了：

- 底座
- 参考应用

### 2. Middleware 化 runtime 很成熟

这意味着它的可扩展性比很多“硬写在 agent loop 里的功能”强得多。

### 3. Skill / MCP / Tool 三层生态很完整

这让能力扩展不依赖改核心代码。

### 4. Memory 是结构化、异步、可演进的

不是简单聊天摘要，而是真正在做长期记忆系统。

### 5. Subagent 是正式执行系统，不是玩具

它有线程池、轮询、取消、超时、trace，这些都是工程化信号。

### 6. Sandbox 做成了真正的运行环境

这让 DeerFlow 更像“Agent 操作系统”，而不是聊天工具。

## 十、它的边界与潜在欠缺

### 1. 系统复杂度很高

DeerFlow 的优点和代价几乎是同一件事。

因为它想做通用 harness，所以它天然会有：

- 更多配置
- 更多中间层
- 更多运行模式
- 更高理解门槛

### 2. Prompt 规则非常重

这能带来稳定性，但也会提高维护成本和迁移成本。

### 3. LangGraph 依赖仍然比较深

虽然 DeerFlow 做了很多自己的封装，但它的 agent runtime 仍然明显建立在 LangGraph / LangChain 生态之上。

这意味着：

- 上手快
- 生态好

但也意味着：

- 某些设计会受底层宿主约束

### 4. 更像底座，不像业务案例

如果你想学“某个行业 Agent 是怎么解决业务问题的”，DeerFlow 不是最佳案例。

它更适合回答：

- 我应该怎样搭通用 Agent 运行时

## 十一、如果把它放进案例库，最适合拿来学什么

我会把 DeerFlow 作为下面这些问题的参考样本：

- 怎么设计一个通用 Super Agent Harness
- 怎么把 prompt、tools、skills、memory、subagents、sandbox 组织成统一 runtime
- 怎么做 middleware-first 的 Agent runtime
- 怎么做可插拔技能生态和 MCP 生态
- 怎么把 runtime 和 app 明确拆层
- 怎么让 Agent 项目具备自托管、可配置、可扩展特征

它不太适合作为这些问题的最佳样本：

- 行业垂直工作流如何编码
- 单一业务闭环如何优化
- 极简 agent loop 如何实现

## 十二、最后用一句话记住 DeerFlow

如果只用一句话记住它，我建议记成这样：

> DeerFlow 不是一个具体任务型 Agent，而是一套把 prompt、skills、tools、MCP、memory、sandbox、subagents 和产品工作台组织成统一运行底座的 Super Agent Harness。
