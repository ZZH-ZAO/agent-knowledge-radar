# Directory Governance（目录治理）

> 目标：让 `D:\claude-code-sourcemap` 的知识库不要随着沉淀越来越乱。以后你日常只看“入口层”，具体内容由平台和脚本自动读取。

## 1. 以后只记四层

```text
入口层：我日常打开和阅读
内容层：真正的沉淀文档
系统层：脚本、索引、平台生成物
归档层：旧体系、原始材料、迁移记录
```

## 2. 入口层

日常只需要先看这些：

| 入口 | 用途 |
| --- | --- |
| `docs/README.md` | 知识库总入口 |
| `docs/DIRECTORY-MAP.md` | 目录地图 |
| `docs/DIRECTORY-GOVERNANCE.md` | 目录治理规则 |
| `apps/knowledge-platform/` | 可视化平台 |

## 3. 内容层

真正有阅读和学习价值的内容只放这里：

| 目录 | 放什么 |
| --- | --- |
| `docs/external-projects/` | 单个外部项目沉淀 |
| `docs/patterns/` | 通用问题、优秀技术框架、可迁移方法 |
| `docs/interviews/` | 面经、答案、面试官记忆、训练场景 |
| `docs/platform/` | 平台产品化方案 |
| `docs/source-research/` | Claude Code sourcemap 和当前项目研究 |

## 4. 系统层

这些目录和文件主要给脚本使用，平时不用手动看：

| 目录 | 用途 |
| --- | --- |
| `data/` | 平台索引输出 |
| `apps/knowledge-platform/src/data/` | 前端内置索引 |
| `docs/project-radar/candidates.json` | 雷达候选数据 |
| `docs/project-radar/candidates.md` | 雷达候选可读版 |
| `scripts/` | 构建索引、项目雷达等脚本 |

## 5. 归档层

这些是历史材料，不作为新沉淀默认入口：

| 目录 | 规则 |
| --- | --- |
| `.claude/docs/` | 旧体系，只迁移，不新增 |
| `docs/legacy-migration/` | 旧文档迁移规则和记录 |
| `docs/interviews/raw/` | 原始面经索引，不直接当最终答案 |

## 6. 新内容放哪里

### 沉淀一个项目

```text
docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md
```

并且至少更新一个：

```text
docs/patterns/{主题中文文件夹}/{topic}-patterns.md
```

### 沉淀一个方案

```text
docs/patterns/{主题中文文件夹}/{topic}-patterns.md
```

### 沉淀一个面试问题

```text
docs/interviews/question-bank.json
docs/interviews/answers/
docs/interviews/scenarios/
docs/interviews/interviewer/
```

### 沉淀一个平台产品想法

```text
docs/platform/
apps/knowledge-platform/DESIGN.md
```

## 7. 自动更新规则

平台展示内容不是手写维护的，它来自文档索引。

每次新增或修改沉淀文档后运行：

```powershell
python scripts\build_knowledge_index.py
npm --prefix apps\knowledge-platform run build
```

平台会自动读取：

- `docs/external-projects/**/*.md`
- `docs/patterns/**/*.md`
- `docs/interviews/question-bank.json`
- `docs/project-radar/candidates.json`

所以真正要沉淀的是文档本身，不要在前端里硬写长内容。

## 8. 减少目录膨胀的规则

- 不为单个小想法新建一级目录。
- 新一级目录必须回答：它是不是一个长期内容域？
- 能归到 `external-projects/`、`patterns/`、`interviews/`、`platform/` 的，不新增目录。
- `docs/` 根目录只放入口文档和少量 PDF。
- Project Radar 发现的新项目先进入候选池，不直接制造大量文件。
