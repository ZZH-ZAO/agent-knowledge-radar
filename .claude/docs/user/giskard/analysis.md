# giskard 项目分析

## Summary

- Project name: giskard
- Project path: `D:\giskard`
- Document type: user
- Purpose: explain what kind of system Giskard really is, and what reusable lessons it offers for evaluating, stress-testing, and regression-testing agentic systems

## 一、先给结论

`giskard` 很值得放进我们案例库里，因为它和 `promptfoo` 一样，不是传统 Agent runtime，但它对 Agent 成熟度非常关键。

它更准确的定位是：

> 一个面向 agentic systems 的评测、测试和脆弱性扫描框架。

相比 `promptfoo`，它更强调：

- multi-turn agent testing
- scenario API
- LLM-as-judge
- RAG evaluation

## 二、它最值得学的层

### 1. 它把“Agent 测试”从静态测试推进成多轮测试

README 明确提到：

- multi-turn testing
- scenario API
- evaluate full conversations

这很关键，因为很多 Agent 的问题不是单轮回复有错，而是：

- 多轮后跑偏
- 工具使用时出问题
- 长链路后结果不稳定

### 2. 它对 RAG 评测特别有价值

README 里明确提到：

- groundedness
- RAG evaluation
- synthetic data generation

这对你当前一直在研究的：

- 检索质量
- rerank
- 规则召回
- 最终生成质量

非常有帮助。

### 3. 它适合拿来补“测试 Agent 的测试系统”

如果说测试 Agent 是“帮别人生成测试”的系统，`giskard` 反过来提醒你：

> 测试 Agent 自己也需要一套测试系统。

## 三、它对你当前方向最有价值的地方

### 对测试 Agent

它特别适合补：

- scenario-based evaluation
- LLM-as-judge
- groundedness 检查
- regression suite

### 对工业 AI

它特别适合补：

- 多轮验证
- 检索依据验证
- 长流程系统测试

## 四、最适合借什么

- scenario API 思路
- 多轮 Agent 测试
- groundedness / conformity / judge 框架
- RAG evaluation 思路

## 五、怎么记住它

> `giskard` 最值得学的是：如何把 Agent 和 RAG 的测试，从“一次性看结果”升级成“多轮、可复跑、可判定、可回归的评测系统”。
