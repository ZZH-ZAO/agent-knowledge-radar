# ByteDance--Auto_prd_test_agent 改进后架构讲稿版

## Summary

- Project name: ByteDance--Auto_prd_test_agent
- Project path: `D:\测开\ByteDance--Auto_prd_test_agent`
- Document type: user
- Purpose: present the improved architecture of this project in a lecture-style, easy-to-explain format that can be used for review, teaching, or project discussion

## 一、这次我们不是在讲“一个测试生成小工具”，而是在讲“一个测试 Agent 系统怎么长出来”

如果我要用一句话来介绍这个项目改进后的方向，我会这样说：

> 它会从一个“PRD 转测试用例的生成工作台”，升级成一个“围绕知识检索、规则证据、人工修订、AI 评审、坏例回流和回归验证共同运转的测试 Agent 系统”。

这句话里最重要的，不是“Agent”两个字，而是后面那几个能力：

- 知识检索
- 规则证据
- 人工修订
- AI 评审
- 坏例回流
- 回归验证

因为真正决定这类系统上限的，往往不是模型会不会说，而是系统能不能形成闭环。

## 二、先看现在这个项目为什么已经有价值

这个项目现在其实已经有几个不错的基础：

1. 有明确场景
   它不是泛化聊天，而是 PRD 转测试用例
2. 有结构化输出
   它不是只给一段文本，而是给 JSON / 表格 / 导出结果
3. 有 RAG
   它已经知道不能只靠模型常识
4. 有人工微调
   它不是一次性生成器
5. 有 evaluator
   它已经开始做质量检查了

所以它不是一个“空壳 Agent Demo”，而是一个已经摸到垂直工作流产品边缘的项目。

但问题也很明显：

- 编排还集中在 UI
- 检索还偏轻
- 评审还没有形成长期闭环
- 记忆还没有走向学习型资产

所以它最值得做的不是“加更多 feature”，而是“把现有链条做厚、做稳、做闭环”。

## 三、改进后的整体架构可以分成七层

为了让大家好理解，我把它拆成七层。  
这七层不是为了显得复杂，而是因为七层各自解决的是不同问题。

### 第一层：产品交互层

解决：

- 用户怎么看、怎么改、怎么审

改进后，前端最好不是一个页面，而是五个工作区：

1. 输入与接入
2. 检索与证据
3. 生成工作区
4. 质量评审
5. 坏例与回归

这一层借鉴了什么：

- 借了 `fault-diagnosis` 的“过程可见性”
- 借了 `repomind` 的“review / verification 面板意识”

为什么这样更好：

- 用户不再只看到“结果”，还能看到“依据”和“问题”

### 第二层：工作流编排层

解决：

- 整个系统的流程怎么推进

这里建议把原来堆在 UI 的逻辑拆到 `services/`，变成：

- ingestion
- retrieval
- generation
- evaluation
- badcase
- benchmark

这一层借鉴了什么：

- 借了 `career-ops` 的 workflow-first
- 借了 `deer-flow` 的 app / runtime 拆层

为什么这样更好：

- 逻辑更清楚
- 更容易测试
- 更容易换前端、接 API

### 第三层：检索与证据层

解决：

- 系统到底要拿什么知识来约束生成

这里不能只做语义检索，而应该做：

- semantic retrieval
- keyword retrieval
- rerank
- evidence assembly

尤其关键词检索很重要，因为测试用例生成特别依赖：

- 业务词
- 规则词
- 逻辑连接词

这一层借鉴了什么：

- 借了 `fault-diagnosis` 的证据链意识
- 借了 `repomind` 的 verification-first 思路

为什么这样更好：

- 检索不再只是“主题像不像”
- 而是“这段内容对测试生成有没有真实价值”

### 第四层：生成与评审层

解决：

- 怎么从证据走到测试资产
- 怎么判断它质量够不够

这层应该形成三段闭环：

1. 生成
2. 微调
3. 评审

这一层借鉴了什么：

- 当前项目本身已有共创 + evaluator 雏形
- `career-ops` 的阶段化任务理解
- `repomind` 的 verification-first

为什么这样更好：

- 系统不是“一次性生成”，而是“生成后还能持续修正和验证”

### 第五层：记忆与资产层

解决：

- 好结果怎么沉淀
- 系统以后怎么变得更贴团队习惯

这一层要分成三层 memory：

1. session memory
2. case memory
3. learning memory

这一层借鉴了什么：

- `fault-diagnosis`：session memory 的边界意识
- `deer-flow`：异步 memory 更新
- `claude-code`：memory 走向共享知识资产

为什么这样更好：

- 把“当前状态”跟“长期知识”分开

### 第六层：质量与验证层

解决：

- 系统到底变好了还是变坏了

这里必须有三样东西：

1. metrics
2. bad-cases
3. benchmarks

这一层借鉴了什么：

- `repomind`：verification lifecycle
- `claude-code`：可观测性和实验治理

为什么这样更好：

- 不再靠感觉优化
- 有指标、有坏例、有回归

### 第七层：平台治理层

解决：

- 新能力怎么安全上线

这里至少要有：

- feature flag
- experiment group
- observability

这一层借鉴了什么：

- `claude-code`

为什么这样更好：

- 新检索策略、新 rerank、新规则都能灰度试验

## 四、为什么这个项目特别适合走“混合检索 + 证据层”这条路

这一点值得单独讲。

因为很多人会想：

- 都有 embedding 了，为什么还要关键词检索？

原因就在于测试生成和通用问答不一样。

测试生成特别依赖这些信息：

- 必须
- 禁止
- 至少
- 超时
- 锁定
- 空值
- 连续失败

这些内容很多时候语义上没那么“特别”，但测试价值极高。  
所以如果只做语义检索，很可能主题相关，但规则漏掉。

所以这类项目特别适合：

- 语义检索保广度
- 关键词检索保规则命中
- rerank 保前列质量

## 五、为什么 bad-case 面板是很关键的一层

很多团队会做：

- 检索
- 生成
- 评审

但不做 bad-case review。

结果就是：

- 平均指标看起来还行
- 但总有几个特别痛的 case 老是出错

所以 bad-case 面板的价值在于：

- 把失败显性化
- 把失败分类化
- 把失败变成可回归资产

这一步借鉴最多的是 `repomind`。

因为 `repomind` 最强的一点，就是它不只给结论，还很重视：

- verification
- false positive
- 修复后再验证

对测试 Agent 来说，这种思想非常值钱。

## 六、为什么记忆层要异步更新

这点很多人一开始不容易想到。

如果你把这些动作全放在主流程里：

- 模板抽取
- 坏例模式沉淀
- benchmark 更新
- 质量统计

用户会感觉系统越来越慢。

所以更合理的是：

- 主流程只做当下任务需要的
- 长期沉淀动作异步做

这一点明显借鉴了 `deer-flow`。

它提醒我们：

> memory 不只是“记住了什么”，还包括“什么时候更新、怎么更新、更新会不会拖慢主流程”。

## 七、如果让你记住这个改进方案的核心，不要记细节，记这三句话就够了

### 第一句

不要把这个项目继续当作“测试生成小工具”做，要把它当作“测试知识系统”做。

### 第二句

不要只优化模型输出，要同时优化：

- 检索
- 证据
- 评审
- 坏例
- 回归

### 第三句

不要硬搬别的项目的完整形态，而要按缺什么借什么：

- 缺 workflow，就借 `career-ops`
- 缺证据透明，就借 `fault-diagnosis`
- 缺验证闭环，就借 `repomind`
- 缺分层和异步记忆，就借 `deer-flow`
- 缺灰度和治理，就借 `claude-code`

## 八、最后一句话总结这份讲稿

> 改进后的 `ByteDance--Auto_prd_test_agent`，最重要的变化不是多了几个 feature，而是它开始从“能生成结果”走向“能解释结果、能验证结果、能沉淀结果、能持续改进结果”。
