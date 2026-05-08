# fault-diagnosis 聚焦专项改造方案

## Summary

- Project name: fault-diagnosis
- Project path: `D:\fault-diagnosis`
- Document type: user
- Purpose: provide a focused upgrade plan for the fault-diagnosis project across MCP development, SSE event streaming, multi-role prompt design, sub-agent manual RAG, FAISS evolution, Agent workflow design, and tool-layer optimization, with explicit motivations and cross-project inspirations

## 一、先给结论：这个项目现在最该补的，不是“再加一个模型”，而是把工业 Agent 的控制面、证据面和协作面做厚

`fault-diagnosis` 现在已经具备一个工业 Agent 的不错基础：

- 有工具链
- 有 SSE 透明事件
- 有 Prompt 化 SOP
- 有子 Agent
- 有 FAISS 手册检索
- 有报告生成

但它现在更像：

> 一个已经能跑通的工业诊断工作流 Agent

还不太像：

> 一个可扩展、可验证、可接入更多系统的工业 Agent 平台

如果聚焦你这次点名的几个方向，我会把改造目标压成七件事：

1. 把 `MCP` 做成真正的外部能力接入层
2. 把 `SSE` 从“能流式输出”升级成“可观测事件总线”
3. 把 Prompt 从“大段 SOP”升级成“角色化可组合 Prompt 体系”
4. 把子 Agent 的故障手册 RAG 做成“专用知识工作台”
5. 把 `FAISS` 从基础向量检索升级成“分层证据系统”
6. 把 Agent workflow 从“能跑通”升级成“有状态、有阶段、有回退”
7. 把已有 tools 从“可调用模块”升级成“可治理能力层”

## 二、MCP 开发：为什么这个项目非常适合加 MCP

### 1. 当前问题是什么

这个项目目前的工具基本都在本地代码里：

- `sql_tools.py`
- `data_tools.py`
- `kb_tools.py`
- `report_tools.py`
- `utility_tools.py`
- `tools/subagent/`

这在当前阶段很好，因为它让项目很直接。  
但它也意味着一个问题：

- 所有能力都要写进主项目
- 外部系统接入会越来越重
- 工具边界不清晰
- 很难形成统一的能力治理层

### 2. 为什么这里适合用 MCP

因为 `fault-diagnosis` 后面天然会遇到很多“外部能力接入”场景：

- CMDB / 资产系统
- 告警系统
- 时序数据库
- 设备台账系统
- 维修工单系统
- 手册知识服务
- 预测模型服务

这些能力如果都继续以内嵌工具方式堆在项目里，会让主项目越来越重。

所以这里很适合把 MCP 当成：

> 工业 Agent 的外部能力接入层

### 3. 推荐的 MCP 分层

建议优先做三类 MCP：

#### 第一类：工业数据 MCP

负责：

- 查询设备信息
- 查询时序数据
- 查询实时告警
- 查询历史故障工单

示例：

- `asset-info-mcp`
- `timeseries-query-mcp`
- `alarm-center-mcp`
- `workorder-history-mcp`

#### 第二类：知识与手册 MCP

负责：

- 查询故障码解释
- 查询设备手册
- 查询操作规程
- 查询案例库

示例：

- `manual-knowledge-mcp`
- `fault-code-mcp`
- `case-memory-mcp`

#### 第三类：报告与协作 MCP

负责：

- 生成报告
- 推送通知
- 写入工单
- 回写诊断结果

示例：

- `report-export-mcp`
- `notification-mcp`
- `ticket-update-mcp`

### 4. 为什么这样改更好

这样做之后：

- 主 Agent 不需要知道每个外部系统的接入细节
- 工业能力可以按 server 拆分
- 后续新增集成时更少改核心代码

### 5. 这块借鉴什么

- `deer-flow`
  借它把 `skills / MCP / runtime` 分层组织的思路
- `claude-code`
  借它对能力开关和平台演进的意识

### 6. 第一版不要怎么做

不要一开始就把所有 tools 全部 MCP 化。  
第一版最值得先 MCP 化的是：

- 工业数据读取
- 手册知识查询
- 工单/通知回写

因为这三类最像真正的“外部能力”。

## 三、SSE 事件流：从流式输出升级成事件协议

### 1. 当前项目已经有什么

这个项目现在已经有很不错的基础：

- `start`
- `token`
- `tool_start`
- `tool_end`
- `complete`
- `server_error`

这已经比很多只吐文本的 Agent 更成熟了。

### 2. 现在还缺什么

如果后面系统变复杂，只靠这些事件会不够，因为你会想知道：

- 当前在哪个工作流阶段
- 检索命中了什么
- rerank 发生了什么
- 子 Agent 干了什么
- 报告生成到了哪一步
- 哪一步失败了、是否降级了

### 3. 推荐的新事件模型

建议把 SSE 事件扩成五大类：

#### 第一类：生命周期事件

- `run_started`
- `run_completed`
- `run_failed`
- `run_cancelled`

#### 第二类：阶段事件

- `stage_started`
- `stage_completed`
- `stage_failed`

阶段可以包括：

- ingestion
- retrieval
- rerank
- diagnosis
- subagent_manual_lookup
- report_generation

#### 第三类：工具事件

- `tool_start`
- `tool_end`
- `tool_error`

#### 第四类：证据事件

- `retrieval_hit`
- `retrieval_summary`
- `rerank_summary`
- `evidence_selected`

#### 第五类：子 Agent 事件

- `subagent_started`
- `subagent_progress`
- `subagent_completed`
- `subagent_error`

### 4. 为什么这样更好

因为这会让 SSE 不只是“流式吐字”，而是：

> 整个工业 Agent 执行过程的可观测协议

这会直接帮助：

- 前端可视化
- 问题排查
- 用户信任
- bad-case 分析

### 5. 前端怎么配合

前端最好同步展示：

- 当前阶段
- 当前工具
- 当前证据来源
- 当前子 Agent 状态
- 当前已生成产物

### 6. 这块借鉴什么

- `fault-diagnosis` 自己已有 SSE 基础
- `repomind`
  借它更强的过程事件与 verification 思维
- `fault-diagnosis` 当前路线延伸

## 四、不同角色的 Prompt 调优：从大 Prompt 升级成角色矩阵

### 1. 当前问题是什么

这个项目现在最大的优点之一，就是 Prompt 很像 SOP。  
但问题也在这里：

- 主 Prompt 会越来越重
- 规则会越来越堆
- 主 Agent 和子 Agent 边界会变模糊

### 2. 推荐的角色矩阵

建议把 Prompt 系统拆成至少四类角色：

#### 第一类：主控诊断 Agent

职责：

- 理解用户问题
- 规划诊断步骤
- 决定先查数据、查知识还是交给子 Agent
- 汇总结论

Prompt 重点：

- 工作流规划
- 工具选择约束
- 不确定性表达

#### 第二类：手册 / 知识分析 Agent

职责：

- 读取手册证据
- 归纳故障码含义
- 从文档中抽处理步骤和限制条件

Prompt 重点：

- 忠于文档
- 不做额外猜测
- 强证据引用

#### 第三类：数据分析 Agent

职责：

- 读取数据结果
- 识别异常波动
- 总结趋势和异常模式

Prompt 重点：

- 描述性分析
- 不越权下结论
- 强调阈值、趋势、异常点

#### 第四类：报告生成 / 解释 Agent

职责：

- 生成用户可读报告
- 组织证据、图表、建议
- 输出适合交付的结构

Prompt 重点：

- 结构清晰
- 区分事实、判断、建议

### 3. 为什么这样拆更好

因为工业 Agent 经常不是“一个超级 Prompt”能长期扛住的。  
拆成角色后有几个好处：

- 每个角色的目标更单纯
- 更容易测 Prompt 效果
- 更容易配不同工具和知识

### 4. 角色 Prompt 设计原则

每个角色 Prompt 最好拆成三层：

1. role identity
2. task procedure
3. output contract

### 5. 这块借鉴什么

- `career-ops`
  借它把 Prompt 写成领域作业规范
- `ByteDance--Auto_prd_test_agent`
  借它把生成者和评审者做角色分离
- `deer-flow`
  借它把 Prompt 当作 runtime governance，而不是纯人设

## 五、子 Agent 的故障手册 RAG：要做成“专用知识子系统”

### 1. 当前问题是什么

现在子 Agent 已经存在，但故障手册 RAG 还是偏基础：

- PDF -> chunk -> embedding -> FAISS -> top-k

这能用，但子 Agent 如果真想成为“手册专家”，这套还不够。

### 2. 推荐的新设计

子 Agent 的手册 RAG 不应该只是“共享一个普通知识库”，而应该做成专用子系统。

建议按三层拆：

#### 第一层：手册原文层

保存：

- 原始 PDF / 文档
- 页码
- 章节
- 版本

#### 第二层：规则 / 步骤抽取层

把手册中的内容结构化成：

- 故障码
- 现象描述
- 原因列表
- 处理步骤
- 注意事项
- 禁止操作

#### 第三层：RAG 检索层

检索时不是只看原文 chunk，还能按结构化字段查：

- fault_code
- symptom
- device_type
- handling_steps
- risk_note

### 3. 为什么这样更好

因为“故障手册”不是普通文档，它高度结构化。  
如果你只把它当 chunk 文本，系统很容易：

- 找到相关页，但抓不到关键步骤
- 找到主题相近段落，但没有真正故障规则

### 4. 子 Agent 该怎么用这个 RAG

建议子 Agent workflow 是：

1. 识别当前设备类型 / 故障码 / 症状关键词
2. 优先查结构化规则字段
3. 再补原文证据 chunk
4. 输出：
   - 事实证据
   - 可能原因
   - 推荐检查步骤
   - 风险提醒

### 5. 这块借鉴什么

- `ByteDance--Auto_prd_test_agent`
  借它“知识库不仅是问答材料，而是生成约束材料”的思路
- `repomind`
  借它 verification-first，不只查到，还要能支撑判断
- `fault-diagnosis`
  自己已有手册 RAG 雏形

## 六、FAISS 向量数据库：怎么从基础检索升级

### 1. 当前问题是什么

`FAISS` 本身没问题，问题在于现在它承载的知识类型太单一抽象：

- 手册
- 故障码
- 案例

这些后面如果混在一个检索层里，会越来越脏。

### 2. 推荐的升级方向

不要先急着换掉 `FAISS`，而是先把知识结构分层。

推荐至少分成三库：

1. `manual_store`
2. `fault_code_store`
3. `case_store`

每一库都可以先继续用 `FAISS`，但检索路由不同。

### 3. 检索路由怎么做

根据 query 识别：

- 如果是故障码驱动，优先 `fault_code_store`
- 如果是设备处理步骤驱动，优先 `manual_store`
- 如果是相似历史场景驱动，优先 `case_store`

### 4. 后续再补什么

在不替换 `FAISS` 的前提下，优先补：

- metadata filter
- knowledge type routing
- rerank
- evidence merge

### 5. 为什么这样更合理

很多团队一遇到问题就想“换库”，但当前真正的问题不是 `FAISS` 不够先进，而是：

- 知识没分层
- 路由没做
- 重排没做

### 6. 这块借鉴什么

- `ByteDance--Auto_prd_test_agent`
  借它把规范知识和历史案例分集合
- `fault-diagnosis` 自己已有多来源证据拼接方向
- `repomind`
  借它“不要只盯向量库，而要先看 retrieval pipeline”

## 七、Agent 工作流：从“能跑通”升级成阶段化诊断流程

### 1. 当前问题是什么

现在这个项目已经是 workflow-first 设计了，但后面还可以更清楚。

建议显式定义诊断阶段：

1. 问题接入
2. 初步分类
3. 数据取证
4. 手册 / 知识取证
5. 子 Agent 专项分析
6. 结论汇总
7. 报告生成
8. 结果归档

### 2. 为什么要更显式

因为后面一旦能力变多：

- 多个 MCP
- 多种 RAG
- 多个子 Agent
- 多种报告类型

如果阶段边界不清，系统会越来越乱。

### 3. 推荐的 workflow state

建议定义一个统一状态对象，例如：

- `thread_id`
- `current_stage`
- `tool_trace`
- `evidence_bundle`
- `intermediate_findings`
- `subagent_outputs`
- `report_paths`

### 4. 阶段化后能做什么

- SSE 更容易展示
- bad-case 更容易定位
- 失败时更容易回退
- 后面更容易做 benchmark

### 5. 这块借鉴什么

- `career-ops`
  借 workflow-first 和阶段合同
- `claude-code-sourcemap`
  借按时间尺度和状态治理来理解 workflow

## 八、已有 tool 优化：从“能用工具”升级成“可治理工具层”

### 1. 当前问题是什么

现在 tools 很丰富，这是优点。  
但后面容易出现三个问题：

- 工具说明不一致
- 工具输入输出不统一
- 工具错误处理风格不统一

### 2. 建议的工具分层

可以把 tools 分成四组：

#### 数据工具

- SQL
- DataFrame
- 图表分析

#### 知识工具

- 手册检索
- 故障码检索
- 案例检索

#### 执行工具

- 调模型
- 调子 Agent
- 调外部服务

#### 交付工具

- 报告生成
- HTML 输出
- 工单回写

### 3. 推荐统一规范

每个 tool 最好统一：

- tool name
- description
- input schema
- output schema
- error schema
- trace event

### 4. 额外建议

后面可以给每个 tool 补：

- timeout
- retry policy
- fallback strategy
- observability tag

### 5. 为什么这样更好

因为工具真正难的地方，不在“能不能调”，而在：

- 副作用怎么治理
- 错误怎么回退
- 工具状态怎么追踪

### 6. 这块借鉴什么

- `claude-code-sourcemap`
  借它对 tool runtime 和副作用治理的理解
- `deer-flow`
  借它统一能力层和可插拔能力的思路

## 九、如果把这些专项改造排优先级，我会这样排

### P0：先补控制面

1. Agent workflow state
2. SSE 阶段事件
3. tool input/output 统一

这是为了先让系统更稳、更可观测。

### P1：再补知识和角色层

1. 子 Agent 角色 Prompt 拆分
2. 手册 RAG 分层
3. FAISS 检索路由

这是为了让诊断更准。

### P2：再补平台接入层

1. 工业数据 MCP
2. 知识 MCP
3. 报告与协作 MCP

这是为了让系统更可扩展。

## 十、一句话总结

如果把这次专项方案压缩成一句话，我会这样说：

> `fault-diagnosis` 下一步最该做的，不是再堆一个更聪明的模型，而是把工业 Agent 的外部接入层、事件控制层、角色 Prompt 层、专用知识层、阶段化 workflow 和工具治理层补完整。
