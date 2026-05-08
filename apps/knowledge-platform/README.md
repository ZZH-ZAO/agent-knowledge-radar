# Agent 项目知识平台

> 一个本地可视化知识工作台，用中文界面展示项目、方案、痛点、面经和 AI 面试官训练材料。

## 1. 更新数据

从仓库根目录运行：

```powershell
python scripts\build_knowledge_index.py

## 可选：Gitingest 深度理解

如果你要先把仓库压成 `summary / tree / content` 再沉淀，可以先跑：

```powershell
python scripts\ingest_repo.py https://github.com/owner/repo
python scripts\project_radar.py distill owner/repo --use-ingest
```
```

脚本会生成：

```text
data/knowledge-index.json
apps/knowledge-platform/src/data/knowledge-index.json
```

## 2. 本地开发

```powershell
cd apps\knowledge-platform
npm install
npm run dev
```

## 3. 构建验证

```powershell
cd apps\knowledge-platform
npm run build
```

## 4. 中文界面规范

界面文案默认使用中文。项目名、仓库名、代码、命令和专业名词可以保留英文，例如 `MCP`、`Tool Runtime`、`Claude Code`。
