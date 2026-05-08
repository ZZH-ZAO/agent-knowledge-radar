# 旧体系共享模板迁移

这里收束 `.claude/docs/*/shared` 里的旧模板和 playbook。它们不作为项目样本，而是作为后续写作、评审、测试 Agent、输出质量控制和产品化设计的模板资产。

## 模板清单

### agent-output-quality-control-template

- 旧路径：`.claude/docs/user/shared/agent-output-quality-control-template.md`
- 摘要：Project name: agent-output-quality-control-template Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 这不是一份“让模型回答更聪明”的模板。 它要解决的是另外一类经常被忽略、但真实项目里非常痛的问题： 这份模板适合回答的问题是： > 当一个 Agent 系统已经开始产出页面、文档、图示或方案时，怎样给它补一层“表达质量控制层”，让它的产出更稳定、更一致、更可复用。 它特别适合下面这类项目：

### agent-project-classification-map

- 旧路径：`.claude/docs/user/shared/agent-project-classification-map.md`
- 摘要：Project name: Agent project classification map Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 很多人看 Agent 项目时最容易犯的错，是把完全不同目标的项目放在一起比较。 例如： 这些项目表面上都叫 Agent，但它们真正解决的问题完全不同。 所以学习 Agent 工程的第一步，不是看它“用了什么模型”，而是先判断： > 这个项目到底属于哪一类，它最强的创新层又在哪一层。 你可以把这张图当成一个学习导航系统。

### development-phase-report-template

- 旧路径：`.claude/docs/user/shared/development-phase-report-template.md`
- 摘要：Document type: shared template Purpose: record each meaningful development phase in a way that is reusable, reviewable, and easy to continue later Use this template when a task spans multiple phases and each phase should leave behind a clear progress record. Typical use cases:

### industrial-agent-design-template

- 旧路径：`.claude/docs/user/shared/industrial-agent-design-template.md`
- 摘要：Project name: industrial-agent-design-template Project path: `D:\claude-code-sourcemap\.claude\docs\user` 这不是一份“写给模型看的 prompt 模板”，而是一份“设计工业 Agent 系统时的分层模板”。 它适合解决的问题是： 如果你以后做的场景类似这些： 这份模板就适合直接参考。 在工业 Agent 里，技术选型通常不是第一问题，第一问题是系统目标。 常见有三类： 很多项目失败，是因为这三类混在一起，却没有主次。

### productized-agent-platform-template

- 旧路径：`.claude/docs/user/shared/productized-agent-platform-template.md`
- 摘要：Project name: productized-agent-platform-template Project path: `D:\claude-code-sourcemap\.claude\docs\user` 这份模板适合的不是所有 Agent 项目，而是这类项目： 典型场景包括： 如果你做的是一个很轻量、很单点的 Agent，这份模板可能太重；但如果你想做一个真正可长期发展的 Agent 产品，这份模板很有参考价值。 这两者差别很大。 如果只是普通产品加聊天框，Agent 往往只是边缘功能。 如果是 Agent 产品，Agent 就会影响：

### refactoring-2nd-edition-notes

- 旧路径：`.claude/docs/user/shared/refactoring-2nd-edition-notes.md`
- 摘要：Project name: Refactoring, 2nd Edition Project path: `D:\claude-code-sourcemap\重构-改善既有代码的设计[第2版].pdf` 很多人一提到《重构》，首先想到的是： 这些当然重要，但如果只把这本书理解成“重构手法词典”，其实会低估它。 这本书真正最值得学的是： > 如何在不改变外部行为的前提下，用一连串小而可控的动作，持续改善代码设计。 这里面最关键的不是“目标多漂亮”，而是： 这套工作方式，对今天的软件开发仍然非常重要。 虽然这本书不是专门写给 Agent 时代的，但它和今天的很多问题其实高度相关。

### refactoring-review-prompt-templates

- 旧路径：`.claude/docs/user/shared/refactoring-review-prompt-templates.md`
- 摘要：Project name: refactoring-review-prompt-templates Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 这份模板不是教模型“怎么聊天更像专家”，而是让它在审代码时： 它特别适合下面几类场景： 适合： ```text 请用“重构导向”的方式审查这段代码，不要只给笼统评价。 请按下面规则输出： 1. 先识别可能存在的坏味道，例如：long function、duplicated code、data clumps、feature envy、repeated switches、large class、message

### refactoring-smell-to-action-cheatsheet

- 旧路径：`.claude/docs/user/shared/refactoring-smell-to-action-cheatsheet.md`
- 摘要：Project name: refactoring-smell-to-action-cheatsheet Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 这份表不是机械规则表，而是： 推荐使用顺序： 1. 先识别更像哪种坏味道 2. 再判断它带来的维护成本 3. 再从 1 到 3 个最小动作开始 4. 最后补一句测试或风险提示 如果你想把建议说得更稳，可以固定按这个句式来： 1. 我怀疑这里更像 `某种坏味道` 2. 它带来的主要成本是 `某种维护/扩展风险`

### sdk-wrapped-agent-runtime-template

- 旧路径：`.claude/docs/user/shared/sdk-wrapped-agent-runtime-template.md`
- 摘要：Project name: sdk-wrapped-agent-runtime-template Project path: `D:\claude-code-sourcemap\.claude\docs\user` 很多团队做 Agent 产品时，会直接把某个 SDK 接到前端： 这种做法在原型期很快，但产品期往往不够。 所谓“SDK 包装型 Agent runtime”，指的是： > 在底层 Agent SDK 之上，再建立一层应用级运行时，把底层事件、会话和工具语义，转换成产品真正需要的状态系统和交互系统。 这类 runtime 通常会处理：

### super-agent-harness-design-template

- 旧路径：`.claude/docs/user/shared/super-agent-harness-design-template.md`
- 摘要：Project name: Super Agent Harness design template Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 这个模板适合分析下面这类项目： 它不主要适合： 因为这类项目的关键问题通常不是： 而是： 在分析任何 super agent harness 之前，先回答这四个问题。 常见答案可能是： 一定要区分清楚： 常见可能在： 不要平均用力。一定要判断： 每个做法都要追问： 例如： 分析时建议至少按下面八层去看。

### testing-agent-design-template

- 旧路径：`.claude/docs/user/shared/testing-agent-design-template.md`
- 摘要：Project name: shared Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 这份模板适合分析或设计这类项目： 也就是说，它适合的是： > 以“测试资产生产”为核心，而不是以“自由聊天”为核心的 Agent 系统。 建议固定按七层来分析： 1. 产品交互层 2. 工作流编排层 3. 检索与证据层 4. 生成与评审层 5. 记忆与资产层 6. 质量与验证层 7. 平台治理层 如果一份分析没有把这七层讲清楚，通常说明它还停留在功能罗列阶段。

### testing-agent-landscape-map

- 旧路径：`.claude/docs/user/shared/testing-agent-landscape-map.md`
- 摘要：Project name: shared Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 如果只看名字，这四个项目都和“测试”有关，但它们解决的问题其实不一样： 研究“多 Agent 怎么提升测试生成” 研究“怎么把 PRD 转测试用例做成工作台产品” 研究“怎么测试 AI 系统本身” 研究“怎么评估多轮 Agent 和 RAG 系统” 所以它们不是互相替代关系，而是可以拼成一条很完整的链： > 测试生成 -> 测试工作台 -> 测试质量 -> 多轮评测与回归

### agent-project-classification-map-condensed

- 旧路径：`.claude/docs/agent/shared/agent-project-classification-map-condensed.md`
- 摘要：Project name: Agent project classification map Project path: `D:\claude-code-sourcemap\.claude\docs\agent\shared` Do not analyze new Agent projects as a flat list of features. First classify the project type, then compare it to the right historical case. 1. Identify the primary type:

### refactoring-review-playbook

- 旧路径：`.claude/docs/agent/shared/refactoring-review-playbook.md`
- 摘要：Project name: shared refactoring review playbook Project path: `D:\claude-code-sourcemap\.claude\docs\agent\shared` Look for named signals rather than generic discomfort: When you report a finding, prefer this structure: 1. name the likely smell 2. explain the maintenance cost it creates

### testing-agent-review-playbook

- 旧路径：`.claude/docs/agent/shared/testing-agent-review-playbook.md`
- 摘要：Project name: shared Project path: `D:\claude-code-sourcemap\.claude\docs\agent\shared` When reviewing a testing-oriented Agent project, first decide which of these it really is: mostly one-shot case generation with light UI testing workflow system with retrieval, refinement, and review

## 行业痛点研究版补充

> 目标：把“旧体系共享模板迁移”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

