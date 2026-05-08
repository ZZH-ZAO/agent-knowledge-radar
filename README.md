# claude-code-sourcemap

> 非官方 Claude Code sourcemap 研究仓库 + Agent 工程知识库 + 可视化知识平台。

## 1. 项目定位

本仓库最初基于公开 npm 包 `@anthropic-ai/claude-code` 内附带的 source map 还原 TypeScript 源码，用于研究 Claude Code 类 Agent Runtime 的内部结构。

现在它已经扩展成三层系统：

```text
Claude Code sourcemap 源码研究
  -> 外部优秀 Agent 项目沉淀
  -> 可视化知识平台与面试训练
```

你可以用它来：

- 学习 Claude Code 类 Agent Runtime 的源码结构。
- 自动发现和筛选优质 Agent / MCP / DevTools 项目。
- 把项目沉淀成通用问题、优秀技术框架和行动项。
- 用中文可视化界面查看项目、方案、痛点、面经和 AI 面试官训练材料。

## 2. 重要声明

> [!WARNING]
> This repository is **unofficial** and is reconstructed from the public npm package and source map analysis, **for research purposes only**.
> It does **not** represent the original internal development repository structure.

本仓库为**非官方**整理版，基于公开 npm 发布包与 source map 分析还原，**仅供技术研究与学习使用**。

- 源码版权归 [Anthropic](https://www.anthropic.com) 所有。
- 本仓库不代表官方原始内部开发仓库结构。
- 请勿用于商业用途。
- 如有侵权，请联系删除。

## 3. 源码来源

- npm 包：[@anthropic-ai/claude-code](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- 还原版本：`2.1.88`
- 还原文件数：约 `4756` 个
- `.ts` / `.tsx` 源文件：约 `1884` 个
- 还原方式：提取 `cli.js.map` 中的 `sourcesContent` 字段

主要源码目录：

```text
restored-src/src/
  main.tsx
  tools/
  commands/
  services/
  query/
  tasks/
  plugins/
  skills/
  memdir/
  bridge/
  remote/
  coordinator/
  ink/
```

## 4. 知识库入口

文档入口：

```text
docs/README.md
```

推荐先看：

- `docs/source-research/当前项目沉淀与路线/current-project-distillation.md`：本项目自身沉淀。
- `docs/platform/可视化知识平台规格/product-platform-vision-and-spec.md`：可视化平台产品规格。
- `docs/project-radar/雷达与沉淀流程规划/project-radar-and-distillation-plan.md`：Project Radar 与项目沉淀系统规划。
- `docs/project-radar/雷达与沉淀流程规划/project-learning-distillation-playbook.md`：优质项目学习沉淀操作手册。
- `docs/legacy-migration/旧案例迁移规则与清单/legacy-migration-rules.md`：旧沉淀迁移规则，以及以后说“沉淀”默认写入的位置。
- `docs/legacy-migration/旧案例迁移规则与清单/legacy-case-migration-index.md`：`.claude/docs` 旧案例迁移清单。

旧沉淀不会废弃：`.claude/docs/` 是历史档案层，后续会逐步迁移到 `docs/external-projects/` 和 `docs/patterns/`。以后只要说“沉淀某个项目”，默认先检索旧体系，再写入新体系并重建索引。

## 5. 可视化知识平台

前端应用位于：

```text
apps/knowledge-platform/
```

注意：根目录没有前端 `package.json`。所以不要在根目录直接运行 `npm run build`。

### 5.1 更新知识索引

从仓库根目录运行：

```powershell
python scripts\build_knowledge_index.py
```

这会生成：

```text
data/knowledge-index.json
apps/knowledge-platform/src/data/knowledge-index.json
```

### 5.2 启动开发服务

方式一：进入前端目录运行。

```powershell
cd apps\knowledge-platform
npm install
npm run dev
```

方式二：留在仓库根目录运行。

```powershell
npm --prefix apps\knowledge-platform install
npm --prefix apps\knowledge-platform run dev
```

启动后访问：

```text
http://127.0.0.1:5173
```

如果你要使用平台里的“沉淀工作台 -> 执行本地沉淀”按钮，还需要单独启动本地桥接服务：

```powershell
python scripts\knowledge_platform_bridge.py
```

桥接服务默认监听：

```text
http://127.0.0.1:8765
```

如果 `8765` 已经被占用，可以切到别的端口：

```powershell
$env:KNOWLEDGE_PLATFORM_BRIDGE_PORT=8766
python scripts\knowledge_platform_bridge.py
```

当前桥接层已经提供：

- `GET /health`
- `POST /api/distill`
- `POST /api/ingest-repo`
- `POST /api/analyze-project`
- `POST /api/writeback-analysis`

这意味着现在不只是前端工作台可用，后续 Agent 也可以直接调用平台来做 GitHub / 本地项目 / 资料源的理解、分析和沉淀。

### 5.2.1 自动回写闭环

`/api/analyze-project` 现在默认会把分析结果继续回写到：

- `docs/patterns/`
- `docs/pain-points/`
- `docs/interviews/`
- `docs/project-radar/writeback-packages/`

也就是说，当前默认链路已经变成：

```text
项目沉淀 / 分析
  -> 生成 writeback package
  -> 增量回写 patterns / pain-points / interviews
  -> 重建 knowledge-index
  -> 平台立即可见
```

如果你只想做分析、不想自动回写，可以在请求体里显式传：

```json
{
  "autoWriteback": false
}
```

### 5.3 构建验证

方式一：

```powershell
cd apps\knowledge-platform
npm run build
```

方式二：

```powershell
npm --prefix apps\knowledge-platform run build
```

## 6. Project Radar

Project Radar 用来自动发现、筛选、评分和沉淀优质项目。

常用命令：

```powershell
python scripts\project_radar.py status
python scripts\project_radar.py discover --query "coding agent mcp" --limit 10
python scripts\project_radar.py list --min-score 70
python scripts\project_radar.py distill owner/repo
python scripts\project_radar.py distill-all --min-score 80
```

### 6.1 Gitingest 深度理解

现在支持把 `gitingest` 接到沉淀前置层，先把仓库转成 `summary / tree / content`，再进入项目沉淀草稿。

```powershell
python scripts\ingest_repo.py https://github.com/owner/repo
python scripts\ingest_repo.py D:\pico --focus src
python scripts\project_radar.py distill owner/repo --use-ingest
python scripts\project_radar.py distill owner/repo --use-ingest --ingest-focus packages/core
```

缓存默认写到：

```text
tmp/ingest-cache/
```

相关文件：

```text
docs/project-radar/
  candidates.json
  candidates.md
  discovery-log.md
  radar-config.json
  scoring-rules.md
```

## 7. 当前数据结构

核心知识目录：

```text
docs/external-projects/   # 单项目沉淀
docs/patterns/            # 通用问题与优秀技术框架
docs/project-radar/       # 项目候选池与评分
docs/pain-points/         # Pain Points（痛点库）
docs/interviews/          # Interviews（面经与面试官）
docs/platform/            # Platform（产品化平台）
docs/source-research/     # Source Research（源码研究）
docs/templates/           # Templates（模板库）
docs/legacy-migration/    # Legacy Migration（旧体系迁移）
docs/legacy-*.md/json     # 旧 .claude/docs 案例迁移规则和清单
.claude/docs/             # 旧沉淀历史档案，迁移前仍然必须检索
data/                     # 生成给前端使用的索引数据
apps/knowledge-platform/  # 可视化知识平台
```

当前平台已支持：

- 沉淀工作台（可直接录入项目 / 资料，生成沉淀指令与推荐命令）
- 项目界面
- 方案界面
- 痛点界面
- 面经与八股界面
- AI 面试官训练场
- Project Radar 状态页

## 8. 中文界面规范

可视化平台界面文案默认使用中文。

可以保留英文的内容：

- 项目名：`Claude Code`、`Goose`、`Chrome DevTools MCP`
- 仓库名：`aaif-goose/goose`
- 专业名词：`MCP`、`Tool Runtime`、`Agent Runtime`、`Provider`
- 代码、命令、路径、配置字段

## 9. 推荐工作流

```powershell
# 1. 先在平台“沉淀工作台”里定义任务，或者直接发现项目
python scripts\project_radar.py discover --query "coding agent mcp" --limit 10

# 2. 查看候选
python scripts\project_radar.py list --min-score 70

# 3. 生成项目沉淀草稿
python scripts\project_radar.py distill owner/repo

# 4. 更新前端索引
python scripts\build_knowledge_index.py

# 5. 打开知识平台
npm --prefix apps\knowledge-platform run dev
```

### 9.1 沉淀工作台说明

知识平台现在新增了一个中文的“沉淀工作台”路由，用来做三件事：

- 录入要沉淀的 GitHub 项目、本地仓库、博客、论文或旧目录资料
- 选择这次重点偏向：项目沉淀 / 方案抽象 / 痛点补强 / 面试训练 / 前端风格
- 自动生成推荐命令、推荐写入位置，以及一份可以直接发给 Codex 的沉淀指令
- 在本地桥接服务启动后，直接执行 GitHub 项目的 `Project Radar distill` 流程

当前执行能力边界：

- `GitHub 项目`：会自动调用 `python scripts\project_radar.py distill owner/repo --refresh`，然后重建知识索引。
- `本地项目`：会自动在 `docs/external-projects/待分类项目池/` 生成一份项目草稿，并重建知识索引。
- `博客 / 论文 / 旧目录`：会自动在 `docs/source-library/用户提供文档/` 生成一份资料草稿，并重建知识索引。
- 所有非 GitHub 来源仍然会额外写入 `tmp/distill-desk/` 待执行任务文件，方便后续继续深挖。
