# fault-diagnosis 与 career-ops 对比分析

## Summary

- Project name: fault-diagnosis vs career-ops
- Project path: `D:\fault-diagnosis` and `D:\career-ops`
- Document type: user
- Purpose: explain how two vertical Agent projects differ in design target, workflow shape, tool strategy, memory, RAG, and delivery model, so future Agent design can choose the right pattern consciously

## 一、先给结论：它们像在哪里，不像在哪里

这两个项目都不属于“底层 Agent runtime 内核型项目”，它们都更像：

- 在现成 Agent 宿主能力之上
- 面向一个明确业务场景
- 把流程、规则、输出物包装成可执行系统

所以它们的共同点是：

- 都是 `vertical-workflow` 类型
- 都强调 prompt 不只是人设，而是作业流程
- 都强调输出物，而不只是聊天内容

但它们最关键的不同在于：

- `career-ops` 更像“知识工作流 Agent”
- `fault-diagnosis` 更像“数据驱动诊断 Agent”

可以把它们理解成两种不同的垂直 Agent 路线：

### 路线 A：流程运营型

代表项目：

- `career-ops`

核心特点：

- 强调步骤编排
- 强调任务分解和角色协同
- 强调结构化产出和文档交付
- 数据通常不是高频时序工业数据，而是文本、简历、岗位信息、研究材料之类

### 路线 B：工业诊断型

代表项目：

- `fault-diagnosis`

核心特点：

- 强调数据查询和诊断证据
- 强调数据库、ML API、知识库、图表、报告联动
- 强调可追溯性、专业性和诊断依据
- 更依赖外部系统稳定性和工具链闭环

## 二、它们各自围绕什么目标建系统

### 1. `career-ops` 的目标

它更像在解决：

- 如何把一套职业咨询、求职分析、岗位研究、交付流程做成可重复执行的 Agent 工作流

所以它的重点通常会落在：

- prompt 作为业务流程
- worker 拆分
- 数据合同和结构化输出
- 人在环审批
- 文档交付

它追求的是：

- 可复用流程
- 稳定产出
- 人机协作顺畅

### 2. `fault-diagnosis` 的目标

它更像在解决：

- 如何把工业设备诊断从“问一句回一句”提升成“查数据、做判断、补知识、出报告”的完整执行链

所以它的重点落在：

- 数据事实
- 工具调用
- 专业诊断过程
- 证据补充
- 最终报告

它追求的是：

- 数据驱动
- 诊断可信
- 输出可审计

## 三、Prompt 设计思路有什么根本区别

### `career-ops`

它的 prompt 更像：

- 面向知识工作流程的任务说明书
- 面向角色协作的任务协议
- 面向产出的模板化约束

重点通常是：

- 任务拆解
- 角色分工
- 交付格式
- 审核标准

### `fault-diagnosis`

它的 prompt 更像：

- 面向工业诊断流程的 SOP
- 面向工具调用和约束条件的决策表
- 面向专业诊断输出的规范书

重点通常是：

- 什么时候查数据库
- 什么时候用子 Agent
- 什么时候查知识库
- 什么工具不能混用
- 最终答案必须包含什么字段

最值得学的差异在这里：

- `career-ops` 更强调“任务怎么推进”
- `fault-diagnosis` 更强调“诊断证据怎么形成”

## 四、Tool Calling / Tool 设计的差异

### `career-ops`

更偏：

- 文档处理
- 信息整理
- 结构化输出
- worker 间分工

它的工具如果很多，核心也更像“流程工具”。

### `fault-diagnosis`

更偏：

- SQL 查询
- 数据提取
- 图表生成
- 知识库检索
- 外部搜索
- 报告落盘
- 子 Agent 诊断

它的工具不是围绕文档协作，而是围绕诊断证据链。

这个差异很重要，因为它说明：

- 垂直 Agent 的工具设计，必须从业务证据链倒推，而不是从“我会哪些技术”正推

## 五、Workflow 编排有什么不同

### `career-ops`

更像：

- coordinator
- worker 批处理
- 文档汇总
- review / revise / finalize

它擅长的是流程编排和角色协作。

### `fault-diagnosis`

更像：

- query loop
- todo task flow
- 诊断子 Agent
- 图表和报告产出

它擅长的是工具驱动的证据式工作流。

所以如果要用一句话总结：

- `career-ops` 是“流程协作型”
- `fault-diagnosis` 是“证据诊断型”

## 六、Memory 与 RAG 的差异

### `career-ops`

更需要的记忆通常是：

- 项目上下文
- 用户偏好
- 任务状态
- 中间产物和交付版本

如果做强，往往会向“项目级长期记忆”发展。

### `fault-diagnosis`

当前更强的是：

- checkpoint 会话记忆
- 摘要压缩
- todo 状态记忆

它的记忆偏执行连续性，而不是知识成长性。

RAG 上也不同：

- `career-ops` 的 RAG 更偏资料研究和外部知识补充
- `fault-diagnosis` 的 RAG 更偏手册、故障码、处置步骤补充

也就是说：

- `career-ops` 的知识更像“研究材料”
- `fault-diagnosis` 的知识更像“诊断手册”

## 七、最终交付物有什么不同

### `career-ops`

更可能产出：

- 分析文档
- 研究报告
- 路线建议
- 结构化结论

### `fault-diagnosis`

更可能产出：

- 诊断报告
- HTML 可视化报告
- 图表
- 故障结论和处置建议

所以它们共同说明了一件事：

- 垂直 Agent 的价值通常不止于对话，而在于“业务可用交付物”

## 八、什么时候该参考谁

### 优先参考 `career-ops`

当你的问题是：

- 怎么把复杂知识工作拆成多步骤流程
- 怎么做 worker 协作
- 怎么做结构化交付
- 怎么把人审和自动化串起来

### 优先参考 `fault-diagnosis`

当你的问题是：

- 怎么让 Agent 读取数据库并形成诊断证据
- 怎么把工具链串成一个行业闭环
- 怎么产出图表和专业报告
- 怎么让结果更可追溯

## 九、对未来设计的启发

如果以后你做新的垂直 Agent，可以先问自己三个问题：

### 1. 我的核心价值更像“流程协作”还是“证据诊断”

这会决定你的 prompt、workflow 和 tool 设计完全不同。

### 2. 我的 RAG 是主引擎，还是补证模块

`fault-diagnosis` 很适合作为“RAG 是补证而非主引擎”的案例。

### 3. 我的最终价值是聊天体验，还是交付物

如果是后者，就一定要提前设计：

- 报告
- 图表
- 结构化输出
- 存档与追溯

## 十、最后一句话记忆

如果用最短的话记住这两个项目的区别，我建议记成这样：

> `career-ops` 教你怎么把知识工作流程做成 Agent，`fault-diagnosis` 教你怎么把工业诊断证据链做成 Agent。
