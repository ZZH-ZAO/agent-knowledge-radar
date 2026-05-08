# Project Radar 评分规则

## 1. 评分目标

Project Radar 的评分目标不是判断项目“火不火”，而是判断它是否值得进入当前知识库的学习沉淀流程。

## 2. 评分维度

| 维度 | 权重 | 判断标准 |
| --- | ---: | --- |
| 相关性 | 30% | 是否匹配 Agent Runtime、MCP、Tool Use、Memory、Prompt、Multi-Agent、DevTools 等主题 |
| 工程质量 | 25% | README、docs、license、examples、CI、测试、源码结构是否完整 |
| 学习价值 | 20% | 是否能抽象出通用问题、优秀技术框架、可迁移原则 |
| 活跃度 | 15% | 最近 commit、release、issue/PR 是否活跃 |
| 稀缺性 | 10% | 是否提供新范式，而不是普通 demo 或薄壳 wrapper |

## 2.1 痛点贡献度

以后 Project Radar 不只判断“项目值不值得沉淀”，还要判断“它能不能补强某个行业痛点”。

新增来源可以来自：

- GitHub 项目
- 优质技术博客
- 论文和研究资料
- Awesome list
- npm / PyPI 包
- 你提供的旧文档、面经和私有资料

每个高质量来源都要额外回答：

```text
它暴露了什么 Agent / 大模型行业痛点？
它给出的解决方法是什么？
这个方法和已有项目有没有共性？
它能补强哪个 docs/pain-points 或 docs/patterns？
它能给当前项目带来什么行动项？
```

这会让平台从“项目发现器”升级成“行业痛点研究器”。

公式：

```text
project_score = relevance * 0.30
              + engineering_quality * 0.25
              + learning_value * 0.20
              + activity * 0.15
              + novelty * 0.10
```

## 3. 推荐等级

```text
85-100：必须深度沉淀
70-84：值得沉淀
55-69：做简短卡片
55 以下：只记录链接或跳过
```

## 4. 第一版自动评分说明

第一版脚本主要根据 GitHub metadata 和 README 可见信息估算分数，包括：

- topics、description、README 关键词匹配度。
- stars、forks、watchers、open issues。
- 最近更新时间。
- README、license、homepage、docs/examples/changelog 等文件信号。
- 是否出现 architecture、runtime、plugin、mcp、sandbox、memory、multi-agent 等学习关键词。

自动评分只是粗筛，最终是否沉淀仍保留人工判断。

## 行业痛点研究版补充

> 目标：把“Project Radar 评分规则”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

