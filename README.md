# Agent Knowledge Radar

> Agent 工程知识库 + 可视化知识平台 + MCP Server。

## 项目定位

本仓库是一个 Agent 工程知识管理系统，围绕 Agent Runtime、MCP 工具体系、大模型应用等方向，持续沉淀项目样本、工程方案、行业痛点和面试训练材料。

核心能力：

- **自动发现和筛选**优质 Agent / MCP / DevTools 项目
- **沉淀**成通用问题、优秀技术框架和行动项
- **可视化平台**查看项目、方案、痛点、面经和 AI 面试官训练材料
- **MCP Server** 让 Claude Code 和 Codex 在编码时直接查询知识库

## 快速开始

### 可视化平台

```powershell
cd apps/knowledge-platform
npm install
npm run dev
```

访问 http://127.0.0.1:5173

### 桥接服务（沉淀工作台需要）

```powershell
python scripts/knowledge_platform_bridge.py
```

### MCP Server

Claude Code 已在 `.mcp.json` 中配置好，重启后自动加载。

手动启动（SSE 模式给 Codex 用）：

```powershell
python scripts/mcp_server.py --transport sse --port 8766
```

详见 [docs/guides/codex-integration.md](docs/guides/codex-integration.md)。

### 更新知识索引

```powershell
python scripts/build_knowledge_index.py
```

生成 `data/knowledge-index.json`，前端通过 vite alias 直接读取。

## 仓库结构

```text
data/
  knowledge-index.json          # 唯一权威索引（前端 + MCP Server 共用）

apps/knowledge-platform/        # React 可视化平台（15 个页面）

scripts/
  mcp_server.py                 # MCP Server（stdio + SSE 双传输）
  knowledge_tools.py            # 知识检索核心（10 个函数）
  build_knowledge_index.py      # 从 docs/ 构建索引
  knowledge_platform_bridge.py  # FastAPI 桥接服务
  project_radar.py              # 项目发现、评分、沉淀
  archive/                      # 一次性迁移脚本（已执行完毕）
  tests/                        # 测试（43 个）

docs/
  patterns/                     # 通用工程方案
  pain-points/                  # 行业痛点
  interviews/                   # 面经与面试官
  project-radar/                # 项目候选池与评分
  source-research/              # 源码研究笔记
  external-projects/            # 单项目沉淀
  guides/                       # 使用指南
```

## MCP Server 工具

MCP Server 暴露 10 个工具，Claude Code 和 Codex 可直接调用：

| 工具 | 说明 |
|------|------|
| `search_knowledge` | 关键词搜索项目、方案、痛点、资料源、面经 |
| `get_project` | 获取项目详情 |
| `get_solution` | 获取方案详情 |
| `get_pain_point` | 获取痛点详情 |
| `list_projects` | 列出项目（支持分类/评分过滤） |
| `list_solutions` | 列出所有方案 |
| `list_pain_points` | 列出痛点（支持严重度过滤） |
| `get_related_entities` | 获取实体关联关系 |
| `get_interview_questions` | 获取面试题 |
| `get_knowledge_stats` | 知识库统计信息 |

## Project Radar

```powershell
python scripts/project_radar.py status
python scripts/project_radar.py discover --query "coding agent mcp" --limit 10
python scripts/project_radar.py list --min-score 70
python scripts/project_radar.py distill owner/repo
```

## 推荐工作流

```powershell
# 1. 发现项目
python scripts/project_radar.py discover --query "coding agent mcp" --limit 10

# 2. 查看候选
python scripts/project_radar.py list --min-score 70

# 3. 沉淀项目
python scripts/project_radar.py distill owner/repo

# 4. 更新索引
python scripts/build_knowledge_index.py

# 5. 打开平台查看
npm --prefix apps/knowledge-platform run dev
```

## 重要声明

> [!WARNING]
> This repository is **unofficial** and is reconstructed from the public npm package and source map analysis, **for research purposes only**.

本仓库最初基于公开 npm 包 `@anthropic-ai/claude-code` 的 source map 还原源码用于研究，现已扩展为 Agent 工程知识管理平台。

- 源码版权归 [Anthropic](https://www.anthropic.com) 所有。
- 请勿用于商业用途。
- 如有侵权，请联系删除。

## 中文界面规范

平台界面文案默认使用中文。保留英文的内容：项目名、仓库名、专业名词（MCP、Agent Runtime 等）、代码和配置字段。
