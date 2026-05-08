# ByteDance--Auto_prd_test_agent 实施草图

## Summary

- Project name: ByteDance--Auto_prd_test_agent
- Project path: `D:\测开\ByteDance--Auto_prd_test_agent`
- Document type: user
- Purpose: translate the target architecture and upgrade plan into a practical first implementation sketch, including module boundaries, interface ideas, workflow pseudocode, rollout phases, and the design inspirations behind each major choice

## 一、这份文档是干什么的

前面的几份文档分别回答了：

- 这个项目现在是什么
- 它应该往哪里改
- 技术上应该补哪些层
- 改完后的整体架构长什么样

这一份再往前走一步，回答的是：

> 如果现在真的开始动手改，第一版应该怎么落。

也就是说，这份文档不再主要讲“原则”，而是讲：

- 模块怎么拆
- 接口怎么定
- 主流程怎么跑
- 先做什么后做什么
- 每一步借鉴了哪个历史项目

## 二、第一版目标不要定太大

如果一下子把前面说的所有能力全做进去，项目会很容易失控。

所以我建议第一版改造只盯住 5 个目标：

1. 把 UI 中的主流程拆到 service 层
2. 补上 hybrid retrieval
3. 补上可解释 rerank
4. 补上 bad-case 基础记录和前端 review
5. 补上最小回归验证集

这 5 个目标已经足够让项目从：

- 可用 Demo

升级成：

- 初步可维护、可验证、可持续迭代的测试 Agent 系统

## 三、建议的第一版目录结构

```text
ui/
  main.py
  sidebar.py
  components.py
  pages/
    retrieval_review.py
    bad_case_review.py

services/
  ingestion_service.py
  retrieval_service.py
  generation_service.py
  evaluation_service.py
  badcase_service.py
  benchmark_service.py

core/
  llm_client.py
  rag_engine.py
  reranker.py
  keyword_extractor.py
  prompt_builder.py
  evaluator.py
  schemas.py

stores/
  vector_store.py
  case_store.py
  badcase_store.py
  benchmark_store.py
  metrics_store.py
```

### 这样拆的动机

- `ui/`
  只负责产品界面
- `services/`
  负责把多步流程串起来
- `core/`
  放通用能力
- `stores/`
  负责持久化

### 解决的问题

- 现在 `ui/main.py` 过重
- 逻辑难测试
- 后续扩展困难

### 借鉴来源

- `deer-flow`
  借 app 和 runtime/能力拆层
- `career-ops`
  借 workflow-first 和阶段职责清晰

## 四、第一版核心模块怎么定义

### 1. `ingestion_service.py`

负责：

- 接收上传文件
- 解析文本
- 抽文档结构
- 抽业务关键词和逻辑关键词
- 产出标准化输入对象

建议接口：

```python
def ingest_files(files: list, options: dict) -> IngestionResult:
    ...
```

返回对象示意：

```python
{
  "documents": [...],
  "merged_prd_text": "...",
  "business_keywords": [...],
  "logic_keywords": [...],
  "structure_outline": [...],
  "ingestion_warnings": [...]
}
```

#### 动机

- 让接入层独立，不跟检索和生成耦合

#### 借鉴来源

- 当前项目已有多模态解析基础
- `fault-diagnosis`
  借“接入后形成后续可用作业输入”的思路

### 2. `retrieval_service.py`

负责：

- query understanding
- semantic retrieval
- keyword retrieval
- 候选归一化
- 调用 reranker
- 组装 evidence context

建议接口：

```python
def retrieve_context(ingestion_result: IngestionResult, options: dict) -> RetrievalResult:
    ...
```

返回对象示意：

```python
{
  "semantic_candidates": [...],
  "keyword_candidates": [...],
  "reranked_candidates": [...],
  "evidence_context": {
    "rule_chunks": [...],
    "history_case_chunks": [...],
    "supporting_chunks": [...]
  },
  "retrieval_metrics_preview": {...}
}
```

#### 动机

- 让“查什么”和“怎么给模型”分开

#### 借鉴来源

- `repomind`
  借 verification-first 和候选组织意识
- `fault-diagnosis`
  借多来源证据拼接

### 3. `reranker.py`

负责：

- 对候选做多维打分
- 输出最终排序和分数明细

建议接口：

```python
def rerank_candidates(query_pack: dict, candidates: list) -> list:
    ...
```

每条输出包含：

- `final_score`
- `score_breakdown`
- `reason_tags`

#### 动机

- 让排序结果能解释

#### 借鉴来源

- `repomind`
  借“不要只输出结论，要能追溯原因”
- `fault-diagnosis`
  借过程透明意识

### 4. `generation_service.py`

负责：

- 构建 generation prompt
- 调主模型生成
- 解析解释和 JSON
- 记录生成版本

建议接口：

```python
def generate_cases(input_pack: dict) -> GenerationResult:
    ...

def refine_cases(input_pack: dict, user_instruction: str) -> GenerationResult:
    ...
```

#### 动机

- 把生成和微调从 UI 中抽出来

#### 借鉴来源

- 当前项目已有共创工作台设计
- `career-ops`
  借阶段化工作流思路

### 5. `evaluation_service.py`

负责：

- 调 evaluator
- 产出用户可读评分
- 产出系统可写回结构

建议接口：

```python
def evaluate_generation(input_pack: dict) -> EvaluationResult:
    ...
```

#### 动机

- evaluator 不只是给用户看，要给系统写回

#### 借鉴来源

- 当前项目已有 evaluator
- `repomind`
  借 verification record 意识

### 6. `badcase_service.py`

负责：

- 检测是否构成 bad-case
- 生成 root cause guess
- 写入坏例库
- 支持前端审查动作

建议接口：

```python
def detect_bad_case(run_pack: dict) -> BadCase | None:
    ...

def update_bad_case(bad_case_id: str, action: dict) -> BadCase:
    ...
```

#### 动机

- 坏例不能只在日志里

#### 借鉴来源

- `repomind`
  借 verification lifecycle

### 7. `benchmark_service.py`

负责：

- 跑回归 benchmark
- 计算指标
- 比较不同 feature flag 下结果

建议接口：

```python
def run_benchmark_suite(name: str, config: dict) -> BenchmarkRunResult:
    ...
```

#### 动机

- 每次改检索和 rerank 要知道有没有真提升

#### 借鉴来源

- `repomind`
  借回归验证文化
- `claude-code`
  借实验治理意识

## 五、第一版主流程伪代码

### 1. 生成主流程

```python
def run_generation_workflow(files, user_options):
    ingestion_result = ingest_files(files, user_options)

    retrieval_result = retrieve_context(ingestion_result, user_options)

    generation_input = {
        "prd_text": ingestion_result["merged_prd_text"],
        "keywords": {
            "business": ingestion_result["business_keywords"],
            "logic": ingestion_result["logic_keywords"],
        },
        "evidence_context": retrieval_result["evidence_context"],
        "retrieval_trace": retrieval_result["reranked_candidates"][:10],
    }

    generation_result = generate_cases(generation_input)

    evaluation_input = {
        "generation_result": generation_result,
        "evidence_context": retrieval_result["evidence_context"],
        "prd_text": ingestion_result["merged_prd_text"],
    }

    evaluation_result = evaluate_generation(evaluation_input)

    bad_case = detect_bad_case({
        "ingestion_result": ingestion_result,
        "retrieval_result": retrieval_result,
        "generation_result": generation_result,
        "evaluation_result": evaluation_result,
    })

    return {
        "ingestion_result": ingestion_result,
        "retrieval_result": retrieval_result,
        "generation_result": generation_result,
        "evaluation_result": evaluation_result,
        "bad_case": bad_case,
    }
```

### 2. 微调主流程

```python
def run_refinement_workflow(current_run, user_instruction):
    refined_result = refine_cases(
        input_pack={
            "current_generation": current_run["generation_result"],
            "evidence_context": current_run["retrieval_result"]["evidence_context"],
            "prd_text": current_run["ingestion_result"]["merged_prd_text"],
        },
        user_instruction=user_instruction,
    )

    evaluation_result = evaluate_generation({
        "generation_result": refined_result,
        "evidence_context": current_run["retrieval_result"]["evidence_context"],
        "prd_text": current_run["ingestion_result"]["merged_prd_text"],
    })

    bad_case = detect_bad_case({
        "ingestion_result": current_run["ingestion_result"],
        "retrieval_result": current_run["retrieval_result"],
        "generation_result": refined_result,
        "evaluation_result": evaluation_result,
    })

    return {
        **current_run,
        "generation_result": refined_result,
        "evaluation_result": evaluation_result,
        "bad_case": bad_case,
    }
```

### 3. 为什么这样排

因为它对应的是一条很清楚的业务逻辑：

- 先理解输入
- 再找证据
- 再生成
- 再评估
- 再识别坏例

### 4. 借鉴来源

- `career-ops`
  workflow-first
- `repomind`
  verification-first

## 六、长文本索引的第一版落地策略

### 1. 推荐落地顺序

先不要一开始就上复杂 Agent 索引器。  
第一版建议按这四层：

1. 正常递归切片
2. 固定窗口硬切
3. 章节结构切片
4. LLM/Agent 兜底

### 2. 可落地伪代码

```python
def build_chunks(text, structure_hint=None):
    chunks = recursive_split(text)
    if is_chunk_quality_ok(chunks):
        return chunks

    chunks = fixed_window_split(text)
    if is_chunk_quality_ok(chunks):
        return chunks

    if structure_hint:
        chunks = structure_aware_split(text, structure_hint)
        if is_chunk_quality_ok(chunks):
            return chunks

    return llm_guided_split(text)
```

### 3. 为什么 Agent 不该一开始就全量上

- 成本高
- 慢
- 批量化差
- 输出不稳定

### 4. 借鉴来源

- 来自我们这次对当前项目索引兜底的讨论
- 也借了 `deer-flow` 那种“高级能力作为增强层，而不是默认层”的思路

## 七、关键词检索第一版怎么做最稳

### 1. 不要一开始做太复杂

第一版关键词检索建议只做：

- 业务关键词字典
- 逻辑关键词字典
- 文档入库时关键词抽取
- BM25 或轻量倒排匹配

### 2. query 侧流程

```python
def extract_query_keywords(prd_text):
    business_keywords = extract_business_terms(prd_text)
    logic_keywords = extract_logic_terms(prd_text)
    return {
        "business_keywords": business_keywords,
        "logic_keywords": logic_keywords,
    }
```

### 3. document 侧流程

```python
def enrich_chunk_metadata(chunk_text):
    return {
        "business_keywords": extract_business_terms(chunk_text),
        "logic_keywords": extract_logic_terms(chunk_text),
        "constraints": extract_constraints(chunk_text),
    }
```

### 4. 为什么这样够用

因为第一版目标不是做最强搜索引擎，而是先把：

- 规则词
- 边界词
- 业务术语

接进召回逻辑。

### 5. 借鉴来源

- 来自当前项目测试生成任务本身的规则性特点
- 也吸收了 `fault-diagnosis` 那种“规则证据比聊天自然度更重要”的思路

## 八、第一版 rerank 最小落地方案

### 1. 最小维度集

第一版建议只上 5 个维度：

- `query_relevance`
- `module_match`
- `testcase_usefulness`
- `rule_strength`
- `source_authority`

### 2. 为什么不一开始上 8 个

因为第一版最重要的是：

- 先把排序逻辑显式化
- 先做出前端可解释性

不是一开始就把模型打分体系做得很复杂。

### 3. 第一版公式

```text
final_score =
  0.35 * query_relevance +
  0.25 * module_match +
  0.20 * testcase_usefulness +
  0.10 * rule_strength +
  0.10 * source_authority
```

### 4. 后续再加什么

第二阶段再加：

- `edge_case_density`
- `version_freshness`
- `human_acceptance`

### 5. 借鉴来源

- 来自我们前面对“第一版不要太重”的判断
- 也借了 `claude-code` 那种 feature 渐进放量思路

## 九、Bad Case Review Panel 第一版怎么做

### 1. 第一版先做最有价值的部分

不要一开始就做成很复杂的质量平台。  
第一版先有这几个能力：

1. 查看 bad-case 列表
2. 查看每条的输入、召回、输出、评估
3. 快速标注类型
4. 加入回归集

### 2. 前端建议字段

- `bad_case_type`
- `severity`
- `query_summary`
- `root_cause_guess`
- `retrieval_snapshot`
- `generation_snapshot`
- `evaluation_snapshot`
- `status`

### 3. 最值得做的两个对比

- `before rerank vs after rerank`
- `expected rules vs generated rules`

### 4. 借鉴来源

- `repomind`
  借 verification 记录和生命周期
- `fault-diagnosis`
  借过程可见性

## 十、第一版回归 benchmark 怎么搭

### 1. 不需要一开始就很大

先建一个小规模 benchmark 集即可：

- 10 个高价值登录类 query
- 10 个支付/订单类 query
- 10 个异常/边界规则类 query

### 2. 每个 benchmark 样本至少包含

- 输入 query / PRD 摘要
- 期望规则
- 期望测试点
- 参考 chunks

### 3. 每次实验后对比

- `Recall@20`
- `Rule Recall@10`
- `Precision@5`
- `Human Acceptance Rate`

### 4. 借鉴来源

- `repomind`
  借 verification-first
- `claude-code`
  借实验治理

## 十一、Feature Flag 第一版怎么加

### 1. 建议至少加三个 flag

- `enable_keyword_retrieval`
- `enable_rerank_v2`
- `enable_bad_case_auto_detect`

### 2. 为什么这三个最值得先加

因为它们分别对应三种高变化能力：

- 检索变化
- 排序变化
- 质量诊断变化

### 3. 用法

在 service 层读配置，而不是写死在 UI 里。

```python
if feature_flags.enable_keyword_retrieval:
    keyword_candidates = keyword_search(...)
```

### 4. 借鉴来源

- `claude-code`

## 十二、建议的实施顺序

### Phase 1：结构重构

做什么：

- service 层拆分
- schema 定义
- UI 只保留交互

解决什么：

- 后面所有改造有落点

### Phase 2：检索升级

做什么：

- 关键词抽取
- hybrid retrieval
- 最小 rerank

解决什么：

- 检索更准、可解释

### Phase 3：质量系统

做什么：

- evaluator 写回
- bad-case review panel
- benchmark 集

解决什么：

- 质量可见、可回归

### Phase 4：长期资产

做什么：

- 高质量案例抽模板
- bad-case 模式沉淀
- learning memory 异步更新

解决什么：

- 系统开始积累长期组织知识

## 十三、如果只给开发团队一句开工建议

> 第一版不要想着把它做成最强 Agent 平台，而要先把它做成“有 service 层、有 hybrid retrieval、有可解释 rerank、有 bad-case review、有 benchmark 回归”的稳定测试知识工作台。
