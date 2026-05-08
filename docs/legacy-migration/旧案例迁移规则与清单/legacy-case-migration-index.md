# 旧案例迁移清单

> 来源：`.claude/docs/user/index.md` 与 `.claude/docs/agent/index.md`。  
> 作用：让旧沉淀先进入新体系视野，再逐步升级成 `docs/external-projects` 和 `docs/patterns`。

## 已迁移

| 旧案例 | 新沉淀 | 关联模式 |
| --- | --- | --- |
| `awesome-design-md` | `docs/external-projects/AI 前端设计规范样本/voltagent-awesome-design-md.md` | `docs/patterns/前端设计控制/frontend-design-control-patterns.md` |

## 已批量迁移

2026-05-04 已将旧体系中尚未迁移的 21 个项目级案例统一收束到：

```text
docs/external-projects/旧体系迁移项目样本/
```

同时将 `.claude/docs/*/shared` 下的共享模板汇总到：

```text
docs/templates/旧体系共享模板/legacy-shared-templates-index.md
```

这次迁移不是原样复制旧目录，而是把每个旧案例改写成可阅读、可索引、可追问的深度学习文档。后续如果某个旧案例需要继续深化，再从 `旧体系迁移项目样本/` 拆到更具体的项目分类或 `docs/patterns/` 专题中。

## 待迁移案例

> 当前已无项目级待迁移案例。下面保留旧清单，作为迁移前的基线和查漏参考。

| 旧案例 | 类型 | 核心价值 | 建议迁移优先级 |
| --- | --- | --- | --- |
| `claude-code-sourcemap` | Agent Runtime | 研究编码 Agent 核心执行引擎、query loop、工具调用和上下文控制 | high |
| `claude-code` | Productization | 研究 Agent Runtime 如何演进成产品平台和控制面 | high |
| `deer-flow` | Agent Runtime | 研究 super-agent harness、middleware、skills、MCP、memory、sandbox | high |
| `hermes-agent` | Long-running Agent | 研究持久会话、记忆、调度、skills、多入口工作台 | high |
| `repomind` | Repository Intelligence | 研究仓库理解、GitHub evidence、结构化 streaming、缓存和安全扫描 | high |
| `fireworks-tech-graph` | Team Knowledge | 研究技术图生成如何做成可复用 skill 和质量控制资产 | high |
| `fault-diagnosis` | Vertical Workflow | 研究工业诊断 Agent 的数据、工具、报告和证据链 | medium |
| `career-ops` | Vertical Workflow | 研究垂直业务流程、输出契约和人工审阅 | medium |
| `cekai-auto-prd-test-agent` | Testing Agent | 研究 PRD 到测试用例的 RAG、结构化生成和 AI 评审 | medium |
| `promptfoo` | Eval / Quality | 研究 eval、red teaming、CI/CD 质量治理 | medium |
| `giskard` | Eval / RAG Testing | 研究多轮 Agent 与 RAG 测试、groundedness、conformity | medium |
| `adk-python` | Agent Framework | 研究 Google 官方 code-first Agent framework | medium |
| `agentset` | RAG Platform | 研究 RAG 平台化、ingestion、indexing、eval、multi-tenancy | medium |
| `ms-agent` | Agent Framework | 研究 MCP、skills、memory、context compression 和参考应用 | medium |
| `langgraph-mcp-agents` | MCP Workbench | 研究 LangGraph + MCP + Streamlit 的轻量工作台 | medium |
| `browser-harness` | Browser / Tool Runtime | 研究浏览器执行环境与工具编排 | medium |
| `qaagent` | Testing Agent | 研究多 Agent 测试生成和中间表示 | medium |
| `arcreel` | Creative Agent Platform | 研究创意生产平台、异步任务和 provider abstraction | medium |
| `awesome-ai-research-writing` | Research Workflow | 研究 AI research writing 的资料组织和产出流程 | low |
| `computer-fundamentals` | Interview Knowledge | 研究计算机基础知识如何做成可复用面试知识库 | low |
| `shared` | Templates | 旧体系共享模板和 playbook | low |

## 每次迁移的完成标准

- 生成 `docs/external-projects/{项目类型中文文件夹}/*.md`。
- 更新或新增至少一个 `docs/patterns/*.md`。
- 在 `docs/legacy-migration/旧案例迁移规则与清单/legacy-case-migration-index.json` 中补充 `migratedTo`。
- 运行：

```powershell
python scripts\build_knowledge_index.py
npm --prefix apps\knowledge-platform run build
```

## 行业痛点研究版补充

> 目标：把“旧案例迁移清单”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

