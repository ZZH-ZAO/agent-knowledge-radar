# Scripts

本目录包含 Agent Knowledge Radar 的 Python 自动化脚本。

## MCP 服务

| 脚本 | 用途 | 运行方式 |
|------|------|---------|
| `mcp_server.py` | MCP Server（Claude Code stdio / Codex SSE） | `python scripts/mcp_server.py` |
| `knowledge_tools.py` | 知识检索核心模块（被 MCP Server 调用） | — |

详见 `docs/guides/codex-integration.md`。

## 核心脚本

| 脚本 | 用途 | 运行方式 |
|------|------|---------|
| `build_knowledge_index.py` | 从 `docs/` 构建 `knowledge-index.json` 索引 | `python scripts/build_knowledge_index.py` |
| `knowledge_platform_bridge.py` | 前端桥接服务（FastAPI），提供 API | `python scripts/knowledge_platform_bridge.py` |
| `bridge_utils.py` | 纯 stdlib 工具函数库 | — |
| `project_radar.py` | 项目发现、评分、沉淀 | `python scripts/project_radar.py status` |
| `knowledge_lint.py` | 知识库健康检查 | `python scripts/knowledge_lint.py` |

## 功能脚本

| 脚本 | 用途 |
|------|------|
| `case_advisor.py` | 从案例库生成建议 |
| `followup_actions.py` | 列出待处理的跟进事项 |
| `session_search.py` | 会话搜索 |
| `register_session.py` | 注册/更新会话条目 |
| `session_archive_audit.py` | 会话归档审计 |
| `export_root_overviews.py` | 生成根目录中文概览文件 |
| `research_writing_router.py` | 研究写作路由 |
| `research_writing_starter.py` | 研究写作启动器 |

## PPT 生成

| 脚本 | 用途 |
|------|------|
| `generate_industrial_ai_ppt.py` | 生成工业 AI PPT（v1） |
| `generate_industrial_ai_ppt_v4.py` | 生成工业 AI PPT（v4） |

## Archive（一次性脚本，已执行完毕）

`archive/` 目录存放迁移和升级用的一次性脚本，保留供参考：

| 脚本 | 原用途 |
|------|--------|
| `migrate_legacy_docs.py` | 将旧 `.claude/docs/` 迁移到新体系 |
| `upgrade_deep_distillation_docs.py` | 给沉淀文档补充面试知识库风格段落 |
| `upgrade_industry_painpoint_docs.py` | 给旧文档补充行业痛点研究结构 |
| `ingest_repo.py` | 仓库内容抓取（已被 bridge API 替代） |
| `patch_ppt_harness.py` | PPT 补丁工具 |

## 依赖安装

```bash
pip install -r requirements.txt
```
