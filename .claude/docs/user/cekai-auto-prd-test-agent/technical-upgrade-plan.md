# ByteDance--Auto_prd_test_agent 技术改造方案

## Summary

- Project name: ByteDance--Auto_prd_test_agent
- Project path: `D:\测开\ByteDance--Auto_prd_test_agent`
- Document type: user
- Purpose: provide a concrete technical upgrade plan for evolving this project from a Streamlit-centered test generation workbench into a more maintainable, retrievable, and quality-closed testing Agent system

## 一、改造目标先定清楚

这个项目的技术改造，不应该理解成“重写一遍”。

更合理的目标是三件事：

1. 让系统更容易维护和扩展
2. 让知识检索更准、更可控
3. 让历史案例和评审结果真正变成组织资产

所以本次改造的核心不是炫技，而是把当前这条链路：

`文档接入 -> 检索增强 -> 用例生成 -> 人工微调 -> AI 评审 -> 资产回流`

升级成一条更稳定的工程流水线。

## 二、建议的目标架构

建议从现在的“UI 主编排”改成“UI + Service + Core + Store”四层。

```text
ui/
  main.py
  sidebar.py
  components.py

services/
  ingestion_service.py
  retrieval_service.py
  generation_service.py
  evaluation_service.py
  archive_service.py
  export_service.py

core/
  llm_client.py
  rag_engine.py
  reranker.py
  evaluator.py
  prompt_builder.py
  schemas.py

stores/
  vector_store.py
  case_store.py
  config_store.py
  feedback_store.py
```

四层职责：

- `ui/`
  只负责交互、展示、上传、结果编辑
- `services/`
  负责工作流编排
- `core/`
  负责底层能力组件
- `stores/`
  负责数据存取和持久化

## 三、分模块技术改造方案

### 1. 编排层改造

#### 当前问题

- `ui/main.py` 过重
- 流程逻辑和展示逻辑耦合
- 状态依赖 `st.session_state`

#### 改造方案

把主流程拆成服务函数：

- `ingest_inputs(files, options) -> IngestionResult`
- `retrieve_context(query, filters) -> RetrievalResult`
- `generate_cases(input_pack) -> GenerationResult`
- `refine_cases(input_pack) -> GenerationResult`
- `evaluate_cases(input_pack) -> EvaluationResult`
- `archive_case(input_pack) -> ArchiveResult`

配套增加统一数据结构：

- `IngestionResult`
- `RetrievalResult`
- `GenerationResult`
- `EvaluationResult`
- `ArchiveResult`

#### 为什么更好

- 更容易测试
- UI 可以换
- 以后容易接 API

### 2. Prompt 层改造

#### 当前问题

- Prompt 全写在一个文件里
- Prompt 既承担角色说明，又承担流程规则，又承担输出契约
- 维护成本会逐渐升高

#### 改造方案

把 Prompt 拆成三类：

1. role prompt
   定义角色身份
2. task prompt
   定义当前任务目标
3. policy / contract prompt
   定义输出格式、禁止事项、评分标准

建议新增：

```text
prompts/
  roles/
    test_designer.md
    qa_evaluator.md
  tasks/
    generate_cases.md
    refine_cases.md
    filter_rag.md
  policies/
    output_contract.md
    coverage_rules.md
    testcase_quality_rules.md
```

#### 为什么更好

- 更清楚哪些规则是长期稳定的
- 更容易做 A/B 测试
- 更容易按场景切换

### 3. RAG 层改造

#### 当前问题

- 只有向量粗召回 + LLM 过滤
- 只有语义检索，缺少关键词检索补充
- 缺 metadata filter
- 缺 rerank
- 知识库和案例库分开了，但检索策略还比较粗

#### 改造方案

RAG 直接升级成五段式：

1. query understanding
2. hybrid retrieval
3. candidate normalization
4. rerank
5. context assembly

细化为：

#### 第一步：Query Understanding

对用户 PRD 或需求做分析，抽出：

- 业务域
- 功能模块
- 风险标签
- 用例生成目标

例如识别出：

- 登录
- 权限
- 密码规则
- 异常路径
- 安全测试

这一层除了抽语义主题，还应该顺手抽两类关键词：

1. 业务关键词
   例如登录、支付、库存、角色、风控、短信验证码
2. 逻辑关键词
   例如如果、并且、或者、必须、禁止、为空、失败、超时、超过、不小于

业务关键词帮助系统找到“讲的是不是同一件业务”。  
逻辑关键词帮助系统找到“这里是不是在说规则、约束、边界和因果关系”。

#### 第二步：Hybrid Retrieval

同时从两个集合召回：

- `company_knowledge`
- `history_cases`

并且按 metadata 控制：

- domain
- source_type
- status
- quality_tag
- version

同时使用两路检索：

1. semantic retrieval
   向量语义召回
2. keyword retrieval
   关键词召回

关键词检索我认为非常值得加，不仅合理，而且对这个项目特别有帮助。

原因很简单：

- 语义检索擅长“意思接近”
- 关键词检索擅长“命中明确术语、规则词、字段名、异常词”

而测试用例生成特别需要后者，因为很多关键测试点并不是靠泛语义，而是靠这些词触发出来的：

- 必须
- 不得
- 最大
- 最小
- 连续失败
- 锁定
- 超时
- 重试
- 空值
- 重复提交

也就是说，混合检索比纯语义检索更适合这种“规则和边界驱动”的业务。

#### 第三步：Candidate Normalization

因为两路检索回来的结果格式、分数和偏好都不一样，所以中间需要一个归一化层。

建议为每条候选都整理出统一字段：

- `candidate_id`
- `source_type`
- `source_name`
- `chunk_text`
- `semantic_score`
- `keyword_score`
- `matched_keywords`
- `metadata`

如果某一条是通过关键词命中的，还可以额外记录：

- 命中了哪些业务关键词
- 命中了哪些逻辑关键词
- 命中次数
- 命中位置是否集中在规则句附近

这样后面的 rerank 才有基础。

#### 第四步：Rerank

不直接把向量结果交给模型，而是先 rerank。

这里就不再只是对“语义相似度”打分，而是对“最终值不值得送给生成模型”打分。

#### 第五步：Context Assembly

最终送给生成模型的上下文，不是“前 K 条拼接”，而是按角色组装：

- 规范约束
- 历史优质案例
- 当前模块相关补充说明

#### 为什么这样更好

- 噪声更少
- 可解释性更强
- 能为不同任务拼不同上下文
- 能同时保住“语义相关性”和“规则命中能力”

### 3.1 关键词检索为什么值得加

很多人会担心：“都已经有语义检索了，还要不要关键词检索？”

对这个项目，我的判断是：

> 要，而且非常合理。

因为测试生成不是开放式问答，它常常高度依赖明确规则词。

例如下面这些句子：

- 密码长度至少 8 位
- 连续输错 5 次后锁定 30 分钟
- 手机号为空时禁止提交
- 优惠券不可叠加使用

这些内容之所以重要，不只是因为语义相关，而是因为里面有明确的：

- 数值阈值
- 禁止条件
- 边界条件
- 因果规则

这些内容非常适合被关键词检索捕获。

### 3.2 关键词可以分哪两大类

#### 第一类：业务关键词

作用是确定“在不在同一业务域里”。

例如：

- 登录
- 注册
- 支付
- 订单
- 库存
- 退款
- 验证码
- 权限
- 风控

这类词适合用于：

- 召回同模块规范
- 召回相近历史案例
- 避免跨模块噪声

#### 第二类：逻辑连接词 / 规则触发词

作用是确定“这一段是不是在讲规则、条件和边界”。

例如：

- 如果
- 当
- 并且
- 或者
- 必须
- 不得
- 禁止
- 至少
- 至多
- 超过
- 不小于
- 为空
- 失败
- 超时
- 重试
- 锁定

这类词特别适合帮助你识别：

- 约束条件
- 异常路径
- 边界场景
- 状态转移条件

也就是说，业务关键词是“讲什么”，逻辑关键词是“怎么规定它”。

### 3.3 混合检索的推荐做法

不要简单把两边结果粗暴合并，而是建议这样做：

1. 语义检索召回 Top N
2. 关键词检索召回 Top M
3. 去重并归一化
4. 用 rerank 做统一排序

关键词检索可以先从轻量版本开始：

- `BM25`
- 倒排索引
- 简单字段匹配

不一定要一开始就做得很重。

### 3.4 一个实用的混合分数思路

在 rerank 之前，可以先给候选一个粗分：

```text
retrieval_score =
  0.7 * semantic_score +
  0.3 * keyword_score
```

如果当前任务特别偏规则和边界，可以调成：

```text
retrieval_score =
  0.55 * semantic_score +
  0.45 * keyword_score
```

这取决于你更想找：

- “主题相近”
还是
- “规则命中”

对测试 Agent 来说，很多时候第二种会更值钱。

### 3.5 逻辑关键词检索要注意什么

逻辑词单独看会很泛，所以不能孤立使用。

例如：

- “如果”
- “或者”
- “并且”

这些词到处都有，如果单独检索，会带来很多噪声。

更好的方式是：

1. 逻辑词和业务词联合匹配
   例如“登录 + 必须”“支付 + 禁止”“库存 + 小于”
2. 逻辑词和规则句式联合识别
   例如“如果……则……”“当……时……”“不得……”
3. 逻辑词只作为加分项，不作为唯一召回条件

所以逻辑连接词是很有用的，但一定要跟业务语义结合。

### 3.6 推荐的关键词字段来源

你可以从三类地方生成关键词：

1. query 侧抽取
   从 PRD / 用户需求中抽关键词
2. document 侧预抽取
   文档入库时抽关键词和规则词
3. 人工词表
   团队维护一份业务词表和规则词表

这是比较稳的方案，因为：

- 自动抽取有覆盖
- 人工词表有控制力

## 六、长文本索引的兜底策略

### 1. 为什么必须有兜底

索引阶段最大的一个现实问题是：

- 文档太长
- 结构太乱
- 纯切片逻辑切不稳
- 多模态解析出的文本不干净

如果系统把“切片失败”理解成“索引失败”，那后面检索质量会非常脆弱。

所以更合理的思路是：

> 索引阶段要设计成多层降级体系，而不是只有一层切片器。

### 2. 推荐的四层兜底

#### 第一层：正常切片

优先使用你当前的递归切片、段落切片、窗口切片。

这是低成本主路径。

#### 第二层：固定窗口硬切

如果正常切片失败，先不要丢文档，而是退化到：

- 固定字符窗口
- 固定 token 窗口
- 少量 overlap

这层的目标不是完美，而是“至少能索引”。

#### 第三层：先抽结构，再切片

如果文档特别长、特别乱，可以先抽：

- 一级标题
- 二级标题
- 小节摘要
- 规则段
- 表格段

然后按结构单元切片，而不是整文硬切。

这层特别适合：

- 长 PRD
- 复杂规范文档
- 会议纪要
- 图文混排文档

#### 第四层：Agent / LLM 分治索引

当普通切片器和结构化切片都不理想时，再引入 Agent 或 LLM 做高成本兜底。

Agent 可以做的事情包括：

- 识别文档结构
- 按业务意义切块
- 抽章节摘要
- 提取规则、约束、风险点
- 给每块打标签

### 3. Agent 可不可以引入

可以，但我的建议是：

> Agent 适合做“复杂文档的最后一层增强”，不适合替代所有基础切片逻辑。

原因很简单：

- Agent 成本高
- Agent 慢
- Agent 输出可能不稳定
- 大批量索引时不经济

所以更稳的策略是：

1. 普通切片优先
2. 结构化切片兜底
3. Agent 只处理疑难文档

### 4. 什么情况下触发 Agent 兜底

你可以给系统设几个触发条件：

- 文档长度超阈值
- 标题识别率太低
- chunk 质量差
- chunk 重复率高
- 召回噪声大
- 多次切片后有效文本覆盖率不足

满足这些条件时，再让 Agent 介入。

### 5. Agent 兜底时的产物应该是什么

不要只让 Agent 输出“摘要”，而是让它输出中间索引表示。

例如每个块输出：

- `section_title`
- `section_summary`
- `business_keywords`
- `logic_keywords`
- `constraints`
- `risk_points`
- `raw_offset_range`

这样后面检索和 rerank 才能真正利用这层智能处理结果。

### 6. 为什么这种兜底设计更合理

因为它的本质是把索引流程变成：

- 主路径低成本、可批量
- 异常路径高智能、可兜底

这比一开始就把所有文档交给 Agent 更工程化，也更适合真实系统。

### 4. Memory / Case Store 改造

#### 当前问题

- 历史案例只有“存了”和“可检索”
- 没有质量标签
- 没有人工采纳反馈

#### 改造方案

为案例增加结构化字段：

- `case_id`
- `project_name`
- `business_domain`
- `module`
- `source_prd_summary`
- `generated_version`
- `final_version`
- `evaluation_score`
- `accepted_by_human`
- `edited_after_generation`
- `quality_tag`
- `template_candidate`
- `created_at`
- `updated_at`

并新增两个概念：

1. `golden_cases`
   真正高质量样本
2. `case_patterns`
   抽象出来的测试模式

#### 为什么更好

- 检索时可控
- 模板化更容易
- 可以做反馈学习

### 5. Evaluator 层改造

#### 当前问题

- 评估是一轮性的
- 结果没有用于持续改进

#### 改造方案

把 evaluator 输出拆成两层：

1. 用户可读层
   给用户看评分、问题、建议
2. 系统可写回层
   给系统记录错误类型、漏测类型、推荐模板化结果

建议 evaluator 增加这些字段：

- `coverage_score`
- `logic_score`
- `dedup_score`
- `compliance_score`
- `risk_score`
- `major_gaps`
- `common_gap_tags`
- `template_worthy`

#### 为什么更好

- 可以长期统计
- 可以反向优化 Prompt
- 可以筛选高质量案例

### 6. Provider / Model 层改造

#### 当前问题

- Gemini / Qwen 已支持，但职责不够清晰
- 不同任务没有明确的模型策略

#### 改造方案

按任务分模型：

- 多模态解析模型
- 主生成模型
- 评审模型
- rerank 模型
- 摘要模型

并在配置层显式声明：

```json
{
  "models": {
    "parser": "...",
    "generator": "...",
    "evaluator": "...",
    "reranker": "...",
    "summarizer": "..."
  }
}
```

#### 为什么更好

- 降本
- 更稳定
- 便于替换供应商

## 四、实施顺序建议

### 阶段一：先重构，不改产品能力

目标：

- UI 解耦
- service 层成型
- 数据结构标准化

这一步不追求“功能更多”，只追求“代码可维护”。

### 阶段二：加强 RAG 与案例资产

目标：

- metadata
- rerank
- case quality tag
- golden sample

这一步开始明显提升结果质量。

### 阶段三：形成质量闭环

目标：

- evaluator 结构化写回
- 统计常见漏测点
- 高质量案例模板化

这一步会让系统越来越像“测试知识系统”。

### 阶段四：再考虑半 Agent 化

目标：

- 统一 tool 接口
- 引入任务级 planner
- 接外部测试平台

这一步属于平台化阶段，应该最后做。

## 五、rerank 打分维度怎么设计

你问的这个问题很关键。  
这个项目的 rerank 不能只看“语义像不像”，否则会把很多“看起来相关、实际上没用”的文档排到前面。

更好的做法是把 rerank 分成“基础相关性 + 测试价值 + 知识可信度”三层。

### 第一层：基础相关性

这是最基本的一层，判断“它和当前任务有没有关系”。

建议维度：

1. query relevance
   这段内容和当前 PRD / 查询的语义相关程度
2. module match
   是否命中同一模块、同一业务域
3. intent match
   是否适合当前任务目的

举例：

- 当前目标是“生成登录测试用例”
- 一段内容虽然也在讲用户系统，但其实是账户注销规范
- 那它 query relevance 可能还行，但 module match 会一般

### 第二层：测试价值

这层是这个项目最该有的，也是普通通用 RAG 最容易忽略的。

建议维度：

1. testcase usefulness
   对测试用例生成有没有直接帮助
2. rule strength
   它是硬规范、软建议，还是背景说明
3. edge-case density
   是否包含异常、边界、安全、约束条件
4. executable specificity
   是否足够具体，可直接转成测试点

直白地说：

- “这个模块很重要，请认真测试”
  相关，但测试价值低
- “密码长度最少 8 位，连续输错 5 次锁定 30 分钟”
  测试价值高

### 第三层：知识可信度

这层决定“这段内容值不值得被优先信任”。

建议维度：

1. source authority
   来源是否权威
2. version freshness
   是否为当前有效版本
3. quality tag
   是否为高质量样本 / golden sample
4. human acceptance
   历史上是否被人工采纳过

这层特别重要，因为企业知识里最怕：

- 旧文档
- 草稿
- 低质量历史案例

## 七、推荐的 rerank 评分公式

如果你想先做一个实用版本，可以这样：

```text
final_score =
  0.35 * query_relevance +
  0.20 * module_match +
  0.20 * testcase_usefulness +
  0.10 * rule_strength +
  0.05 * edge_case_density +
  0.05 * source_authority +
  0.03 * version_freshness +
  0.02 * human_acceptance
```

这是一个偏“生成测试用例”场景的初始配方。

它表达的是：

- 先保证相关
- 再保证有测试价值
- 最后再看可信度和新鲜度

## 八、不同知识类型的 rerank 维度应略有不同

这点很重要。

不要对所有文档用同一套打分。

### 1. 规范文档

更看重：

- rule_strength
- version_freshness
- source_authority
- executable_specificity

### 2. 历史案例

更看重：

- testcase_usefulness
- module_match
- human_acceptance
- evaluation_score

### 3. 模板样本 / golden sample

更看重：

- quality_tag
- structure completeness
- reuse potential

所以更成熟的做法是：

- 先按文档类型分桶
- 再做类型内 rerank
- 最后按上下文组装策略拼接

## 九、如果让我给你一个最实用的 rerank 维度清单

如果你想先落地一个不复杂但很够用的版本，我建议直接从这 8 个维度开始：

1. `query_relevance`
2. `module_match`
3. `testcase_usefulness`
4. `rule_strength`
5. `edge_case_density`
6. `source_authority`
7. `version_freshness`
8. `human_acceptance`

这 8 个维度已经能把“相关但无用”和“真正值得送给生成模型的内容”区分开很多。

## 十、一句话建议

这个项目的技术改造重点应该是：

> 先把编排解耦，再把检索做准，再把历史案例和评审结果沉淀成质量闭环。

而这个项目的 rerank 维度，最重要的不是只有“语义相关性”，而是：

> 相关性、测试价值、知识可信度三层同时打分。

## 十一、RAG 评测指标怎么设计

这个项目后续如果真的开始做 hybrid retrieval、rerank、golden case 和记忆回流，就不能只靠“感觉好像更准了”来判断效果。

更合理的做法是把指标分成三层：

1. 检索层指标
2. 重排层指标
3. 最终生成收益指标

### 11.1 检索层指标

这层回答的是：

- 找没找到
- 找得全不全
- 找出来的噪声多不多

建议保留经典 RAG 指标：

- `Recall@K`
- `Precision@K`
- `Hit@K`
- `MRR`
- `nDCG@K`

但要注意，这个项目里的“相关”不要只定义成“语义相似”，而要至少分成：

- 强相关
  能直接支持测试点生成
- 中相关
  有背景帮助，但不能直接生成测试点
- 弱相关 / 噪声
  主题接近但没有真正测试价值

这样 `nDCG` 才有意义。

### 11.2 业务化检索指标

这一层是这个项目比普通 RAG 更需要的。

建议额外增加：

- `Rule Recall@K`
  关键规则有没有被召回
- `Edge-case Recall@K`
  边界和异常规则有没有被召回
- `Golden Case Hit@K`
  高质量历史案例有没有命中
- `Constraint Coverage`
  当前 PRD 里的关键约束，被召回内容覆盖了多少
- `Noise Rate@K`
  前 K 条里无关噪声占比多少

这些指标会比单纯 Precision 更贴近你的真实目标，因为你关心的不只是“相关”，而是：

- 关键规则在不在
- 异常场景有没有进来
- 高质量样本有没有被看到

### 11.3 Rerank 层指标

这层回答的是：

- rerank 到底有没有把好内容排前
- 有没有把真正有用的规则和案例压掉

建议同时看：

- `Recall@20 before rerank`
- `Precision@5 before rerank`
- `nDCG@10 before rerank`
- `Noise Rate@10 before rerank`

和：

- `Recall@20 after rerank`
- `Precision@5 after rerank`
- `nDCG@10 after rerank`
- `Noise Rate@10 after rerank`

你理想中应该看到的是：

- rerank 前：召回较广，但噪声大
- rerank 后：前几条更准，规则命中更集中

### 11.4 最终生成收益指标

这是最重要但最容易被忽略的一层。

因为这个项目不是“检索即答案”，而是“检索服务于测试用例生成”。

所以最后要看：

- `Case Coverage Gain`
  加 RAG 后覆盖率有没有提升
- `Edge-case Gain`
  加 RAG 后边界和异常场景有没有更多
- `Compliance Gain`
  加 RAG 后结果是否更符合规范
- `Human Acceptance Rate`
  人工采纳率有没有提升
- `Evaluator Score Gain`
  evaluator 分数有没有提升

也就是说，后面最好做 A/B：

- 不加 RAG
- 只加语义检索
- 混合检索
- 混合检索 + rerank

最后比较输出质量，而不是只比较检索分数。

### 11.5 第一版最值得先落的指标

如果你不想一开始做太重，我建议先落这 6 个：

- `Recall@20`
- `Precision@5`
- `nDCG@10`
- `Rule Recall@10`
- `Noise Rate@10`
- `Human Acceptance Rate`

这 6 个已经能比较完整地回答：

- 找没找到
- 排得好不好
- 关键规则丢没丢
- 噪声多不多
- 最后有没有真的帮到生成

## 十二、Bad Case 应该怎么处理

这个问题非常关键。  
如果系统只统计平均指标，不看 bad-case，就会出现一个典型问题：

- 平均分不错
- 但用户仍然会遇到一些很痛的错误

所以 bad-case 不应该只是日志，而应该是一种可管理资产。

### 12.1 先定义什么叫 bad-case

建议至少分成五类：

1. `retrieval_bad_case`
   该召回的没召回，或者召回了大量噪声
2. `rerank_bad_case`
   好内容被压后，坏内容排前
3. `generation_bad_case`
   漏测、幻觉、结构损坏、格式错误
4. `evaluation_bad_case`
   evaluator 误判
5. `workflow_bad_case`
   文件解析、状态传递、上下文拼接、导出等流程问题

这样做的好处是：  
坏例不是一个抽象概念，而是能定位到层。

### 12.2 bad-case 应该记录哪些字段

建议每条 bad-case 至少记录：

- `case_id`
- `bad_case_type`
- `severity`
- `query_summary`
- `expected_behavior`
- `actual_behavior`
- `retrieved_context`
- `retrieved_candidates`
- `final_output`
- `evaluator_report`
- `user_feedback`
- `root_cause_guess`
- `status`
- `created_at`
- `updated_at`

状态建议：

- `new`
- `triaging`
- `confirmed`
- `fixed`
- `won't_fix`

严重度建议：

- `P0`
  严重误导，直接影响结果可用性
- `P1`
  结果明显不完整，需要人工大改
- `P2`
  局部问题，可以接受但值得优化

### 12.3 bad-case 不只是“失败样本”，还应该是回归资产

建议每个 bad-case 最终可以流向三处：

1. 回归评测集
   以后改检索、改 rerank、改 Prompt 时都重新跑
2. 规则库
   高频错误转成新规则、新 Prompt、新过滤条件
3. 案例库
   保留 query、召回、输出、人工判断，作为未来分析材料

也就是说，bad-case 最终要进入系统学习闭环，而不是只在当下报警。

## 十三、前端 Bad Case Review Panel 怎么设计

你前面说“想在前端展示”，我非常赞同，而且我觉得这一步很有价值。

因为 bad-case 如果只在日志里，通常只对开发者有意义；  
但如果在前端可见、可分类、可标注，它就会变成产品和算法共同能用的质量面板。

### 13.1 最好单独做一个 Review Panel

建议在前端单独增加一个：

- `Bad Case Review`

可以是独立 tab，也可以是管理页。

不要把它埋在日志页里，因为它不是原始日志，而是质量审查工具。

### 13.2 前端最值得展示什么

不要只是把长文本摊开。  
前端最有价值的是“差异展示”和“链路定位”。

建议每条 bad-case 展示 4 个区块：

1. 输入
   PRD 摘要、用户目标、关键词
2. 检索
   召回了什么、漏了什么、噪声是什么
3. 生成
   输出了什么、缺了什么、结构是否损坏
4. 系统判断
   更像检索问题、rerank 问题、prompt 问题还是知识库问题

这会让你看到的不是“一堆原始数据”，而是一条完整出错链路。

### 13.3 前端最该强调的是“对比视图”

bad-case 审查最怕一件事：  
你只能看见结果，却看不清差异。

所以建议加下面几种对比视图：

- `expected vs actual retrieval`
- `expected test points vs generated test points`
- `must-have rules vs actually hit rules`
- `before rerank vs after rerank`
- `原始输出 vs 人工修订后输出`

这样你能一眼看出：

- 问题出在召回
- 还是出在排序
- 还是出在生成

### 13.4 一定要有人工快速标注按钮

这一步非常重要。

建议前端提供快捷动作：

- `标记为召回问题`
- `标记为排序问题`
- `标记为生成问题`
- `标记为评审问题`
- `加入回归测试集`
- `加入 golden bad-case`
- `标记已修复`

为什么这很重要：

- 你能持续积累坏例库
- 能慢慢形成真实回归集
- 能把“主观感觉不好”变成“有类型、有标签的问题”

### 13.5 建议系统自动给出 root cause guess

前端里最好让系统先自动猜一个原因，人工再确认。

例如：

- `missing_rule_recall`
- `wrong_rerank_priority`
- `prompt_under_specified`
- `history_case_noise`
- `json_format_failure`
- `evaluator_false_negative`

这个猜测不需要 100% 准，但它会极大提升 triage 速度。

### 13.6 最后让前端不只是“看”，还要能“回流”

建议从前端可以直接触发：

- 回写 bad-case 标签
- 回写 root cause
- 回写人工修正结果
- 加入回归集
- 加入模板候选

这样你的前端就不是观察台，而是质量运营入口。

## 十四、把 bad-case 和前面改造点连起来

如果把前面整套改造连起来看，会形成一个很完整的闭环：

1. 长文本先稳定索引
2. 混合检索提高召回
3. rerank 提高前列质量
4. evaluator 评估输出质量
5. bad-case 面板发现典型错误
6. 人工标注错误类型
7. 回流到规则、检索、模板和回归集

这才是真正的“测试 Agent 质量系统”。

## 十五、一句话总结

这个项目后续如果要做成熟，不应该只有“生成能力增强”，还应该补齐下面三件事：

- 有指标，知道系统好不好
- 有 bad-case 面板，知道坏在哪里
- 有回归闭环，知道以后能不能更好

## 十六、结合之前沉淀项目，还能借什么亮点

这部分很重要。  
一个项目往前改，最怕两种情况：

1. 只盯着自己当前代码修修补补
2. 看到别的项目亮点就全搬进来

更合理的方式是：

> 看清这个测试 Agent 当前缺什么，再去借别的项目里正好成熟的那一层。

下面我按“可借鉴亮点 -> 为什么适合 -> 该怎么借 -> 不该怎么硬搬”来讲。

### 16.1 从 `career-ops` 借：把 workflow 做成真正的业务生产线

`career-ops` 最值得借的不是某个模型技巧，而是：

- workflow 编排意识很强
- prompt 不只是提示，而是领域作业规范
- 数据合同意识清楚
- worker 并行处理很务实

这对当前项目特别有帮助，因为这个项目虽然已经有：

- 文档接入
- RAG
- 生成
- 微调
- 评估
- 归档

但这些环节还偏“串起来能跑”，离“业务生产线”还有距离。

#### 可以借什么

1. 数据合同
   把生成、评估、归档、坏例回流都变成清晰 schema
2. 任务分段
   明确每个阶段的输入、输出、失败状态
3. worker 化批处理
   以后如果一次要处理多个 PRD 或多个模块，可以并行处理

#### 为什么适合

因为测试生成天然不是一次性问答，而是重复性很高的业务流水线。

#### 不要硬搬什么

不要为了模仿 `career-ops` 就一上来重做复杂多 worker 系统。  
对这个项目来说，最先借的是：

- workflow 切段
- 数据合同
- 阶段职责清晰

而不是先追求大规模并行。

### 16.2 从 `fault-diagnosis` 借：证据链、报告化输出、过程可见性

`fault-diagnosis` 特别值得借的是：

- tool/workflow 很贴近业务动作
- 过程可见
- 报告和证据是一级产物
- 用户能看到系统“怎么得出结论”

这对当前项目很有启发，因为测试 Agent 未来如果只输出 JSON，其实还不够。

#### 可以借什么

1. 证据展示
   在前端明确展示“哪些规则、哪些历史案例影响了这次生成”
2. 过程透明
   检索、rerank、评估、bad-case 识别可以有阶段状态可见
3. 报告化产物
   不只是导出 JSON，而是输出“测试设计说明 + 规则依据 + 质量评估摘要”

#### 为什么适合

因为测试团队很多时候不只关心结果，还关心：

- 这个测试点是怎么来的
- 它依据了哪些规范
- 为什么系统说这里漏测

#### 不要硬搬什么

不要把工业诊断里的重工具链全部照搬。  
这个项目更适合借“证据透明”和“报告化交付”，不需要借整套工业数据工具层。

### 16.3 从 `repomind` 借：verification-first、缓存层次、坏例验证闭环

`repomind` 最值得借的是：

- verification-first 思路
- 不是只生成 finding，而是验证 finding
- 有更清楚的缓存层次
- 结果会进入验证记录和生命周期管理

这对当前项目非常有价值，因为你现在已经开始思考：

- rerank 指标
- bad-case
- 前端 review panel

这本质上已经是在走 verification-first 路线了。

#### 可以借什么

1. verification-first 思路
   不只是“生成了什么”，而是“这次生成依据是否充分、质量是否验证过”
2. bad-case 生命周期
   `new -> triaging -> confirmed -> fixed`
3. 分层缓存
   query 级、候选级、最终上下文级缓存
4. 回归验证集
   每次升级检索和 rerank 都跑固定回归样本

#### 为什么适合

因为测试 Agent 跟安全扫描有一个共通点：

- 都不能只靠第一次生成结果
- 都需要降低误判和漏判
- 都需要长期维护“哪些问题经常错”

#### 不要硬搬什么

不要把 `repomind` 的 GitHub/CAG/安全扫描实现细节搬进来。  
真正该借的是：

- verification-first 思路
- bad-case 生命周期
- 回归验证文化

### 16.4 从 `deer-flow` 借：分层、可插拔能力、异步记忆更新

`deer-flow` 最大的亮点是：

- runtime 和 app 明确拆层
- middleware-first
- skill / MCP / tool 是统一扩展生态
- memory 是结构化且异步更新的

当前项目虽然不用直接长成 super-agent harness，但其中有几层思想非常值得借。

#### 可以借什么

1. app 和能力层拆开
   这正好对应我们前面说的 `ui + services + core + stores`
2. 插件化接入能力
   未来接 Jira、TestRail、企业知识库、规则词表时，不要都写死在核心流程里
3. 异步 memory 更新
   高质量案例抽模板、bad-case 回流、反馈统计，不必每轮同步阻塞主流程

#### 为什么适合

因为这个项目后面一旦越做越大，最容易出问题的不是模型，而是：

- 接入越来越多
- 逻辑越来越散
- 主流程越来越慢

#### 不要硬搬什么

不要为了“显得高级”就上完整 middleware runtime、sandbox、subagent 体系。  
现在最适合借的是：

- 分层
- 可插拔
- 异步记忆更新

### 16.5 从 `claude-code-sourcemap` 借：时间尺度分层的 workflow 治理

`claude-code-sourcemap` 最值得借的不是 coding tool 本身，而是它对 workflow 的理解：

- 单轮 query loop
- 会话级治理
- compact / reinjection
- 长时间尺度的状态管理

这对当前项目的启发在于：

> workflow 不是一张流程图，而是多时间尺度的治理系统。

#### 可以借什么

1. 把流程按时间尺度分层
   单轮生成、一次会话、多轮资产积累要分开设计
2. 状态治理
   不要把所有状态都塞在前端 session 里
3. 长流程收敛
   如果以后会话变长，要考虑上下文压缩和关键状态 reinjection

#### 为什么适合

因为当前项目一旦从“单次 PRD”扩展到：

- 多轮修改
- 多人协作
- 多版本用例演化

就会立刻遇到状态治理问题。

#### 不要硬搬什么

不要试图把完整 query loop runtime 搬过来。  
当前项目更适合借的是它对“workflow 时间尺度分层”的思考方式。

### 16.6 从 `claude-code` 借：平台演进意识、feature flag、可控上线

`claude-code` 最值得借的是平台意识：

- feature flags
- runtime gating
- 新功能灰度
- 高风险能力可快速关停

这个项目现在看起来还像单一产品，但一旦你后面加：

- hybrid retrieval
- rerank
- bad-case 面板
- 模板抽取
- 自动脚本生成

系统复杂度会迅速升高。

#### 可以借什么

1. feature flag
   新检索策略、新 rerank、新 evaluator 规则可以独立开关
2. 分版本灰度
   对一部分 query 或一部分用户先启用新策略
3. 可观测性
   每个 feature 的效果和代价单独看

#### 为什么适合

因为检索和生成系统最怕的是：

- 一次改很多
- 结果变差却不知道是哪一层导致的

有 feature flag 之后，你就能更稳地实验。

#### 不要硬搬什么

不需要把 `claude-code` 那种完整平台能力全搬进来。  
最先该借的其实只有三件事：

- feature flag
- 灰度发布
- 可观测性

## 十七、如果把这些亮点汇总成一张“借鉴地图”

如果我把这些项目的亮点压成一句话，会是这样：

- `career-ops`
  借 workflow 编排和数据合同
- `fault-diagnosis`
  借证据链展示和报告化交付
- `repomind`
  借 verification-first 和 bad-case 生命周期
- `deer-flow`
  借分层、可插拔能力、异步记忆更新
- `claude-code-sourcemap`
  借时间尺度分层的 workflow 治理
- `claude-code`
  借 feature flag、灰度和平台演进意识

## 十八、最适合当前项目的组合方案

如果只让我给这个项目挑一套最现实、最值得落地的组合，我会选：

1. 从 `career-ops` 借 workflow 和数据合同
2. 从 `fault-diagnosis` 借证据展示和报告化产物
3. 从 `repomind` 借 verification-first 和 bad-case 回归
4. 从 `deer-flow` 借分层和异步记忆更新
5. 从 `claude-code` 借 feature flag 做灰度

这五个组合起来，已经足够让这个项目从：

- 一个好用的测试生成工作台

升级成：

- 一个更稳、更可解释、更可验证、更可持续演进的测试知识系统

## 十九、数据结构版：核心 schema 应该怎么设计

前面讲了很多架构和流程，这里把它们往工程实现再推一步。  
如果后面你真的要落地，最先该稳定下来的其实是数据结构。

因为一旦 schema 不清楚，后面这些能力都会变得很散：

- 检索
- rerank
- 评估
- bad-case
- 回归测试
- 模板沉淀

### 19.1 Document Chunk Schema

这是知识库和案例库里最基础的索引单元。

建议至少包含：

```json
{
  "chunk_id": "doc_xxx_chunk_01",
  "doc_id": "doc_xxx",
  "source_type": "spec",
  "source_name": "login_spec_v3.pdf",
  "business_domain": "auth",
  "module": "login",
  "content": "...",
  "summary": "...",
  "business_keywords": ["登录", "密码", "验证码"],
  "logic_keywords": ["必须", "至少", "失败", "锁定"],
  "constraints": [
    "密码长度至少8位",
    "连续失败5次锁定30分钟"
  ],
  "quality_tag": "reviewed",
  "status": "active",
  "version": "v3",
  "created_at": "2026-04-12T10:00:00Z"
}
```

动机：

- 让 chunk 不只是文本片段，还带业务意义和规则意义

解决的问题：

- 纯语义检索看不出“这段是不是规则”
- rerank 没有可用特征

借鉴来源：

- 当前项目已有 `company_knowledge` / `history_cases` 双集合思路
- `fault-diagnosis` 的证据拼接意识
- `repomind` 的“检索对象要有可验证结构”

### 19.2 Retrieval Candidate Schema

这是进入 rerank 之前的候选统一结构。

```json
{
  "candidate_id": "cand_001",
  "chunk_id": "doc_xxx_chunk_01",
  "source_type": "spec",
  "semantic_score": 0.82,
  "keyword_score": 0.64,
  "matched_business_keywords": ["登录", "密码"],
  "matched_logic_keywords": ["必须", "至少"],
  "metadata_match": {
    "business_domain": true,
    "module": true,
    "status": true
  },
  "chunk_summary": "...",
  "content_preview": "..."
}
```

动机：

- 把语义检索和关键词检索结果放进同一张表里比较

解决的问题：

- 两路召回结果难以统一排序

借鉴来源：

- `repomind` 的 verification / state record 思路
- 我们前面设计的 hybrid retrieval

### 19.3 Rerank Score Schema

rerank 不应该只是输出一个分数，最好保留维度明细。

```json
{
  "candidate_id": "cand_001",
  "final_score": 0.86,
  "score_breakdown": {
    "query_relevance": 0.90,
    "module_match": 0.95,
    "testcase_usefulness": 0.88,
    "rule_strength": 0.80,
    "edge_case_density": 0.72,
    "source_authority": 0.92,
    "version_freshness": 0.85,
    "human_acceptance": 0.60
  },
  "reason_tags": [
    "same_module",
    "contains_constraints",
    "contains_edge_case_rule"
  ]
}
```

动机：

- 以后 bad-case 面板里可以解释“为什么这条排前面”

解决的问题：

- rerank 是黑盒，前端很难解释

借鉴来源：

- `fault-diagnosis` 的过程可见性
- `repomind` 的 verification-first 和记录意识

### 19.4 Generation Result Schema

测试用例生成结果建议不要只存原始 JSON，还要带版本和质量上下文。

```json
{
  "generation_id": "gen_001",
  "query_id": "query_001",
  "prd_summary": "...",
  "retrieval_context_ids": ["chunk_1", "chunk_8"],
  "model_config": {
    "provider": "qwen",
    "model": "qwen-plus"
  },
  "cases": [],
  "explanation": "...",
  "generated_at": "2026-04-12T10:00:00Z",
  "edited_after_generation": true,
  "finalized": false
}
```

动机：

- 让生成结果可追踪，不是一次性文本

解决的问题：

- 无法回看“这次结果到底受了哪些上下文影响”

借鉴来源：

- 当前项目已有“解释 + JSON 分离”的好思路
- `career-ops` 的数据合同意识

### 19.5 Evaluation Result Schema

```json
{
  "evaluation_id": "eval_001",
  "generation_id": "gen_001",
  "score_total": 84,
  "score_breakdown": {
    "coverage_score": 82,
    "logic_score": 88,
    "dedup_score": 90,
    "compliance_score": 76,
    "risk_score": 80
  },
  "coverage_gaps": [
    "未覆盖密码为空场景"
  ],
  "logic_issues": [],
  "duplicates": [],
  "suggestions": [
    "增加连续失败锁定场景"
  ],
  "template_worthy": false
}
```

动机：

- evaluator 结果以后不仅给人看，还要给系统回写

解决的问题：

- 评估结果无法被统计、模板化、规则化

借鉴来源：

- 当前项目已有 evaluator 基础
- `repomind` 的 verification record 思路

### 19.6 Bad Case Schema

```json
{
  "bad_case_id": "bad_001",
  "query_id": "query_001",
  "bad_case_type": "rerank_bad_case",
  "severity": "P1",
  "status": "triaging",
  "query_summary": "...",
  "expected_behavior": "高质量登录规则应排在前3",
  "actual_behavior": "背景说明排在前3，关键规则排在第9",
  "retrieved_candidates": [],
  "final_generation_id": "gen_001",
  "evaluation_id": "eval_001",
  "root_cause_guess": "wrong_rerank_priority",
  "user_feedback": "遗漏关键锁定规则",
  "created_at": "2026-04-12T10:00:00Z",
  "updated_at": "2026-04-12T10:30:00Z"
}
```

动机：

- 把坏例从“日志”升级成“可运营质量资产”

解决的问题：

- 系统知道错了，但不知道错因和后续如何回归

借鉴来源：

- `repomind` 的 verification lifecycle
- 你前面提出的前端可审查 bad-case 面板想法

### 19.7 Regression Benchmark Schema

```json
{
  "benchmark_id": "bench_001",
  "name": "login_rules_regression",
  "query_input": "...",
  "expected_rules": [
    "密码长度至少8位",
    "连续失败5次锁定30分钟"
  ],
  "expected_case_points": [
    "密码为空",
    "密码过短",
    "连续失败锁定"
  ],
  "golden_chunks": ["chunk_1", "chunk_2"],
  "golden_cases": ["case_1"],
  "difficulty": "medium"
}
```

动机：

- 让每次改检索和 rerank 都能回归

解决的问题：

- 系统升级全靠主观感觉

借鉴来源：

- `repomind` 的 verification-first
- `claude-code` 的 feature 灰度和可观测性思路

## 二十、直接给你一个“改进后的版本”长什么样

这一节不是讲抽象原则，而是直接描述：

> 如果把上面的改造大体做完，这个项目会变成什么样。

你可以把它理解成一个目标版本蓝图。

### 20.1 用户看到的前端会是什么样

改进后，前端不再只是“上传文件 + 出 JSON + 下载”。

更完整的产品工作台会有五个主区：

1. `Input / Ingestion`
   上传 PRD、PDF、图片、补充文档，看到解析状态和结构摘要
2. `Retrieval / Evidence`
   展示召回结果、关键词命中、规则命中、rerank 结果、证据来源
3. `Generation Workspace`
   左侧解释，右侧结构化测试用例，可继续微调
4. `Evaluation / Quality`
   展示质量评分、漏测点、合规性和建议
5. `Bad Case / Regression Review`
   审查坏例、标注根因、加入回归集

动机：

- 让系统不只是生成器，而是完整测试设计工作台

解决的问题：

- 当前产品侧过于聚焦单次生成，缺少质量运营面

借鉴来源：

- 当前项目已有左右双区共创基础
- `fault-diagnosis` 的证据和过程透明
- `repomind` 的验证闭环意识

### 20.2 系统内部 workflow 会是什么样

改进后的主流程会更像这样：

1. 文档接入与结构提取
2. hybrid retrieval
3. rerank
4. 上下文组装
5. 测试用例生成
6. 人工微调
7. AI 评估
8. bad-case 检测与标注
9. 高质量结果归档为案例或模板
10. 进入回归基准集

动机：

- 把“生成一次”升级成“长期能积累质量和知识”的系统

解决的问题：

- 当前结果虽然能回流，但还没形成强闭环

借鉴来源：

- `career-ops` 的 workflow-first
- `repomind` 的 verification-first
- `deer-flow` 的分层与异步更新

### 20.3 内部架构会是什么样

改进后的系统不再是 UI 主导一切，而是：

- `ui/`
  产品交互层
- `services/`
  工作流编排层
- `core/`
  检索、rerank、生成、评估核心能力
- `stores/`
  文档、案例、bad-case、benchmark 持久化层

动机：

- 让系统可维护、可替换、可扩展

解决的问题：

- 当前 `ui/main.py` 过重

借鉴来源：

- `deer-flow` 的 app / runtime 拆层
- 我们前面给出的 service 化改造方案

### 20.4 检索层会是什么样

改进后的检索不是“向量查一下再过滤”这么简单，而是：

1. query understanding
2. semantic retrieval
3. keyword retrieval
4. candidate normalization
5. rerank
6. context assembly

并且前端能看到：

- 命中了哪些业务关键词
- 命中了哪些逻辑规则词
- 哪些规范文档被优先使用
- 哪些历史案例被纳入上下文

动机：

- 让检索从“黑箱”变成“可解释证据层”

解决的问题：

- 现在你很难判断检索是查到了、没查到，还是查到了但没排好

借鉴来源：

- 当前项目的 RAG 雏形
- `fault-diagnosis` 的证据展示思路
- `repomind` 的 verification-first

### 20.5 记忆层会是什么样

改进后会把 memory 分成三层：

1. session memory
   当前会话状态
2. case memory
   历史高价值案例
3. learning memory
   模板、规则、坏例模式、人工反馈

其中：

- session memory 同步走
- case / learning memory 异步更新

动机：

- 避免所有沉淀动作拖慢主流程

解决的问题：

- 当前只有会话状态和简单回流，没有真正学习层

借鉴来源：

- `fault-diagnosis` 的 session memory 边界意识
- `deer-flow` 的异步结构化 memory 更新
- `claude-code` 的团队知识资产方向

### 20.6 质量层会是什么样

改进后质量系统会有三类核心对象：

1. `metrics`
   指标面板
2. `bad_cases`
   坏例审查与生命周期
3. `benchmarks`
   回归测试集

这三者会互相联动：

- 指标发现波动
- 坏例定位问题
- benchmark 验证修复是否有效

动机：

- 让系统从“感觉迭代”变成“证据驱动迭代”

解决的问题：

- 当前缺少系统化质量运营手段

借鉴来源：

- `repomind` 的 verification-first 和结果生命周期
- `claude-code` 的可观测性和 feature 管理意识

## 二十一、每个关键改进点的动机、借鉴来源与解决问题

这一节我给你做成一张“设计决策表”，方便你以后直接复盘。

### 21.1 Service 化编排

- 改进思路：
  把 UI 编排拆到 service 层
- 动机：
  让流程可测试、可复用、可 API 化
- 解决的问题：
  `ui/main.py` 过重、前后端耦合、后续难扩展
- 借鉴来源：
  `deer-flow` 的 app/runtime 分层

### 21.2 Hybrid Retrieval

- 改进思路：
  语义检索 + 关键词检索
- 动机：
  测试生成不只靠语义，还依赖规则词、边界词、业务术语
- 解决的问题：
  纯语义检索容易错过关键规则
- 借鉴来源：
  当前项目的 RAG 基础 + 我们对测试场景规则性的判断

### 21.3 Rerank 多维打分

- 改进思路：
  从相关性、测试价值、可信度三层打分
- 动机：
  “相关”不等于“适合生成测试用例”
- 解决的问题：
  好内容召回到了但没排前面
- 借鉴来源：
  `repomind` 的 verification-first 思路

### 21.4 证据展示层

- 改进思路：
  前端展示召回依据、规则命中、来源文档
- 动机：
  用户需要知道结果怎么来的
- 解决的问题：
  检索和生成过程太黑箱
- 借鉴来源：
  `fault-diagnosis`

### 21.5 Bad Case Review Panel

- 改进思路：
  前端可见、可标注、可回流的坏例面板
- 动机：
  平均指标好不代表没有痛点问题
- 解决的问题：
  系统只知道出错，不知道坏在哪里、该如何回归
- 借鉴来源：
  `repomind` 的 verification lifecycle

### 21.6 异步 memory / asset update

- 改进思路：
  高质量案例、模板、坏例模式异步沉淀
- 动机：
  不让主生成链路被沉淀流程拖慢
- 解决的问题：
  记忆层和主流程耦合，后期会变慢
- 借鉴来源：
  `deer-flow`

### 21.7 Workflow 数据合同

- 改进思路：
  generation、evaluation、bad-case、benchmark 都有明确 schema
- 动机：
  让多阶段流水线稳定
- 解决的问题：
  阶段之间输入输出容易混乱
- 借鉴来源：
  `career-ops`

### 21.8 Feature Flag 与灰度

- 改进思路：
  hybrid retrieval、rerank、评估策略等都可独立开关
- 动机：
  让新策略可以安全试验
- 解决的问题：
  一次改很多时难定位回退
- 借鉴来源：
  `claude-code`

## 二十二、一句话看懂“改进后版本”

如果把这个项目的改进后版本压缩成一句话，我会这样说：

> 它会从一个“基于 Prompt 和本地 RAG 的测试用例生成工作台”，升级成一个“有证据层、有混合检索、有 rerank、有质量评测、有 bad-case 面板、有回归闭环、能持续沉淀测试知识资产的测试 Agent 系统”。
