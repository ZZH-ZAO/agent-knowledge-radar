# Tencent CSIG Interviewer Memory（面试官记忆）

> 这份文件给后续 AI 面试官使用，用来持续追踪你的面试弱点和训练策略。

## 1. 候选人当前定位

- 测试开发方向。
- 主项目：AI 测试用例生成系统。
- 辅项目：智慧食安多租户监管平台。
- 技术表达重点：Python、RAG、Prompt / Context Engineering、AI Critic、pytest、接口自动化、多租户、状态机、质量闭环。

## 2. 真实一面暴露的问题

### 问题 1：项目主线不够锋利

原来容易讲成：

```text
我做了 RAG、Prompt、评估、反馈
```

以后必须讲成：

```text
RAG 解决证据选择
结构化生成解决结果稳定
AI Critic 解决质量评估
人工回流解决经验沉淀
```

### 问题 2：RAG 容易被追细节

重点追：

- chunk 为什么这样切。
- query rewrite / HyDE / 多查询什么时候用。
- hybrid retrieval 怎么融合。
- rerank 权重怎么来。
- Top-K 怎么选。
- 怎么判断是召回失败、排序失败还是生成失败。

### 问题 3：评估模块要讲得更像生产系统

必须强调：

- AI Critic 是辅助质检，不是最终裁判。
- 评估要看 PRD、证据、生成结果三者一致性。
- 人工确认后才能回流。
- bad case 要进入回归集。

### 问题 4：Agent / MCP / Skills 要分层

固定记忆：

```text
Function Calling = 动作契约
Tool Use = 外部行动能力
MCP = 能力接入协议
Agent = 受控任务推进循环
Skills = 经验资产化
```

### 问题 5：算法题需要固定模板

当前不能只靠项目亮点抵消算法短板。

短期优先练：

- 合并两个有序链表。
- 反转链表。
- 有效括号。
- 二分查找。
- 两数之和。

## 3. 旧目录证据卡

面试官可以要求候选人把自己的项目和旧案例对齐：

- `cekai-auto-prd-test-agent`：PRD 到测试用例工作台，RAG 约束生成，AI evaluator。
- `testing-agent-review-playbook`：成熟测试 Agent 要有 workflow、retrieval、generation、evaluation、bad case。
- `promptfoo`：AI 系统测试和 eval 要工程化。
- `giskard`：多轮 Agent 和 RAG evaluation 要可复跑、可判定、可回归。
- `agentset`：RAG 不是功能点，而可以成为 ingestion、indexing、eval、API、hosting 的平台能力。
- `fault-diagnosis`：垂直 Agent 要围绕证据链和报告交付，而不是泛泛聊天。

## 4. 后续训练策略

每次模拟面试按这个顺序：

1. 1 分钟项目介绍。
2. 10 分钟 RAG 连续追问。
3. 5 分钟 AI Critic / feedback / memory。
4. 5 分钟 Agent / MCP / Skills。
5. 5 分钟智慧食安平台测开追问。
6. 5 分钟基础题。
7. 10 分钟算法题。

## 5. 面试官追问模板

当回答过于抽象时，追问：

- 你能举一个真实 bad case 吗？
- 这个指标是怎么算的？
- 如果 Top-K 里没有关键规则，你怎么定位？
- 如果 Top-K 里有但模型没生成，是哪里的问题？
- 这个能力现在实现到什么程度，哪些是后续规划？
- 你怎么避免把人工反馈污染知识库？

## 行业痛点研究版补充

> 目标：把“Tencent CSIG Interviewer Memory（面试官记忆）”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

