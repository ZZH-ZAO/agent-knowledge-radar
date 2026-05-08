# 平台优化 Backlog：来自 GitHub 与优质文档平台对标

> 目标：把外部优秀平台的做法，转成当前知识平台可以持续执行的工程 backlog。  
> 相关研究：
> - `docs/source-library/GitHub 优质项目/github-knowledge-platform-samples-2026-05-04.md`
> - `docs/platform/可视化知识平台规格/frontend-reference-patterns-from-leading-docs-sites.md`

## 1. 最新补充结论

这轮对标后，结论比以前更明确了：

- 我们最该补的不是页面装饰，而是长文阅读基础设施。
- `项目页 / 方案页 / 痛点页 / 工程逻辑页` 需要开始区分“列表效率模式”和“长文阅读模式”。
- 搜索结果要从“找到文档”升级成“跳到命中段落”。
- 页面要支持复制、导出、反馈和后续 AI 转化。
- 平台后续要开始度量内容质量，而不是只度量能不能展示。

## 2. P0：基础阅读能力补强

### 2.1 Markdown Reader AST 化

目标：

- 支持 GFM 表格、任务列表、代码块
- 支持稳定 heading anchor
- 支持右侧 TOC
- 支持链接跳转
- 支持自定义 evidence / action block

建议依赖：

```text
react-markdown
remark-gfm
rehype-slug
rehype-autolink-headings
```

### 2.2 长文阅读模式

目标：

- 方案页、痛点页、工程逻辑页不再只是窄详情卡
- 增加右侧目录、标题跳转、页面操作区
- 支持复制链接、复制 Markdown、导出

参考来源：

- Docusaurus TOC
- Starlight 默认布局
- Mintlify contextual menu

### 2.3 构建搜索索引

目标：

- 搜索不只过滤标题
- 支持项目、方案、痛点、资料源、面经、工程逻辑统一检索
- 搜索结果展示命中类型、来源、推荐阅读视角

第一版数据结构可继续基于 `scripts/build_knowledge_index.py`。

### 2.4 搜索命中段落与高亮

目标：

- 搜索结果定位到段落，而不是只定位到页面
- 打开后自动滚到对应标题或命中块
- 在正文中高亮搜索词

参考来源：

- Pagefind section results
- Pagefind highlighting

### 2.5 Knowledge Lint

目标：防止知识库越沉淀越乱。

检查项：

- 项目没有关联痛点或方案
- 痛点没有证据来源
- pattern 没有项目案例
- 文档没有行动项
- 资料源没有进入痛点或方案

## 3. P1：搜索与记录升级

### 3.1 Pagefind / MiniSearch

策略：

- 少量内容：MiniSearch 内嵌到 JSON
- 文档变多：Pagefind 构建静态索引
- 需要更强语义时，再考虑向量或 hybrid search

### 3.2 文档 Block ID

目标：

- 痛点页可引用项目文档里的具体段落
- 面试官可引用某一证据块继续追问
- 搜索结果能跳到命中块

### 3.3 页面反馈与质量信号

目标：

- 页面底部支持“有帮助吗 / 缺什么 / 转行动项”
- 后台记录搜索零结果、页面跳转、反馈和引用率
- 让内容优化有依据，而不是只靠感觉

参考来源：

- GitBook comments
- ReadMe Docs Audit
- Mintlify analytics

### 3.4 资料源 Intake

目标：

```text
GitHub / 博客 / 论文 / 用户文档
  -> 资料源卡片
  -> 行业痛点
  -> 共性做法
  -> 当前项目行动项
```

## 4. P2：成熟平台能力

### 4.1 图谱与双链

可借鉴：

- Trilium
- 思源

目标：

- 项目 -> 痛点 -> pattern -> 面试题
- 资料源 -> 证据块 -> 行动项

### 4.2 版本历史

记录每个痛点、方案和工程逻辑页的演进：

- 新增了哪些证据
- 哪些做法被证明有效
- 哪些行动项已完成

### 4.3 协作与评注

暂时不是第一优先级，但后续可借鉴：

- 评论
- 审核状态
- 空间 / 分类权限

## 5. 当前项目行动项

- [x] 用 `react-markdown + remark-gfm` 替换手写 Markdown 渲染
- [x] 在 `knowledge-index.json` 增加 `searchIndex`
- [x] 新增 `scripts/knowledge_lint.py`
- [x] 给平台增加“搜索结果”展示
- [ ] 给 `MarkdownPreview` 补标题锚点与右侧目录
- [ ] 给搜索结果补命中段落与高亮跳转
- [ ] 给详情页补页面操作菜单
- [ ] 为长文路由设计真正的阅读模式
- [ ] 给资料源补 `sourceType / evidenceStrength / relatedPainPoints / relatedPatterns`
- [ ] 加入页面反馈与文档质量统计

## 6. 行业痛点研究版补充

### 6.1 这个 backlog 对应的行业普遍问题

知识平台最容易失败的地方，是内容越多越难找、越难读、越难证明来源、越难持续更新。

### 6.2 可作为证据的来源类型

- OpenKB
- QMD
- Pagefind
- Docusaurus
- Starlight
- Docmost
- Trilium
- 思源
- remark / unified
- GitBook
- Mintlify
- ReadMe

### 6.3 优秀平台的共性做法

它们都在做同一件事：把文本变成结构化对象，再围绕搜索、导航、记录、版本、引用和自动化来治理知识。

### 6.4 后续建议追踪的数据

- 搜索命中率
- 搜索零结果率
- 无关联文档数
- 无行动项文档数
- 页面跳转次数
- bundle size
- 构建耗时
- 文档被引用率

### 6.5 自动进化规则

每次平台改动后，都要回写这份 backlog：哪些已经完成，哪些因为收益低被推迟，哪些需要新的优秀样本来继续验证。
