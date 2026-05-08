# Interviews（面经与面试官）

这里存放面经、八股、答案框架、面试场景方案和 AI 面试官记忆。目标不是堆题库，而是把你的真实面经和当前项目结合起来，沉淀成可以直接练、可以被追问、也可以持续更新的平台数据。

## 目录结构

```text
interviews/
  question-bank.json   # 平台直接读取的结构化题库
  raw/                 # Raw Questions（原始面经索引）
  answers/             # Answer Frameworks（答案框架）
  scenarios/           # Interview Scenarios（面试场景）
  interviewer/         # Interviewer Memory（面试官记忆）
```

## 当前已接入

- [结构化题库](question-bank.json)：从 `D:\面经` 和旧目录案例整理出的平台数据。
- [Tencent CSIG 一面来源索引](raw/tencent-csig-first-round-source-index.md)：保留原始材料、问题主线和证据入口。
- [Tencent CSIG 答案框架](answers/tencent-csig-answer-framework.md)：把项目回答整理成可直接练习的表达结构。
- [RAG + 测试开发模拟面试场景](scenarios/tencent-csig-rag-testing-dev-scenario.md)：用于 AI 面试官按真实节奏追问。
- [Tencent CSIG Interviewer Memory](interviewer/tencent-csig-interviewer-memory.md)：记录薄弱点、追问策略和训练顺序。

## 平台更新方式

每次新增或修改面经后运行：

```powershell
python scripts\build_knowledge_index.py
npm --prefix apps\knowledge-platform run build
```

平台会读取 `question-bank.json`，并把题目、推荐答案、追问方向、关联项目、关联方案和面试官记忆同步到可视界面。

## 沉淀规则

- 原始面经只做索引，不直接丢进平台。
- 能直接训练的问题进入 `question-bank.json`。
- 项目类问题必须绑定“项目做法 + 指标证据 + trade-off”。
- 八股题尽量结合你的项目回答，避免背概念。
- 面试官记忆要持续记录薄弱点，下一轮模拟面试优先追问这些点。
