# Project Radar 发现日志

> 用途：记录每次项目发现、搜索、评分、沉淀动作，方便回看项目来源和筛选过程。

## 日志


- 2026-05-02T16:14:09Z 手动添加 `anthropics/claude-code`，score=61
- 2026-05-02T16:14:32Z 生成沉淀草稿 `docs\external-projects\anthropics-claude-code.md`
- 2026-05-02T16:15:20Z 重新评分候选池
- 2026-05-02T16:15:34Z 生成沉淀草稿 `docs\external-projects\anthropics-claude-code.md`
- 2026-05-02T16:15:55Z 关键词发现完成 queries=['coding agent mcp']，repos=3
- 2026-05-02T16:22:03Z 批量生成沉淀草稿 `docs\external-projects\affaan-m-everything-claude-code.md`
- 2026-05-02T16:22:03Z 批量生成沉淀草稿 `docs\external-projects\aaif-goose-goose.md`
- 2026-05-02T16:22:15Z 批量生成沉淀草稿 `docs\external-projects\chromedevtools-chrome-devtools-mcp.md`
- 2026-05-02T16:23:19Z 初始化 Project Radar 目录和基础文件
- 2026-05-03T18:25:16Z 手动添加 `oil-oil/draw-ui`，score=49
- 2026-05-03T18:25:30Z 手动添加 `freestylefly/awesome-gpt-image-2`，score=55
- 2026-05-03T18:25:30Z 手动添加 `CookSleep/gpt_image_playground`，score=53
- 2026-05-03T18:25:30Z 手动添加 `Desima-AP/autoimage-claude`，score=62
- 2026-05-03T18:26:02Z 重新评分候选池
- 2026-05-03T18:26:21Z 手动添加 `freestylefly/awesome-gpt-image-2`，score=64
- 2026-05-03T18:26:32Z 手动添加 `CookSleep/gpt_image_playground`，score=58
- 2026-05-03T18:26:41Z 重新评分候选池
- 2026-05-04T08:40:30Z 手动添加 `shadcn-ui/ui`，score=55
- 2026-05-04T08:40:43Z 手动添加 `Kiranism/next-shadcn-dashboard-starter`，score=59
- 2026-05-04T08:41:02Z 手动添加 `Qualiora/shadboard`，score=50
- 2026-05-04T08:41:14Z 手动添加 `tremorlabs/tremor`，score=46
- 2026-05-04T08:41:25Z 手动添加 `cruip/tailwind-dashboard-template`，score=43
- 2026-05-04T08:41:39Z 手动添加 `ibelick/motion-primitives`，score=47
- 2026-05-04T08:41:50Z 手动添加 `ephraimduncan/blocks`，score=47
- 2026-05-04T08:42:20Z 重新评分候选池

## 行业痛点研究版补充

> 目标：把“Project Radar 发现日志”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

- 2026-05-06T18:49:42Z 生成沉淀草稿 `docs\external-projects\待分类项目池\coderamp-labs-gitingest.md`
