# 旧体系项目沉淀：shared templates

> 来源：`.claude/docs`  
> 迁移日期：2026-05-04  
> 旧案例 ID：`shared`  
> 类型：Templates / Playbook  
> 迁移优先级：low  
> 关联方案：observability、frontend-design-control

## 1. 项目一句话

旧体系共享模板，包括测试 Agent 设计模板、输出质量控制模板和 refactoring review playbook。

## 2. 这件事到底考什么

如何从旧体系项目案例中抽象出可迁移的 Agent 工程问题。

旧文档的价值不在于保留历史文件本身，而在于把里面的项目判断、架构分析、路线规划和模板沉淀，转成现在平台能继续索引、阅读、追问和行动的知识资产。

## 3. 口语版回答

我会先看它解决的真实问题，再看旧文档里的证据和实现建议，最后归并到当前 patterns 与平台行动项。

如果面试官追问“你为什么要迁移旧文档”，可以这样答：旧体系里已经有大量项目分析和模板，如果不迁移，新平台看到的只是新文档，会漏掉历史判断。迁移后它们会进入项目页、方案页和痛点页，继续参与平台的自动索引和深度阅读。

## 4. 旧文档证据

- `.claude/docs/user/shared/agent-output-quality-control-template.md`：Project name: agent-output-quality-control-template Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 这不是一份“让模型回答更聪明”的模板。 它要解决的是另外一类经常被忽略、但真实项目里非常痛的问题： 这份模板适合回答的问题是： > 当一个 Agent 系统已经开始产出页面、文档、图示或方案时，怎样给它补一层“表达质量控制层”，让它的产出更稳定、更一致、更可复用。 它特别适合下面这类项目：
- `.claude/docs/user/shared/agent-project-classification-map.md`：Project name: Agent project classification map Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared` 很多人看 Agent 项目时最容易犯的错，是把完全不同目标的项目放在一起比较。 例如： 这些项目表面上都叫 Agent，但它们真正解决的问题完全不同。 所以学习 Agent 工程的第一步，不是看它“用了什么模型”，而是先判断： > 这个项目到底属于哪一类，它最强的创新层又在哪一层。 你可以把这张图当成一个学习导航系统。
- `.claude/docs/user/shared/development-phase-report-template.md`：Document type: shared template Purpose: record each meaningful development phase in a way that is reusable, reviewable, and easy to continue later Use this template when a task spans multiple phases and each phase should leave behind a clear progress record. Typical use cases:
- `.claude/docs/user/shared/industrial-agent-design-template.md`：Project name: industrial-agent-design-template Project path: `D:\claude-code-sourcemap\.claude\docs\user` 这不是一份“写给模型看的 prompt 模板”，而是一份“设计工业 Agent 系统时的分层模板”。 它适合解决的问题是： 如果你以后做的场景类似这些： 这份模板就适合直接参考。 在工业 Agent 里，技术选型通常不是第一问题，第一问题是系统目标。 常见有三类： 很多项目失败，是因为这三类混在一起，却没有主次。
- `.claude/docs/user/shared/productized-agent-platform-template.md`：Project name: productized-agent-platform-template Project path: `D:\claude-code-sourcemap\.claude\docs\user` 这份模板适合的不是所有 Agent 项目，而是这类项目： 典型场景包括： 如果你做的是一个很轻量、很单点的 Agent，这份模板可能太重；但如果你想做一个真正可长期发展的 Agent 产品，这份模板很有参考价值。 这两者差别很大。 如果只是普通产品加聊天框，Agent 往往只是边缘功能。 如果是 Agent 产品，Agent 就会影响：
- `.claude/docs/user/shared/refactoring-2nd-edition-notes.md`：Project name: Refactoring, 2nd Edition Project path: `D:\claude-code-sourcemap\重构-改善既有代码的设计[第2版].pdf` 很多人一提到《重构》，首先想到的是： 这些当然重要，但如果只把这本书理解成“重构手法词典”，其实会低估它。 这本书真正最值得学的是： > 如何在不改变外部行为的前提下，用一连串小而可控的动作，持续改善代码设计。 这里面最关键的不是“目标多漂亮”，而是： 这套工作方式，对今天的软件开发仍然非常重要。 虽然这本书不是专门写给 Agent 时代的，但它和今天的很多问题其实高度相关。

## 5. 可迁移的工程问题

- 这个案例对应的不是单个功能，而是 `Templates / Playbook` 方向的工程问题。
- 它应该被归并到 `observability、frontend-design-control` 等 patterns 中，而不是停留在旧目录。
- 如果旧文档里包含 roadmap、template、comparison 或 upgrade plan，应进一步拆成平台行动项。

## 6. 常见误区

- 只把旧文档复制到新目录，不做问题抽象。
- 只保留 README，不迁移 analysis、roadmap、template 和 comparison。
- 只把它当作历史材料，不让它进入平台索引。
- 迁移后不更新相关 patterns，导致知识仍然是孤立笔记。

## 7. Trade-off 与边界

旧文档迁移有两个边界：

- 不能无差别把所有旧文件平铺到新目录，否则目录会更乱。
- 不能只迁移摘要，否则会丢失旧文档里真正有价值的架构判断和行动建议。

所以当前采用“按案例生成深度沉淀文档 + 保留旧路径证据 + 后续逐步拆分专题”的方式。

## 8. 当前项目行动项

- [ ] 把该案例作为旧体系迁移样本，继续补充项目证据、通用问题和行动项。
- [ ] 检查旧文档中的 roadmap、template、comparison 是否需要拆成单独 pattern。
- [ ] 在平台中通过项目页阅读该案例，并根据内容补充痛点页证据。
- [ ] 后续不再向 `.claude/docs` 新增沉淀，新内容统一进入 `docs/` 新体系。

## 9. 面试官追问

**追问：旧文档迁移和简单归档有什么区别？**

答：归档只是保存文件，迁移是让旧知识重新进入当前平台的索引、阅读、方案抽象和行动项闭环。

**追问：怎么避免迁移后目录更乱？**

答：按案例收束到 `旧体系迁移项目样本`，用文档内部引用旧路径，不把旧目录结构原样复制出来。

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“旧体系项目沉淀：shared templates 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

### 1. 这件事到底考什么

这里考察的是 Agent 系统从 demo 走向可用产品时，如何处理风险、审计和可复现。

如果只回答功能点，说明还停留在“看过项目”的层面；如果能回答问题来源、工程约束、取舍和行动项，才说明这份沉淀真正进入了自己的方法论。

### 2. 口语版回答

我会把权限、沙箱和可观测性看成 Agent 产品化的底座。模型输出不稳定，工具又可能有副作用，所以系统必须知道什么动作能自动执行，什么动作要确认，出错以后如何回放，用户如何知道 Agent 做过什么。

这段回答可以直接用于复盘、面试或方案评审。它的结构是：先定义问题，再讲工程边界，最后落到可迁移做法。

### 3. 工程视角拆解

可以按四层来理解：

- 问题层：这个设计到底在解决什么不稳定、不可控或不可复用的问题。
- 机制层：它用了哪些结构、协议、运行时、文档或流程来解决。
- 证据层：有哪些 README、源码、指标、案例或平台行为能证明它不是口号。
- 迁移层：它对 `claude-code-sourcemap`、知识平台、Project Radar 或面试训练有什么可执行启发。

### 4. 常见误区

只做功能成功路径，不记录失败、拒绝、审批和执行证据。

另一个常见误区是只把优秀项目当作模板照抄。真正应该学的是它为什么这样拆分，以及这个拆分在自己的场景里是否仍然成立。

### 5. Trade-off 与边界

严格治理会降低一些自动化速度，但能换来用户信任、问题定位和企业场景可落地。

判断一个方案是否成熟，不是看它有没有更多能力，而是看它有没有明确说明代价、适用场景和不适用场景。

### 6. 当前项目行动项

- [ ] 在项目雷达和平台中把安全治理作为评分维度，沉淀项目时必须记录其权限、沙箱和审计设计。
- [ ] 把这份文档中的通用问题同步到对应 `docs/patterns/` 文档，避免停留在单项目笔记。
- [ ] 在平台详情页中保留“口语版回答、工程拆解、误区、行动项”，让它能直接用于学习和面试表达。

### 7. 面试官追问

**追问：这个项目或方案最值得学习的不是功能，而是什么？**

答：最值得学习的是它如何把一个模糊问题变成可治理的工程结构。功能只是表层，真正可迁移的是它的边界划分、执行流程、证据链和取舍。

**追问：如果迁移到当前平台，第一步应该做什么？**

答：第一步不是照搬实现，而是把它抽象成平台中的一个通用问题，补齐文档、索引、行动项和验证方式，让后续沉淀能自动进入平台展示。

## 行业痛点研究版补充

> 目标：把“旧体系项目沉淀：shared templates”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

