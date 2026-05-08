# 通用问题：Tool Runtime

## 1. 问题定义

Tool Runtime 真正要解决的，不是“模型怎么触发一个函数”，而是“模型一旦开始对外部世界动手，它的行动怎么被约束、解释、恢复和复盘”。

只要工具开始接触文件、命令、浏览器、网络、数据库或外部服务，问题就从调用问题变成了治理问题。

## 2. 为什么普通做法不够

很多系统一开始把工具接上就觉得差不多了，后面才发现所有难题都在工具层暴露：

- 模型会误调工具
- 参数看起来合法，但语义上根本不该执行
- 工具结果太大，直接把上下文撑爆
- 有副作用的工具一旦出错，很难说清到底改了什么
- 工具越来越多以后，权限、审计、结果格式全部发散

这说明普通做法只解决了“能调”，没有解决“调了以后怎么稳定工作”。

## 3. 典型方案结构

成熟 Tool Runtime 至少要有下面这些部分：

```text
Tool Definition
  -> Input Validation
  -> Semantic Validation
  -> Risk Classification
  -> Permission Policy
  -> Execution Adapter
  -> Result Normalization
  -> Transcript / Audit
```

这里面最关键的不是模块名，而是顺序。真正成熟的运行链不是“模型决定 -> 工具执行”，而是：

```text
模型提议动作
  -> 校验参数
  -> 判断风险
  -> 命中权限策略
  -> 执行
  -> 归一化结果
  -> 写入证据链
```

## 4. 成熟系统通常怎么做

### 4.1 先统一工具注册，而不是让每个工具各写各的

一旦工具数上来，最先崩的不是模型，而是工程组织。成熟系统会先把工具收进统一注册表，至少为每个工具补齐这些元数据：

- name
- category
- source
- riskLevel
- stateful
- artifactPolicy
- permission

### 4.2 再把“校验”分成两层

很多人只做 schema 校验，但这还不够。真正稳定的 Tool Runtime 至少要分：

- 结构校验：字段齐不齐、类型对不对
- 语义校验：这次动作在当前上下文里合不合理

比如“删除文件”这个动作，schema 再合法，也不代表此刻就该做。

### 4.3 把结果当协议，而不是当自由文本

Tool Runtime 最容易被低估的，是结果结构。成熟系统会明确区分：

- 小结果：直接结构化返回
- 中结果：摘要 + 关键字段
- 大结果：artifact reference
- 专家结果：insight + evidence ref + next actions

如果没有这层，系统很容易出现“工具很强，但结果没人能用”的问题。

### 4.4 工具有副作用时，必须把审计和恢复一起做进去

只要工具可能改文件、发请求、点浏览器、写状态，执行层就不能只关心成功与否，还要记录：

- 输入是什么
- 改了什么
- 哪一步失败
- 是否需要确认
- 后续怎么恢复

## 5. 常见错误做法

### 5.1 把工具当普通函数直接调用

这会让风险判断、审计、恢复全部散在各处，最后每个工具都像一套小系统。

### 5.2 只有 schema，没有语义边界

很多误调用不是因为 JSON 格式错了，而是因为动作本身在当前时机不合理。

### 5.3 结果直接拼自由文本

这样最开始看着快，后面很快会变成：

- 模型难复用
- 搜索难命中
- 审计难回放
- artifact 无法管理

### 5.4 不区分观察型工具和高风险工具

如果 screenshot、grep、write_file、bash、browser click 全都按一个级别处理，权限系统最终一定会失真。

## 6. 证据项目

### 6.1 anthropics/claude-code

它给出的最强证据，是公开产品层已经把 settings、hooks、MCP、commands、subagents 这些能力摆成了正式边界。说明工具治理不是后补功能，而是 runtime 主线。

### 6.2 ChromeDevTools/chrome-devtools-mcp

它证明了工具结果治理和 artifact reference 是一等问题。浏览器工具不是不能强，而是必须在“强能力”和“可消费结果”之间做重新包装。

### 6.3 zzh/pico

它在本地 runtime 里已经把 tool execution 放进了受控执行链：参数、路径、审批、trace、memory 更新、checkpoint 都被纳入主循环。

## 7. Trade-off 与边界

### 7.1 治理越完整，接入成本越高

这几乎是不可避免的。你会多写很多元数据、日志、权限逻辑、结果结构、恢复逻辑。但工具一旦有副作用，这些成本迟早都要付。

### 7.2 不是所有工具都需要同样重的治理

只读观察型工具可以更轻；高风险、强副作用、强状态的工具必须更重。关键不是一刀切，而是风险分层。

## 8. 我的项目行动项

- [ ] 给平台里的工具沉淀增加固定字段：`category / source / riskLevel / stateful / artifactPolicy`。
- [ ] 把工具结果结构统一成 `summary / structuredData / artifactRefs / nextActions`。
- [ ] 后续项目沉淀时，把“工具是怎么被治理的”作为固定阅读视角，而不是只看工具名。
- [ ] 在痛点页里持续回写工具结果过大、权限失真、副作用不可追踪这几类高频问题。

## 自动回写补充

<!-- AUTO-WRITEBACK:anthropics-claude-code-tool-runtime:START -->
### Anthropics/claude-code

- 命中原因：来自项目已有 relatedPatterns
- 来源项目：`anthropics-claude-code`
- 项目地址：https://github.com/anthropics/claude-code
- 草稿文件：`docs/external-projects/Claude Code ???????/anthropics-claude-code.md`

#### 新增证据项目

???????????????????????????????????????????????????????????????????????

#### 项目里的具体做法

Claude Code ?? terminal ??????????? settings?hooks?commands?MCP?subagents?skills ?????????????????????????????????????????????????

#### 对当前平台的直接启发

- ?????????? Tool Runtime?MCP Integration ? Productization ????
<!-- AUTO-WRITEBACK:anthropics-claude-code-tool-runtime:END -->
