# Hermes Agent 项目分析

## Summary

- Project name: `hermes-agent`
- Project path: `D:\hermes-agent`
- Document type: `user`
- Purpose: systematize why Hermes Agent is worth studying as a long-running, self-improving, multi-surface agent system

## 一、先给结论：Hermes Agent 更像“长期运行型 Agent 工作台”

`hermes-agent` 不是单纯的 terminal coding assistant，也不是只会套一个 prompt 的多平台聊天机器人。

更准确的定位是：

> 一个把通用 Agent loop、长期记忆、技能沉淀、跨平台入口、计划调度、远程执行环境和研究训练能力放进同一底座里的长期运行型 Agent 工作台。

它最值得单独研究的地方，不是某一个点状 feature，而是它把下面这些原本常常分散在不同系统里的东西，尽量收进同一个 runtime：

- 交互式 CLI
- 多平台 messaging gateway
- 持久会话与跨会话搜索
- 内置与外置 memory provider
- 技能系统与 Skills Hub
- cron 调度
- subagent delegation
- MCP 接入
- 多种终端/沙箱后端
- trajectory / RL / Atropos 研究管线

这意味着它在回答的问题不是“Agent 会不会调用工具”，而是：

- Agent 能不能长期存在
- 能不能跨入口连续工作
- 能不能把经验沉淀成资产
- 能不能在真实产品与研究训练之间共用一套底座

## 二、它真正想解决的核心问题

Hermes Agent 的核心问题不是“单轮回答质量再高一点”，而是：

- 如何让 Agent 在多次会话之间保留长期价值
- 如何让 Agent 不只活在本地终端，而是同时活在 Telegram、Discord、Slack 等入口
- 如何让 Agent 不只是 react to request，而是能被定时任务和后台流程驱动
- 如何让 Agent 的“学会了什么”沉淀成 memory、skills、session history，而不是每次清零
- 如何让同一套底座既能服务日常使用，也能服务 trajectory 采集与 RL 训练

从仓库结构就能直接看出这种野心：

- `run_agent.py`
- `cli.py`
- `gateway/`
- `ui-tui/`
- `tui_gateway/`
- `cron/`
- `tools/`
- `skills/`
- `environments/`
- `tinker-atropos/`

这不是典型“小而专”的 agent 项目结构，而是明显在向一个综合工作台演进。

## 三、系统骨架：它至少有六层

### 1. Agent loop 核心层

核心主循环在 [run_agent.py](D:/hermes-agent/run_agent.py)。

从文件头和导入可以看出，它负责：

- 模型调用与 provider 兼容
- 工具 schema 注入
- 消息历史管理
- context compression
- prompt caching
- memory context 注入
- tool result 持久化与预算控制
- 子代理、浏览器、终端等资源清理

这说明 Hermes 的内核仍然是比较典型的 tool-calling agent loop，但它不是“裸 loop”，而是已经挂了很多运行时治理模块。

最重要的不是 loop 本身，而是它已经把：

- prompt builder
- memory manager
- context compressor
- usage pricing
- trajectory saving

都挂成了运行时的一部分。

也就是说，Hermes 不是把“对话”当成唯一对象，而是把“长期运行的一次次回合”当成更高层对象。

### 2. 入口层：CLI、Gateway、TUI、ACP 并存

Hermes 的一个很强信号，是它不是单一入口。

证据非常明确：

- `cli.py`：传统交互式 CLI
- `hermes_cli/`：命令、配置、setup、skills/tools 开关等 CLI 子系统
- `gateway/run.py`：多平台消息入口
- `gateway/platforms/`：Telegram、Discord、Slack、WhatsApp、Signal、Email 等平台适配
- `ui-tui/` + `tui_gateway/`：Node/Ink 前端 + Python JSON-RPC 后端的 TUI 体系
- `acp_adapter/`：ACP server，面向 VS Code / Zed / JetBrains 等编辑器接入

这和很多项目只做一个 CLI 或只做一个 Web app 很不一样。

Hermes 的设计思路更像：

> 不同入口只是“对同一 agent 底座的接入方式”，而不是不同产品各自复制一套 Agent 逻辑。

从 [gateway/run.py](D:/hermes-agent/gateway/run.py) 可以看到，它甚至会把 `config.yaml` 里的 terminal、auxiliary、agent、display、timezone、安全设置桥接进环境变量，让 gateway 运行环境和 agent runtime 尽量保持一致。

这类设计很值得学，因为它说明项目在认真处理：

- 多入口配置一致性
- 会话生命周期统一
- 不同表层 UI 背后复用同一 agent substrate

### 3. 长期记忆与会话检索层

Hermes 最强的差异化之一，是它明显把 memory 当成系统主轴，而不是附属 feature。

最关键证据在：

- `agent/memory_manager.py`
- `tools/memory_tool.py`
- `hermes_state.py`
- `hermes_cli/memory_setup.py`

[agent/memory_manager.py](D:/hermes-agent/agent/memory_manager.py) 很有代表性。它不是临时拼一段记忆 prompt，而是明确做了：

- builtin memory provider
- 最多一个 external memory provider
- provider tool schema 路由
- prefetch / queue_prefetch / sync_turn
- fenced memory-context 注入

这意味着 Hermes 已经把 memory 看成正式的 provider 层，而不只是两三个读写文件的 helper。

[hermes_state.py](D:/hermes-agent/hermes_state.py) 进一步说明了这一点：

- SQLite-backed session store
- FTS5 全文搜索
- session metadata + full message history
- source tagging（cli / telegram / discord 等）
- compression chain / parent_session_id

它在做的不是简单聊天记录，而是一个可跨入口、可搜索、可延续的会话知识层。

这和很多“只有当前上下文”的 agent 项目相比，最大的差异是：

- 它开始认真考虑跨会话 recall
- 开始把 session 当成长期资产
- 开始让 memory 与 transcript search 形成互补

这类系统更适合长期陪伴型 Agent，而不是一次性问答 agent。

### 4. Skills 不是提示词附件，而是可增长的程序性资产

Hermes 的另一个核心是 skills。

关键线索包括：

- `skills/`
- `optional-skills/`
- `hermes_cli/skills_hub.py`
- `tools.skills_hub` 相关调用
- README 对“self-improving AI agent”的描述

[hermes_cli/skills_hub.py](D:/hermes-agent/hermes_cli/skills_hub.py) 已经不是简单列目录，而是在做：

- 搜索多技能源
- inspect / install / browse
- trust/source 分类
- 统一 CLI 与 slash command 接口

这说明 Hermes 把 skill 当成一种：

- 可安装
- 可检索
- 可启停
- 可复用
- 可持续累积

的能力资产。

再结合 README 里“creates skills from experience”“skills self-improve during use”的定位，可以判断 Hermes 的设计目标不是只提供一批静态内置 skill，而是让 skill 成为 Agent 的长期学习介质。

这点非常值得和普通“system prompt + tools”项目区分开：

- 普通项目更多是在调一次任务
- Hermes 更像是在积累之后会反过来改变未来任务表现的 procedural memory

## 四、它最特别的一点：让 Agent 从“被问一次”变成“长期存在”

Hermes 很像在做一种“长期存在型 Agent”。

这个判断不是空泛的，因为它同时具备四个支撑件：

### 1. 跨入口持续存在

README 和 `gateway/platforms/` 已经说明它能同时活在：

- CLI
- Telegram
- Discord
- Slack
- WhatsApp
- Signal
- Email

这意味着 agent 不再绑定某个前端壳子。

### 2. 长期会话搜索与恢复

`hermes_state.py` 的 FTS5 session search 让它能回到过去，而不是每次靠用户重复解释背景。

### 3. 定时任务驱动

`cron/scheduler.py` 说明 Hermes 有内建调度器，而且还能把结果投递回 origin 或 home channel。

这件事非常重要，因为它把 agent 从：

- “等待用户输入”

推进到：

- “被时间触发”
- “被定期工作驱动”
- “天然适合日报、备份、巡检、周报这类场景”

### 4. 远程和持久终端环境

从 README 和 `tools/environments/` 能看到 Hermes 支持：

- local
- Docker
- SSH
- Daytona
- Singularity
- Modal

这不只是多后端，而是在回答“Agent 工作环境放在哪”。

特别是 Daytona / Modal 这种“空闲休眠、需要时唤醒”的方向，说明 Hermes 在把 Agent 从“本地笔记本助手”继续推进到“云上长期助手”。

## 五、子代理与并行化：它是认真做 delegation 的

`tools/delegate_tool.py` 不是薄薄一层 wrapper，而是相当正式的子代理机制。

从这个文件可以清楚看到：

- 子代理有独立上下文
- 子代理有独立 task_id
- 子代理有独立 terminal session
- 子代理可限制 toolset
- 默认禁止 recursive delegation、clarify、memory 写入、cross-platform side effect
- 有并发上限、超时、最大深度、orchestrator kill switch

这里最值得学的不是“它支持 subagent”，而是：

> 它把 delegation 当成一个需要治理边界、深度、并发、权限的正式运行时能力。

这说明 Hermes 对多 agent 的理解比很多项目成熟：

- 不是“会 spawn 就算支持”
- 而是要明确 child context、tool boundary、共享状态隔离和失败处理

## 六、MCP 与工具体系：它想做统一扩展总线

Hermes 的工具体系也不是简单散装集合。

关键证据：

- `model_tools.py`
- `toolsets.py`
- `tools/registry.py`
- `tools/mcp_tool.py`
- `tools/environments/`

[tools/mcp_tool.py](D:/hermes-agent/tools/mcp_tool.py) 很说明问题。它支持：

- stdio MCP
- HTTP / streamable HTTP MCP
- 自动重连
- credential stripping
- 环境变量过滤
- sampling/createMessage
- 动态 tool discovery

这说明 Hermes 已经把 MCP 视为一条正式能力总线，而不是“顺手再接几个外部工具”。

再结合 `toolsets.py` 和 README 里的 toolset/config 体系，可以看出 Hermes 的能力层分成了至少三块：

- 内置工具
- toolset 级能力组合
- MCP 外部扩展

这样的结构很利于长期演进，因为 runtime 不需要把所有能力都硬编码死。

## 七、研究取向很强：不是只做产品，也在做训练数据和 RL 底座

Hermes 最少见的一点，是它把“真实用户工作台”和“研究训练管线”放进了同一仓库。

证据很强：

- `batch_runner.py`
- `trajectory_compressor.py`
- `environments/`
- `tinker-atropos/`
- README 里的 trajectory generation / Atropos RL / compression 说明

`environments/README.md` 直接把它定位成 hermes-agent 和 Atropos 的集成层，用于：

- multi-turn tool-calling loops
- reward 计算
- 训练或评估数据流

这说明 Hermes 的一个重要价值在于：

> 它不是只关心“把 Agent 做出来”，还关心“如何把 Agent 运行轨迹再反馈给下一代模型训练”。

这条线非常适合研究型团队借鉴，因为它把：

- 真实工具调用
- 长序列交互
- 会话压缩
- 环境模拟
- RL 训练

串进了一个连续面。

## 八、它和已有案例最不一样的地方

如果把它和你前面已经沉淀的几个项目做粗粒度对比，大致可以这样理解：

- 相比 `claude-code-sourcemap`，Hermes 没那么聚焦“coding runtime 内核”，而更强调长期存在、跨入口和知识沉淀。
- 相比 `claude-code`，Hermes 更像社区驱动的长期 agent workbench，而不是 feature-flag 和产品治理导向的平台分支。
- 相比 `deer-flow`，Hermes 没那么强调 harness/app 形式化分层，但更强调真实使用层的 memory、gateway、skills、cron 和运行环境。
- 相比 `fault-diagnosis` 这类垂直工作流系统，Hermes 明显是通用底座，不是 SOP 优先的行业代理。

所以我会这样给它分类：

- 主标签：`long-running-agent`
- 次标签：`memory-first`
- 次标签：`platform-expansion`
- 次标签：`research-ready`

## 九、它最值得借鉴的几个方法论

### 1. 不要把 memory 只当“偏好记录”

Hermes 把 memory、session search、profiles、external provider 接口都放进一条线上，这比“记住几个用户喜好”成熟很多。

### 2. 让技能成为可增长资产，而不是一次性提示词

如果系统真的会长期运行，skill 应该是安装、复用、改进、沉淀的对象，而不是 prompt 里的静态段落。

### 3. 入口层可以很多，但底座最好统一

CLI、gateway、TUI、ACP 并存而不完全分叉，是它很值得学的工程选择。

### 4. 调度和长期环境会改变 Agent 的本质

一旦引入 cron、云端持久终端、跨入口 continuity，Agent 的定位就从“问答器”变成“工作体”。

### 5. 研究闭环最好从一开始就嵌进系统

trajectory、compression、Atropos integration 说明：如果未来想做 agent 训练或 eval，最好别把运行时和数据生成系统分家太早。

## 十、最后一句总结

如果只记一句话，我会建议记这个：

> `hermes-agent` 最值得学的，不是某个单点能力，而是它如何把 Agent 做成一个能长期运行、跨入口存在、沉淀记忆和技能、还能反哺研究训练的综合工作台。
