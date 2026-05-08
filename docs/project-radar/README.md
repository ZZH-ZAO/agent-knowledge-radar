# Project Radar 使用说明

> Project Radar 用来自动发现、筛选、评分优质项目，并把高价值项目送入沉淀流水线。

## 1. 常用命令

初始化目录和基础文件：

```powershell
python scripts\project_radar.py init
```

手动添加一个项目：

```powershell
python scripts\project_radar.py add https://github.com/anthropics/claude-code
```

按关键词搜索项目：

```powershell
python scripts\project_radar.py discover --query "coding agent mcp" --limit 10
```

按预设主题搜索项目：

```powershell
python scripts\project_radar.py discover --topic agent-runtime --limit 5
```

重新评分：

```powershell
python scripts\project_radar.py score
```

查看高分候选：

```powershell
python scripts\project_radar.py list --min-score 70
```

查看当前状态：

```powershell
python scripts\project_radar.py status
```

生成单个项目沉淀草稿：

```powershell
python scripts\project_radar.py distill anthropics/claude-code
```

批量生成高分项目沉淀草稿：

```powershell
python scripts\project_radar.py distill-all --min-score 80
```

## 2. 输出文件

Project Radar 会维护这些文件：

```text
docs/project-radar/candidates.json
docs/project-radar/candidates.md
docs/project-radar/discovery-log.md
docs/project-radar/radar-config.json
docs/project-radar/scoring-rules.md
```

深度沉淀草稿会写入：

```text
docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md
```

通用问题和优秀技术框架会写入：

```text
docs/patterns/*.md
```

## 3. 推荐工作流

```text
discover
  -> list
  -> 人工选择高价值项目
  -> distill
  -> 精读项目资料
  -> 补全 external-projects 文档
  -> 更新 patterns 文档
```

第一版自动评分只用于粗筛，不代表最终判断。真正进入知识库的方法论层之前，仍然需要人工或 Codex 深度阅读 README、docs、源码和 CHANGELOG。
