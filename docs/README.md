# claude-code-sourcemap 知识库入口

> 这里是 `D:\claude-code-sourcemap` 的新知识体系入口。它不是一个散落文档目录，而是一套围绕“项目沉淀、方案抽象、痛点研究、工程决策、学习表达”组织起来的知识平台。

## 1. 以后“沉淀”默认放哪里

以后你说“沉淀”，默认写入新的 `docs/` 体系，不再默认写到 `.claude/docs`。

- 项目沉淀：`docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md`
- 通用问题 / 技术框架：`docs/patterns/{技术主题中文文件夹}/{topic}-patterns.md`
- 平台规划 / 路由 / 工程逻辑：`docs/platform/{中文主题文件夹}/{topic}.md`
- 自动发现 / 候选池 / 评分：`docs/project-radar/`
- 外部博客 / 论文 / 用户资料：`docs/source-library/`
- 面经 / 面试题 / 问答：`docs/interviews/`

`.claude/docs` 现在的作用是：

- 历史资料来源
- 旧文档迁移源
- 查漏补缺时的证据层

它不再是新沉淀的默认落点。

## 2. 最值得先看的五个入口

| 入口 | 作用 |
| --- | --- |
| `external-projects/` | 看单个优质项目到底解决了什么问题、为什么值得学 |
| `patterns/` | 看多个项目背后的通用问题、成熟做法和可迁移框架 |
| `project-radar/` | 看候选项目、自动发现、评分和后续沉淀流程 |
| `interviews/` | 看面经、问答、追问链路和表达训练材料 |
| `apps/knowledge-platform/` | 用可视化平台统一浏览、搜索、阅读和跳转 |

## 3. 核心目录说明

| Folder | 用途 |
| --- | --- |
| `external-projects/` | 外部项目深度沉淀 |
| `patterns/` | 通用问题、优秀技术、工程框架 |
| `project-radar/` | 自动发现、候选池、评分与沉淀流水线 |
| `source-library/` | GitHub、博客、论文、用户资料等资料源 |
| `source-research/` | 对当前项目和源码研究的沉淀 |
| `platform/` | 可视化知识平台的产品规划、路由设计、阅读交互、工程逻辑 |
| `pain-points/` | 辅助整理痛点主题的历史或专题文档 |
| `interviews/` | 面经、答案、场景题、AI 面试官资料 |
| `legacy-migration/` | 旧体系迁移规则、清单和对照关系 |
| `templates/` | 可复用模板和写作规范 |

## 4. 推荐阅读顺序

如果你要快速进入上下文，建议按这个顺序看：

1. `docs/platform/可视化知识平台规格/platform-master-plan.md`
2. `docs/platform/可视化知识平台规格/platform-fit-assessment-and-delivery-roadmap.md`
3. `docs/platform/可视化知识平台规格/engineering-logic-route-framework.md`
4. `docs/platform/可视化知识平台规格/product-platform-vision-and-spec.md`
5. `docs/source-research/当前项目沉淀与路线/current-project-distillation.md`
6. `docs/project-radar/雷达与沉淀流程规划/project-radar-and-distillation-plan.md`

## 5. 平台目标

这套知识库最终要做成一个可以持续进化的 Agent 工程学习平台：

```text
外部项目 / 博客 / 论文 / 用户资料
  -> 自动发现
  -> 自动筛选
  -> 自动沉淀
  -> 项目页 / 方案页 / 痛点页 / 工程逻辑页
  -> 学习使用 / 项目决策 / 面试表达
```

重点不是“收集链接”，而是把高质量输入转成你以后做项目时真正能用的工程逻辑。

## 6. 常用命令

```powershell
python scripts\build_knowledge_index.py
python scripts\knowledge_lint.py
npm --prefix apps\knowledge-platform run build
python scripts\project_radar.py status
```
