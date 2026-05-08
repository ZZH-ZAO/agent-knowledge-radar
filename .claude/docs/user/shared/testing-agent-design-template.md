# Testing Agent Design Template

## Summary

- Project name: shared
- Project path: `D:\claude-code-sourcemap\.claude\docs\user\shared`
- Document type: user
- Purpose: provide a reusable design and analysis template for testing-oriented Agent systems, based on lessons extracted from ByteDance--Auto_prd_test_agent and earlier case studies

## 一、这份模板适合什么项目

这份模板适合分析或设计这类项目：

- PRD 转测试用例
- 规则文档转测试点
- 测试设计 Copilot
- 测试知识工作台
- 测试质量审查 Agent

也就是说，它适合的是：

> 以“测试资产生产”为核心，而不是以“自由聊天”为核心的 Agent 系统。

## 二、分析一个测试 Agent，先看哪七层

建议固定按七层来分析：

1. 产品交互层
2. 工作流编排层
3. 检索与证据层
4. 生成与评审层
5. 记忆与资产层
6. 质量与验证层
7. 平台治理层

如果一份分析没有把这七层讲清楚，通常说明它还停留在功能罗列阶段。

## 三、每一层应该问什么问题

### 1. 产品交互层

问：

- 用户是在聊天，还是在工作台里完成任务
- 结果是否可编辑、可审查、可导出
- 检索证据和质量评估是否对用户可见

重点看：

- 工作台而不是单轮聊天
- 证据透明
- 坏例 review 面板

借鉴项目：

- `fault-diagnosis`
- `repomind`
- `ByteDance--Auto_prd_test_agent`

### 2. 工作流编排层

问：

- 流程是在 UI 里硬串，还是有 service/workflow 层
- 阶段输入输出是否清晰
- 是否有数据合同

重点看：

- workflow-first
- 阶段职责
- 可 API 化

借鉴项目：

- `career-ops`
- `deer-flow`

### 3. 检索与证据层

问：

- 是纯语义检索，还是 hybrid retrieval
- 是否有业务关键词和逻辑关键词
- 是否有 rerank
- 前端能不能看到证据和排序依据

重点看：

- semantic retrieval
- keyword retrieval
- rerank
- evidence layer

借鉴项目：

- `ByteDance--Auto_prd_test_agent`
- `fault-diagnosis`
- `repomind`

### 4. 生成与评审层

问：

- 系统是否支持生成、修订、评审三段闭环
- 输出是否是结构化测试资产
- evaluator 是否只是展示，还是能回写系统

重点看：

- generation
- refinement
- evaluation
- structured output

借鉴项目：

- `ByteDance--Auto_prd_test_agent`
- `career-ops`
- `repomind`

### 5. 记忆与资产层

问：

- 有哪些 memory
- 是否区分 session、case、learning
- 高质量案例是否能沉淀为模板
- 坏例是否能沉淀为反例知识

重点看：

- session memory
- case memory
- learning memory
- async update

借鉴项目：

- `fault-diagnosis`
- `deer-flow`
- `claude-code`

### 6. 质量与验证层

问：

- 有没有 metrics
- 有没有 bad-case 管理
- 有没有 benchmark / regression
- 是不是 verification-first

重点看：

- retrieval metrics
- generation outcome metrics
- bad-case lifecycle
- regression suite

借鉴项目：

- `repomind`
- `claude-code`

### 7. 平台治理层

问：

- 新策略能不能灰度
- 新特性能不能 feature flag 控制
- 系统是否有实验和观测能力

重点看：

- feature flags
- experiment groups
- observability

借鉴项目：

- `claude-code`

## 四、设计一个测试 Agent，推荐的标准主链路

建议主链路固定成：

1. 文档接入
2. query 理解
3. hybrid retrieval
4. rerank
5. evidence assembly
6. test case generation
7. human refinement
8. AI evaluation
9. bad-case detection
10. archive / template extraction / benchmark update

如果一个测试 Agent 缺少其中后半段，通常说明它更像“生成工具”而不是“测试系统”。

## 五、测试 Agent 的检索层特别要看什么

测试 Agent 和普通问答 Agent 最大的不同之一，是它更依赖：

- 规则
- 约束
- 边界
- 异常
- 状态转换

所以检索层建议重点分析：

1. 是否只有语义检索
2. 是否有业务关键词检索
3. 是否有逻辑关键词 / 规则词检索
4. 是否有 rerank
5. 是否有证据展示

## 六、测试 Agent 的 rerank 推荐维度

建议分三层：

### 相关性层

- `query_relevance`
- `module_match`
- `intent_match`

### 测试价值层

- `testcase_usefulness`
- `rule_strength`
- `edge_case_density`
- `executable_specificity`

### 可信度层

- `source_authority`
- `version_freshness`
- `quality_tag`
- `human_acceptance`

## 七、测试 Agent 的最小质量体系

如果项目还不大，至少应该有：

### 指标

- `Recall@20`
- `Precision@5`
- `Rule Recall@10`
- `Noise Rate@10`
- `Human Acceptance Rate`

### 坏例

- retrieval bad-case
- rerank bad-case
- generation bad-case
- evaluation bad-case

### 回归集

- 小规模 benchmark
- 高价值规则 query
- 高频异常 query

## 八、最值得借鉴的项目地图

### `ByteDance--Auto_prd_test_agent`

最值得借：

- PRD 转测试资产工作台
- 共创模式
- evaluator 雏形

### `career-ops`

最值得借：

- workflow-first
- prompt 作为领域作业规范
- 数据合同

### `fault-diagnosis`

最值得借：

- 证据透明
- 过程可见
- 报告化交付

### `repomind`

最值得借：

- verification-first
- bad-case / verification lifecycle
- 回归和记录意识

### `deer-flow`

最值得借：

- app/runtime 分层
- 可插拔能力
- 异步 memory 更新

### `claude-code`

最值得借：

- feature flags
- 灰度
- 平台演进意识

## 九、最后一条最重要的判断标准

如果你要判断一个测试 Agent 到底成熟不成熟，不要只问：

- 它能不能生成测试用例

而要问：

- 它知不知道该检索什么
- 它能不能说明依据是什么
- 它能不能让人修
- 它能不能自评
- 它能不能把坏例留住
- 它能不能做回归
- 它能不能越用越像团队自己的系统

## 十、一句话记住这个模板

> 一个成熟的测试 Agent，不是“更会写测试用例的模型”，而是“把检索、证据、生成、评审、坏例、回归和知识沉淀组织成闭环的测试知识系统”。
