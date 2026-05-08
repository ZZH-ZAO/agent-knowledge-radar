# Testing Agent 项目横向图

## Summary

- Project name: shared
- Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared`
- Document type: user
- Purpose: connect QAagent, ByteDance--Auto_prd_test_agent, promptfoo, and giskard into one learning map, so a human reader can understand what each project solves, where each one is strong, and how they complement each other in the testing Agent landscape

## 一、先给结论：这四个项目不是同一类东西，但正好能拼成一条完整的测试 Agent 学习线

如果只看名字，这四个项目都和“测试”有关，但它们解决的问题其实不一样：

- `QAagent`
  研究“多 Agent 怎么提升测试生成”
- `ByteDance--Auto_prd_test_agent`
  研究“怎么把 PRD 转测试用例做成工作台产品”
- `promptfoo`
  研究“怎么测试 AI 系统本身”
- `giskard`
  研究“怎么评估多轮 Agent 和 RAG 系统”

所以它们不是互相替代关系，而是可以拼成一条很完整的链：

> 测试生成 -> 测试工作台 -> 测试质量 -> 多轮评测与回归

## 二、四个项目分别代表什么位置

### 1. `QAagent`

它代表的是：

- 测试 Agent 的研究型原型层

它最强的是：

- 多 Agent 分工
- 中间推理表示
- 覆盖率导向思路

它回答的问题是：

> 怎样通过“先推理实现，再生成测试”提升测试质量？

### 2. `ByteDance--Auto_prd_test_agent`

它代表的是：

- 测试 Agent 的工作台产品层

它最强的是：

- PRD -> 测试用例工作流
- Prompt 规程化
- RAG 约束生成
- 人工微调
- evaluator

它回答的问题是：

> 怎样把测试生成做成一个可用的业务工作台？

### 3. `promptfoo`

它代表的是：

- AI 系统测试平台层

它最强的是：

- eval
- benchmark
- red team
- CI/CD 中的 AI 质量治理

它回答的问题是：

> 当 Agent 系统已经能工作后，怎么系统性测试它？

### 4. `giskard`

它代表的是：

- Agent 评测与 RAG 评测层

它最强的是：

- multi-turn scenario
- groundedness
- LLM-as-judge
- RAG evaluation

它回答的问题是：

> 怎样测试多轮 Agent 和 retrieval-backed 系统，而不是只看单轮输出？

## 三、如果把它们排成一条学习路径，应该怎么排

我建议这样排：

### 第一步看 `QAagent`

先理解：

- 测试生成为什么可以拆成多个角色
- 为什么中间表示会影响覆盖率

这是“测试 Agent 的生成逻辑”。

### 第二步看 `ByteDance--Auto_prd_test_agent`

再理解：

- 怎么把测试生成放进真实工作台
- 怎么接 RAG、人工修订、评审

这是“测试 Agent 的产品工作流”。

### 第三步看 `promptfoo`

再理解：

- 测试 Agent 自己怎么被测试
- bad-case、benchmark、自动评测怎么进入工程流程

这是“测试 Agent 的质量治理”。

### 第四步看 `giskard`

最后理解：

- 多轮 Agent 怎么评测
- retrieval-backed 输出怎么做 groundedness 检查

这是“测试 Agent 的多轮验证和回归系统”。

## 四、如果把四个项目画成一张能力地图

可以这样理解：

```text
QAagent
  -> 教你怎么提升测试生成逻辑

ByteDance--Auto_prd_test_agent
  -> 教你怎么把测试生成做成工作台

promptfoo
  -> 教你怎么测试这个工作台本身

giskard
  -> 教你怎么评测多轮交互、RAG 和 Agent 行为
```

所以它们加在一起，其实对应的是一条完整链路：

```text
测试生成能力
  -> 测试工作流产品化
  -> 测试 Agent 的质量治理
  -> 测试 Agent 的多轮评测与回归
```

## 五、这四个项目分别最值得借什么

### `QAagent` 最值得借

- 中间推理表示
- 多 Agent 分工
- 覆盖率导向

### `ByteDance--Auto_prd_test_agent` 最值得借

- Prompt 作为测试 SOP
- PRD 驱动的测试工作台
- RAG + 微调 + evaluator 闭环

### `promptfoo` 最值得借

- benchmark
- red team
- CI/CD 中的 AI 测试
- quality-first 文化

### `giskard` 最值得借

- scenario API
- multi-turn testing
- groundedness / conformity
- retrieval-backed system evaluation

## 六、如果你现在要反过来改 `prd_test_agent`，最值得吸收什么

如果以 `ByteDance--Auto_prd_test_agent` 为中心往回吸收这三者，我会这样看：

### 从 `QAagent` 吸收

- 不要只一步生成测试用例
- 可以先生成中间结构：
  - 测试点树
  - 约束清单
  - 边界值清单
  - 风险矩阵

### 从 `promptfoo` 吸收

- 给测试 Agent 本身建立 benchmark 和 regression
- 建立 bad-case 集
- 把“改 Prompt / 改检索”纳入评测流程

### 从 `giskard` 吸收

- 不只看最终 JSON
- 要评测多轮微调后的稳定性
- 要评测 retrieval groundedness

## 七、一句话记住这条横向图

> `QAagent` 解决“怎么更聪明地生成测试”，`ByteDance--Auto_prd_test_agent` 解决“怎么把测试生成做成工作台”，`promptfoo` 解决“怎么测试这个工作台本身”，`giskard` 解决“怎么评测多轮 Agent 和 RAG 行为”。
