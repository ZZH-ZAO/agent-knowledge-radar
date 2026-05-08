# ByteDance--Auto_prd_test_agent 改进后整体架构设计

## Summary

- Project name: ByteDance--Auto_prd_test_agent
- Project path: `D:\测开\ByteDance--Auto_prd_test_agent`
- Document type: user
- Purpose: describe what the improved end-state architecture of this project should look like, how each layer works together, what problem each design solves, and which earlier projects inspired each major design choice

## 一、先给结论：改进后它不再只是“测试用例生成器”，而是一套测试知识与质量闭环系统

如果把这个项目现在的状态和改进后的状态做个最直观的对比，可以这样理解：

### 当前版本更像

- 一个基于 Streamlit 的测试生成工作台
- 有 Prompt
- 有本地 RAG
- 有人工微调
- 有 AI 评审

### 改进后目标版本更像

- 一个围绕测试知识、规则证据、历史案例、生成质量、坏例回流和回归验证共同运转的测试 Agent 系统

也就是说，改进后的重点不是：

- 让模型“更会说”

而是：

- 让系统更会检索
- 更会解释
- 更会验证
- 更会沉淀
- 更会持续演进

## 二、整体架构总图

改进后建议把整个项目分成七层：

1. 产品交互层
2. 工作流编排层
3. 检索与证据层
4. 生成与评审层
5. 记忆与资产层
6. 质量与验证层
7. 平台治理层

可以把它理解成这样一张文字架构图：

```text
User / Tester
    ↓
Product Workbench UI
    ↓
Workflow Services
    ↓
Retrieval + Rerank + Evidence Layer
    ↓
Generation + Refinement + Evaluation Layer
    ↓
Memory / Asset / Case Store
    ↓
Metrics / Bad Case / Regression / Feature Flags
```

这七层不是为了显得复杂，而是为了回答七个不同问题：

1. 用户怎么工作
2. 流程怎么推进
3. 知识怎么找
4. 内容怎么生成和审核
5. 结果怎么沉淀
6. 系统怎么知道自己做得好不好
7. 新能力怎么安全上线

## 三、产品交互层：从“上传+生成”升级成完整测试工作台

### 1. 这一层长什么样

改进后，前端不应该只是一页聊天 + 一页预览。  
更合理的是形成五个主要工作区：

1. `Input / Ingestion`
2. `Retrieval / Evidence`
3. `Generation Workspace`
4. `Evaluation / Quality`
5. `Bad Case / Regression Review`

### 2. 每个工作区解决什么问题

#### `Input / Ingestion`

解决：

- 用户怎么上传 PRD、PDF、图片、补充说明
- 文档怎么被解析
- 结构抽取得怎么样

用户应该看到：

- 文件解析状态
- 文档结构摘要
- 抽出的业务关键词
- 抽出的逻辑关键词

#### `Retrieval / Evidence`

解决：

- 系统到底找到了什么规范和历史案例
- 为什么这些内容被送进模型

用户应该看到：

- semantic retrieval 结果
- keyword retrieval 结果
- rerank 后结果
- 命中规则
- 来源文档

#### `Generation Workspace`

解决：

- 测试用例怎么生成
- 用户怎么微调

用户应该看到：

- 左侧解释
- 右侧结构化结果
- 多轮编辑记录

#### `Evaluation / Quality`

解决：

- 当前结果好不好
- 漏了哪些测试点
- 是否符合规范

用户应该看到：

- 总评分
- 分项评分
- 漏测点
- 合规问题
- 优化建议

#### `Bad Case / Regression Review`

解决：

- 哪些 case 是坏例
- 坏在哪里
- 怎么加入回归集

用户应该看到：

- bad-case 分类
- root cause guess
- 对比视图
- 快速标注按钮

### 3. 为什么这一层要这样改

因为测试工作不是“问一句、答一句”，而是一条有证据、有评估、有修正、有沉淀的工作链。

### 4. 借鉴来源

- 当前项目已有左右双区工作台基础
- `fault-diagnosis`
  借它的证据透明和过程可视化
- `repomind`
  借它的 review / verification 视角

## 四、工作流编排层：从 UI 串流程升级成可维护的服务层

### 1. 改进后这一层长什么样

建议形成 `services/`：

```text
services/
  ingestion_service.py
  retrieval_service.py
  generation_service.py
  refinement_service.py
  evaluation_service.py
  archive_service.py
  benchmark_service.py
  badcase_service.py
```

### 2. 它解决什么问题

这一层负责把完整流程拆成可管理阶段：

1. 文档接入
2. query 理解
3. 检索与重排
4. 上下文组装
5. 生成
6. 微调
7. 评估
8. 归档
9. 坏例回流
10. 回归验证

### 3. 为什么要这样分

因为如果工作流继续都堆在 `ui/main.py`：

- 调试困难
- 逻辑耦合
- 难做 API 化
- 难做批量任务

### 4. 这一层最关键的设计原则

每个服务都要有：

- 明确输入
- 明确输出
- 明确失败状态

也就是 workflow 不是“函数拼起来”，而是“阶段合同拼起来”。

### 5. 借鉴来源

- `career-ops`
  借它的 workflow-first 思路和数据合同意识
- `deer-flow`
  借它的 app / runtime 分层意识

## 五、检索与证据层：从轻量 RAG 升级成 Hybrid Retrieval + Rerank + Evidence

### 1. 改进后这一层长什么样

完整流程建议是：

1. query understanding
2. semantic retrieval
3. keyword retrieval
4. candidate normalization
5. rerank
6. context assembly
7. evidence presentation

### 2. 为什么不是只做语义检索

因为这个项目是测试用例生成，不是开放问答。  
测试生成特别依赖两类东西：

- 业务关键词
- 规则 / 逻辑词

所以必须引入 hybrid retrieval。

### 3. 关键词分哪两类

#### 业务关键词

例如：

- 登录
- 注册
- 支付
- 订单
- 权限
- 风控

作用：

- 保证召回同业务域内容

#### 逻辑关键词

例如：

- 必须
- 禁止
- 至少
- 超过
- 空值
- 超时
- 锁定

作用：

- 强化规则、边界、异常条件的命中

### 4. rerank 应该怎么理解

不是“重新排相似度”，而是：

> 判断哪些内容最值得送给测试生成模型。

所以 rerank 分三层：

- 相关性
- 测试价值
- 知识可信度

### 5. 证据层为什么重要

这一层最终要回答：

- 当前测试点依据了哪些规则
- 哪些历史案例参与了生成
- 哪些文档被排前
- 为什么它们被排前

### 6. 这一层解决的问题

- 检索黑箱
- 噪声高
- 关键规则漏召回
- 前端无法解释结果依据

### 7. 借鉴来源

- 当前项目已有本地向量 RAG 和 LLM 过滤雏形
- `fault-diagnosis`
  借它的证据链和多来源拼接意识
- `repomind`
  借它 verification-first 思路

## 六、生成与评审层：从“生成一次”升级成“生成-修订-审核”三段闭环

### 1. 改进后这一层怎么工作

完整主链路：

1. generation
2. refinement
3. evaluation

也就是：

- 先生成
- 再人工微调
- 再 AI 评审

### 2. 为什么三段都要保留

#### generation

负责把 PRD 和证据转成结构化测试资产

#### refinement

负责把人工意图融进去

#### evaluation

负责做质量检查和规则审查

如果少掉任何一段，系统都会变弱：

- 没有 generation，效率低
- 没有 refinement，不贴业务
- 没有 evaluation，质量不可控

### 3. evaluator 后续要升级成什么

不只是输出给人看的报告，还要输出给系统写回的结构化结果。

比如：

- coverage_score
- compliance_score
- major_gaps
- template_worthy

### 4. 这一层解决的问题

- 单次生成不可控
- 结果好坏难以判断
- 评估结果无法回流

### 5. 借鉴来源

- 当前项目已有“解释 + JSON 分离”的设计和 evaluator 雏形
- `career-ops`
  借 workflow 中阶段职责清晰的意识
- `repomind`
  借 verification-first 和结果生命周期意识

## 七、记忆与资产层：从 session state 升级成三层 memory

### 1. 改进后分哪三层

#### session memory

保存当前会话：

- messages
- 当前结果
- 当前检索上下文
- 当前评估结果

#### case memory

保存历史高价值案例：

- 生成版本
- 最终版本
- 评估分数
- 人工采纳情况

#### learning memory

保存长期可复用知识：

- 测试模板
- 高频规则
- 高质量案例模式
- 常见 bad-case 模式

### 2. 为什么要三层分开

因为这三种 memory 的用途不同：

- session memory
  为了继续工作
- case memory
  为了检索复用
- learning memory
  为了长期改进

### 3. 哪些更新应该异步做

这些最好异步：

- 模板抽取
- 高质量案例标注
- bad-case 模式沉淀
- benchmark 更新

这样不会阻塞主流程。

### 4. 这一层解决的问题

- 现在只有状态，没有真正学习
- 长期资产沉淀和主链路耦合

### 5. 借鉴来源

- `fault-diagnosis`
  借 session memory 的边界意识
- `deer-flow`
  借结构化、异步的 memory 更新
- `claude-code`
  借 memory 走向团队资产的方向感

## 八、质量与验证层：从“看起来还行”升级成可度量、可回归、可修复

### 1. 这一层由什么组成

建议形成三个核心对象：

1. `metrics`
2. `bad_cases`
3. `benchmarks`

### 2. metrics 做什么

负责回答：

- 检索质量好不好
- rerank 是否有效
- 最终生成是不是更有价值

重点指标包括：

- `Recall@K`
- `Precision@K`
- `Rule Recall@K`
- `Noise Rate@K`
- `Human Acceptance Rate`

### 3. bad_cases 做什么

负责回答：

- 系统最痛的失败样本是什么
- 错在检索、排序、生成还是评审
- 这些错误以后怎么追踪

### 4. benchmarks 做什么

负责回答：

- 一次改动有没有真的变好
- 修过的问题会不会重新坏掉

### 5. 为什么这三者必须一起存在

因为：

- 只有 metrics，你知道趋势，不知道具体怎么坏
- 只有 bad-case，你知道问题，不知道整体趋势
- 只有 benchmark，你能回归，但不知道线上真实痛点

三者一起才是完整质量系统。

### 6. 借鉴来源

- `repomind`
  借 verification lifecycle、record 和回归验证意识
- `claude-code`
  借 feature 管理和可观测性意识

## 九、平台治理层：从单一产品升级成可灰度、可实验、可回退

### 1. 为什么要单独有这一层

因为后面你一旦加这些能力：

- hybrid retrieval
- rerank
- bad-case panel
- benchmark
- 模板抽取
- 自动脚本生成

系统就会变成高变化系统。  
高变化系统如果没有治理层，实验很容易失控。

### 2. 这一层至少要有什么

#### feature flags

例如：

- 是否启用 keyword retrieval
- 是否启用新 rerank 策略
- 是否启用新的 evaluator

#### experiment groups

例如：

- A 组只用 semantic retrieval
- B 组用 hybrid retrieval

#### observability

例如：

- 每个版本的指标
- 每种策略的坏例数
- 每类 feature 的成本和收益

### 3. 这一层解决什么问题

- 新功能上线风险大
- 难以定位是哪层改坏了系统
- 试验无法可控进行

### 4. 借鉴来源

- `claude-code`
  借它的 feature flag、灰度和平台演进意识

## 十、改进后整套系统的一次完整运行会是什么样

这里我直接给你描述一遍最终版本的一次完整请求链路。

### 第一步：用户上传材料

系统做：

- 文档解析
- 结构提取
- 关键词抽取
- 长文本切片或兜底索引

### 第二步：系统理解 query

系统抽出：

- 业务域
- 模块
- 风险点
- 业务关键词
- 逻辑关键词

### 第三步：开始 hybrid retrieval

同时做：

- semantic retrieval
- keyword retrieval

### 第四步：rerank 与上下文组装

系统按：

- 相关性
- 测试价值
- 可信度

统一排序，并生成：

- 规范证据块
- 案例参考块
- 关键规则块

### 第五步：生成测试用例

模型基于：

- PRD
- 证据上下文
- 输出合同

生成解释 + JSON。

### 第六步：用户微调

用户对结果继续对话修正，系统保留版本差异。

### 第七步：AI 评审

evaluator 输出：

- 总分
- 分项分
- 漏测点
- 合规问题
- 是否值得沉淀成模板

### 第八步：bad-case 检测

系统根据：

- 指标异常
- 用户反馈
- evaluator 结果

判断是否形成 bad-case。

### 第九步：回流

系统异步做：

- 高质量案例归档
- 模板抽取
- bad-case 入库
- benchmark 更新

### 第十步：治理与观测

平台记录：

- 当前实验版本
- 当前策略命中率
- 本轮成本
- 本轮质量指标

## 十一、每一层最核心的设计动机、解决的问题和借鉴来源

### 产品交互层

- 动机：
  让用户在一个工作台里完成测试设计全流程
- 解决的问题：
  当前只有生成，没有质量运营面
- 借鉴来源：
  `fault-diagnosis`、`repomind`

### 工作流编排层

- 动机：
  让流程可维护、可复用、可 API 化
- 解决的问题：
  当前 UI 过重
- 借鉴来源：
  `career-ops`、`deer-flow`

### 检索与证据层

- 动机：
  让系统找到真正有测试价值的规则和案例
- 解决的问题：
  纯语义检索不够、检索黑箱
- 借鉴来源：
  当前项目雏形、`fault-diagnosis`、`repomind`

### 生成与评审层

- 动机：
  提升生成质量并建立审核闭环
- 解决的问题：
  结果无法持续验证
- 借鉴来源：
  当前项目 evaluator、`career-ops`、`repomind`

### 记忆与资产层

- 动机：
  让结果从一次性内容变成长期知识资产
- 解决的问题：
  当前只有 session state 和简单回存
- 借鉴来源：
  `fault-diagnosis`、`deer-flow`、`claude-code`

### 质量与验证层

- 动机：
  让系统进化靠证据，不靠感觉
- 解决的问题：
  没有系统性 metrics / bad-case / benchmark 机制
- 借鉴来源：
  `repomind`、`claude-code`

### 平台治理层

- 动机：
  让新能力可以安全试验和回退
- 解决的问题：
  检索和生成策略升级风险高
- 借鉴来源：
  `claude-code`

## 十二、最后一句话怎么记住这个目标架构

> 改进后的 `ByteDance--Auto_prd_test_agent`，不再只是一个“把 PRD 变成测试用例的生成工具”，而是一套把知识检索、规则证据、人工修订、AI 评审、坏例回流、回归验证和持续治理组织在一起的测试 Agent 生产系统。
