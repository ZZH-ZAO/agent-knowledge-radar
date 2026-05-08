# cekai-auto-prd-test-agent Case Folder

## Summary

- Project name: ByteDance--Auto_prd_test_agent
- Project path: `D:\测开\ByteDance--Auto_prd_test_agent`
- Document type: user folder guide
- Purpose: help a human reader quickly understand what documents exist for this testing Agent workflow case and in what order to read them

## Recommended Reading Order

1. `analysis.md`
   先看项目本质、系统分层、Prompt/RAG/workflow/memory/HITL 的完整判断。
2. `improvement-roadmap.md`
   再看这个项目下一步最值得怎么改、为什么先改这些、这些改动分别适合什么阶段。
3. `technical-upgrade-plan.md`
   再看更偏工程落地的改造方案，包括架构拆分、模块改造顺序，以及 rerank 评分维度设计。
4. `target-architecture.md`
   最后看改进后的整体架构总图，理解各层怎么协同、每层借鉴了哪些项目、最终会长成什么样。
5. `implementation-sketch.md`
   如果要真正开始实施，再看这一份，里面是第一版模块拆分、接口草图、主流程伪代码和分阶段落地顺序。
6. `architecture-walkthrough.md`
   如果你想把这套架构讲给别人听，或者自己快速复盘，可以看这份讲稿版。
7. `further-improvement-directions.md`
   如果你想继续深挖这个项目还能怎么更聪明地做测试设计，而不只是做工程重构，可以看这份。

## What This Case Is Best For

- 学习“PRD 到测试用例生成”的垂直 AI 工作流怎么设计
- 学习 Prompt-heavy、UI-centric 的 LLM 应用如何落地
- 学习 RAG、人工微调、AI 评审如何拼成一个测试生成闭环
