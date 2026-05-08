# Claude Docs Layout

## Summary

- Project name: Agent research case library
- Project path: `D:\claude-code-sourcemap\.claude\docs`
- Document type: layout guide
- Purpose: explain how the long-term case library is organized, why it is split into multiple layers, and how future project analyses should be stored

## 这是什么

这个目录不是普通的杂项文档目录，而是这套 Agent 工作台的长期案例库。

它的职责不是临时记笔记，而是把每一次有价值的项目分析沉淀下来，变成以后还能反复复用的知识资产。

## 为什么要分层

同一个项目分析，通常服务两个不同目标：

- 你自己学习、复盘、理解设计思路
- 后续 Agent 快速读取、对照、复用结论

如果把这两种目标混在同一份文档里，最后往往会变成两头都不够好：

- 对人来说，解释不够完整，学不到东西
- 对 Agent 来说，结构不够紧，检索效率差

所以这里固定分成两层。

## 目录结构

### `user/`

面向你自己阅读和学习的文档。

特点是：

- 更完整
- 更讲解式
- 更强调为什么这样设计
- 更适合复盘和吸收方法论

现在建议再按项目分子目录，例如：

- `user/arcreel/`
- `user/fault-diagnosis/`
- `user/claude-code/`

这样同一个项目的分析、对比、路线图、升级方案会自然聚在一起。

### `agent/`

面向后续 Agent 快速读取和复用的文档。

特点是：

- 更压缩
- 更结构化
- 更强调怎么判断、怎么复用
- 更像运行时参考卡片

这里也同样按项目分子目录，例如：

- `agent/arcreel/`
- `agent/fault-diagnosis/`
- `agent/claude-code/`

这样后续 Agent 做检索时，不会把不同项目的压缩笔记混在一起。

### `user/shared/`

这是通用模板和跨项目方法论文档目录。

适合放：

- 设计模板
- runtime 模板
- 通用方法论
- 不归属于某一个单独项目的沉淀

这里也建议放一个 `README.md`，告诉你这些模板分别适合什么问题、应该和哪些真实案例搭配阅读。

### `index.md`

这是整个案例库的总入口。

它负责：

- 告诉你当前已经沉淀了哪些项目
- 告诉你每个项目最适合学习什么
- 告诉你新项目分析时应该优先对照哪个历史案例

### `user/index.md`

这是给人读的案例库入口。

它负责从“学习价值”的角度解释每个项目：

- 它最值得学的层面是什么
- 为什么值得学
- 什么场景下应该把它拿出来对照

### `agent/index.md`

这是给后续 Agent 用的压缩入口。

它负责从“检索与判断”的角度组织案例：

- 它属于哪一类项目
- 强项在哪些层
- 适合在什么分析任务里复用

## 文档写作原则

每一份案例文档都应该在开头写清楚总述信息，至少包括：

- 项目名
- 项目路径
- 文档类型
- 目的

推荐格式：

```md
## Summary

- Project name: career-ops
- Project path: `D:\career-ops`
- Document type: user
- Purpose: explain how this project encodes domain workflow and what can be reused from it
```

## 推荐工作方式

当你完成一个值得保留的项目分析后，建议固定做这几步：

1. 在 `user/<project-name>/` 里写一份完整讲解版。
2. 在 `agent/<project-name>/` 里写一份压缩复用版。
3. 在这两个项目目录里各补一个局部 `README.md`，说明阅读顺序和文档用途。
4. 如果这个项目形成了新类别或新判断模式，更新 `index.md`。

这样案例库就不是“文档堆积”，而是一个越来越强的研究参考系。

## 一句话记忆

`user/` 负责帮人学会，`agent/` 负责帮 Agent 复用，`index` 负责帮两边快速找到正确案例。
