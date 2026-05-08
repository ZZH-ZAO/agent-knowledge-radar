# 旧体系项目沉淀：cekai-auto-prd-test-agent

> 来源：`.claude/docs`  
> 迁移日期：2026-05-04  
> 旧案例 ID：`cekai-auto-prd-test-agent`  
> 类型：Testing Agent / RAG / Vertical Workflow  
> 迁移优先级：medium  
> 关联方案：observability、productization

## 1. 项目一句话

研究 PRD 到测试用例的结构化生成、local RAG、人类修订和 AI 质量评审。

## 2. 这件事到底考什么

AI / Agent 系统如何证明输出质量，而不是只依赖一次看起来正确的生成结果。

旧文档的价值不在于保留历史文件本身，而在于把里面的项目判断、架构分析、路线规划和模板沉淀，转成现在平台能继续索引、阅读、追问和行动的知识资产。

## 3. 口语版回答

我会把它理解成质量治理问题：要把用例、评测、人工确认、失败分类和回归检查串起来，让模型输出从一次性结果变成可持续改进的质量闭环。

如果面试官追问“你为什么要迁移旧文档”，可以这样答：旧体系里已经有大量项目分析和模板，如果不迁移，新平台看到的只是新文档，会漏掉历史判断。迁移后它们会进入项目页、方案页和痛点页，继续参与平台的自动索引和深度阅读。

## 4. 旧文档证据

- `.claude/docs/user/cekai-auto-prd-test-agent/analysis.md`：Project name: ByteDance--Auto_prd_test_agent Project path: `D:\测开\ByteDance--Auto_prd_test_agent` 如果只看名字，你可能会以为它是一个“自动测试 Agent”。 但真正读完代码以后，更准确的判断是： > 它首先是一个面向“PRD 转测试用例”的垂直 AI 工作流系统，其次才是一个带有 Agent 味道的应用。 也就是说，它不是 `claude-code-sourcemap`、`deer-flow` 那种“通用 Agent runtime”，不是那种重点解决“模型如何稳定推理、如何标准化 tool calling、如何组织多 Agent 控制面”的系统。
- `.claude/docs/agent/cekai-auto-prd-test-agent/analysis-condensed.md`：Project name: ByteDance--Auto_prd_test_agent Project path: `D:\测开\ByteDance--Auto_prd_test_agent` main control plane is in prompts orchestration center is the Streamlit UI layer ChromaDB with `history_cases` and `company_knowledge` provider switching across Gemini and Qwen
- `.claude/docs/user/cekai-auto-prd-test-agent/architecture-walkthrough.md`：Project name: ByteDance--Auto_prd_test_agent Project path: `D:\测开\ByteDance--Auto_prd_test_agent` 如果我要用一句话来介绍这个项目改进后的方向，我会这样说： > 它会从一个“PRD 转测试用例的生成工作台”，升级成一个“围绕知识检索、规则证据、人工修订、AI 评审、坏例回流和回归验证共同运转的测试 Agent 系统”。 这句话里最重要的，不是“Agent”两个字，而是后面那几个能力： 因为真正决定这类系统上限的，往往不是模型会不会说，而是系统能不能形成闭环。
- `.claude/docs/user/cekai-auto-prd-test-agent/further-improvement-directions.md`：Project name: ByteDance--Auto_prd_test_agent Project path: `D:\测开\ByteDance--Auto_prd_test_agent` 前面的文档已经讲了很多工程层改造： 这些都很重要。 但如果再往前想一步，这个项目还有一个更深层的问题： > 它现在更擅长“把已有材料变成测试用例”，但还不够擅长“像真正测试设计者那样思考”。 所以它下一步如果想更强，我觉得应该从五个方面继续增强： 1. 中间表示层 2. 测试设计推理层 3. 检索约束层 4. 多轮质量评测层
- `.claude/docs/user/cekai-auto-prd-test-agent/implementation-sketch.md`：Project name: ByteDance--Auto_prd_test_agent Project path: `D:\测开\ByteDance--Auto_prd_test_agent` 前面的几份文档分别回答了： 这一份再往前走一步，回答的是： > 如果现在真的开始动手改，第一版应该怎么落。 也就是说，这份文档不再主要讲“原则”，而是讲： 如果一下子把前面说的所有能力全做进去，项目会很容易失控。 所以我建议第一版改造只盯住 5 个目标： 1. 把 UI 中的主流程拆到 service 层 2. 补上 hybrid retrieval
- `.claude/docs/user/cekai-auto-prd-test-agent/improvement-roadmap.md`：Project name: ByteDance--Auto_prd_test_agent Project path: `D:\测开\ByteDance--Auto_prd_test_agent` 如果只从表面看，很多人第一反应会是： 但真正从系统角度看，这个项目的主要瓶颈并不在“模型太弱”，而在下面四件事： 1. 编排逻辑过度集中在 UI 层 2. RAG 还停留在轻量检索增强阶段 3. 历史资产能回存，但还不能真正形成经验学习 4. 评审已经有了，但还没有形成质量闭环和组织级复用 所以这类项目如果想继续变强，正确方向不是“堆功能”，而是：

## 5. 可迁移的工程问题

- 这个案例对应的不是单个功能，而是 `Testing Agent / RAG / Vertical Workflow` 方向的工程问题。
- 它应该被归并到 `observability、productization` 等 patterns 中，而不是停留在旧目录。
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

- [ ] 把该案例迁移到 Observability / Evaluation / Testing Agent 方案中，补充指标、失败分类和面试追问。
- [ ] 检查旧文档中的 roadmap、template、comparison 是否需要拆成单独 pattern。
- [ ] 在平台中通过项目页阅读该案例，并根据内容补充痛点页证据。
- [ ] 后续不再向 `.claude/docs` 新增沉淀，新内容统一进入 `docs/` 新体系。

## 9. 面试官追问

**追问：旧文档迁移和简单归档有什么区别？**

答：归档只是保存文件，迁移是让旧知识重新进入当前平台的索引、阅读、方案抽象和行动项闭环。

**追问：怎么避免迁移后目录更乱？**

答：按案例收束到 `旧体系迁移项目样本`，用文档内部引用旧路径，不把旧目录结构原样复制出来。

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“旧体系项目沉淀：cekai-auto-prd-test-agent 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

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

> 目标：把“旧体系项目沉淀：cekai-auto-prd-test-agent”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

