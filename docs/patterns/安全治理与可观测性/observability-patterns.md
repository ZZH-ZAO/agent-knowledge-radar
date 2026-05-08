# 通用问题：Observability

## 1. 问题定义

Observability 解决的是：Agent 系统如何记录模型调用、工具执行、权限决策、错误、耗时、token、上下文变化和用户可见状态，以便调试、回放、评估和治理。

## 2. 为什么重要

- Agent 行为链路长，失败原因不总在模型本身。
- 工具执行和权限决策需要审计。
- 长任务需要可恢复和可回放。
- 产品化后需要理解真实用户使用和错误模式。

## 3. 常见错误做法

- 只记录最终回答。
- 不记录工具输入输出。
- 没有 trace id 或 session id。
- telemetry 和本地 debug 日志边界不清。

## 4. 成熟系统通常怎么做

- Structured Logs
- Traces / Spans
- Tool Execution Events
- Model Request Metadata
- Permission Decision Events
- Error Taxonomy
- Session Replay
- Privacy Controls

## 5. 优秀项目案例

| 项目 | 值得学习的点 | 证据 |
| --- | --- | --- |
| anthropics/claude-code | 官方 CHANGELOG 持续出现 telemetry、managed settings、企业配置等产品化信号 | `docs/anthropics-claude-code-official-distillation.md` |

## 6. 可迁移技术框架

```text
Session
  -> Model Event
  -> Tool Event
  -> Permission Event
  -> Error Event
  -> Trace / Metrics
  -> Local Debug / Remote Telemetry Boundary
```

## 7. 我的项目行动项

- [ ] 给每次任务分配 session id。
- [ ] 记录工具执行事件。
- [ ] 区分本地 debug 日志和远程 telemetry。

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“通用问题：Observability 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

### 1. 这件事到底考什么

这里真正考察的不是会不会调用一个 API，而是能不能把 Agent 对外部世界的行动放进可治理的执行管线。

如果只回答功能点，说明还停留在“看过项目”的层面；如果能回答问题来源、工程约束、取舍和行动项，才说明这份沉淀真正进入了自己的方法论。

### 2. 口语版回答

我会把工具调用理解成 Agent Runtime 的行动边界。成熟系统不能只关心函数能不能执行，还要关心输入协议、权限分级、执行隔离、结果压缩、错误恢复和审计回放。否则模型一旦误调工具，风险会直接落到真实文件、浏览器、网络或业务系统上。

这段回答可以直接用于复盘、面试或方案评审。它的结构是：先定义问题，再讲工程边界，最后落到可迁移做法。

### 3. 工程视角拆解

可以按四层来理解：

- 问题层：这个设计到底在解决什么不稳定、不可控或不可复用的问题。
- 机制层：它用了哪些结构、协议、运行时、文档或流程来解决。
- 证据层：有哪些 README、源码、指标、案例或平台行为能证明它不是口号。
- 迁移层：它对 `claude-code-sourcemap`、知识平台、Project Radar 或面试训练有什么可执行启发。

### 4. 常见误区

把 MCP 或 Tool Calling 当成普通 API wrapper，只写 schema，不写权限、结果治理和失败恢复。

另一个常见误区是只把优秀项目当作模板照抄。真正应该学的是它为什么这样拆分，以及这个拆分在自己的场景里是否仍然成立。

### 5. Trade-off 与边界

治理越完整，接入成本越高；但如果工具有副作用，前期省掉治理，后期会以安全事故、上下文爆炸和不可复现的形式还回来。

判断一个方案是否成熟，不是看它有没有更多能力，而是看它有没有明确说明代价、适用场景和不适用场景。

### 6. 当前项目行动项

- [ ] 给每个工具补齐 riskLevel、permission、resultPolicy、auditTrail，并在平台中把相关项目和工具治理 pattern 关联起来。
- [ ] 把这份文档中的通用问题同步到对应 `docs/patterns/` 文档，避免停留在单项目笔记。
- [ ] 在平台详情页中保留“口语版回答、工程拆解、误区、行动项”，让它能直接用于学习和面试表达。

### 7. 面试官追问

**追问：这个项目或方案最值得学习的不是功能，而是什么？**

答：最值得学习的是它如何把一个模糊问题变成可治理的工程结构。功能只是表层，真正可迁移的是它的边界划分、执行流程、证据链和取舍。

**追问：如果迁移到当前平台，第一步应该做什么？**

答：第一步不是照搬实现，而是把它抽象成平台中的一个通用问题，补齐文档、索引、行动项和验证方式，让后续沉淀能自动进入平台展示。

## 行业痛点研究版补充

> 目标：把“通用问题：Observability”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

### 1. 它对应的行业痛点

Agent 接入外部工具后，行业共性痛点是权限、结果大小、执行副作用、工具质量和可观测性会同时失控。优秀项目不会把工具当普通函数，而会把它放进 Tool Runtime / MCP Integration 的治理管线。

判断它是不是值得持续沉淀，不看它是否新奇，而看它能不能解释一个反复出现的行业问题，并能不能给当前项目带来可执行改变。

### 2. 可作为证据的来源类型

GitHub 工具型项目、MCP server、旧体系工具文档、源码 README、浏览器自动化案例。

后续如果新增 GitHub、优质博客、论文或你提供的文档，都应该先判断它能否补强这一类证据，而不是直接堆进知识库。

### 3. 优秀项目或资料的共性做法

共性做法是 Tool Registry + Permission Mapping + Result Summary + Artifact Reference + Audit Trail，把调用、权限、结果和追踪拆开治理。

这里真正要学的不是表层功能名，而是成熟项目如何划分边界、控制风险、组织证据、形成可复用流程。

### 4. 数据支撑与判断信号

可观察信号包括工具数量、权限等级覆盖率、单次结果 token 数、artifact 引用比例、失败调用可复现率。

这些信号用于避免主观判断。后续平台应该让痛点页自动展示证据项目数、来源类型、关联方案数和行动项数量。

### 5. 给当前项目的启发

这份文档应该反哺 `claude-code-sourcemap` 的三个位置：

- 项目页：说明它作为样本值得学习什么。
- 痛点页：说明它补强了哪个 Agent / 大模型行业共性问题。
- 方案页：说明它能沉淀成什么可迁移框架。

### 6. 当前项目行动项

- [ ] 把该文档关联到 Tool Runtime / MCP 行业痛点，并检查是否能补充工具权限、结果治理或审计行动项。
- [ ] 检查它是否需要更新 `docs/pain-points/` 的行业痛点说明。
- [ ] 检查它是否需要更新 `docs/patterns/` 的通用技术框架。
- [ ] 如果它来自外部资料，把它登记到 `docs/source-library/` 或 Project Radar 候选池。

### 7. 自动进化规则

每次新增相关资料后，按以下顺序更新：

```text
资料源
  -> 行业痛点
  -> 证据项目/资料
  -> 共性做法
  -> 数据支撑
  -> 当前项目行动项
  -> 面试官追问
```

## Pico 源码补充：可观测性不是日志，而是可回放运行合同

### 1. `pico` 给了一个很好的判断标准

很多项目会说自己“有 trace”“有 report”，但真正值得学的是:

> 这些产物是不是运行协议的一部分，而不是调试时顺手打印的副产物。

`pico` 在这件事上已经走得比较清楚了。`run_store.py` 把运行期产物拆成四类:

- `session.json`：恢复现场
- `task_state.json`：记录任务级状态机
- `trace.jsonl`：追加式过程事件流
- `report.json`：最终结果摘要

这四类产物职责分离得很明确，所以后续无论是做回放、诊断、评估还是前端展示，都有稳定抓手。

### 2. 为什么 `jsonl trace + atomic report` 是成熟信号

`trace.jsonl` 用追加式写入，`task_state` 和 `report` 用原子写入。这个实现细节很值得学，因为它说明作者考虑的不是“能不能写日志”，而是:

- 长任务中途失败时，过程证据能不能尽量留下
- 最终结果文件能不能避免半截 JSON
- 恢复、审计、回归时，读取语义是不是稳定

很多系统在这一步会把所有信息混在一个大对象里，短期看省事，长期会让恢复、比对和增量分析都变得很重。

### 3. `metrics.py` 真正补上的，是“证据怎么变成判断”

`pico` 的 `metrics.py` 不只是汇总通过率，它还把运行期信号转成可以解释的指标:

- `pass_rate`
- `avg_tool_steps`
- `avg_attempts`
- `cache_hit_rate`
- `cached_token_ratio`
- `prefix_reuse_rate`
- `avg_run_duration_ms`
- `avg_tool_duration_ms`
- `avg_prompt_build_duration_ms`
- `tool_status_counts`
- `security_event_counts`
- `stop_reason_counts`

这套指标特别有价值，因为它把“系统好不好”拆成了几条不同维度:

- 结果层：到底过没过
- 效率层：用了多少步、多少尝试
- 成本层：缓存和 prompt 是否复用
- 运行层：慢在哪里
- 风险层：安全事件和 stop reason 是什么

### 4. 评估闭环为什么比单次 demo 更重要

`aggregate_benchmark_artifact()` 和 `aggregate_run_artifacts()` 说明 `pico` 已经在做两层证据汇总:

- benchmark 侧：任务是否通过、失败类型是什么
- run 侧：真实运行时的 tool / prompt / cache / duration 信号

这比只看 pass rate 强很多。因为 pass rate 上升，并不自动代表系统更成熟，它也可能意味着:

- prompt 变长了
- 尝试次数更多了
- cache 没命中
- 风险动作更多了

一个成熟平台要能同时看“结果变好了没有”和“代价变坏了没有”。

### 5. 对行业痛点的抽象

Agent 行业在可观测性上的共性痛点，通常不是“没有日志”，而是下面几件事同时缺位:

- 过程事件不可重建
- 结果文件不可比较
- 失败原因没有 taxonomy
- 成本信号没有进入评估
- 安全事件和业务效果分开统计

`pico` 的做法给了一个很好的最小框架:

```text
Run Artifact
  -> session
  -> task_state
  -> trace
  -> report
  -> benchmark aggregate
  -> run aggregate
```

### 6. 我们平台后续应该怎么接

- 项目页不要只展示“这个项目有 trace”，要展示 `trace / report / metrics / failure taxonomy` 各自解决什么问题
- 痛点页要把“缺少失败分类”“只有 pass rate 没有代价指标”“过程不可回放”列为行业共性痛点
- 自动沉淀时，优先抽取项目是否具备 `event log`、`artifact split`、`failure taxonomy`、`cost metrics` 四类信号

## 自动回写补充

<!-- AUTO-WRITEBACK:anthropics-claude-code-observability-patterns:START -->
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
<!-- AUTO-WRITEBACK:anthropics-claude-code-observability-patterns:END -->
