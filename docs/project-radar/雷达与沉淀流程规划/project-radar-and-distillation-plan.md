# Project Radar 与项目沉淀系统规划文档

> 状态：规划中  
> 创建日期：2026-05-03  
> 适用仓库：`D:\claude-code-sourcemap`  
> 后续上下文：以后所有“自动找优质项目”“沉淀项目”“抽象通用问题和优秀技术框架”的工作，都以本文档作为项目级上下文。

## 1. 项目背景

当前仓库已经开始沉淀 Claude Code、Agent Runtime、Tool Runtime、Memory、MCP、Multi-Agent 等方向的资料，但现有方式主要依赖人工给出项目链接，再由 Codex 进行总结。

下一步要把这个过程升级成两个相互衔接的能力：

1. **Project Radar**：自动发现、筛选、评分优质项目，形成候选池。
2. **项目沉淀流水线**：把候选项目转化成可学习、可复用、可指导开发的知识文档。

这两个能力合起来，要让知识库具备一种“主动学习外部优秀项目”的能力。

```text
外部项目发现
  -> 候选项目评分
  -> 候选池管理
  -> 人工确认
  -> 单项目沉淀
  -> 通用问题抽象
  -> 优秀技术框架沉淀
  -> 自己项目行动项
```

## 2. 总体目标

这个系统的目标不是简单收藏 GitHub 链接，而是建立一条稳定的学习转化链路。

最终要做到：

- 能主动找到 Agent / LLM / DevTools / MCP / Coding Agent 方向的高质量项目。
- 能给项目打分，判断哪些值得深度学习。
- 能生成候选项目卡片，避免知识库变成链接堆。
- 能把高价值项目沉淀成结构化文档。
- 能把单项目特性抽象成通用工程问题。
- 能把优秀项目做法转化成自己的技术框架和行动项。

一句话：

```text
把外部优秀项目变成自己的 Agent 工程方法论资产。
```

## 3. 两个子项目

### 3.1 子项目一：Project Radar

Project Radar 负责“找项目”和“判断是否值得学”。

第一版只做 GitHub，后续再扩展到 Hacker News、Papers with Code、Awesome Lists、npm、PyPI、Reddit、技术博客等来源。

第一版输入：

- 主题关键词，例如 `agent runtime`、`coding agent`、`mcp`、`llm tools`、`ai devtools`。
- 已沉淀项目，例如 `anthropics/claude-code`、`liuup/claude-code-analysis`。
- 人工指定项目链接。

第一版输出：

- `docs/project-radar/candidates.md`
- `docs/project-radar/discovery-log.md`
- `docs/project-radar/radar-config.json`

候选项目卡片格式：

```md
## owner/repo

- URL:
- 主题:
- 来源：keyword / similar-repo / manual / trending
- 推荐等级：High / Medium / Low
- 总分：
- 推荐理由：
- 核心价值：
- 风险/不足：
- 建议沉淀角度：
- 下一步动作：skip / watch / distill
```

### 3.2 子项目二：项目沉淀流水线

项目沉淀流水线负责“把项目转成知识”。

它不只是总结 README，而是固定输出三类结果：

1. **单项目沉淀**：这个项目本身为什么值得学。
2. **通用问题更新**：它背后的通用工程问题是什么。
3. **行动项**：我自己的项目可以怎么吸收。

第一版输出目录：

```text
docs/external-projects/
docs/patterns/
```

单项目沉淀文档格式：

```text
docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md
```

通用问题文档格式：

```text
docs/patterns/{topic}-patterns.md
```

总纲文档：

```text
docs/patterns/agent-engineering-framework.md
```

## 4. 目录规划

后续建议形成以下目录：

```text
docs/
  project-radar/
    candidates.md
    discovery-log.md
    radar-config.json
    scoring-rules.md

  external-projects/
    anthropics-claude-code.md
    liuup-claude-code-analysis.md
    openhands.md
    aider.md

  patterns/
    agent-engineering-framework.md
    agent-runtime-patterns.md
    context-engineering-patterns.md
    prompt-runtime-patterns.md
    tool-runtime-patterns.md
    memory-system-patterns.md
    permission-sandbox-patterns.md
    plugin-system-patterns.md
    multi-agent-patterns.md
    observability-patterns.md
    productization-patterns.md

scripts/
  project_radar.py
```

当前已经存在：

- `docs/project-radar/雷达与沉淀流程规划/project-learning-distillation-playbook.md`
- `docs/liuup-claude-code-analysis-distillation.md`
- `docs/anthropics-claude-code-official-distillation.md`

后续应逐步把已有沉淀迁移或索引到新目录体系里。

## 5. Project Radar 功能规划

### 5.1 第一版能力

第一版只做最小可用能力：

- 支持根据关键词搜索 GitHub 项目。
- 支持手动录入项目。
- 支持读取 GitHub repo 基础信息。
- 支持生成项目评分。
- 支持写入候选项目卡片。
- 支持高分项目标记为 `distill`。

命令形态：

```powershell
python scripts/project_radar.py discover --topic agent-runtime
python scripts/project_radar.py discover --query "mcp agent tools"
python scripts/project_radar.py add https://github.com/anthropics/claude-code
python scripts/project_radar.py score
python scripts/project_radar.py list --min-score 80
```

### 5.2 后续能力

第二阶段再做：

- 从已沉淀项目 README 中抽取相关链接。
- 根据 topics、stars、forks、依赖项目做相似扩散。
- 接入 GitHub trending 或 star growth。
- 自动生成月度候选报告。
- 自动去重。
- 根据已有 `patterns/` 判断项目与当前知识体系的匹配度。

第三阶段再做：

- 接入 Hacker News、Papers with Code、Awesome Lists、npm、PyPI。
- 支持定期运行。
- 支持自动生成候选项目学习路线。
- 支持把高分项目自动送入沉淀流水线。

## 6. 项目评分规则

评分不只看 star，要看项目能不能带来学习价值。

建议评分：

| 维度 | 权重 | 说明 |
| --- | ---: | --- |
| 相关性 | 30% | 是否匹配 Agent Runtime、MCP、Tool Use、Memory、Prompt、Multi-Agent、DevTools 等主题 |
| 工程质量 | 25% | 架构、代码、README、docs、license、CI、测试、examples 是否完整 |
| 学习价值 | 20% | 是否能抽象出通用问题和可迁移设计原则 |
| 活跃度 | 15% | 最近 commit、release、issue/PR 活跃度 |
| 稀缺性 | 10% | 是否提供新范式，而不是普通 demo 或薄壳 wrapper |

公式：

```text
project_score = relevance * 0.30
              + engineering_quality * 0.25
              + learning_value * 0.20
              + activity * 0.15
              + novelty * 0.10
```

推荐等级：

```text
85-100：必须深度沉淀
70-84：值得沉淀
55-69：做简短卡片
55 以下：只记录链接或跳过
```

### 6.1 相关性关键词

优先主题：

- `agent runtime`
- `coding agent`
- `developer agent`
- `mcp`
- `tool calling`
- `tool use`
- `memory`
- `prompt engineering`
- `context engineering`
- `multi-agent`
- `ai devtools`
- `llm framework`
- `sandbox`
- `plugin system`
- `observability`

### 6.2 优先学习项目类型

优先级从高到低：

1. 完整产品型 Agent，例如 Claude Code、OpenHands、Cursor 类工具相关开源组件。
2. Agent Runtime / SDK / Framework。
3. MCP server / MCP client / tool integration 项目。
4. Prompt / Memory / Context 工程项目。
5. Plugin / Workflow / Automation 项目。
6. 只有 demo 的薄壳项目。

## 7. 沉淀流水线规划

沉淀流程固定为：

```text
读取项目资料
  -> 生成项目速览
  -> 提取核心场景
  -> 提取通用问题
  -> 提取优秀技术和框架
  -> 形成可迁移原则
  -> 形成行动项
  -> 写入 external-projects
  -> 更新 patterns
```

### 7.1 单项目沉淀模板

```md
# 项目沉淀：owner/repo

> 来源：
> 沉淀日期：
> 推荐等级：
> 学习主题：

## 1. 项目一句话

## 2. 为什么值得学

## 3. 核心场景

## 4. 它解决的通用问题

## 5. 优秀技术和框架

## 6. 可迁移设计原则

## 7. 对我当前项目的行动项

## 8. 证据链接
```

### 7.2 通用问题文档模板

```md
# 通用问题：{Topic}

## 1. 问题定义

## 2. 为什么重要

## 3. 常见错误做法

## 4. 成熟系统通常怎么做

## 5. 优秀项目案例

## 6. 可迁移技术框架

## 7. 我的项目行动项
```

## 8. 第一阶段实现计划

第一阶段目标：先让系统可用，而不是一次性全自动。

### 阶段 1：文档和目录基础

目标：

- 建立项目规划文档。
- 建立 `docs/project-radar/`。
- 建立 `docs/external-projects/`。
- 建立 `docs/patterns/`。
- 建立候选项目和评分规则文档。

验收标准：

- 目录存在。
- 有候选池模板。
- 有评分规则。
- 有单项目沉淀模板。
- 有通用问题模板。

### 阶段 2：Project Radar 脚本雏形

目标：

- 新增 `scripts/project_radar.py`。
- 支持手动添加 GitHub repo。
- 支持根据关键词搜索 GitHub repo。
- 支持读取 repo 基础信息。
- 支持本地评分。
- 支持更新 `docs/project-radar/candidates.md`。

验收标准：

```powershell
python scripts/project_radar.py add https://github.com/anthropics/claude-code
python scripts/project_radar.py discover --query "coding agent"
python scripts/project_radar.py score
```

### 阶段 3：半自动沉淀

目标：

- 支持指定 repo 生成沉淀草稿。
- 自动拉取 README、docs 入口、CHANGELOG、repo metadata。
- 生成 `docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md`。
- 生成或提示应更新的 `docs/patterns/*.md`。

验收标准：

```powershell
python scripts/project_radar.py distill anthropics/claude-code
```

执行后生成一份可人工继续修改的沉淀草稿。

### 阶段 4：通用问题库持续化

目标：

- 建立 `agent-engineering-framework.md`。
- 建立 Tool Runtime、Memory、MCP、Plugin、Multi-Agent 等主题文档。
- 每次项目沉淀后更新至少一个主题文档。

验收标准：

- 每个主题文档至少包含问题定义、成熟做法、项目案例、可迁移框架、行动项。
- 每个单项目文档都能链接到至少一个 `patterns/` 文档。

## 9. 人机协作规则

第一版保留人工确认，不直接全自动写大量文档。

默认流程：

1. Radar 自动发现项目。
2. Radar 自动评分并写候选卡片。
3. 用户或 Codex 选择 High 项目。
4. Codex 深度阅读项目资料。
5. Codex 写单项目沉淀。
6. Codex 更新通用问题库。
7. 用户决定是否把行动项转成开发任务。

除非用户明确要求“自动沉淀所有高分项目”，否则不要批量生成大量项目文档。

## 10. 后续 Codex 工作约定

以后用户说：

- “找一些优质项目”
- “项目雷达跑一下”
- “沉淀这个项目”
- “把这个项目转成通用问题”
- “更新优秀技术框架”

Codex 应默认遵循本文档。

具体要求：

- 先判断任务属于 Project Radar、单项目沉淀、通用问题库更新，还是三者组合。
- 如果是找项目，优先输出候选卡片，不直接深度沉淀。
- 如果是沉淀项目，必须输出单项目文档，并尽量更新一个相关 `patterns/` 文档。
- 如果是技术框架更新，要抽象成通用问题，不要只复述项目功能。
- 每次沉淀都要有证据链接。
- 每次沉淀都要有“对我当前项目的行动项”。

## 11. 当前下一步

建议下一步按顺序执行：

1. 创建目录：`docs/project-radar/`、`docs/external-projects/`、`docs/patterns/`。
2. 创建候选池模板：`docs/project-radar/candidates.md`。
3. 创建评分规则：`docs/project-radar/scoring-rules.md`。
4. 创建总纲草稿：`docs/patterns/agent-engineering-framework.md`。
5. 创建 `scripts/project_radar.py` 第一版。
6. 把已有两份沉淀文档迁移或链接到 `docs/external-projects/`。

## 12. 关键判断标准

这个系统是否成功，不看找到了多少项目，而看：

- 是否能持续发现真正值得学的项目。
- 是否能避免低质量链接污染知识库。
- 是否能把项目功能抽象成通用问题。
- 是否能把优秀技术转成可复用框架。
- 是否能产生具体行动项，反哺自己的项目。

最终产物应该是一套越来越完整的 Agent 工程知识体系，而不是项目收藏夹。

## 行业痛点研究版补充

> 目标：把“Project Radar 与项目沉淀系统规划文档”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

