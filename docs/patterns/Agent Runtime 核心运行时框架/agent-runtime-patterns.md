# 通用问题：Agent Runtime

## 1. 问题定义

`Agent Runtime` 解决的不是“怎么发起一次模型调用”，而是“怎么让模型在真实环境里持续做事，并且整个过程可控、可解释、可恢复、可验证”。

如果把问题说得再具体一点，它关心的是六件事：

- 任务是怎么开始的
- 上下文是怎么组织的
- 工具是怎么进入执行链的
- 副作用是怎么被约束的
- 中断后怎么恢复
- 一次运行结束后，证据怎么留下来

没有这六件事，系统就更像一个会话壳；有了这六件事，系统才更接近正式 runtime。

## 2. 为什么普通做法不够

很多 Agent 项目在最开始都能跑起来，但很快会卡在同一类问题上。根本原因不是模型不够强，而是系统把太多责任堆进了同一个黑盒里。

典型症状是：

- prompt 里什么都塞，最后谁都救不了上下文膨胀
- 工具能调用，但失败后说不清是模型错、参数错还是环境错
- 任务中断以后只能“重新开始”，没有可信恢复
- UI、工具、状态、评估缠在一起，功能一多就散

这说明普通做法只解决了“能不能跑”，没有解决“跑起来之后怎么长期稳定”。

## 3. 典型方案结构

一个成熟的 Agent Runtime，至少应该能被拆成下面这几个稳定部分：

```text
User Entry
  -> Session / Task State
  -> Context Builder
  -> Model Loop
  -> Tool Runtime
  -> Permission / Policy Layer
  -> Memory / Checkpoint
  -> Trace / Report / Eval
  -> UI or API Adapter
```

这里最重要的不是模块名，而是职责边界：

- `Session / Task State` 负责回答“现在进行到哪一步了”
- `Context Builder` 负责回答“这一轮到底该给模型什么”
- `Tool Runtime` 负责回答“允许做什么、怎么做、失败了怎么算”
- `Permission / Policy` 负责回答“高风险动作什么时候需要拦”
- `Memory / Checkpoint` 负责回答“系统怎样带着现场继续工作”
- `Trace / Eval` 负责回答“这次运行到底有没有价值”

## 4. 成熟系统通常怎么做

### 4.1 先把一次运行变成有名字的对象

成熟系统不会把一次执行藏在一段对话里，而是会把它落成 `task / session / run / checkpoint / report` 这些对象。这样做的价值不是“结构更美观”，而是后续才能：

- 复盘
- 恢复
- 比较
- 回归
- 统计

`pico` 已经在本地 runtime 里把这件事做得很清楚：`TaskState` 记录运行状态，`RunStore` 负责工件落盘，`report.json` 和 `trace.jsonl` 让一次运行不再只是聊天记录。

### 4.2 再把工具调用从“函数调用”升级成“执行协议”

工具难的地方从来都不是 schema，而是执行协议。成熟运行时通常会把下面这些东西一起处理：

- 参数校验
- 路径边界
- 权限等级
- 执行前确认
- 副作用跟踪
- 结果压缩
- 错误分类

这也是为什么 `Claude Code` 这种产品会把 settings、hooks、MCP、commands 单独做成公开产品概念。因为工具一旦进入真实仓库，就不能再只是“函数列表”。

### 4.3 上下文不是拼接字符串，而是预算治理

真正成熟的 Context Engineering，不是“把更多上下文塞给模型”，而是“用更少但更对的上下文完成当前任务”。这意味着 runtime 必须回答：

- 当前任务最相关的上下文是什么
- 哪些历史可以压缩
- 哪些摘要已经过期
- 哪些结果应该变成 artifact，而不是继续塞回 prompt

`pico` 在这点上已经给了很好的源码信号：`context_manager.py`、`memory.py`、freshness / invalidation 机制，说明它开始把上下文当预算治理问题来做，而不是自由文本累加。

### 4.4 恢复能力必须恢复“现场”，而不是恢复“旧聊天”

很多项目把 resume 理解成“把上一次消息再喂回来”。这其实是最容易失真的地方。成熟 runtime 真正要恢复的是：

- 当前任务状态
- 关键文件的新鲜度
- 当前工作区是否一致
- 当前工具签名和配置是否一致
- 上次执行留下的证据能不能继续接上

没有这层，系统只能做 demo；有了这层，系统才有资格承担真实工作。

### 4.5 评估闭环不是最后补一个 benchmark，而是从一开始就进入结构

如果 trace、report、metrics、benchmark 是最后才补的，说明系统一开始并没有按可验证方式设计。成熟做法应该是：运行时一开始就为评估留接口。

这样做的结果是，评估不再只是“跑几道题”，而是能反推：

- 哪类任务容易失败
- 哪一步最耗成本
- 哪种上下文策略更稳
- 哪类工具最容易出错

## 5. 常见错误做法

### 5.1 把 Agent Runtime 做成一层 API wrapper

这类系统表面上也能跑，但一旦任务变长、工具变多、风险变高，就会迅速暴露出边界缺失。

### 5.2 把 UI 当成 runtime 本体

很多项目其实是“一个好看的聊天壳”，不是 runtime。只要离开这个 UI，它的状态管理、工具执行、恢复能力就都不成立。

### 5.3 把 memory 当聊天历史

聊天历史是记录，不是记忆。真正的 memory 系统应该能做筛选、分层、过期、检索和注入。

### 5.4 把 resume 当重新读历史

如果恢复时没有核对环境、文件和运行身份，resume 只是在制造“我好像接上了”的错觉。

## 6. 证据项目

### 6.1 anthropics/claude-code

它给出的关键证据不是某个单点实现，而是公开产品结构已经明确区分了：

- terminal / IDE / GitHub 入口
- settings
- hooks
- slash commands
- subagents
- MCP
- memory

这说明它已经把 runtime 当成产品核心，而不是隐藏在对话后面的实现细节。

### 6.2 zzh/pico

它给出的关键证据是源码级拆分已经落地：

- `runtime.py`
- `task_state.py`
- `run_store.py`
- `memory.py`
- `context_manager.py`
- `evaluator.py`
- `metrics.py`

这类结构最有价值的地方是，它已经能把运行状态、工具副作用、恢复协议和评估闭环拆开讲清楚。

## 7. Trade-off 与边界

### 7.1 Runtime 越正式，前期工程成本越高

你需要多写状态对象、工件结构、权限规则、恢复逻辑和评估闭环。这些工作短期看起来不像“在做功能”，但它们决定了系统后面能不能稳定扩展。

### 7.2 并不是所有项目都值得一开始做重 runtime

如果只是个人实验、一次性脚本或单轮辅助工具，过早引入完整 runtime 结构会显得过重。真正需要它的场景通常同时满足：

- 多步任务
- 真实副作用
- 长时间使用
- 可恢复需求
- 评估需求

## 8. 我的项目行动项

- [ ] 在知识平台索引里，把项目的 `问题 / 做法 / 边界 / 行动项` 作为固定 section，而不是只展示 summary。
- [ ] 继续把 `Claude Code` 和 `pico` 的 runtime 证据回写到项目页、痛点页和面试页，形成统一证据链。
- [ ] 在后续沉淀模板里固定增加四个问题：主循环在哪里、工具协议在哪里、恢复协议在哪里、评估闭环在哪里。
- [ ] 平台后续增加“按运行时能力过滤项目”的视图，比如只看有 checkpoint、有 tool governance、有 eval 的项目。

## 自动回写补充

<!-- AUTO-WRITEBACK:anthropics-claude-code-agent-runtime:START -->
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
<!-- AUTO-WRITEBACK:anthropics-claude-code-agent-runtime:END -->
