# 如何从 0 到 1 复刻一个类似 Claude Code 的 Agent 平台

## 0. 这份文档的目标

这不是“评价 Claude Code 做得怎么样”的文档，而是一份实施路线文档。

它回答的问题是：

- 如果我要从零开始做一个类似的 Agent 平台，应该先做什么，后做什么？
- 哪些能力是 MVP 必需，哪些能力应该延后？
- 每一阶段的重点设计目标是什么？
- 到了什么场景，系统会逼着你进入下一阶段？

我会用下面这条主线来写：

1. 产品目标
2. 系统分层
3. 分阶段建设路线
4. 每阶段要解决的关键问题
5. 常见误区
6. 推荐技术栈与工程边界

---

## 1. 先别上来就做“超级 Agent”，先定义你的目标

在真正开工之前，你必须先确定自己想做的是哪一类 Agent 平台。因为不同目标，会决定完全不同的技术栈。

### 1.1 三种常见目标

#### 目标 A：聊天增强型 Agent

典型特点：

- 基本还是聊天产品
- 偶尔调用工具
- 会话不长
- 不强调复杂编排

核心优先级：

- Prompt
- 少量工具
- 基础 memory

#### 目标 B：工作流执行型 Agent

典型特点：

- 要完成多步任务
- 会频繁读写文件、调用 shell、访问外部系统
- 会话较长
- 开始需要 compact、恢复、权限等能力

核心优先级：

- Query loop
- Tool runtime
- Context management
- Compact

#### 目标 C：多 Agent 协作型平台

典型特点：

- 一个任务会拆给多个执行体
- 有 coordinator / worker 角色分工
- 有任务系统、状态系统、通知系统
- 更像“Agent OS”

核心优先级：

- Task protocol
- Agent lifecycle
- Permission bridge
- Memory / knowledge governance

如果你的目标是做“类似 Claude Code”的系统，通常不是 A，而是 B 向 C 演进。

---

## 2. 先给总路线：推荐的六阶段建设顺序

如果你要复刻类似平台，我建议按这六阶段推进：

1. `P0`：最小单 Agent 闭环
2. `P1`：Prompt 分层与上下文治理
3. `P2`：工具运行时与权限体系
4. `P3`：长会话生存能力（compact / resume / recovery）
5. `P4`：文件型记忆与知识沉淀
6. `P5`：多 Agent 编排与企业级知识底座

这个顺序非常重要。因为很多团队会犯两个错误：

- 太早做多 Agent
- 太早做向量知识库

结果往往是主循环都没打稳，系统已经非常复杂。

你应该记住一个基本原则：

> 没有稳定的单 Agent Runtime，就没有靠谱的多 Agent 平台。

---

## 3. P0：先做最小单 Agent 闭环

### 3.1 阶段目标

先证明一件事：

- 用户输入
- 模型能决定下一步
- 系统能执行动作
- 模型能根据结果继续工作

也就是先打通最小 Agent 闭环。

### 3.2 这个阶段你必须有的东西

#### 3.2.1 会话对象

至少要有一个 Session / QueryEngine 对象，维护：

- messages
- current tool context
- runtime config
- basic usage stats

为什么现在就要做：

因为如果一开始不把“会话”建模成对象，后面加入 compact、resume、memory 时会非常痛苦。

#### 3.2.2 Query loop

至少要支持：

1. 组装输入
2. 调模型
3. 识别 tool call
4. 执行工具
5. 把结果回写
6. 再调模型直到结束

如果你的系统现在只能：

- 用户输入
- 模型回一句完整答案

那它还不是 Agent runtime，只是聊天包装器。

#### 3.2.3 3-5 个基础工具

推荐最小工具集：

- `read_file`
- `write_file` / `edit_file`
- `bash`
- `grep` / `glob`

为什么这组工具最适合代码场景：

- 能完成最基础的读、查、改、执行
- 足够覆盖大量真实软件工程任务

### 3.3 推荐技术栈

如果做 CLI 型产品：

- 语言：TypeScript 或 Python
- 模型 SDK：官方 SDK
- Schema：Zod / Pydantic
- 终端交互：Ink（Node）或 Textual / Rich（Python）
- 本地状态：JSONL / SQLite / 文件缓存

### 3.4 这一阶段不要做什么

- 不要先做多 Agent
- 不要先做复杂 memory
- 不要先做向量库
- 不要先做插件市场

为什么：

- 这些都不是闭环成立的前提
- 它们只会增加复杂度，不会帮你证明基础 runtime 是对的

### 3.5 这个阶段的验收标准

你至少应该能稳定完成：

- 读一个代码文件并解释
- 搜索 bug 位置并修改
- 跑一个命令并根据结果继续操作

如果这三件事还不稳定，别进入下一阶段。

---

## 4. P1：做 Prompt 分层与上下文治理

### 4.1 阶段目标

从“能跑”升级到“能稳定跑”。

你要解决的问题不再是模型会不会调用工具，而是：

- 上下文会不会越来越乱
- 不同模式下 Prompt 会不会冲突
- 系统提示会不会越来越难维护

### 4.2 这一阶段需要的关键设计

#### 4.2.1 Prompt 模块化

不要把 system prompt 写成一个超长字符串。至少拆成：

- 身份与角色
- 工具使用规则
- 安全边界
- 输出风格
- 当前模式增量

为什么：

- 后续一定会出现模式切换
- 单体 prompt 无法维护优先级

#### 4.2.2 Prompt 优先级系统

你要明确：

- 默认 prompt
- agent prompt
- user custom prompt
- temporary append prompt

谁覆盖谁，谁追加谁。

如果没有这个规则，系统很快会进入“到底哪段 Prompt 在生效”的混乱状态。

#### 4.2.3 动态上下文分层

至少把上下文拆成：

- static prompt
- dynamic environment info
- user/project rules
- attachments or dynamic reminders

为什么：

- 这是后面引入缓存和 compact 的基础

### 4.3 推荐做法

建议引入类似下面的抽象：

- `getStaticPromptSections()`
- `getDynamicPromptSections()`
- `getAttachmentMessages()`
- `buildEffectiveSystemPrompt()`

### 4.4 这一阶段典型新场景

当你遇到下面这些情况，就说明必须进入 P1：

- 用户开始要求不同模式
- 系统提示越来越长
- 项目规则越来越多
- 你已经说不清“当前 prompt 到底是什么”

### 4.5 这一阶段可能的不足

即便做了 Prompt 分层，你仍然可能没有解决：

- 长会话上下文过长
- 工具结果太多
- 历史越来越贵

那就要进入 P3。

---

## 5. P2：做工具运行时与权限体系

### 5.1 阶段目标

从“模型能调工具”升级到“系统能治理工具”。

你要解决的核心问题是：

- 哪些工具能并发
- 哪些工具有风险
- 用户拒绝后怎么办
- 外部工具怎么接入

### 5.2 这一阶段必须补上的四层

#### 5.2.1 Tool 抽象层

统一定义：

- 名字
- 输入 schema
- 输出消息形态
- 并发安全标记
- 风险类型

#### 5.2.2 调度层

至少支持：

- 串行执行
- 并行执行
- 失败传播
- 取消 / 中断

这是很多 demo 系统缺失的一层。

#### 5.2.3 权限层

至少区分：

- 自动允许
- 自动拒绝
- 需要用户确认

如果你的 Agent 会碰：

- 文件写入
- Shell
- 网络修改
- 外部系统 API

权限层不是锦上添花，而是基本盘。

#### 5.2.4 外部扩展层

如果你想把系统做大，必须考虑：

- 工具能否从外部接入
- 工具描述如何管理
- 工具认证如何处理

这时候你可以选：

- 自定义 plugin API
- MCP
- 内部 service adapter

我会建议优先选类似 MCP 这种“工具总线”思路。

### 5.3 为什么这一阶段不能再往后拖

如果你已经开始接入：

- GitHub
- Slack
- 浏览器
- 搜索
- 内部系统

而工具仍然只是“函数映射表”，系统会迅速崩掉。

### 5.4 推荐技术栈

- Schema：Zod / Pydantic
- 并发控制：Promise queue / asyncio task group
- 权限策略：规则表 + 交互层
- 外部扩展：MCP 或 JSON-RPC over stdio/http

### 5.5 这一阶段的短板

即便工具运行时成型，你仍会遇到：

- 历史太长
- tool results 太多
- resume 难

这就是为什么接下来必须做长会话治理。

---

## 6. P3：做长会话生存能力

### 6.1 阶段目标

让系统不仅能完成任务，还能“活得久”。

这是 Agent 产品从 demo 迈向真实生产力工具的分水岭。

### 6.2 必须解决的三个问题

#### 6.2.1 历史会无限增长

如果不处理：

- token 成本暴涨
- latency 上升
- 很快触顶

#### 6.2.2 中途会失败

会遇到：

- 输出超 token 上限
- prompt too long
- 用户中断
- 工具超时

#### 6.2.3 用户不接受“重新开始”

真实用户希望：

- 会话不断掉
- 历史还能接上
- 工作不丢

### 6.3 这一阶段建议做的能力

#### 6.3.1 Micro-compact

先做轻量压缩：

- 去掉重复
- 去掉不必要冗余块
- 先尽量不做大摘要

#### 6.3.2 Full compact

真正把历史替换为摘要边界。

#### 6.3.3 Post-compact reinjection

compact 之后要恢复关键骨架：

- 当前模式
- 关键规则
- 必要 attachment

#### 6.3.4 Resume / session recovery

至少要支持：

- 从本地 transcript 恢复
- 或从后端 session 恢复

### 6.4 什么时候必须做这一阶段

你出现以下任何一个信号，都说明该做了：

- 用户会话开始超过十几轮甚至几十轮
- 一个任务经常要跑几分钟甚至更久
- 你已经开始做自动化 coding / shell 流程

### 6.5 这一阶段的难点

- 摘要质量
- 关键状态不丢
- compact 之后行为风格保持一致

这是为什么 Claude Code 里 compact 不只是一个命令，而是一个子系统。

---

## 7. P4：做文件型记忆与知识沉淀

### 7.1 阶段目标

让系统不仅记住当前会话，还能在未来会话中变得更懂用户、更懂项目。

### 7.2 我为什么建议你先做“文件型 memory”

而不是一上来就做向量库。

因为文件型 memory 有几个现实优势：

- 可解释
- 易审计
- 容易和 Git / 项目规则体系融合
- Agent 本身就擅长读写文件
- 用户也能直接编辑

对于代码 Agent，这条路线性价比极高。

### 7.3 你至少要拆出三类知识

#### 7.3.1 规则型知识

例如：

- 项目约定
- 团队规范
- 代码库要求

载体适合：

- `CLAUDE.md` / rules files

#### 7.3.2 长期偏好型知识

例如：

- 用户协作偏好
- 常见禁忌
- 常用工作方式

载体适合：

- `memory/*.md`

#### 7.3.3 会话产出型知识

例如：

- 当前会话中抽取出的长期事实

这类信息适合通过 extraction pipeline 进入长期 memory，而不是直接混入规则层。

### 7.4 这一阶段建议做的最小能力

1. 文件型 memory store
2. memory index 文件
3. relevance selection
4. extraction pipeline

### 7.5 为什么需要 relevance selection

因为 memory 一旦多起来，不能每次全塞给模型。

你需要：

- metadata scan
- lightweight selector
- top-k injection

这时候可以先用：

- metadata + LLM selector

而不必立刻上 embedding。

### 7.6 什么时候这一层会开始不够

当你出现这些情况时：

- memory 数量上万
- 跨项目知识检索需求很强
- 用户与团队知识边界复杂
- 需要快速、大规模语义召回

这时就要考虑进入 P5 的知识中台能力。

---

## 8. P5：做多 Agent 编排与企业级知识底座

### 8.1 这是最后一阶段，不是开始阶段

为什么：

- 多 Agent 是复杂度放大器
- 企业级知识底座是治理层，不是 MVP 层

### 8.2 多 Agent 平台需要的最小四件套

#### 8.2.1 Agent spec

至少要定义：

- prompt
- tool scope
- permission scope
- memory scope
- execution mode

#### 8.2.2 Task protocol

必须统一：

- started
- progress
- completed
- failed
- killed

#### 8.2.3 Result return channel

你需要一个统一结果回流机制，例如：

- task notifications
- mailbox
- event queue

#### 8.2.4 Permission bridge

一旦子 Agent 没有 UI，就必须回答：

- ask 权限时怎么问用户

这一步如果没有，你的多 Agent 很快会变成不安全或不可用系统。

### 8.3 企业级知识底座需要什么

当你真的进入企业环境，会逐渐需要：

- 统一 KnowledgeProvider 抽象
- 文件知识 + 向量知识混合索引
- 权限治理
- 版本治理
- 可信度和来源管理
- 反馈与评估体系

### 8.4 为什么这一步不能早做

因为它们的价值依赖于规模：

- 数据规模
- 用户规模
- 组织规模

在规模没起来之前，这些设计成本往往高于收益。

---

## 9. 如果我是技术负责人，我会怎么组团队做这件事

如果你真的打算做类似平台，建议按职责拆团队，而不是按“功能模块文件夹”拆。

### 9.1 Runtime 组

负责：

- Query loop
- compact
- resume
- reliability

### 9.2 Tools 组

负责：

- Tool framework
- permission
- MCP / external integrations

### 9.3 Memory / Knowledge 组

负责：

- memory extraction
- knowledge retrieval
- knowledge governance

### 9.4 Agent Orchestration 组

负责：

- subagents
- coordinator
- task protocol
- UI feedback

### 9.5 Eval / Telemetry 组

负责：

- usage
- latency
- retrieval quality
- compact quality
- failure analysis

为什么这样分组：

因为这几部分最终会形成不同的复杂度中心，适合分别演进。

---

## 10. 你最容易踩的七个坑

### 10.1 太早做多 Agent

后果：

- 主循环没稳
- 调试难度翻倍

### 10.2 把工具系统做成简单函数注册表

后果：

- 后续没有并发、权限、中断和可观测性空间

### 10.3 不把会话建模成对象

后果：

- compact、resume、memory 都会很难接

### 10.4 不做 Prompt precedence

后果：

- 模式一多就不知道谁覆盖谁

### 10.5 一上来就做向量库

后果：

- 基础 runtime 还不稳，知识系统先复杂化

### 10.6 只做 extraction，不做 consolidation

后果：

- memory 越来越多，但越来越乱

### 10.7 没有评估体系就不断加功能

后果：

- 系统越来越重
- 却不知道是否真的更好

---

## 11. 推荐的最小技术栈组合

这里给一个实用而非炫技的组合。

### 11.1 CLI / coding agent 路线

- 语言：TypeScript
- 终端 UI：Ink
- Schema：Zod
- 模型调用：官方 SDK
- 本地状态：JSONL + 文件缓存
- 检索：先文件扫描 + metadata + LLM selector
- 外部工具总线：MCP

为什么我推荐这个组合：

- 和 Claude Code 的形态接近
- 对工具和文件操作支持好
- 类型系统与 schema 协同方便

### 11.2 服务化 / 平台路线

- 语言：Python 或 TypeScript 都可以
- Runtime：异步服务框架
- Session store：Postgres / Redis / object store
- Retrieval：混合检索服务
- Observability：OpenTelemetry + 日志 + metrics

为什么服务化要分出来：

- 一旦你不再只是本地 CLI，而是多用户平台，状态与权限问题会大得多

---

## 12. 最后的实施建议：你应该怎么开始

如果今天就开始做，我会建议这样排 12 周左右的节奏。

### 第 1-2 周

目标：

- Query loop 跑通
- 4 个基础工具可用

### 第 3-4 周

目标：

- Prompt 分层
- 会话对象稳定
- 基本日志打通

### 第 5-6 周

目标：

- 工具权限
- 串并行调度
- 中断与错误处理

### 第 7-8 周

目标：

- compact
- resume
- usage 统计

### 第 9-10 周

目标：

- 文件型 memory
- extraction pipeline

### 第 11-12 周

目标：

- 选一个最简单的 subagent 场景
- 做最小多 Agent 验证

这比一上来做完整 coordinator 更稳。

---

## 13. 总结

如果你要复刻一个类似 Claude Code 的系统，最重要的不是“先把所有高级能力都做出来”，而是遵守下面这个顺序：

1. 先有稳定单 Agent 闭环
2. 再做 Prompt 分层和上下文治理
3. 再做工具运行时与权限
4. 再做长会话生存能力
5. 再做 memory 与知识沉淀
6. 最后做多 Agent 与企业级知识底座

因为真正的 Agent 平台不是“能力堆叠”，而是“复杂性分期管理”。

你如果跳过前面几层，直接做后面的大功能，最终大概率会得到一个：

- 能演示
- 但不稳定
- 不可控
- 不可维护

的系统。

而 Claude Code 这类系统最值得借鉴的地方，恰恰不是某个单点技巧，而是这种分阶段、分层、围绕真实复杂度演化的工程路线。

---

## 14. 参考阅读

- [agent-llm-engineering-analysis.md](agent-llm-engineering-analysis.md)
- [agent-llm-architecture-guide.md](agent-llm-architecture-guide.md)

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“如何从 0 到 1 复刻一个类似 Claude Code 的 Agent 平台 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

### 1. 这件事到底考什么

这里真正考察的不是会不会调用一个 API，而是能不能把 Agent 对外部世界的行动放进可治理的执行管线。

如果只回答功能点，说明还停留在“看过项目”的层面；如果能回答问题来源、工程约束、取舍和行动项，才说明这份沉淀真正进入了自己的方法论。

### 2. 口语版回答

我会把工具调用理解成 Agent Runtime 的行动边界。成熟系统不能只关心函数能不能执行，还要关心输入协议、权限分级、执行隔离、结果压缩、错误恢复和审计回放。否则模型一旦误调工具，风险会直接落到真实文件、浏览器、网络或业务系统上。

这段回答可以直接用于复盘、面试或方案评审。它的结构是：先定义问题，再讲工程边界，最后落到可迁移做法。

### 3. 工程视角拆解

可以按四层来理解：

- 问题层：这个设计到底在解决什么不稳定、不可控或不可复用的问题。
- 机制层：它用了哪些结构、协议、运行时、文档或流程来解决。
- 证据层：有哪些 README、源码、指标、案例或平台行为能证明它不是口号。
- 迁移层：它对 `claude-code-sourcemap`、知识平台、Project Radar 或面试训练有什么可执行启发。

### 4. 常见误区

把 MCP 或 Tool Calling 当成普通 API wrapper，只写 schema，不写权限、结果治理和失败恢复。

另一个常见误区是只把优秀项目当作模板照抄。真正应该学的是它为什么这样拆分，以及这个拆分在自己的场景里是否仍然成立。

### 5. Trade-off 与边界

治理越完整，接入成本越高；但如果工具有副作用，前期省掉治理，后期会以安全事故、上下文爆炸和不可复现的形式还回来。

判断一个方案是否成熟，不是看它有没有更多能力，而是看它有没有明确说明代价、适用场景和不适用场景。

### 6. 当前项目行动项

- [ ] 给每个工具补齐 riskLevel、permission、resultPolicy、auditTrail，并在平台中把相关项目和工具治理 pattern 关联起来。
- [ ] 把这份文档中的通用问题同步到对应 `docs/patterns/` 文档，避免停留在单项目笔记。
- [ ] 在平台详情页中保留“口语版回答、工程拆解、误区、行动项”，让它能直接用于学习和面试表达。

### 7. 面试官追问

**追问：这个项目或方案最值得学习的不是功能，而是什么？**

答：最值得学习的是它如何把一个模糊问题变成可治理的工程结构。功能只是表层，真正可迁移的是它的边界划分、执行流程、证据链和取舍。

**追问：如果迁移到当前平台，第一步应该做什么？**

答：第一步不是照搬实现，而是把它抽象成平台中的一个通用问题，补齐文档、索引、行动项和验证方式，让后续沉淀能自动进入平台展示。

## 行业痛点研究版补充

> 目标：把“如何从 0 到 1 复刻一个类似 Claude Code 的 Agent 平台”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

### 1. 它对应的行业痛点

Agent 接入外部工具后，行业共性痛点是权限、结果大小、执行副作用、工具质量和可观测性会同时失控。优秀项目不会把工具当普通函数，而会把它放进 Tool Runtime / MCP Integration 的治理管线。

判断它是不是值得持续沉淀，不看它是否新奇，而看它能不能解释一个反复出现的行业问题，并能不能给当前项目带来可执行改变。

### 2. 可作为证据的来源类型

GitHub 工具型项目、MCP server、旧体系工具文档、源码 README、浏览器自动化案例。

后续如果新增 GitHub、优质博客、论文或你提供的文档，都应该先判断它能否补强这一类证据，而不是直接堆进知识库。

### 3. 优秀项目或资料的共性做法

共性做法是 Tool Registry + Permission Mapping + Result Summary + Artifact Reference + Audit Trail，把调用、权限、结果和追踪拆开治理。

这里真正要学的不是表层功能名，而是成熟项目如何划分边界、控制风险、组织证据、形成可复用流程。

### 4. 数据支撑与判断信号

可观察信号包括工具数量、权限等级覆盖率、单次结果 token 数、artifact 引用比例、失败调用可复现率。

这些信号用于避免主观判断。后续平台应该让痛点页自动展示证据项目数、来源类型、关联方案数和行动项数量。

### 5. 给当前项目的启发

这份文档应该反哺 `claude-code-sourcemap` 的三个位置：

- 项目页：说明它作为样本值得学习什么。
- 痛点页：说明它补强了哪个 Agent / 大模型行业共性问题。
- 方案页：说明它能沉淀成什么可迁移框架。

### 6. 当前项目行动项

- [ ] 把该文档关联到 Tool Runtime / MCP 行业痛点，并检查是否能补充工具权限、结果治理或审计行动项。
- [ ] 检查它是否需要更新 `docs/pain-points/` 的行业痛点说明。
- [ ] 检查它是否需要更新 `docs/patterns/` 的通用技术框架。
- [ ] 如果它来自外部资料，把它登记到 `docs/source-library/` 或 Project Radar 候选池。

### 7. 自动进化规则

每次新增相关资料后，按以下顺序更新：

```text
资料源
  -> 行业痛点
  -> 证据项目/资料
  -> 共性做法
  -> 数据支撑
  -> 当前项目行动项
  -> 面试官追问
```

