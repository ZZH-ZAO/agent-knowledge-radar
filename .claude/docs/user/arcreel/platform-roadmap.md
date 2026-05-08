# ArcReel 可改进点与升级路线图

## Summary

- Project name: ArcReel
- Project path: `D:\ArcReel`
- Document type: user
- Purpose: explain what ArcReel should improve next, why those improvements matter, and how to prioritize future platform evolution without losing architectural coherence

## 一、先给结论：ArcReel 下一步最该补什么

如果只用一句话概括，我会这样说：

> ArcReel 下一步最值得补的，不是再接更多模型，而是把“知识资产层、平台观测层、工作流治理层”做得更完整。

原因是现在的 ArcReel 已经有很强的底座了：

- 有产品工作台
- 有 Agent runtime 包装
- 有工作流编排
- 有多供应商抽象
- 有后台任务系统
- 有认证、配置、计费、版本等平台能力

也就是说，它已经不是“能不能成为平台”的问题，而是“怎么把平台做得更深、更稳、更可持续”的问题。

所以我建议它后续重点围绕三类目标升级：

- 让 Agent 更可治理
- 让创作知识真正沉淀
- 让平台运营和观测能力更成熟

## 二、我建议的升级顺序

我建议按下面三层顺序推进：

- `P0`：先补治理与可观测性
- `P1`：再补知识资产与创作记忆
- `P2`：最后补更高级的协作和平台生态能力

这个顺序的逻辑是：

- ArcReel 现在已经够复杂了
- 复杂系统先需要可治理，才能安全继续扩展
- 如果在没有治理和沉淀的前提下继续加功能，只会让系统越来越重

## 三、P0：治理与可观测性

### P0-1. 增强 Agent runtime 观测能力

ArcReel 已经做了会话管理、snapshot、interrupt、turn normalization，这很好，但如果继续产品化，下一步最值得补的是：

- 更细粒度的 runtime tracing
- 每轮 turn 的关键耗时与阶段标记
- skill / subagent dispatch 的结构化日志
- 用户确认节点的链路可追踪

为什么重要：

- ArcReel 的 Agent 已经不是实验性质，而是工作台核心能力
- 一旦某次创作流程卡住，需要知道是卡在：
  - runtime
  - skill dispatch
  - background task
  - provider call

建议方向：

- 为每个 session 和每个 turn 增加 trace id
- 为 skill 调度、subagent 调度、pending question 建立统一事件模型
- 前端可以只展示精简版，后台保留完整审计

### P0-2. 补全跨层错误分类

现在 ArcReel 的复杂度决定了错误来源很多：

- SDK runtime 错误
- 权限或工具调用错误
- 工作流阶段错误
- 供应商能力不一致错误
- worker / queue 错误
- 文件系统和项目状态错误

为什么优先补：

- 平台越复杂，越不能只靠“500 + detail 文本”
- 如果没有清晰错误分层，运维和产品支持成本会快速上升

建议方向：

- 建立统一错误码体系
- 明确区分：
  - user actionable
  - system recoverable
  - operator actionable
- 前端错误文案和后台错误类型分离

### P0-3. 更完整的 provider 能力画像

ArcReel 已经有 provider abstraction，这是强项，但继续升级时最值得补的是：

- 更细粒度 capability matrix
- 参数兼容性声明
- 失败模式与限制说明
- fallback 和替代建议

为什么重要：

- 多供应商平台最常见的问题不是“接不进去”
- 而是“接进去了但行为并不等价”

建议方向：

- 在 `ImageBackend` / `VideoBackend` / `TextBackend` 协议之上，再补一层 capability profile
- 让 UI、workflow、成本估算、参数编辑器都能读取这个画像

## 四、P1：知识资产与创作记忆

### P1-1. 从项目状态升级到创作知识资产层

ArcReel 现在已经有很强的 project state，但还缺一层更高价值的东西：

- 风格经验
- 成功 prompt 模式
- 角色一致性经验
- 常用镜头方案
- 剧本结构经验

为什么重要：

- 创作平台如果只记项目文件，而不沉淀创作资产，每个项目都像重新来
- 这会限制平台长期变聪明

建议方向：

- 建立 asset knowledge layer
- 按类型沉淀：
  - style recipes
  - character design patterns
  - storyboard prompt templates
  - failure / fix patterns

### P1-2. 建设案例库和复用层

和 `fault-diagnosis` 一样，ArcReel 也适合有自己的案例层，只不过它不是诊断案例，而是创作案例。

例如：

- 某类题材下什么分镜策略效果好
- 某个 provider 对某种镜头表现最好
- 某种风格参考图对最终一致性帮助更大

为什么有价值：

- 这会让 ArcReel 从“工作台”进一步升级成“创作经验平台”

建议方向：

- 把项目导出结果、成本、用户反馈、关键选择结构化
- 建立可检索案例摘要
- 后续可做创作建议和相似案例推荐

### P1-3. 补知识增强而不一定要重 RAG

ArcReel 当前不以 RAG 为核心，这没问题，但以后如果要增强创作质量，可以考虑的是“知识增强”，而不一定是传统文档 RAG。

更合适的方向可能是：

- prompt pattern library
- style reference memory
- successful pipeline patterns
- provider-specific heuristics

这和典型 FAQ 文档 RAG 不一样，更接近“经验知识库”。

## 五、P2：更高级的协作与平台生态

### P2-1. 更强的多 Agent 协作治理

ArcReel 现在的多 Agent 设计已经比较成熟：

- orchestrator skill
- focused subagent

如果未来要继续升级，我不建议追求“更多 Agent 数量”，而建议追求：

- 调度可观测
- 责任边界更清晰
- 子任务产物标准化

可以考虑的升级方向：

- subagent result contract
- richer coordinator policy
- cross-subagent artifact handoff metadata

### P2-2. 更强的团队协作能力

ArcReel 已经具备产品化基础，如果走向更强平台化，下一步很自然是：

- 多用户项目协作
- 审批节点
- 团队级资源与配额
- 团队资产库

为什么这一步后置：

- 因为团队能力会放大现有状态复杂度
- 先把治理和知识层做好，再加多人协作更稳

### P2-3. 更开放的平台生态

ArcReel 已经支持 OpenClaw 集成和 skill.md 暴露，这很好。

后续可以进一步考虑：

- 更清晰的外部 Agent 调用协议
- 插件或 skill marketplace
- 更开放的 provider extension interface

但这一步一定要晚于内部系统稳定化。

## 六、不建议现在优先做什么

### 1. 不建议优先继续扩更多供应商

原因：

- 当前更大的瓶颈是治理和一致性，而不是供应商数量

### 2. 不建议优先做超复杂的 swarm

原因：

- ArcReel 现在的 focused subagent 已经是很合适的复杂度
- 再加更多协作层，收益未必大于复杂度

### 3. 不建议优先做重 RAG

原因：

- ArcReel 的核心问题不是文档检索不足
- 更值得做的是创作经验资产化

## 七、一个可执行的阶段规划

### 版本 A：治理升级

建议包含：

- runtime trace
- error taxonomy
- provider capability profile
- 更清晰的跨层日志与诊断工具

### 版本 B：知识资产化

建议包含：

- style / prompt / storyboard patterns 库
- 创作案例结构化沉淀
- 可复用经验层

### 版本 C：协作平台化

建议包含：

- 更强团队协作
- 更强多 Agent contract
- 更开放平台接口

## 八、最后一句话记忆

如果用一句话记住 ArcReel 的升级方向，我建议记成这样：

> ArcReel 的下一阶段关键，不是再变“更会生成”，而是变得更可治理、更会沉淀经验、也更像真正的平台。
