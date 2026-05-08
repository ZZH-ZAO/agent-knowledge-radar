# Agent 项目分类总图

## Summary

- Project name: Agent project classification map
- Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared`
- Document type: shared learning map
- Purpose: 把当前案例库中不同类型的 Agent 项目整理成一张学习地图，帮助从“项目是什么类型、最该学什么、适合和谁对比、下一步该看什么”这几个维度建立整体认知

## 一、先给结论：Agent 项目不要混着看，要先分类型

很多人看 Agent 项目时最容易犯的错，是把完全不同目标的项目放在一起比较。

例如：

- 通用 runtime
- 行业工作流 Agent
- 产品化 Agent 平台
- 仓库分析 Agent
- SDK 包装型 Agent

这些项目表面上都叫 Agent，但它们真正解决的问题完全不同。

所以学习 Agent 工程的第一步，不是看它“用了什么模型”，而是先判断：

> 这个项目到底属于哪一类，它最强的创新层又在哪一层。

## 二、这张总图怎么用

你可以把这张图当成一个学习导航系统。

每看一个新项目，就先回答四个问题：

1. 它最像哪一类项目
2. 它最强的是哪一层
3. 它更适合和哪个案例对比
4. 我应该从它身上学什么，而不是被它的表面功能带跑

## 三、Agent 项目六大类型总图

我建议把目前这类项目先分成六大类。

### 1. `runtime-first`

这类项目最关心的是：

- Agent 内核怎么跑
- model -> tool -> state -> continue 这个循环怎么稳定
- session、compact、memory insertion、多 Agent 协调如何嵌进执行引擎

它的核心问题是：

- “这台 Agent 发动机怎么设计”

典型特征：

- 很重 query loop
- 很重 tool result 回流
- 很重上下文窗口控制
- 很重 session / run state

最适合学：

- Agent 执行内核
- Prompt 与 tool loop 的结合
- 多轮执行稳定性

当前代表案例：

- `claude-code-sourcemap`

一句话记忆：

- 这是“Agent 发动机”类型项目

### 2. `platform-expansion`

这类项目最关心的是：

- 当 Agent runtime 已经可用以后，怎样扩成产品平台

它的核心问题是：

- “如何把一个能跑的 Agent，变成一个能长期运营、治理、扩展的系统”

典型特征：

- feature gating
- 运营与控制面
- 更强的产品表面
- 更重治理、观测、权限、版本化

最适合学：

- 平台产品化
- 能力投放节奏
- 平台治理

当前代表案例：

- `claude-code`
- `ArcReel`

但两者重点不同：

- `claude-code` 更偏平台治理与能力扩展
- `ArcReel` 更偏创作工作台与产品化工作流平台

一句话记忆：

- 这是“Agent 平台长大以后”类型项目

### 3. `vertical-workflow`

这类项目最关心的是：

- 如何把一个具体领域流程编码成 Agent 系统

它的核心问题是：

- “这个行业里的工作到底怎样被稳定地自动化、半自动化和可审计化”

典型特征：

- 强 SOP / 强 procedure
- tool-rich workflow
- 输出往往是报告、工单、诊断、建议书，而不是闲聊
- 人机协作点通常很明确

最适合学：

- 业务流程工程化
- prompt 作为 SOP
- 工具链围绕领域流程组织

当前代表案例：

- `career-ops`
- `fault-diagnosis`

两者区别：

- `career-ops` 更偏业务流程与交付流程
- `fault-diagnosis` 更偏工业数据、诊断证据、图表与报告

一句话记忆：

- 这是“把行业流程变成 Agent”类型项目

### 4. `tool-runtime`

这类项目最关心的是：

- 能力系统怎样组织

它的核心问题是：

- “tool、skill、plugin、MCP、sandbox、provider 怎么形成一个统一能力层”

典型特征：

- 工具分层明显
- 常有 skills / MCP / plugins / adapters
- 能力不是简单函数集合，而是生态结构

最适合学：

- 能力体系设计
- 外部能力接入协议
- Agent 生态扩展

当前代表案例：

- `deer-flow`
- `repomind`

但重点不同：

- `deer-flow` 更偏通用 runtime 能力生态
- `repomind` 更偏围绕 GitHub / repo intelligence 的证据工具层

一句话记忆：

- 这是“Agent 能力底盘”类型项目

### 5. `memory-first`

这类项目最关心的是：

- 系统如何在多轮、多会话、长期交互中记住真正有价值的东西

它的核心问题是：

- “什么该记、怎样记、何时注入、怎样避免记忆污染”

典型特征：

- 有显式 memory schema
- 有 memory update / extraction / injection 机制
- 很重用户画像、历史事实、长期状态

最适合学：

- 长期个性化
- 结构化记忆
- 记忆卫生与记忆边界

当前代表案例：

- `deer-flow`
- `claude-code-sourcemap`

两者区别：

- `deer-flow` 更偏长期结构化 memory
- `claude-code-sourcemap` 更偏执行过程中的上下文控制与记忆插入点

一句话记忆：

- 这是“Agent 长期记忆系统”类型项目

### 6. `RAG-first` / `evidence-first`

这类项目最关心的是：

- 怎样把外部知识或证据可靠地接入 Agent

它的核心问题是：

- “模型回答时，证据从哪里来，怎么增强，怎么保证不是瞎说”

典型特征：

- 有检索增强
- 有知识库 / 文件选择 / 外部搜索 / 数据快照
- 强调证据、来源和事实约束

最适合学：

- 检索增强模式
- context construction
- 证据驱动回答

当前代表案例：

- `repomind`
- `fault-diagnosis`

两者区别：

- `repomind` 更像 agentic CAG + GitHub / web 证据层
- `fault-diagnosis` 更像工业知识与业务数据支撑的 evidence workflow

一句话记忆：

- 这是“Agent 先拿证据再说话”类型项目

## 四、把当前案例库放进这张地图

下面是你现在案例库里几个核心项目在地图中的位置。

### `claude-code-sourcemap`

主类型：

- `runtime-first`

次类型：

- `memory-first`
- `tool-runtime`

最该学：

- query loop
- tool continuation
- session compact
- memory extraction
- 多 Agent 协调内核

### `claude-code`

主类型：

- `platform-expansion`

次类型：

- `persistent-agent`
- `team-knowledge`

最该学：

- runtime 如何长成平台
- 平台治理
- feature rollout
- 更高层能力控制

### `career-ops`

主类型：

- `vertical-workflow`

次类型：

- `tool-runtime`

最该学：

- 业务流程编码
- prompt 作为 SOP
- structured output contract

### `fault-diagnosis`

主类型：

- `vertical-workflow`

次类型：

- `RAG-first`
- `evidence-first`

最该学：

- 工业诊断流程
- 数据 + 工具 + 知识 + 报告闭环
- 证据链和交付物

### `ArcReel`

主类型：

- `platform-expansion`

次类型：

- `vertical-workflow`
- `sdk-wrapped-runtime`

最该学：

- 创作工作台
- runtime 与产品协同
- 多供应商媒体能力平台

### `repomind`

主类型：

- `vertical-workflow`

次类型：

- `tool-runtime`
- `evidence-first`

最该学：

- repo intelligence
- agentic CAG
- GitHub 证据工具层
- verification-first 安全扫描

### `deer-flow`

主类型：

- `runtime-first`

次类型：

- `tool-runtime`
- `memory-first`
- `platform-expansion`

最该学：

- super agent harness
- runtime / app 分层
- skills / MCP / sandbox / memory / subagent 统一底座

## 五、学习路径建议：按什么顺序看最容易形成体系

如果你想真正把这套案例学成知识体系，我推荐按下面顺序。

### 路线 A：先学“底层怎么跑”

适合你现在这种想把 Agent 工程理解得更深的人。

顺序：

1. `claude-code-sourcemap`
   学执行内核
2. `deer-flow`
   学通用底座
3. `claude-code`
   学平台化
4. `ArcReel`
   学工作台和产品协同
5. `repomind`
   学证据驱动的垂直产品
6. `fault-diagnosis`
   学行业 Agent 的证据与交付闭环

### 路线 B：先学“怎么做产品”

适合更想做应用的人。

顺序：

1. `ArcReel`
2. `claude-code`
3. `repomind`
4. `deer-flow`
5. `claude-code-sourcemap`

这条路线先让你看到产品和平台，再回到底座和引擎。

### 路线 C：先学“行业 Agent”

顺序：

1. `career-ops`
2. `fault-diagnosis`
3. `repomind`
4. `ArcReel`
5. `deer-flow`

这条路线更适合从业务落地往回学。

## 六、以后分析新项目时，你可以这样快速定位

拿到一个新项目后，先用下面这组问题把它塞进地图。

### Step 1：先判断主类型

问自己：

- 它最像引擎、底座、平台、工作流还是知识系统

### Step 2：再判断次类型

问自己：

- 它有没有特别强的 memory、tool ecology、RAG、platform surface、workflow

### Step 3：找最像的历史案例

例如：

- 像执行内核 -> 对比 `claude-code-sourcemap`
- 像 harness -> 对比 `deer-flow`
- 像平台产品 -> 对比 `claude-code`
- 像垂直流程 -> 对比 `career-ops` / `fault-diagnosis`
- 像 repo intelligence -> 对比 `repomind`
- 像创作工作台 -> 对比 `ArcReel`

### Step 4：决定应该借鉴哪一层

不要说“这个项目像 DeerFlow”就结束。
要继续说清楚：

- 它像 DeerFlow 的 skill/mcp/sandbox 层
- 还是像 claude-code-sourcemap 的 loop 层
- 还是像 claude-code 的平台治理层

## 七、和 shared 模板怎么配合

这张总图负责回答：

- 这个项目属于哪一类

而 `shared/` 里的模板负责回答：

- 这一类项目应该怎样系统分析

推荐搭配：

- 想分析 harness 项目：
  先看 `agent-project-classification-map.md`
  再看 `super-agent-harness-design-template.md`
- 想分析平台项目：
  先看总图
  再看 `productized-agent-platform-template.md`
- 想分析工业 Agent：
  先看总图
  再看 `industrial-agent-design-template.md`

## 八、最后用一句话记住这张图

如果只用一句话记住它，我建议记成这样：

> Agent 项目不是一团“都差不多的 AI 应用”，而是至少可以分成引擎、底座、平台、垂直工作流、记忆系统和证据系统几类；先分类型，后谈优缺点，学习才会越来越清楚。
