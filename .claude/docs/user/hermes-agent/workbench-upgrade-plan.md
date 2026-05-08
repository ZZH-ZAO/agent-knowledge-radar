# 当前工作台升级规划

## Summary

- Project name: current workbench upgrade plan
- Project path: `D:\claude-code-sourcemap\.claude`
- Document type: `user`
- Purpose: turn the Hermes Agent borrowing analysis into a concrete implementation roadmap for upgrading the current `.mcp + docs + memory` workbench

## 1. 这份文档和 `what-to-borrow-for-this-workbench.md` 的区别

前一份文档回答的是：

- 从 Hermes Agent 最值得借什么
- 哪些现在不要急着照搬
- 大方向优先级怎么排

这份规划文档回答的是：

- 具体要做成什么样
- 分几期做
- 每期交付什么
- 先做哪些，后做哪些
- 怎么判断做成了

一句话说：

- `what-to-borrow-for-this-workbench.md` 是“方向判断”
- `workbench-upgrade-plan.md` 是“实施规划”

## 2. 最终目标状态

升级完成后，这套工作台会从：

- 能分析项目
- 能写 docs
- 能存 memory

变成：

- 能分析项目
- 能沉淀正式成果
- 能保留历史工作过程
- 能回取历史过程和正式成果
- 能让 skills / memory / docs 互相反哺
- 能低频自整理

也就是说，最终不是简单多一个目录，而是多出一层“长期工作记忆与回流系统”。

## 3. 目标架构

升级后建议形成 5 层结构：

### 1. `skills`

负责：

- 怎么做
- 分析流程
- 任务方法入口

### 2. `memory`

负责：

- 稳定原则
- 长期判断标准
- 项目分类 heuristics

### 3. `sessions`

负责：

- 历史工作过程
- 中间判断
- 任务摘要
- 尚未正式升格为 docs 的候选知识

### 4. `docs`

负责：

- 正式沉淀
- 面向人和面向 agent 的长期案例资产

### 5. `.mcp.json`

负责：

- repo 读取
- docs / memory / sessions 检索
- 外部研究补充

最终关系应该是：

- `skills` 指导执行
- `memory` 提供稳定判断
- `sessions` 提供历史工作回取
- `docs` 提供正式长期资产
- `MCP` 负责把这些能力接进 runtime

## 4. 分期规划

## Phase 1：建立 Session Archive 最小骨架

### 目标

先把“历史工作过程”正式落盘，不再只保留最终文档。

### 交付物

- 新目录：`.claude/sessions/`
- 新索引文件：`.claude/sessions/index.json`
- 每次 session 的记录文件格式定义
- 一份 README 说明 session archive 的用途和字段

### 推荐字段

- `id`
- `created_at`
- `project`
- `task_type`
- `title`
- `summary`
- `keywords`
- `related_cases`
- `source_paths`
- `derived_docs`
- `status`

### 完成标准

- 能手动新增一条 session 记录
- 能从索引里看懂最近做过什么
- 新结构不破坏现有 `docs/memory/skills`

## Phase 2：补 Session Search 能力

### 目标

让 archive 不只是存档，而是真能回取。

### 交付物

- 一个本地检索脚本或工具
- 支持以下查询方式：
  - 按项目名
  - 按关键词
  - 按标签
  - 按时间
- 输出适合后续任务引用的简明结果

### 完成标准

- 给一个项目名，能找到它过去相关工作
- 给一个主题词，能找到相关历史任务
- 输出结果足够短，能直接作为上下文材料

## Phase 3：把 Session Archive 接进当前沉淀流程

### 目标

让“分析任务 -> archive -> docs”形成稳定闭环。

### 交付物

- 一份沉淀流程约定文档
- 每次案例分析时同步更新：
  - session archive
  - `user/` 文档
  - `agent/` 文档
  - `docs/index.md`（必要时）
- 记录 session 与正式文档的映射关系

### 完成标准

- 新案例完成后，不会只留下 docs
- 能从 session 追到正式沉淀文档
- 能从正式文档反查来源 session

## Phase 4：让 Skills 开始被案例反哺

### 目标

把 skill 从静态说明，推进成可增长能力资产。

### 交付物

- 给核心 skill 增加元信息段落：
  - 适用场景
  - 不适用场景
  - 常搭配 docs / memory
  - 相关案例
- 一套“案例完成后是否更新 skill”的检查清单

### 完成标准

- 至少 2 到 3 个核心 skill 被改造成可反哺格式
- 新案例能明确判断要不要反哺某个 skill

## Phase 5：把 Memory 升级成三层 operating model

### 目标

把 memory 从一个目录，升级成一套使用模型。

### 三层定义

- `stable memory`
  - 继续用 `.claude/memory/`
- `session memory`
  - 由 `.claude/sessions/` 承担
- `retrieved memory`
  - 由每次任务运行时动态拼装

### 交付物

- 一份 memory operating model 文档
- 规定哪些内容该进 memory，哪些只该留在 sessions，哪些该升格进 docs

### 完成标准

- 新任务出现时，能清楚判断信息该落哪一层
- 避免把所有信息都堆进 `.claude/memory/`

## Phase 6：把 Sessions 接进 `.mcp.json`

### 目标

让 Agent 像读取 docs 一样读取历史工作记录。

### 交付物

- 在 `.mcp.json` 中补一个面向 `.claude/sessions/` 的读取入口
- 或做一个更轻量的 session-search 读取层

### 完成标准

- runtime 可以统一读取 repo / docs / memory / sessions
- session archive 不再只能靠手工翻目录

## Phase 7：补低频自整理动作

### 目标

让工作台开始具备“长期维护节奏”。

### 可选动作

- 检查新案例是否补齐 `user/` 和 `agent/`
- 检查哪些案例可上升成 `shared/` 模板
- 检查 memory 是否过时或重复
- 检查 session 是否已绑定正式沉淀

### 完成标准

- 至少有一套低频检查流程
- 工作台维护不再完全依赖临时想起来再整理

## 5. 优先级建议

### `P1`

- Phase 1：Session Archive 骨架
- Phase 2：Session Search
- Phase 3：接入沉淀闭环

这是第一阶段必须做的，因为它们直接决定工作台能不能从“只会沉淀最终结论”升级成“能回找历史工作”。

### `P2`

- Phase 4：Skills 反哺
- Phase 5：Memory operating model
- Phase 6：Sessions 接入 MCP

这是第二阶段，重点是把系统做得更稳、更顺。

### `P3`

- Phase 7：低频自整理动作

这是锦上添花，但对长期维护很重要。

## 6. 风险和边界

### 1. 不要一开始就做重系统

当前最需要的是轻量、稳定、可用的 archive 和 search，不是复杂数据库或完整平台。

### 2. 不要让 sessions 替代 docs

`sessions` 是过程层，不是正式沉淀层。

### 3. 不要让 memory 继续无限膨胀

这次升级的一个目的，就是把很多本不该进 stable memory 的内容分流到 sessions。

### 4. 不要先做花哨入口层

Telegram、TUI、ACP、重型远程环境，这些都不是当前瓶颈。

## 7. 建议的实际执行顺序

如果马上开始动手，我建议这样推进：

1. 先创建 `.claude/sessions/` 结构和 README
2. 再定义 `index.json` 与 session entry schema
3. 再做最小检索脚本
4. 再把新案例沉淀流程接进 session archive
5. 然后才开始做 skill 反哺和 memory 分层文档

这条顺序的好处是：

- 每一步都能立即产生可见收益
- 不需要先做大规模重构
- 不会打断现有工作台使用

## 8. 验收标准

这次改造做完，至少应该满足下面这些结果：

- 能检索历史分析任务，而不只是翻 docs 目录
- 每个新案例都能留下过程记录和正式沉淀的映射
- `skills / memory / docs / sessions` 的职责边界更清楚
- `.mcp.json` 可以覆盖新加的历史工作层
- 工作台开始具备“长期积累能力”，而不是只积累最终文章

## 9. 最后一句总结

如果把整个计划压缩成一句话，就是：

> 先补一层轻量但正式的 `session archive + search`，再用它把 `skills / memory / docs / MCP` 串成一个真正会积累的研究工作台。
