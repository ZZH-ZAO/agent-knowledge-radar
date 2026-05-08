# Agent 项目知识平台产品化规格文档

> 创建日期：2026-05-03  
> 适用项目：`D:\claude-code-sourcemap`  
> 产品目标：把当前文档型知识库升级成一个可视化、可检索、可持续进化的 Agent 项目学习与面试训练平台。  
> 后续上下文：以后开发“项目界面、方案界面、痛点界面、面经与面试官系统”时，以本文档作为产品规格入口。

## 1. 产品一句话

这个平台要把当前沉淀在 `docs/` 里的 Agent 项目、技术方案、通用痛点、解决方法、面经和面试问答，变成一个可以直接浏览、筛选、学习、追问和训练面试官的可视化系统。

它不是普通 Markdown 浏览器，而是一个面向“学习优秀 Agent 项目 + 提炼工程方法论 + 准备项目面试”的知识产品。

```text
项目知识库
  -> 可视化项目地图
  -> 方案与技术框架
  -> 通用痛点与解决路径
  -> 面经/八股吸收
  -> 自我进化的项目面试官
```

## 2. 核心用户和使用场景

### 2.1 核心用户

第一用户就是你自己。

你需要它帮助你：

- 快速看清当前收集了哪些优质项目。
- 判断每个项目属于什么类型、解决什么问题、有什么学习价值。
- 按技术主题查看沉淀出的方案。
- 看到不同项目背后的共同痛点和成熟解决方法。
- 喂入面经和八股后，自动生成与你项目相关的面试问题和答案。
- 让系统逐渐变成一个懂你项目、会追问、能模拟面试官的训练工具。

### 2.2 高频场景

#### 场景一：今天我想看项目

你打开平台首页，先进入项目界面，看到：

- 当前有多少项目。
- 每个项目属于什么类型。
- 哪些已经深度沉淀。
- 哪些只是草稿。
- 哪些值得下一步学习。

#### 场景二：我想学一类方案

你进入方案界面，比如选择 `Tool Runtime`，看到：

- 这个方案解决什么问题。
- 涉及哪些项目。
- 成熟项目怎么做。
- 可迁移框架是什么。
- 当前项目行动项是什么。

#### 场景三：我想知道项目痛点

你进入痛点界面，比如选择 `MCP Integration` 或 `Permission & Sandbox`，看到：

- 通用痛点是什么。
- 为什么重要。
- 常见错误做法。
- 成熟解决方法。
- 证据来自哪些项目。
- 我们现在怎么解决。

#### 场景四：我准备面试

你把面经、八股、岗位 JD 或目标公司问题喂给系统。系统会：

- 抽取问题类型。
- 关联你的项目内容。
- 生成面试官可能怎么问。
- 生成推荐回答。
- 继续追问细节。
- 根据你的回答更新薄弱点。

## 3. 产品信息架构

建议第一版路由如下：

```text
/
  -> Dashboard 总览

/projects
  -> 项目界面

/projects/:id
  -> 单项目详情

/solutions
  -> 方案界面

/solutions/:topic
  -> 单方案详情

/pain-points
  -> 痛点界面

/pain-points/:id
  -> 单痛点详情

/interviews
  -> 面经与八股管理

/interviews/:id
  -> 单面经解析

/interviewer
  -> AI 面试官训练场

/radar
  -> Project Radar 候选池

/settings
  -> 数据源、模型、同步、导入配置
```

第一版可以先做四个核心页面：

1. `/projects`
2. `/solutions`
3. `/pain-points`
4. `/interviewer`

`/radar` 可以复用现有 `docs/project-radar/candidates.json`。

## 4. 页面设计

### 4.1 项目界面

目标：让你一眼看清“我现在有哪些项目，它们分别是什么类型”。

数据来源：

- `docs/external-projects/{项目类型中文文件夹}/*.md`
- `docs/project-radar/candidates.json`
- `docs/source-research/当前项目沉淀与路线/current-project-distillation.md`

页面内容：

- 顶部统计：
  - 项目总数
  - 深度沉淀数
  - 草稿数
  - 高分候选数
  - 待学习项目数
- 分类筛选：
  - Agent Runtime
  - MCP Server
  - Coding Agent
  - Tool Runtime
  - Memory
  - Plugin / Skill
  - Productization
  - Provider Abstraction
  - Interview / Learning
- 项目卡片：
  - 项目名
  - 一句话
  - 类型标签
  - 推荐等级
  - 沉淀状态：草稿 / 深度沉淀 / 待更新
  - 关联方案
  - 关联痛点
  - 下一步动作

项目卡片示例：

```text
ChromeDevTools/chrome-devtools-mcp
类型：MCP Server / Tool Runtime / Browser Debugging
状态：深度沉淀
价值：复杂专家工具如何包装成 Agent 可调用 MCP 工具
关联方案：MCP Integration、Tool Runtime
关联痛点：工具结果太大、外部环境有状态、Agent 需要可靠浏览器调试
```

### 4.2 单项目详情

目标：完整展示一个项目的学习结果。

页面模块：

- 项目摘要
- 为什么值得学
- 核心场景
- 通用问题
- 优秀技术和框架
- 可迁移原则
- 行动项
- 证据链接
- 关联 patterns
- 面试可问点

这里直接渲染 `docs/external-projects/{项目类型中文文件夹}/{project}.md`，但要把结构解析成分区，而不是只显示一坨 Markdown。

### 4.3 方案界面

目标：按技术方案查看沉淀结果。

数据来源：

- `docs/patterns/*.md`

方案列表：

- Agent Runtime
- Tool Runtime
- MCP Integration
- Memory System
- Plugin System
- Permission & Sandbox
- Multi-Agent
- Observability
- Productization
- Provider Abstraction

每个方案卡片显示：

- 方案名
- 问题定义
- 成熟做法摘要
- 关联项目数
- 可迁移框架
- 当前行动项数量

### 4.4 单方案详情

目标：展示一个技术方向的完整知识框架。

页面结构：

- 问题定义
- 为什么重要
- 常见错误做法
- 成熟系统通常怎么做
- 优秀项目案例
- 可迁移技术框架
- 我的项目行动项
- 相关面试问题

示例：`MCP Integration`

```text
问题：Agent 如何通过统一协议接入外部工具、数据源和专家系统？
案例：Chrome DevTools MCP、Goose、Claude Code
框架：MCP Server -> Transport/Auth -> Tool Discovery -> Permission Mapping -> Result Summary -> Artifact Reference
```

### 4.5 痛点界面

目标：把 Agent / 大模型应用行业内的共性痛点集中展示，并给出基于优质项目、博客、论文、旧文档和当前项目证据的解决方法。

痛点不是“我觉得难”，也不是单个项目的功能缺口，而是从多个来源里反复出现的结构性问题。平台的目标是搜索优质资料，研究它们如何解决这些问题，再提炼共性做法，反哺当前项目。

痛点卡片字段：

- 痛点标题
- 所属主题
- 严重程度
- 影响场景
- 典型项目
- 证据来源
- 来源类型：GitHub / 博客 / 论文 / 旧文档 / 当前项目
- 常见错误做法
- 优秀项目做法
- 共性解法
- 数据和判断信号
- 推荐解决方案
- 可执行行动项

第一批痛点建议：

#### 痛点一：工具结果太大，容易打爆上下文

- 来源项目：Chrome DevTools MCP
- 证据：Design Principles 强调 token-optimized 和 reference over value
- 方法：Summary + Artifact Reference + Follow-up Tool

#### 痛点二：MCP 工具生态接入后难治理

- 来源项目：Claude Code、Goose、Chrome DevTools MCP
- 方法：Tool Registry + Category + RiskLevel + Permission Mapping + Lifecycle

#### 痛点三：多模型 provider 差异污染 runtime

- 来源项目：Goose、Claude Code
- 方法：Provider Interface + Capability Metadata + Event Normalizer

#### 痛点四：项目沉淀容易停留在读书笔记

- 来源项目：当前项目自身
- 方法：单项目沉淀 -> patterns -> 行动项

#### 痛点五：Agent 项目难以进入产品化

- 来源项目：Claude Code、Goose
- 方法：安装/更新/配置/治理/安全/反馈/文档体系化

### 4.6 面经与八股管理界面

目标：接收你喂入的面经、八股、岗位 JD、公司问题，并把它们转成结构化训练材料。

数据来源：

- 你手动粘贴
- Markdown 文件
- PDF / Word 后续可加
- 面试记录文本

页面模块：

- 面经列表
- 标签：
  - 八股
  - 项目追问
  - 系统设计
  - Agent / LLM
  - 前端 / 后端 / 工程化
  - 行为面
- 解析结果：
  - 原始问题
  - 问题类型
  - 考察点
  - 关联项目
  - 推荐答案
  - 可追问方向
  - 我的薄弱点

### 4.7 AI 面试官训练场

目标：让系统不只是生成答案，而是变成会结合你项目追问的面试官。

核心能力：

- 根据岗位和项目生成面试题。
- 根据你的回答继续追问。
- 把回答映射到项目证据。
- 给出答案评分。
- 更新薄弱点。
- 自动补充题库。

面试模式：

1. **项目深挖模式**
   - 专问 `claude-code-sourcemap`
   - 问 Project Radar、patterns、外部项目沉淀、Agent Runtime

2. **八股结合项目模式**
   - 比如问“什么是插件系统”
   - 要求结合 Claude Code、Goose、当前项目回答

3. **系统设计模式**
   - 让你设计一个 Project Radar 平台
   - 追问数据模型、评分、扩展性、搜索、权限、产品化

4. **压力追问模式**
   - 连续问为什么、怎么验证、有什么 trade-off、失败怎么办

## 5. 数据模型

第一版建议采用“本地文件为主，构建索引为辅”。

### 5.1 Project

```ts
type Project = {
  id: string
  name: string
  url?: string
  summary: string
  types: string[]
  status: 'candidate' | 'draft' | 'deep'
  score?: number
  sourceFile: string
  relatedPatterns: string[]
  relatedPainPoints: string[]
  evidenceLinks: string[]
  nextActions: string[]
}
```

### 5.2 Solution / Pattern

```ts
type Solution = {
  id: string
  title: string
  problemDefinition: string
  whyImportant: string[]
  commonMistakes: string[]
  maturePractices: string[]
  framework: string
  projects: string[]
  actions: string[]
  sourceFile: string
}
```

### 5.3 PainPoint

```ts
type PainPoint = {
  id: string
  title: string
  topic: string
  severity: 'high' | 'medium' | 'low'
  evidence: {
    projectId: string
    sourceFile: string
    note: string
  }[]
  commonMistakes: string[]
  solutionMethod: string
  actions: string[]
}
```

### 5.4 InterviewItem

```ts
type InterviewItem = {
  id: string
  source: string
  rawQuestion: string
  questionType: '八股' | '项目追问' | '系统设计' | '行为面' | '开放题'
  knowledgePoints: string[]
  relatedProjects: string[]
  relatedPatterns: string[]
  recommendedAnswer: string
  followUps: string[]
  weakSpots: string[]
}
```

### 5.5 InterviewSession

```ts
type InterviewSession = {
  id: string
  mode: '项目深挖' | '八股结合项目' | '系统设计' | '压力追问'
  targetRole?: string
  questions: InterviewItem[]
  answers: {
    questionId: string
    userAnswer: string
    score: number
    feedback: string
    nextFollowUp?: string
  }[]
}
```

## 6. 数据来源映射

### 6.1 项目界面

```text
docs/external-projects/{项目类型中文文件夹}/*.md
docs/project-radar/candidates.json
docs/source-research/当前项目沉淀与路线/current-project-distillation.md
```

### 6.2 方案界面

```text
docs/patterns/*.md
```

### 6.3 痛点界面

第一版从 `scripts/build_knowledge_index.py` 中的行业痛点 seed 生成，并吸收 `external-projects`、旧文档和 patterns。后续单独维护：

```text
docs/pain-points/*.md
```

痛点的自动进化规则：

```text
新增优质项目/博客/论文/文档
  -> 识别它解决的行业痛点
  -> 提取优秀做法和数据支撑
  -> 对比已有项目共性
  -> 更新 pain-points
  -> 更新 patterns
  -> 生成当前项目行动项
```

### 6.4 面经界面

建议新增：

```text
docs/interviews/raw/
docs/interviews/processed/
docs/interviews/question-bank.md
docs/interviews/interviewer-memory.md
```

## 7. 第一版技术路线

当前仓库根目录没有前端项目，所以第一版建议新建一个独立 app：

```text
apps/knowledge-platform/
```

推荐技术栈：

- Vite
- React
- TypeScript
- Tailwind CSS
- shadcn/ui 或轻量自写组件
- lucide-react
- 本地 Node 脚本生成 JSON 索引

第一版不需要数据库，先用构建脚本把 Markdown 转成 JSON：

```text
docs/**/*.md
  -> scripts/build_knowledge_index.py
  -> apps/knowledge-platform/src/data/knowledge-index.json
```

原因：

- 当前数据都在 Markdown。
- 本地静态页面就能先跑起来。
- 后续再接后端、搜索、向量库和模型。

## 8. 一期范围

一期目标：先把知识库看得见、筛得动、能关联。

### 8.1 必做

- 项目列表页。
- 项目详情页。
- 方案列表页。
- 方案详情页。
- 痛点列表页。
- 痛点详情页。
- 本地 Markdown -> JSON 索引脚本。
- 基础搜索和分类筛选。

### 8.2 暂不做

- 真正在线 LLM 对话。
- 复杂权限系统。
- 多用户。
- 向量数据库。
- PDF 上传解析。
- 自动面试评分。

### 8.3 一期验收标准

- 打开平台能看到所有项目卡片。
- 每个项目能看到类型、状态、关联方案和沉淀内容。
- 能按 `MCP / Agent Runtime / Tool Runtime / Productization` 筛选项目。
- 能进入方案页看到成熟做法和项目案例。
- 能进入痛点页看到痛点、依据、方法和行动项。

## 9. 二期范围

二期目标：加入面经与 AI 面试官。

### 9.1 面经导入

- 支持粘贴面经。
- 支持保存原始面经。
- 自动拆问题。
- 标记问题类型。
- 关联项目和 patterns。

### 9.2 答案生成

答案不能只背八股，必须结合你的项目：

```text
通用知识
  -> 当前项目实践
  -> 外部项目证据
  -> trade-off
  -> 可落地行动
```

### 9.3 面试官进化

系统需要维护：

```text
docs/interviews/interviewer-memory.md
```

记录：

- 高频问题。
- 你的薄弱点。
- 你项目中最值得讲的亮点。
- 常见追问链。
- 推荐回答结构。

## 10. 面试官设计

### 10.1 面试官应该怎么问

面试官不能只问：

```text
什么是 MCP？
```

而应该问：

```text
你在自己的项目里做了 Project Radar。
如果要接入 MCP 项目发现和工具调用生态，你会怎么设计 Tool Registry？
你怎么区分内建工具、插件工具和 MCP 工具？
Chrome DevTools MCP 给了你什么启发？
```

### 10.2 推荐回答结构

每个答案建议用五段式：

```text
1. 先定义问题
2. 说明为什么重要
3. 结合我的项目怎么做
4. 引用外部优秀项目证据
5. 说 trade-off 和下一步
```

示例：

```text
问题：你怎么理解 Tool Runtime？

回答结构：
- Tool Runtime 不是函数调用，而是模型影响外部世界的执行管线。
- 它重要是因为工具有副作用，需要权限、校验、日志和恢复。
- 我在项目里用 `docs/patterns/Tool 与 MCP 工具体系/tool-runtime-patterns.md` 沉淀了 Tool Definition -> Schema -> Permission -> Execution -> Result -> Telemetry。
- Chrome DevTools MCP 给我的启发是大结果要返回 artifact reference，而不是直接塞进上下文。
- 下一步我会在 Project Radar 评分里加入 artifact-aware 和 risk-level 字段。
```

## 11. 视觉和交互风格

这个平台不是营销官网，不需要大 hero。

它应该像一个安静、高密度、可扫描的知识工作台：

- 左侧导航。
- 顶部搜索。
- 中间列表/详情。
- 右侧关联信息。
- 卡片只用于项目、方案、痛点等重复项。
- 信息层级清楚，避免大段不可扫文本。

建议主导航：

```text
项目
方案
痛点
面经
面试官
雷达
设置
```

每个详情页右侧固定展示：

- 关联项目
- 关联方案
- 关联痛点
- 面试可问点
- 下一步行动

### 11.1 中文界面规范

平台界面文案默认使用中文。

可以保留英文的内容：

- 项目名，例如 `Claude Code`、`Goose`、`Chrome DevTools MCP`。
- 仓库名，例如 `aaif-goose/goose`。
- 专业名词和协议名，例如 `MCP`、`Tool Runtime`、`Agent Runtime`、`Provider`、`CLI`、`API`。
- 代码、命令、路径、配置字段。

需要翻译成中文的内容：

- 导航、按钮、状态、筛选项、说明文字。
- 页面标题和模块标题。
- 空状态、错误提示、帮助说明。
- 面试官反馈和推荐答案。

推荐风格：

```text
中文为主，英文点到为止。
专业名词首次出现时可以使用 “中文解释 + 英文术语”。
例如：工具运行时（Tool Runtime）、模型上下文协议（MCP）。
```

## 12. 开发阶段计划

### 阶段 1：产品规格和数据索引

- [x] 写产品规格文档。
- [ ] 新建 `docs/pain-points/`。
- [ ] 新建 `docs/interviews/`。
- [ ] 写 `scripts/build_knowledge_index.py`。
- [ ] 输出 `knowledge-index.json`。

### 阶段 2：前端应用骨架

- [ ] 新建 `apps/knowledge-platform/`。
- [ ] 建 Vite + React + TypeScript。
- [ ] 建路由和基础布局。
- [ ] 接入 JSON 数据。

### 阶段 3：项目/方案/痛点界面

- [ ] 项目列表。
- [ ] 项目详情。
- [ ] 方案列表。
- [ ] 方案详情。
- [ ] 痛点列表。
- [ ] 痛点详情。

### 阶段 4：面经与面试官

- [ ] 面经导入。
- [ ] 问题拆解。
- [ ] 项目关联。
- [ ] 推荐答案生成模板。
- [ ] 面试官追问模式。
- [ ] 面试记忆更新。

## 13. 风险和取舍

### 13.1 风险：一开始就做太复杂

不要第一版就做数据库、登录、向量检索、在线 LLM。先把已有 Markdown 知识可视化。

### 13.2 风险：页面好看但知识不可用

核心不是 UI 炫，而是信息结构清楚。每个页面都要服务学习和面试准备。

### 13.3 风险：面试官变成普通聊天机器人

面试官必须绑定你的项目、patterns 和外部项目证据。它要问“你为什么这样设计”，而不是泛泛问八股。

### 13.4 取舍：先本地静态，再智能交互

第一版先做静态可视化和结构化索引；第二版再接 LLM 做自我进化。

## 14. 当前最推荐的下一步

下一步直接进入实现：

1. 建 `docs/pain-points/`，把现有 patterns 抽成第一批痛点。
2. 建 `docs/interviews/`，定义面经数据结构和面试官记忆文件。
3. 写 `scripts/build_knowledge_index.py`，把项目、方案、痛点统一生成 JSON。
4. 新建 `apps/knowledge-platform/`，做项目界面和方案界面。

第一版只要能做到：

```text
打开页面
  -> 看项目
  -> 点项目看沉淀
  -> 按方案筛选
  -> 看痛点和解决方法
```

这个产品化方向就站住了。

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“Agent 项目知识平台产品化规格文档 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

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

> 目标：把“Agent 项目知识平台产品化规格文档”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

