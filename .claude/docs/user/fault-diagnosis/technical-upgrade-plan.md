# fault-diagnosis 下一阶段技术改造方案

## Summary

- Project name: fault-diagnosis
- Project path: `D:\fault-diagnosis`
- Document type: user
- Purpose: translate the roadmap into an implementation-oriented technical plan, including module-level changes, data structure proposals, knowledge/memory design, and a practical execution order

## 一、这份文档解决什么问题

前面的路线图已经回答了：

- 先补什么
- 为什么这样排优先级

这份文档继续往前走一步，回答的是：

- 具体怎么改
- 先动哪些模块
- 要增加什么数据结构
- memory、case library、RAG 分层怎么真正落地

也就是说，这不是再讲方向，而是开始讲“施工图”。

## 二、先明确改造目标

我建议下一阶段不要把目标写成“升级 Agent 能力”，而应该写成下面四条更工程化的目标：

### 目标 1：让工具执行链更稳

也就是解决：

- `globals()` 状态共享
- 多会话隔离
- 图表与数据分析链路脆弱

### 目标 2：让诊断结果变成可积累资产

也就是解决：

- 报告只是文件
- 历史案例无法结构化复用
- 系统不会从过去诊断中受益

### 目标 3：让知识层从“单一 FAISS 检索”升级成“分层证据系统”

也就是解决：

- 手册、故障码、案例知识混在一起
- 检索结果缺少明确知识类型边界

### 目标 4：让系统更像可运行服务，而不是仅能跑通的工程样例

也就是解决：

- 健康检查不足
- 依赖失败时行为不清晰
- 观测与审计能力不足

## 三、建议的改造阶段

我建议拆成四个阶段，而不是一次大重构。

### 阶段 A：执行状态重构

核心目标：

- 去掉高风险的跨工具全局共享状态

### 阶段 B：案例资产化

核心目标：

- 把报告和诊断结果转成结构化案例库

### 阶段 C：知识层重构

核心目标：

- 建立分层知识库和更清晰的证据召回路径

### 阶段 D：服务化与平台化底座

核心目标：

- 补运维、审计、依赖治理和后续平台扩展能力

这个顺序和前面的路线图是一致的，只是这里会具体落到文件和结构。

## 四、阶段 A：执行状态重构

### 1. 当前问题在哪里

当前最明显的问题点在：

- [`data_tools.py`](D:\fault-diagnosis\tools\data_tools.py)

这里的：

- `extract_data`
- `fig_inter`

通过 `globals()` 共享 DataFrame。

这类实现短期方便，但中长期会有几个问题：

- 多线程或多会话可能互相污染
- 中间状态无法按 `thread_id` 管理
- 无法清理过期数据
- 很难给图表链路做审计

### 2. 推荐的新结构

建议新增一个“会话运行时状态层”，例如：

- `runtime_state/`
  - `session_store.py`
  - `models.py`
  - `cleanup.py`

推荐的数据结构可以很简单：

```python
@dataclass
class SessionArtifactState:
    thread_id: str
    dataframes: dict[str, Any]
    generated_images: list[str]
    generated_reports: list[str]
    updated_at: datetime
```

然后把现在依赖 `globals()` 的地方改成：

- `extract_data` 把 DataFrame 写入当前 `thread_id` 的 session state
- `fig_inter` 从当前 `thread_id` 的 session state 取 DataFrame

### 3. 需要动哪些模块

建议优先修改：

- [`streaming.py`](D:\fault-diagnosis\streaming.py)
  这里已经有 `thread_id`，适合把会话上下文贯穿下去
- [`tools/data_tools.py`](D:\fault-diagnosis\tools\data_tools.py)
  把 `globals()` 改成 session store
- [`app.py`](D:\fault-diagnosis\app.py)
  在应用生命周期中初始化 session store

### 4. 为什么这样改更好

这样改的本质不是“代码更优雅”，而是：

- 让工具执行状态真正成为 Agent runtime 的一部分
- 让每个会话的数据分析上下文可管理
- 为后面的案例存档和审计打基础

### 5. 这一阶段的交付标准

做到下面几件事，就算阶段 A 合格：

- 不再依赖 `globals()` 共享 DataFrame
- 同时开启多个会话不会互串
- 图表生成可以追踪到 `thread_id`
- 有过期清理策略

## 五、阶段 B：案例资产化

### 1. 当前问题在哪里

当前已经有很好的报告输出能力，主要在：

- [`report_tools.py`](D:\fault-diagnosis\tools\report_tools.py)

但现在的问题是：

- 报告主要以 `.md` 和 `.html` 文件形式落盘
- 对人可读，但对系统不可计算

这意味着后面做不了这些事情：

- 查相似诊断案例
- 统计某类故障的高频结论
- 把历史建议回灌给新诊断

### 2. 推荐新增的案例层

建议新增：

- `case_memory/`
  - `models.py`
  - `repository.py`
  - `service.py`
  - `extractors.py`

推荐至少定义一个案例主结构：

```python
@dataclass
class DiagnosisCase:
    case_id: str
    thread_id: str
    created_at: datetime
    device_type: str
    diagnosis_type: str
    severity: str
    key_metrics: list[dict]
    conclusion: str
    recommendations: list[str]
    evidence_summary: str
    report_paths: list[str]
    image_paths: list[str]
```

### 3. 案例如何生成

建议在生成报告后，多做一步：

- 从本次最终结论中抽取结构化字段
- 同时写入案例存储

也就是说：

- `save_report` / `save_html_report` 继续负责文件
- 新增一个 `save_case_record` 或内部 case service 负责结构化入库

### 4. 案例存储先怎么落地

第一阶段不需要很复杂，建议这样：

- PostgreSQL 中新增案例表
- 同时保留报告文件路径

为什么优先用 PostgreSQL：

- 现有系统已经依赖 PostgreSQL 做 checkpoint
- 能减少新基础设施引入

如果以后案例检索更复杂，再考虑：

- 案例 embedding
- 案例向量索引

### 5. 这一阶段的关键价值

这一层补上以后，系统会发生质变：

- 从“会生成报告”变成“会积累案例”
- 从“当前会话有记忆”变成“系统级有经验”

## 六、阶段 C：知识层重构

### 1. 当前问题在哪里

现在知识层主要集中在：

- [`knowledge_base.py`](D:\fault-diagnosis\knowledge_base.py)
- [`kb_tools.py`](D:\fault-diagnosis\tools\kb_tools.py)

当前模式是：

- PDF -> chunk -> embedding -> FAISS -> top-k 返回

这没问题，但对于工业场景，知识类型其实至少有三种：

- 规范知识
- 设备知识
- 案例知识

如果这些知识以后都混在一起检索，结果很快会变脏。

### 2. 推荐的新知识层设计

建议新增：

- `knowledge/`
  - `manual_store.py`
  - `fault_code_store.py`
  - `case_store.py`
  - `router.py`
  - `schemas.py`

推荐按知识类型分三层：

#### 第一层：手册与标准层

内容：

- PDF 手册
- 操作规程
- 维护标准

用途：

- 回答规范性问题
- 补充专业依据

#### 第二层：故障码与结构化规则层

内容：

- 故障码说明
- 触发条件
- 常见处理步骤

用途：

- 快速结构化召回
- 减少模型在简单领域知识上的不稳定发挥

这一层甚至不一定非要向量检索，也可以是结构化表 + 精确查找。

#### 第三层：案例层

内容：

- 历史诊断案例
- 典型问题与建议

用途：

- 查相似情境
- 给新诊断提供经验参考

### 3. 查询路径应该怎么改

现在更像一个单工具：

- `query_knowledge_base(query)`

建议以后升级成：

- `query_manual_knowledge`
- `query_fault_code_knowledge`
- `query_case_memory`

或者保留一个统一入口，但内部做 router：

- 先判断问题类型
- 再决定打哪个知识源

### 4. 为什么这样更好

这样做的真正价值是：

- 不同证据源的语义角色被分清
- 模型拿到的上下文更有层次
- 后续更容易做检索质量优化

## 七、阶段 D：服务化与平台化底座

### 1. 依赖治理

建议新增：

- `infra/health.py`
- `infra/dependency_status.py`
- `infra/retry.py`

目标：

- 对 MySQL、PostgreSQL、Embedding、外部 ML API 做显式健康检查
- 给请求过程增加统一的 timeout / fallback 策略

### 2. 结构化日志与审计

建议新增：

- `observability/`
  - `logging.py`
  - `audit.py`
  - `trace.py`

至少记录：

- thread_id
- case_id
- tool sequence
- tool errors
- report generation result
- external dependency status

### 3. 平台化边界预留

现在先不用过度抽象，但建议预留这几个未来边界：

- 工具注册层
- 知识源注册层
- 案例存储接口层
- 子 Agent 工厂层

为什么要预留：

- 这不是为了“现在就平台化”
- 而是为了避免以后扩设备、扩场景时彻底推倒重来

## 八、建议的数据库与存储改造

### 1. PostgreSQL 新增案例表

建议增加：

- `diagnosis_cases`

建议字段方向：

- `case_id`
- `thread_id`
- `created_at`
- `device_type`
- `diagnosis_type`
- `severity`
- `conclusion`
- `evidence_summary`
- `recommendations_json`
- `report_paths_json`
- `image_paths_json`
- `raw_summary`

### 2. 故障码知识表

如果故障码数据比较结构化，建议独立表：

- `fault_code_knowledge`

字段可以包括：

- `fault_code`
- `title`
- `trigger_conditions`
- `possible_causes`
- `recommended_actions`
- `source`

### 3. 案例向量索引

后续需要时再加，不建议第一步就做复杂。

可以后置的原因是：

- 先把案例结构化存下来更重要
- 没有结构化案例，向量化也没有稳定输入

## 九、建议的代码目录演进方向

如果后面持续升级，我建议目录逐渐演进成这样：

```text
fault-diagnosis/
├── app.py
├── streaming.py
├── middleware.py
├── prompts/
├── tools/
├── runtime_state/
├── case_memory/
├── knowledge/
├── observability/
├── infra/
├── tests/
└── agent_fronted/
```

这样做的核心目的不是“好看”，而是把系统里的四类能力分开：

- 任务执行
- 会话状态
- 知识资产
- 服务治理

## 十、建议的实施顺序

### 第一步

先做会话运行时状态重构。

因为这是最底层的稳定性问题。

### 第二步

做报告结构化与案例表设计。

因为这是从“产出文件”走向“积累资产”的关键一步。

### 第三步

做知识层分层与 router 改造。

因为等案例和故障码层准备好以后，知识系统才值得重构。

### 第四步

补健康检查、审计日志、依赖治理。

这一步也可以部分提前，但建议在核心数据结构确定后统一做。

### 第五步

如果系统规模继续扩大，再考虑更正式的平台边界与多 Agent 扩展。

## 十一、什么叫这次改造成功

我建议不要用“功能变多了”来判断是否成功，而用下面这些标准：

- 多会话执行更稳定了
- 报告可以转成结构化案例资产
- 检索结果能区分手册、故障码、案例
- 出错时能知道是哪一层出了问题
- 后续扩设备和扩知识源时不需要重做主框架

## 十二、最后一句话记忆

如果用一句话记住这份技术改造方案，我建议记成这样：

> `fault-diagnosis` 的下一阶段改造，不是继续堆能力，而是把执行状态、案例资产、知识分层和服务治理这四个底座补齐。
