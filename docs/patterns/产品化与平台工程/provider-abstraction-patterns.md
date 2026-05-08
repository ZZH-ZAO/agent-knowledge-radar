# 通用问题：Provider Abstraction

## 1. 问题定义

Provider Abstraction 解决的是：Agent Runtime 如何接入多个 LLM provider，同时把模型差异限制在适配层，保持上层 query loop、tool runtime、memory、UI 和 workflow 稳定。

## 2. 为什么重要

- 不同 provider 的 API、模型能力、tool calling、流式输出、错误格式和认证方式不同。
- Agent 产品不能因为切换模型就重写核心运行时。
- 企业场景常常需要 OpenAI、Anthropic、Bedrock、Vertex、本地模型或私有网关并存。

## 3. 常见错误做法

- 在业务逻辑里到处写 provider 分支。
- 把模型返回格式直接暴露给 runtime。
- 不统一 token、tool call、stream event、error、retry 语义。
- 没有 capability negotiation，默认所有模型能力一样。

## 4. 成熟系统通常怎么做

- Provider Interface / Trait
- Model Capability Metadata
- Unified Message Format
- Unified Tool Call Format
- Streaming Event Normalizer
- Error / Retry Policy
- Auth / Env / Config Adapter
- Provider-Specific Escape Hatch

## 5. 优秀项目案例

| 项目 | 值得学习的点 | 证据 |
| --- | --- | --- |
| aaif-goose/goose | README 强调 15+ LLM providers，`AGENTS.md` 指向 Provider trait 实现路径 | `docs/external-projects/完整开源 Agent 平台样本/aaif-goose-goose.md` |
| anthropics/claude-code | 官方 CHANGELOG 持续出现 Bedrock、Vertex、model gateway、service tier 等企业模型接入信号 | `docs/anthropics-claude-code-official-distillation.md` |

## 6. 可迁移技术框架

```text
Runtime Request
  -> Unified Message
  -> Provider Selection
  -> Capability Check
  -> Provider Adapter
  -> Raw Model Response
  -> Stream / Tool / Error Normalizer
  -> Runtime Event
```

## 7. 我的项目行动项

- [ ] 为模型 provider 定义统一接口。
- [ ] 给每个 provider 声明 capability：tool calling、vision、streaming、JSON mode、context length。
- [ ] 把 provider 原始错误转换成统一错误类型。
- [ ] 保留 provider-specific options，但不要污染主 runtime。

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“通用问题：Provider Abstraction 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

### 1. 这件事到底考什么

这里考察的是能不能把长链路任务里的上下文当成工程资源管理，而不是把所有历史都塞给模型。

如果只回答功能点，说明还停留在“看过项目”的层面；如果能回答问题来源、工程约束、取舍和行动项，才说明这份沉淀真正进入了自己的方法论。

### 2. 口语版回答

我会把 Memory 理解成上下文治理系统，而不是聊天记录。它至少要解决作用域、生命周期、存储、召回、注入和隐私边界。真正有价值的记忆不是越多越好，而是能在正确时间召回正确证据，并减少重复读取和重复推理。

这段回答可以直接用于复盘、面试或方案评审。它的结构是：先定义问题，再讲工程边界，最后落到可迁移做法。

### 3. 工程视角拆解

可以按四层来理解：

- 问题层：这个设计到底在解决什么不稳定、不可控或不可复用的问题。
- 机制层：它用了哪些结构、协议、运行时、文档或流程来解决。
- 证据层：有哪些 README、源码、指标、案例或平台行为能证明它不是口号。
- 迁移层：它对 `claude-code-sourcemap`、知识平台、Project Radar 或面试训练有什么可执行启发。

### 4. 常见误区

把 memory 做成无差别追加日志，导致上下文越来越大、旧信息污染新任务。

另一个常见误区是只把优秀项目当作模板照抄。真正应该学的是它为什么这样拆分，以及这个拆分在自己的场景里是否仍然成立。

### 5. Trade-off 与边界

记忆越结构化，维护成本越高；但没有结构化，模型长期任务会反复读取、遗忘关键约束，甚至引用过期事实。

判断一个方案是否成熟，不是看它有没有更多能力，而是看它有没有明确说明代价、适用场景和不适用场景。

### 6. 当前项目行动项

- [ ] 把任务摘要、文件摘要、面试弱点、项目行动项分层存储，并给每类记忆定义 freshness 校验。
- [ ] 把这份文档中的通用问题同步到对应 `docs/patterns/` 文档，避免停留在单项目笔记。
- [ ] 在平台详情页中保留“口语版回答、工程拆解、误区、行动项”，让它能直接用于学习和面试表达。

### 7. 面试官追问

**追问：这个项目或方案最值得学习的不是功能，而是什么？**

答：最值得学习的是它如何把一个模糊问题变成可治理的工程结构。功能只是表层，真正可迁移的是它的边界划分、执行流程、证据链和取舍。

**追问：如果迁移到当前平台，第一步应该做什么？**

答：第一步不是照搬实现，而是把它抽象成平台中的一个通用问题，补齐文档、索引、行动项和验证方式，让后续沉淀能自动进入平台展示。

## 行业痛点研究版补充

> 目标：把“通用问题：Provider Abstraction”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

