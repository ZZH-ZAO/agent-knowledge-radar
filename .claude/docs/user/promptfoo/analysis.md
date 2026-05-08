# promptfoo 项目分析

## Summary

- Project name: promptfoo
- Project path: `D:\promptfoo`
- Document type: user
- Purpose: explain what kind of system promptfoo really is, and what reusable lessons it offers for testing, evaluation, red teaming, and quality governance of LLM / Agent systems

## 一、先给结论

`promptfoo` 不是传统意义上的“Agent 项目”，但它对 Agent 项目非常重要。

它更准确的定位是：

> 一个面向 LLM / Agent 应用的测试、评测和红队化平台。

所以它最适合放进我们的案例库里作为：

- `quality-first`
- `evaluation-first`

类型的参考项目。

## 二、它最值得学的层

### 1. 它把“AI 测试”做成了一等公民

README 非常明确地强调：

- evals
- red teaming
- vulnerability scanning
- CI/CD
- compare models

这意味着它的核心价值不在“生成能力”，而在：

> 怎么让 AI 系统被系统性测试。

### 2. 它非常适合补你现在的 bad-case / benchmark / 质量指标思路

你最近一直在考虑：

- bad-case
- benchmark
- 评测指标
- 回归验证

`promptfoo` 正好能给你一个更系统化的参考：

- 测试不是附属功能
- 测试应该是平台能力

### 3. 它很重开发流程集成

它明确强调：

- CLI
- library
- CI/CD
- PR review

这说明它很适合拿来借“AI 应用质量怎么进开发流程”。

## 三、它对你当前方向最有价值的地方

### 对测试 Agent

它可以帮助你想清楚：

- 测试 Agent 本身也需要被测试
- 评测不只是人工看一眼
- benchmark、红队、自动检查应该进入工程流程

### 对工业 AI

它可以帮助你想清楚：

- 工业 Agent 的质量不能只靠主观判断
- 高风险业务需要验证和回归文化

## 四、最适合借什么

- eval / benchmark 体系
- CI/CD 里的 AI 检查
- red teaming / vulnerability scanning 思路
- quality governance 视角

## 五、怎么记住它

> `promptfoo` 最值得学的不是 Agent runtime，而是“怎么把 AI 系统的测试、评测和红队化变成一套工程实践”。
