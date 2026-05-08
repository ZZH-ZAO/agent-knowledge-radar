# Tencent CSIG First Round（腾讯 CSIG 一面原始面经索引）

> 来源目录：`D:\面经`  
> 整理日期：2026-05-03  
> 用途：保留原始面试问题、已有回答稿和后续训练入口。

## 1. 原始材料

| 文件 | 作用 |
| --- | --- |
| `D:\面经\腾讯csig一面_问答整理.md` | 真实一面问题清单，最重要 |
| `D:\面经\transcript_full.txt` | 录音完整转写 |
| `D:\面经\transcript_draft.txt` | 录音草稿转写 |
| `D:\面经\面经回答优化建议.md` | 一面回答复盘和改法 |
| `D:\面经\面经回答深度版_知识库风格.md` | 已优化的知识库风格答案 |
| `D:\面经\AI测试用例生成系统_RAG深度项目介绍稿.md` | AI 测试用例生成系统主项目讲稿 |
| `D:\面经\RAG项目深度讲稿_检索生成评估闭环.md` | RAG 深挖讲稿 |
| `D:\面经\测试开发面试防问倒手册.md` | 测试开发通用追问 |
| `D:\面经\食安平台讲稿.md` | 智慧食安项目测开方向讲稿 |

PDF、音频和图片先不进入结构化整理；已优先使用 Markdown 和 txt。

## 2. 真实一面问题结构

这场面试不是普通八股，主线非常清楚：

1. 开场和自我介绍。
2. AI 测试用例生成系统项目深挖。
3. RAG 切片、检索、重排、指标、bad case 追问。
4. 低质量 PRD、噪声、反馈、长期记忆追问。
5. Prompt Engineering、MCP、Function Calling、Skills 追问。
6. 其他 AI 项目经验。
7. TCP、进程线程协程等基础。
8. 算法题：合并两个有序链表。
9. 面试官建议和反问。

## 3. 需要记住的真实弱点

来自 `面经回答优化建议.md` 和 `面经回答深度版_知识库风格.md`：

- 项目回答有亮点，但容易变成功能罗列。
- RAG 要讲成工程链路，而不是“向量库 + Prompt”。
- 评估模块要讲成 AI Critic + 人工确认 + bad case 回归，不要讲成万能自动评判。
- 低质量 PRD 要先质检、澄清、显式假设或拒答。
- 人工反馈和长期记忆要结构化，不要讲成保存聊天记录。
- Agent / MCP / Function Calling / Skills 要分层。
- 算法题需要补稳定模板。

## 4. 旧目录可引用案例

| 旧案例 | 迁移价值 |
| --- | --- |
| `.claude/docs/user/cekai-auto-prd-test-agent/` | PRD 到测试用例工作台、RAG 约束生成、AI evaluator |
| `.claude/docs/agent/shared/testing-agent-review-playbook.md` | 测试 Agent 评审框架：workflow、retrieval、evaluation、bad case |
| `.claude/docs/user/shared/testing-agent-landscape-map.md` | QAagent、PRD 测试工作台、promptfoo、giskard 的测试 Agent 学习线 |
| `.claude/docs/user/promptfoo/analysis.md` | AI 系统 eval、red team、benchmark |
| `.claude/docs/user/giskard/analysis.md` | 多轮 Agent 与 RAG evaluation |
| `.claude/docs/user/agentset/analysis.md` | RAG 平台化：ingestion、indexing、eval、API、multi-tenancy |
| `.claude/docs/user/fault-diagnosis/analysis.md` | 垂直 Agent 的数据、RAG、工具和报告证据链 |

## 5. 已生成的新资产

- `docs/interviews/question-bank.json`
- `docs/interviews/answers/tencent-csig-answer-framework.md`
- `docs/interviews/scenarios/tencent-csig-rag-testing-dev-scenario.md`
- `docs/interviews/interviewer/tencent-csig-interviewer-memory.md`

## 行业痛点研究版补充

> 目标：把“Tencent CSIG First Round（腾讯 CSIG 一面原始面经索引）”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

