# Agent 接平台分析项目：接口与演进规划

> 更新时间：2026-05-07  
> 目标：把“平台会展示文档”升级成“平台能被 Agent 直接调用、直接分析项目、直接产出沉淀”的工作底座。

## 1. 这次要解决的不是按钮，而是入口

现在平台已经有了项目页、方案页、痛点页、资料源、面经页和沉淀工作台，但它更像一个“可视化知识工作台”。  
如果我们希望它继续进化成一个真正会主动学习、会帮你分析项目、会把外部样本转成工程资产的系统，就不能只靠前端按钮和手动整理。

真正缺的是一个统一入口：

- 前端可以调它
- Agent 可以调它
- 后面如果要接 MCP，也可以直接映射过去

所以这次的重点不是再加一个页面，而是把平台的能力正式暴露成一层稳定接口。

## 2. 为什么要让 Agent 直接接平台

如果 Agent 只能“看文件然后自己猜”，会有几个明显问题：

- 它每次都要重新理解平台结构，成本高，也不稳定
- 它无法复用平台已经做好的 Project Radar、索引构建、资料源落库、沉淀目录规则
- 它能分析出内容，但未必知道应该写到哪里、怎么回写、怎么刷新前端索引
- 后续想做自动发现、自动筛选、自动沉淀时，会缺一个中间编排层

让 Agent 直接调用平台接口之后，平台的角色会变成：

```text
外部项目 / 本地项目 / 博客 / 论文
  -> 平台接口层
  -> 仓库理解层（Gitingest / 元数据 / 草稿生成）
  -> 沉淀层（external-projects / patterns / sources）
  -> 索引层（knowledge-index）
  -> 前端阅读层
```

这意味着 Agent 不再只是“会写文档”，而是能真正进入这条知识流水线。

## 3. 第一阶段架构

第一阶段不急着上 MCP Server，先做 HTTP First。

原因很简单：

- 前端已经天然适合调 HTTP
- 本地验证最快
- 便于后面再封装成 MCP tools
- 能先把最核心的分析链路跑通

当前建议结构：

```text
apps/knowledge-platform/
  前端阅读与沉淀工作台

scripts/knowledge_platform_bridge.py
  平台本地桥接层
  - /health
  - /api/distill
  - /api/ingest-repo
  - /api/analyze-project
  - /api/writeback-analysis

scripts/ingest_repo.py
  仓库理解层
  - 调 gitingest
  - 输出 summary / tree / content
  - 写入 tmp/ingest-cache

scripts/project_radar.py
  GitHub 项目发现与沉淀草稿层
  - candidate
  - score
  - distill

scripts/build_knowledge_index.py
  索引重建层
  - 把 docs 重建成前端可读 JSON
```

## 4. 三个核心接口怎么分工

### 4.1 `/api/ingest-repo`

作用不是沉淀，而是“先理解仓库”。

适合场景：

- 先看某个项目值不值得深入
- 想快速拿到目录树和代码摘要
- Agent 先做仓库结构理解，再决定要不要正式沉淀

请求示例：

```json
{
  "source": "https://github.com/coderamp-labs/gitingest",
  "sourceType": "github",
  "focus": "src"
}
```

返回重点：

- ingest cache 文件
- summary / tree / content 长度
- 可直接预览的一小段 summary / tree

### 4.2 `/api/distill`

这是“执行沉淀任务”的接口。

它的职责不是给你一个完美的最终文档，而是先把任务正式落到平台目录体系里，并刷新索引，让平台立刻能看见。

它要处理三类来源：

1. GitHub 项目  
   走 `project_radar.py distill`，必要时先加 `--use-ingest`

2. 本地项目  
   直接写入 `docs/external-projects/待分类项目池/`

3. 博客 / 论文 / 用户资料  
   先写入 `docs/source-library/用户提供文档/`

这一步的价值，是让“沉淀”变成平台内的正式动作，而不是会话里的一段临时回答。

### 4.3 `/api/analyze-project`

这是给 Agent 用的主接口。

它不只是“写草稿”，而是：

1. 理解项目
2. 触发沉淀
3. 读取结果
4. 返回结构化分析 JSON

它返回的重点不应该只是 markdown，而应该带着平台已经抽出来的结构字段，比如：

- title
- oneLine
- whyWorthStudying
- coreScenario
- generalProblems
- technicalFrameworks
- designPrinciples
- actions

这样 Agent 后续就能继续：

- 自动补方案页
- 自动补痛点页
- 自动补面试页
- 自动做项目比较

### 4.4 `/api/writeback-analysis`

这是“把分析结果继续送回知识库”的接口。

第一阶段我建议它先做稳一点的回写草稿，而不是直接粗暴覆盖主文档：

- 生成 `patterns` 回写草稿
- 生成 `pain-points` 补充草稿
- 生成 `interviews` 题库补充
- 自动重建索引

这样用户已经能一键把分析结果送回平台，同时又保留了后续人工审阅和继续升级的空间。

## 5. 为什么现在先 HTTP，后面再 MCP

这一步我建议不要一开始就把事情复杂化。

先做 HTTP 的原因：

- 平台前端现在就能直接调
- 本地调试最快
- 接口语义最容易稳定下来
- 后面转 MCP 时，只是把 HTTP 能力映射成 tools，而不是重新发明一套能力

等 HTTP 跑稳后，MCP 层可以这样映射：

```text
analyze_project
  -> POST /api/analyze-project

ingest_repository
  -> POST /api/ingest-repo

distill_project
  -> POST /api/distill

rebuild_knowledge_index
  -> python scripts/build_knowledge_index.py
```

也就是说，MCP 不应该是平台能力的起点，而应该是平台能力的协议外壳。

## 6. 第一阶段落地边界

这次不追求一次性做完“全自动进化”，先把最关键的最小闭环打通：

### 已经要落地的

- 本地桥接服务恢复
- `/api/distill`
- `/api/ingest-repo`
- `/api/analyze-project`
- `/api/writeback-analysis`
- GitHub / 本地项目 / 资料源三类入口
- 自动重建知识索引

### 这次先不强行做满的

- 自动回写 patterns
- 自动回写 pain points
- 自动回写 interviews
- 自动发现博客 / 论文并批量入库
- MCP server 正式化

不是这些不重要，而是接口层还没稳定前，直接把整条自动演化链路做满，会让问题变得难排查。

## 7. 平台后续最应该怎么接这个能力

后面前端最好增加一个明确的“Agent 分析入口”，而不是只藏在沉淀工作台里。

建议分两层：

### 第一层：操作入口

在“沉淀台”里保留现有人工填写入口，但增加一个更明确的动作：

- `仓库理解`
- `分析并生成草稿`
- `正式沉淀`

这样用户一眼就知道：

- 只是想先看结构，用 ingest
- 想让平台先给出判断，用 analyze
- 想正式落库并进平台，用 distill

### 第二层：结果阅读

`analyze-project` 的结果最好直接进入一个独立阅读器，而不是和概览卡片混在一起。

原因很直接：

- 概览页负责“值不值得看”
- 分析页负责“为什么、怎么做、有什么启发”
- 正式沉淀页负责“留档、索引、复用”

这三个层次混在一起，用户读起来就会乱。

## 8. 它对你这个平台真正的意义

这件事的价值不是多了三个接口。

真正的价值是，平台开始从：

```text
我来手动喂项目
  -> 你来写文档
```

变成：

```text
我给平台一个项目
  -> 平台先理解
  -> 平台先给判断
  -> 平台生成沉淀草稿
  -> 平台重建索引
  -> Agent 再继续补强方案、痛点、面试与工程动作
```

这才是“自动发现 + 自动筛选 + 自动沉淀”后面能继续长成真正产品能力的底层前提。

## 9. 当前结论

这一步最对的做法，不是继续堆页面，而是先把平台能力做成一层可调用接口。

因为只有这样，平台才会从“展示已有内容”升级成“接住新项目、理解新项目、吸收新项目”的系统。

## 10. 下一步建议

- [x] 先补桥接层，恢复本地服务
- [x] 落 `/api/ingest-repo`
- [x] 落 `/api/analyze-project`
- [x] 保持 `/api/distill` 兼容现有前端
- [ ] 前端增加“仓库理解 / 分析 / 正式沉淀”三级动作
- [ ] 给 analyze 结果增加专属阅读器入口
- [ ] 把 analyze 结果进一步回写到 patterns / pain-points / interviews
- [ ] 再把这套能力正式映射成 MCP tools
