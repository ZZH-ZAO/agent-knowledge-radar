# Directory Map（目录地图）

> 目录名优先服务“打开文件夹就能看懂”。英文目录负责脚本稳定性，中文子目录负责业务语义。

## 1. Docs Root（根目录）

根目录只保留入口和少量 PDF：

```text
docs/
  README.md
  DIRECTORY-MAP.md
  *.pdf                 # PDF 先不迁移
```

其他 Markdown 文档应归入业务目录。

## 2. External Projects（外部项目沉淀）

```text
external-projects/
  完整开源 Agent 平台样本/
  Claude Code 生态与源码样本/
  MCP 工具与浏览器自动化样本/
  AI 前端设计规范样本/
  AI 前端设计生成样本/
  前端风格与工作台样本/
  旧体系迁移项目样本/
  待分类项目池/
```

规则：

```text
docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md
```

## 3. Patterns（通用问题与技术框架）

```text
patterns/
  总纲与方法论/
  Agent Runtime 核心运行时框架/
  Tool 与 MCP 工具体系/
  Memory Plugin Multi-Agent 扩展能力/
  安全治理与可观测性/
  产品化与平台工程/
  前端设计控制/
```

规则：

```text
docs/patterns/{技术主题中文文件夹}/{topic}-patterns.md
```

## 4. Source Research（源码研究）

```text
source-research/
  Claude Code Runtime 源码研究/
  当前项目沉淀与路线/
  外部 Claude Code 分析资料/
  其他项目学习笔记/
```

## 5. Project Radar（项目雷达）

```text
project-radar/
  candidates.json
  candidates.md
  discovery-log.md
  radar-config.json
  scoring-rules.md
  雷达与沉淀流程规划/
```

## 6. Source Library（外部优质资料源）

```text
source-library/
  GitHub 优质项目/
  优质技术博客/
  论文研究资料/
  用户提供文档/
```

来源层负责吸收 GitHub、博客、论文和你提供的资料，再决定是否更新项目沉淀、行业痛点、patterns 或面试官。

## 7. Platform（产品化平台）

```text
platform/
  可视化知识平台规格/
```

## 8. Interviews（面经与面试官）

```text
interviews/
  raw/
  answers/
  scenarios/
  interviewer/
```

## 9. Legacy Migration（旧体系迁移）

```text
legacy-migration/
  旧案例迁移规则与清单/
```

旧体系 `.claude/docs/` 是历史档案层，后续只迁移，不作为新沉淀默认落点。

已迁移项目级文档统一进入：

```text
external-projects/
  旧体系迁移项目样本/
```

已迁移共享模板统一进入：

```text
templates/
  旧体系共享模板/
```

这样保留旧体系的学习价值，但不把旧目录树原样复制进新知识库。
