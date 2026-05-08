# 旧沉淀迁移规则

> 目的：把 `.claude/docs` 里的历史沉淀纳入现在的平台化知识体系，避免以后再漏看旧案例。

## 1. 三层目录分工

### `.claude/docs/`

旧体系沉淀目录，定位是历史案例库和上下文档案。

这里保存的是早期对项目的阅读、精简笔记、对比材料和复用建议。以后分析新项目时必须先检索这里，尤其是：

- `.claude/docs/user/<project>/`
- `.claude/docs/agent/<project>/`
- `.claude/docs/user/index.md`
- `.claude/docs/agent/index.md`

### `docs/external-projects/`

新体系的单项目沉淀目录，定位是给可视化平台直接消费的项目内容。

每个值得长期学习的项目都应该迁移成一份稳定文档：

```text
docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md
```

如果是本地项目或非 GitHub 项目，使用项目名：

```text
docs/external-projects/{项目类型中文文件夹}/{project-name}.md
```

### `docs/patterns/`

新体系的通用问题和优秀技术框架目录。

每次深度沉淀不能只写项目做了什么，还要抽象出它解决的通用问题，例如：

- Tool Runtime 如何安全执行外部动作
- MCP 工具生态如何治理
- Agent Memory 如何分层、注入和更新
- 前端风格如何成为 Agent 可复用的设计控制资产

## 2. 以后我说“沉淀”默认放在哪里

以后用户说“沉淀某个项目”时，默认执行这条流水线：

1. 先检索 `.mcp.json` 暴露的目录、`docs/`、`.claude/docs/` 和相关本地仓库。
2. 如果旧体系已有材料，先读取旧材料，不重新从零写。
3. 在 `docs/external-projects/{项目类型中文文件夹}/` 生成或更新单项目沉淀。
4. 在 `docs/patterns/` 生成或更新至少一个通用问题文档。
5. 如果项目来自 Project Radar，更新 `docs/project-radar/candidates.*` 状态。
6. 运行索引构建，让平台能看到新内容：

```powershell
python scripts\build_knowledge_index.py
```

## 3. 单项目沉淀必须包含什么

每份 `docs/external-projects/{项目类型中文文件夹}/*.md` 至少包含：

- 项目一句话
- 核心场景
- 它解决的通用问题
- 优秀技术和框架
- 可迁移设计原则
- 对当前项目的行动项
- 证据链接
- 旧体系来源，如果来自 `.claude/docs`

## 4. 迁移旧案例时怎么做

迁移顺序建议：

1. 先迁移和当前产品平台最相关的案例。
2. 再迁移 Agent Runtime、MCP、Tool Runtime、Memory、Multi-Agent、RAG、Eval 等主题。
3. 对暂时不迁移的旧案例，先进入 `docs/legacy-migration/旧案例迁移规则与清单/legacy-case-migration-index.json`，在平台里显示为“旧体系待迁移”。

迁移时不要机械复制旧文档，要做一次学习转化：

```text
旧项目笔记
  -> 单项目沉淀
  -> 通用问题
  -> 技术框架
  -> 当前项目行动项
```

## 5. 当前已确认的迁移规则

- `.claude/docs` 不是废弃目录，而是历史档案层。
- `docs/external-projects` 是平台展示层，下面必须按项目类型中文文件夹归档。
- `docs/patterns` 是方法论沉淀层。
- `docs/legacy-migration/旧案例迁移规则与清单/legacy-case-migration-index.json` 是旧案例过渡索引。
- 已迁移的旧案例要在索引里写 `migratedTo`，避免重复出现。

## 行业痛点研究版补充

> 目标：把“旧沉淀迁移规则”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

