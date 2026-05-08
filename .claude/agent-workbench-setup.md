# Agent Workbench 使用入口

## Summary

- Project name: Agent research workbench
- Project path: `D:\claude-code-sourcemap\.claude`
- Document type: setup guide
- Purpose: explain how this workbench is structured, how to choose the right skill or document path, and how future project analysis should be turned into reusable knowledge

## 0. 这是什么

这一套 `.claude/` 结构，不是普通配置文件集合，而是一个专门为 Agent 项目研究、分析、设计和路线规划准备的工作台。

它的目标很明确：

- 以后分析别的 Agent 项目时，不从零开始搭分析框架
- 以后设计自己的 Agent 平台时，不凭感觉东补一块西补一块
- 以后给项目排优先级时，不写功能愿望单，而是围绕真实瓶颈推进

你可以把它理解成：

> 这是一个“研究 Agent 项目用的 Agent 工作台”。

---

## 1. 这套结构分成哪几层

### 1.1 `skills/`

作用：定义“怎么做”。

这里的 skill 不是知识仓库，而是做事方法的入口。它负责告诉 Agent：

- 面对某类任务应该按什么顺序思考
- 该重点看哪些维度
- 输出应该长什么样

当前核心 skill 包括：

- `agent-architecture-review`
  适合看懂一个 Agent 项目的运行结构、主链路和工程重点。
- `agent-platform-design`
  适合做新系统设计，把 prompt、tool、memory、workflow 分层讲清楚。
- `agent-feature-roadmap`
  适合判断项目下一步该补什么，哪些能力现在上会过重。
- `agent-research-workbench`
  适合综合型任务，把 review、design、roadmap 串起来。

### 1.2 `memory/`

作用：定义“怎么判断”。

它存的是长期稳定、反复复用的判断原则，而不是某一次任务的临时内容。

当前包括：

- `agent-principles.md`
  核心 Agent 原则。
- `agent-review-checklist.md`
  分析项目时的检查表。
- `agent-patterns.md`
  常见架构模式与适用边界。
- `project-preferences.md`
  你的偏好、文风、输出方式。
- `mcp-strategy.md`
  MCP 应该在什么时候引入，以及引入的目标是什么。

### 1.3 `.mcp.json`

作用：定义“怎么接能力”。

它不是装饰项，而是这套工作台的外部能力接入口。当前主要围绕三类方向：

- 本地仓库分析
- 本地文档与知识读取
- 外部网页抓取与联网研究

也就是说，这套工作台不是只会“写分析”，而是能真正去读仓库、读文档、查资料。

### 1.4 `.claude/docs/`

作用：定义“怎么沉淀”。

这一步非常关键，因为工作台不能只会产出一次性答案，还要把分析结果转成长期可复用资产。

这里已经分成三层入口：

- `.claude/docs/index.md`
  案例库总入口，先判断应该看哪一个案例。
- `.claude/docs/user/`
  给你自己学习和复盘的详细版。
- `.claude/docs/agent/`
  给后续 Agent 快速检索和复用的压缩版。

并且现在建议在 `user/` 和 `agent/` 下面继续按项目分子目录：

- `user/arcreel/`
- `user/fault-diagnosis/`
- `user/claude-code/`
- `agent/arcreel/`
- `agent/fault-diagnosis/`
- `agent/claude-code/`

如果是跨项目模板或通用方法论文档，放到：

- `.claude/docs/user/shared/`

---

## 2. 遇到任务时，应该怎么选入口

### 2.1 如果你想“看懂一个 Agent 项目”

优先使用：

- `agent-architecture-review`

适合问题：

- 这个项目本质上是什么系统
- 它的 prompt、tool、workflow、memory 各自落在哪一层
- 它到底是 serious runtime，还是只是薄封装

### 2.2 如果你想“设计一个类似系统”

优先使用：

- `agent-platform-design`

适合问题：

- 我想做一个 coding agent，应该怎么分层
- prompt、tool、memory、workflow 怎么组合更稳
- 什么时候该上多 Agent，什么时候先不要上

### 2.3 如果你想“判断下一步该补什么”

优先使用：

- `agent-feature-roadmap`

适合问题：

- 现在的真正瓶颈是什么
- memory、RAG、多 Agent 哪个先做
- 什么能力现在上会带来过重复杂度

### 2.4 如果你想“做一次完整研究任务”

优先使用：

- `agent-research-workbench`

适合问题：

- 先分析项目，再提炼可学之处，再形成设计建议
- 对比两个或多个 Agent 项目
- 把研究结果沉淀成以后可复用的方法论

### 2.5 如果你想“找到已有案例对照”

优先阅读：

- `.claude/docs/index.md`
- `.claude/docs/user/index.md`
- `.claude/docs/agent/index.md`

用途分别是：

- 总入口先判断“该对照谁”
- `user/index.md` 看“我应该从这个案例学什么”
- `agent/index.md` 看“这个案例适合在哪类任务里复用”

---

## 3. 一套推荐工作流

如果以后要用这套工作台做一次完整研究，我建议按下面顺序推进。

### 第一步：先理解目标系统

使用：

- `agent-research-workbench`
  或直接 `agent-architecture-review`

目标：

- 找到主执行链
- 判断系统本质
- 看清 prompt、tool、workflow、memory、多 Agent 的真实位置

### 第二步：提炼可迁移的方法

重点参考：

- `memory/agent-principles.md`
- `memory/agent-patterns.md`

目标：

- 不只是描述“它做了什么”
- 而是提炼“为什么这样做有效、哪些部分可以迁移”

### 第三步：形成设计建议

使用：

- `agent-platform-design`

目标：

- 把前面的分析转成可执行的系统设计建议
- 讲清楚推荐分层、适用场景和边界

### 第四步：排未来路线图

使用：

- `agent-feature-roadmap`

目标：

- 围绕当前瓶颈排优先级
- 明确下一步先补什么，什么先不要做

### 第五步：沉淀进案例库

每次完成一次有长期价值的分析后，都建议落两份文档：

- 一份写到 `.claude/docs/user/`
  负责完整讲解、复盘学习、解释原因
- 一份写到 `.claude/docs/agent/`
  负责压缩结论、方便后续 Agent 检索复用

如果这个项目形成了新的分类或新的对照价值，还要更新：

- `.claude/docs/index.md`

并且现在建议把这个动作再补完整：

- 在 `user/<project-name>/README.md` 写清楚这个项目目录里每篇文档的阅读顺序
- 在 `agent/<project-name>/README.md` 写清楚压缩笔记的用途

这一步意味着这套工作台会越来越“有记忆”，而不是每次都重新开始。

---

## 4. 这套工作台最适合解决什么问题

### 4.1 项目分析类

比如：

- 分析 Claude Code、OpenHands、Codex 这类 Agent 项目
- 判断一个项目到底是 demo、runtime、平台，还是垂直工作流系统
- 看清某个项目真正的工程重心在哪里

### 4.2 系统设计类

比如：

- 设计 coding agent
- 设计 long-session assistant
- 设计 tool runtime、memory、RAG、multi-agent 方案

### 4.3 规划决策类

比如：

- 项目下一步优先做什么
- 哪些能力上得太早会过重
- 哪些信号说明现在该升级复杂度

### 4.4 方法论沉淀类

比如：

- 把多个 Agent 项目的共性提炼成原则
- 建立自己的 Agent 研发判断框架
- 让后续项目分析不再每次从零开始

---

## 5. MCP 在这套工作台里扮演什么角色

不要把 MCP 理解成“多接几个工具”。

在这套工作台里，MCP 主要补的是三类能力：

### 5.1 本地仓库分析

让 Agent 真正读取代码仓库，而不是只靠猜测做评论。

### 5.2 本地知识读取

让 Agent 能把已经沉淀下来的文档、memory、references 真正用起来。

### 5.3 外部研究补充

让 Agent 能抓网页、查官方资料、做外部验证，而不是闭门分析。

所以理想状态不是某一个模块单打独斗，而是：

- `skills` 规定工作流
- `memory` 提供判断标准
- `MCP` 提供能力半径
- `docs` 负责长期沉淀

---

## 6. 以后你自己维护时，优先怎么扩

### 第一优先级：补 `memory`

一旦发现新的稳定原则、常见坑、偏好和判断框架，就优先写进 `memory/`。

因为 memory 决定这套工作台的长期判断风格。

### 第二优先级：补 `skills/references/`

把复杂模板、评审清单、设计模板、路线图模板继续拆细。

因为这样 skill 会越来越像真正的方法工具，而不是一段说明文字。

### 第三优先级：补 `.mcp.json`

逐步接成真实可用的能力层，比如：

- GitHub
- issue tracker
- docs search
- 外部知识抓取

因为 MCP 决定这套工作台能走多远、能查多深。

### 第四优先级：持续扩案例库

每分析完一个高价值项目，就按标准流程补进 `.claude/docs/`。

因为真正让工作台变强的，不只是模板，而是不断积累的对照案例。

---

## 7. 一句话记住这套东西

如果要用一句话记住它，我建议记成这样：

> `skills` 负责“怎么做”，`memory` 负责“怎么判断”，`MCP` 负责“怎么接能力”，`docs` 负责“怎么把经验留下来”。

只要这四层长期分得清，这套 Agent 工作台就会越来越稳，也会越来越像你自己的研究操作系统。
