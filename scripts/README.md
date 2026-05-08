# Scripts

本目录包含 Agent Knowledge Radar 的 Python 自动化脚本。

## 核心脚本

| 脚本 | 用途 | 运行方式 |
|------|------|---------|
| `build_knowledge_index.py` | 从 `docs/` 构建 `knowledge-index.json` 索引 | `python scripts/build_knowledge_index.py` |
| `knowledge_platform_bridge.py` | 前端桥接服务，提供 API | `python scripts/knowledge_platform_bridge.py` |
| `project_radar.py` | 项目发现、评分、沉淀 | `python scripts/project_radar.py status` |
| `ingest_repo.py` | 仓库内容抓取（基于 gitingest） | `python scripts/ingest_repo.py <url>` |
| `knowledge_lint.py` | 知识库健康检查 | `python scripts/knowledge_lint.py` |

## 迁移与升级

| 脚本 | 用途 |
|------|------|
| `migrate_legacy_docs.py` | 将旧 `.claude/docs/` 迁移到新体系 |
| `upgrade_deep_distillation_docs.py` | 给沉淀文档补充面试知识库风格段落 |
| `upgrade_industry_painpoint_docs.py` | 给旧文档补充行业痛点研究结构 |

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `case_advisor.py` | 从案例库生成建议 |
| `export_root_overviews.py` | 生成根目录中文概览文件 |
| `followup_actions.py` | 列出待处理的跟进事项 |
| `session_search.py` | 会话搜索 |
| `register_session.py` | 注册/更新会话条目 |
| `session_archive_audit.py` | 会话归档审计 |

## PPT 生成

| 脚本 | 用途 |
|------|------|
| `generate_industrial_ai_ppt.py` | 生成工业 AI PPT（v1） |
| `generate_industrial_ai_ppt_v4.py` | 生成工业 AI PPT（v4） |
| `patch_ppt_harness.py` | PPT 补丁工具 |

## 研究写作

| 脚本 | 用途 |
|------|------|
| `research_writing_router.py` | 研究写作路由 |
| `research_writing_starter.py` | 研究写作启动器 |

## 依赖安装

```bash
pip install -r requirements.txt
```
