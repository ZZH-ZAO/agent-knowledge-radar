# 内容重构覆盖清单

> 更新时间：2026-05-08  
> 作用：这份清单不讲愿景，只记录这轮“内容重构主线”已经覆盖到哪里、哪些还是旧风格，避免平台看起来很满，但实际深度不均匀。

## Batch A：external-projects

### 已重构为新骨架

- [x] `anthropics/claude-code`
- [x] `zzh/pico`
- [x] `ChromeDevTools/chrome-devtools-mcp`
- [x] `aaif-goose/goose`

### 下一批建议优先补

- [ ] `affaan-m/everything-claude-code`
- [ ] 旧体系迁移项目样本组
- [ ] 前端设计样本组

## Batch B：patterns

### 已重构为新骨架

- [x] `agent-runtime`
- [x] `tool-runtime`
- [x] `mcp-integration`
- [x] `memory-system`
- [x] `permission-sandbox`

### 下一批建议优先补

- [ ] `provider-abstraction`
- [ ] `productization`
- [ ] `multi-agent`
- [ ] `plugin-system`
- [ ] `observability`

## Batch C：pain-points

### 已拆成单篇正文

- [x] `tool-result-context-overload`
- [x] `mcp-ecosystem-governance`
- [x] `memory-context-staleness-and-bloat`
- [x] `runtime-recovery-and-eval-gap`
- [x] `agent-productization-gap`

### 备注

- [x] 已接入 `build_knowledge_index.py`，痛点页可直接读取单篇正文。
- [ ] 后续继续补“provider 差异污染 runtime”“扩展生态治理更细分支”。

## Batch D：interviews + source-research

### 已重构样板

- [x] `tencent-csig-answer-framework`
- [x] `anthropics-claude-code-official-distillation`

### 下一批建议优先补

- [ ] `claude-code-learning-highlights`
- [ ] `liuup-claude-code-analysis-distillation`
- [ ] `tencent-csig-rag-testing-dev-scenario`
- [ ] `tencent-csig-interviewer-memory`

## Batch E：辅助层

### 已完成

- [x] `document-refactor-spec.md`

### 待继续推进

- [ ] `source-library`
- [ ] `platform` 规划类文档统一成产品判断文档
- [ ] `legacy-migration`
- [ ] `templates`
- [ ] 各目录 `README.md`

## 这一轮的验收结论

- [x] 索引脚本已经把深 section 当成一等字段处理。
- [x] 项目页、方案页、痛点页都能直接展示深正文。
- [x] 痛点页不再只能吃脚本种子，也能读单篇痛点文档。
- [ ] 全库文档深度仍然不均匀，后续还需要继续批量推进。
