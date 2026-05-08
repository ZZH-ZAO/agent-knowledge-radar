# 旧体系项目沉淀：deer-flow

> 来源：`.claude/docs`  
> 迁移日期：2026-05-04  
> 旧案例 ID：`deer-flow`  
> 类型：Agent Runtime / MCP / Memory / Permission / Sandbox  
> 迁移优先级：high  
> 关联方案：agent-runtime、plugin-system、mcp-integration、permission-sandbox

## 1. 项目一句话

研究 super-agent harness 如何组织 middleware、skills、MCP、memory、subagents 和 sandbox。

## 2. 这件事到底考什么

Agent 如何安全、可追踪地接入外部工具生态。

旧文档的价值不在于保留历史文件本身，而在于把里面的项目判断、架构分析、路线规划和模板沉淀，转成现在平台能继续索引、阅读、追问和行动的知识资产。

## 3. 口语版回答

我会把它理解成 Tool Runtime 问题：工具不是函数，而是带权限、状态、结果治理和审计要求的外部行动。

如果面试官追问“你为什么要迁移旧文档”，可以这样答：旧体系里已经有大量项目分析和模板，如果不迁移，新平台看到的只是新文档，会漏掉历史判断。迁移后它们会进入项目页、方案页和痛点页，继续参与平台的自动索引和深度阅读。

## 4. 旧文档证据

- `.claude/docs/user/deer-flow/analysis.md`：Project name: DeerFlow Project path: `D:\deer-flow` DeerFlow 不是一个单功能垂直 Agent，也不是一个只会跑 Deep Research 的工作流脚本。 它更准确的定位是： > 一个面向长任务、多工具、多子代理、多运行环境的通用 Super Agent Harness，并且同时给出了一套建立在这个底座之上的参考应用。 它自己官方文档已经把这个区别讲得很清楚： 是运行时底座、Python SDK、可复用核心能力 是基于 Harness 搭出来的最佳实践产品实现
- `.claude/docs/agent/deer-flow/analysis-condensed.md`：Project name: DeerFlow Project path: `D:\deer-flow` DeerFlow is a super-agent harness plus reference app. Important distinction: Not a narrow vertical workflow system. Best understood as a configurable agent operating substrate. Reusable lesson: Memory is not just prompt history.
- `.claude/docs/user/deer-flow/vs-claude-code-sourcemap-vs-claude-code.md`：Project name: DeerFlow / claude-code-sourcemap / claude-code Project path: `D:\deer-flow` / `D:\claude-code-sourcemap` 如果把这三个项目放在一条连续谱上，我会这样理解： 更像 `Agent engine` 更像 `Agent harness` 更像 `Agent platform` 这不是说谁高谁低，而是说它们在回答不同的问题。 它最像在回答： > 一个 serious Agent 的执行内核，到底是怎么运转的？
- `.claude/docs/user/deer-flow/vs-claude-code-sourcemap.md`：Project name: DeerFlow / claude-code-sourcemap Project path: `D:\deer-flow` / `D:\claude-code-sourcemap` 如果只看表面，你会觉得这两个项目很像： 但如果更深一层看，它们的设计重心其实不同。 它更像： > 一个围绕 coding agent 主循环而展开的“内核级运行机制样本”。 它最值得学的是： 也就是说，它更像在回答： 它更像： > 一个可被别人复用、改造、部署和扩展的“Agent Harness”。 它最值得学的是：

## 5. 可迁移的工程问题

- 这个案例对应的不是单个功能，而是 `Agent Runtime / MCP / Memory / Permission / Sandbox` 方向的工程问题。
- 它应该被归并到 `agent-runtime、plugin-system、mcp-integration、permission-sandbox` 等 patterns 中，而不是停留在旧目录。
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

- [ ] 把该案例同步到 Tool Runtime / MCP Integration / Browser Tool Runtime 方案中。
- [ ] 检查旧文档中的 roadmap、template、comparison 是否需要拆成单独 pattern。
- [ ] 在平台中通过项目页阅读该案例，并根据内容补充痛点页证据。
- [ ] 后续不再向 `.claude/docs` 新增沉淀，新内容统一进入 `docs/` 新体系。

## 9. 面试官追问

**追问：旧文档迁移和简单归档有什么区别？**

答：归档只是保存文件，迁移是让旧知识重新进入当前平台的索引、阅读、方案抽象和行动项闭环。

**追问：怎么避免迁移后目录更乱？**

答：按案例收束到 `旧体系迁移项目样本`，用文档内部引用旧路径，不把旧目录结构原样复制出来。

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“旧体系项目沉淀：deer-flow 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

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

> 目标：把“旧体系项目沉淀：deer-flow”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

