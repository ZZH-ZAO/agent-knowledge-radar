# 优质项目学习沉淀操作手册

> 目标：把搜集到的优质项目，从“看过、收藏过”转化成“能学习、能复用、能指导自己项目建设”的知识资产。  
> 适用对象：Agent、LLM 应用、开发工具、工程平台、开源框架、优秀产品型项目。  
> 推荐用法：每看一个项目，都按这份手册产出一份项目沉淀，并同步更新通用问题库。

## 1. 最重要的原则

看优秀项目时，不要停在“它有哪些功能”。真正有价值的学习链路是：

```text
项目功能
  -> 它解决的通用问题
  -> 它采用的优秀技术/框架
  -> 可迁移的设计原则
  -> 我自己的项目可以怎么用
```

举例：

```text
Claude Code 支持 MCP
  -> 通用问题：Agent 如何统一接入外部工具生态？
  -> 技术框架：Tool Registry + Transport Adapter + Auth + Permission Mapping + Observability
  -> 可迁移原则：外部工具进入系统后，要变成统一工具池的一部分
  -> 行动项：给自己的工具系统补工具注册表、权限字段、错误格式、执行日志
```

这份手册的核心就是帮助你把每个项目都转成这种结构化结果。

## 2. 推荐目录结构

建议在 `docs/` 下建立三类文档。

```text
docs/
  external-projects/
    anthropics-claude-code.md
    openhands.md
    aider.md

  patterns/
    agent-engineering-framework.md
    tool-runtime-patterns.md
    memory-system-patterns.md
    plugin-system-patterns.md
    permission-sandbox-patterns.md
    multi-agent-patterns.md
    observability-patterns.md

  project-radar/
    candidates.md
    discovery-log.md
    scoring-rules.md
```

三类文档的职责不同：

- `external-projects/`：记录单个项目本身，回答“这个项目为什么值得学”。
- `patterns/`：抽取多个项目背后的通用问题和技术框架，回答“这类问题应该怎么设计”。
- `project-radar/`：记录候选项目、评分、筛选理由，回答“接下来值得看什么”。

## 3. 一次完整沉淀的流程

拿到一个项目后，按下面 7 步走。

### 第 1 步：快速判断是否值得沉淀

先用 10 到 20 分钟做粗筛，不要一上来就深读。

检查这些信息：

- 项目解决什么问题？
- 是否和当前学习主题相关？
- README 是否清晰？
- 是否有源码、文档、示例、CHANGELOG？
- 最近是否还在维护？
- 它是否有可迁移的架构或工程方法？
- 它是完整产品，还是薄壳 demo？

快速结论分三档：

```text
High：值得深度沉淀
Medium：先做简短卡片，后续再看
Low：只记录链接，不进入沉淀
```

### 第 2 步：建立项目信息卡

每个项目先写一张卡片，放到 `docs/project-radar/candidates.md` 或单项目文档开头。

模板：

```md
## 项目：owner/repo

- URL:
- 类型：工具 / 框架 / 平台 / SDK / 产品 / 研究项目
- 主题：Agent / MCP / Tool Runtime / Memory / Prompt / Multi-Agent / DevTools
- 一句话：这个项目解决什么问题
- 适合学习：架构 / 工程化 / 交互 / 插件 / 安全 / 产品化
- 推荐等级：High / Medium / Low
- 推荐理由：
- 风险或不足：
- 建议沉淀角度：
```

### 第 3 步：收集资料证据

沉淀不是凭印象写，要有证据链接。

优先看这些材料：

- `README.md`：产品定位、核心功能、安装方式。
- `docs/`：设计理念、使用指南、架构说明。
- `examples/`：真实用法。
- `CHANGELOG.md` / Releases：演进方向和真实问题。
- `src/`：核心实现。
- `issues` / `discussions`：用户痛点。
- `plugins` / `templates` / `packages`：扩展生态。

记录时用这种格式：

```md
## 证据链接

- README:
- Docs:
- Architecture:
- Examples:
- CHANGELOG:
- Core source:
- Related issues:
```

### 第 4 步：写单项目沉淀

每个值得深读的项目，都产出一份单项目沉淀文档。

文件名建议：

```text
docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md
```

模板：

```md
# 项目沉淀：owner/repo

> 来源：
> 沉淀日期：
> 推荐等级：
> 学习主题：

## 1. 项目一句话

用一两句话说明它是什么，给谁用，解决什么问题。

## 2. 为什么值得学

不要只列功能，要说明它的学习价值：

- 它解决了什么真实工程问题？
- 它在哪些设计上比普通项目更成熟？
- 它对我的项目有什么启发？

## 3. 核心场景

写清楚用户为什么需要它：

- 用户是谁？
- 用户在什么场景下使用？
- 这个项目替用户省掉了什么复杂度？

## 4. 它解决的通用问题

把功能翻译成问题。

示例：

- 外部工具如何统一接入 Agent Runtime？
- 长上下文如何裁剪、压缩和恢复？
- 高风险工具如何做权限、安全和审计？
- 多 Agent 如何分工、通信和合并结果？
- 插件如何把团队经验产品化？

## 5. 优秀技术和框架

按技术模块拆：

- 架构分层：
- 核心 runtime：
- 数据模型：
- 插件/扩展：
- 权限/安全：
- 可观测性：
- UI/交互：
- 部署/分发：

## 6. 可迁移设计原则

把项目做法抽象成自己的原则。

示例：

- 工具调用不是函数调用，而是一条 runtime pipeline。
- Memory 首先要区分 scope、lifecycle、visibility。
- 插件应该是能力包，而不是单个命令。
- 权限系统要和执行系统绑定，而不是只做弹窗。

## 7. 对我当前项目的行动项

把学习结果变成可以做的事。

- [ ] 现在就能做：
- [ ] 需要调研后做：
- [ ] 暂时不做但保留方向：

## 8. 证据链接

- README:
- Docs:
- Source:
- CHANGELOG:
- Examples:
```

### 第 5 步：抽象成通用问题

单项目沉淀之后，一定要再问一句：

> 这个项目背后，反复出现的通用工程问题是什么？

常见通用问题可以这样分类。

#### Agent Runtime

- Agent 的主循环应该如何设计？
- UI、SDK、CLI、Remote 如何复用同一个执行内核？
- 一轮模型调用和多轮工具执行如何组织？

#### Context Engineering

- 哪些上下文应该进入模型？
- 长上下文如何压缩？
- 项目文件、历史记录、用户规则如何分层？

#### Prompt Runtime

- Prompt 如何模块化？
- 系统规则、项目规则、任务规则、动态状态如何组合？
- 专项 prompt 和主对话 prompt 如何分离？

#### Tool Runtime

- 工具如何注册、校验、调度、执行、回流？
- 并发、安全、权限、错误、日志如何统一治理？
- 外部工具和内建工具如何进入同一个工具池？

#### Memory System

- 记忆的作用域如何区分？
- 短期、长期、项目、团队、Agent 记忆如何分层？
- 记忆什么时候写入，什么时候注入上下文？

#### Permission & Sandbox

- 哪些操作是高风险？
- 如何做 allow / ask / deny？
- 沙箱、权限、审计、用户确认如何配合？

#### Plugin System

- 插件承载什么能力？
- command、agent、skill、hook、MCP、workflow 如何一起发布？
- 插件如何安装、校验、禁用、升级？

#### Multi-Agent

- 子 Agent 什么时候有价值？
- 多 Agent 如何分工？
- 谁负责规划、谁负责执行、谁负责合并？
- 通信、权限、上下文隔离如何设计？

#### Observability

- Agent 做了什么，如何记录？
- 工具执行、模型调用、错误、耗时、token 如何追踪？
- 用户和开发者如何回放问题？

#### Productization

- 如何安装、更新、配置？
- 如何跨平台运行？
- 如何适配企业代理、私有模型、组织策略？

### 第 6 步：更新通用问题库

每次沉淀完单项目，都要更新一个 `patterns/*.md` 文档。

例如项目里有很强的 Tool Runtime 设计，就更新：

```text
docs/patterns/Tool 与 MCP 工具体系/tool-runtime-patterns.md
```

通用问题库模板：

```md
# 通用问题：Tool Runtime

## 1. 问题定义

Agent 调用工具时，真正的问题不是“执行函数”，而是如何安全、可追踪、可恢复地让模型影响外部世界。

## 2. 为什么重要

- 模型输出可能不稳定。
- 工具有副作用。
- 用户需要知道 Agent 做了什么。
- 错误需要能恢复。

## 3. 成熟系统通常怎么做

- Tool Registry
- Schema Validation
- Semantic Validation
- Permission Policy
- Runtime Scheduler
- Sandbox / Isolation
- Tool Result Normalization
- Observability

## 4. 优秀项目案例

| 项目 | 值得学习的点 | 证据 |
| --- | --- | --- |
| Claude Code | 工具执行 pipeline、权限、安全、MCP | 链接 |
| OpenHands | 浏览器/终端/文件工具集成 | 链接 |

## 5. 可迁移框架

一个成熟 Tool Runtime 至少包括：

```text
Tool Definition
  -> Input Schema
  -> Safety Metadata
  -> Permission Check
  -> Execution Adapter
  -> Result Normalizer
  -> Transcript Writer
  -> Telemetry / Audit
```

## 6. 我的项目行动项

- [ ] 给每个工具定义风险等级。
- [ ] 增加统一 tool result 格式。
- [ ] 记录每次工具执行的输入、输出、耗时、错误。
```

### 第 7 步：沉淀成自己的技术框架

当你看过 5 到 10 个项目后，不要只保留项目笔记。要把它们收束成一份自己的总纲：

```text
docs/patterns/agent-engineering-framework.md
```

推荐结构：

```md
# Agent 工程通用问题与优秀技术框架

## 1. Agent Runtime
## 2. Context Engineering
## 3. Prompt Runtime
## 4. Tool Runtime
## 5. Memory System
## 6. Permission & Sandbox
## 7. Plugin System
## 8. Multi-Agent Collaboration
## 9. Observability
## 10. Productization
```

每一章都按这个固定结构写：

```md
## 主题名

### 问题定义
### 为什么重要
### 常见错误做法
### 成熟项目怎么做
### 可迁移设计框架
### 优秀项目案例
### 我自己的行动项
```

## 4. 项目评分表

为了避免随便收藏项目，可以给每个候选项目打分。

| 维度 | 分值 | 判断标准 |
| --- | ---: | --- |
| 相关性 | 20 | 是否和当前学习主题高度相关 |
| 工程质量 | 20 | 架构、代码、测试、文档是否扎实 |
| 学习价值 | 20 | 是否能抽象出通用问题和设计原则 |
| 活跃度 | 15 | 最近 commit、release、issue 是否活跃 |
| 完整度 | 10 | 是否有 README、docs、examples、CHANGELOG |
| 稀缺性 | 10 | 是否有独特设计，而不是普通 demo |
| 可迁移性 | 5 | 是否能直接启发自己的项目 |

推荐判断：

```text
85-100：必须深度沉淀
70-84：值得沉淀
55-69：做简短卡片
55 以下：只记录链接
```

## 5. 学习时的提问清单

看项目时，可以直接拿下面这组问题问。

### 产品问题

- 它服务谁？
- 用户为什么需要它？
- 它替用户减少了什么复杂度？
- 它和同类项目相比强在哪里？
- 它的边界是什么？

### 架构问题

- 系统入口在哪里？
- 核心 runtime 是什么？
- 模块如何分层？
- 哪些模块是平台能力，哪些只是业务功能？
- 是否有插件、SDK、外部扩展点？

### 数据与状态问题

- 它保存哪些状态？
- 状态在哪里存？
- 状态生命周期如何管理？
- 哪些数据会进入模型、数据库、日志、远程服务？

### 工具与执行问题

- 它如何调用外部工具？
- 工具输入如何校验？
- 工具失败如何恢复？
- 工具结果如何回到主流程？
- 是否支持并发、取消、重试、超时？

### 安全与权限问题

- 哪些操作有副作用？
- 权限是怎么判断的？
- 用户什么时候需要确认？
- 是否有沙箱、隔离、审计？
- 错误配置会导致什么风险？

### 可观测性问题

- 用户如何知道系统正在做什么？
- 开发者如何 debug？
- 是否有日志、trace、metrics？
- 是否能复现一次失败任务？

### 可迁移问题

- 这个项目最值得学的 3 个设计是什么？
- 哪些做法我现在能用？
- 哪些做法适合以后项目变大后再用？
- 哪些做法不适合我，为什么？

## 6. 把“优秀技术”写成可直接使用的格式

不要只写：

```text
它的插件系统很好。
```

要写成：

```md
## 技术框架：插件能力包

### 解决的问题
团队经验、命令、Agent 角色、工具接入和安全规则需要被一起分发。

### 核心组成
- Commands：用户可直接调用的入口。
- Agents：专门角色和任务边界。
- Skills：可复用能力说明和资源。
- Hooks：行为约束和自动化触发。
- MCP Servers：外部工具接入。
- Themes / Output Styles：输出与体验定制。

### 适用场景
- 团队规范沉淀。
- 重复工作流自动化。
- 多项目复用 Agent 能力。

### 设计原则
- 插件必须可校验。
- 插件必须可禁用。
- 插件依赖必须可追踪。
- 插件能力要和权限系统打通。

### 我可以怎么用
- 先做本地插件目录规范。
- 再做命令和 skill 注册。
- 最后接入 hook、MCP 和版本校验。
```

这种写法最适合学习和复用。

## 7. 一个完整示例

下面是一个从项目功能抽象到通用框架的例子。

### 项目功能

Claude Code 有 `MCP` 支持。

### 通用问题

Agent 如何统一接入外部工具生态？

### 优秀技术框架

```text
MCP Server
  -> Transport Adapter
  -> Auth / OAuth
  -> Tool Discovery
  -> Tool Naming
  -> Permission Mapping
  -> Tool Registry
  -> Execution Runtime
  -> Result Normalization
  -> Observability
```

### 可迁移原则

- 外部工具进入系统后，要和内建工具使用同一套执行协议。
- 工具命名要稳定，避免冲突。
- 认证、权限、超时、错误恢复不能放在业务层临时处理。
- MCP 是工具生态入口，不只是 API wrapper。

### 我的行动项

- [ ] 设计统一工具注册表。
- [ ] 给工具增加 `source` 字段：builtin / mcp / plugin / custom。
- [ ] 给工具增加 `riskLevel` 字段。
- [ ] 统一 tool result 格式。
- [ ] 记录外部工具调用日志。

## 8. 每次沉淀的最终交付物

每次认真学习一个项目，最终至少产出 3 个东西：

```text
1. 一份单项目沉淀
   docs/external-projects/{项目类型中文文件夹}/{owner}-{repo}.md

2. 一次通用问题库更新
   docs/patterns/{topic}-patterns.md

3. 一组行动项
   放在单项目文档或 docs/patterns/agent-engineering-framework.md 里
```

如果只是随手发现项目，则产出 1 个东西：

```text
docs/project-radar/candidates.md 里的候选卡片
```

## 9. 推荐工作节奏

建议用轻重结合的节奏。

### 每周

- 搜集 5 到 10 个候选项目。
- 给每个项目写候选卡片。
- 选 1 到 2 个高分项目深度沉淀。

### 每月

- 汇总本月所有项目。
- 更新通用问题库。
- 抽象 3 到 5 条新的技术框架。
- 删除低价值候选，避免知识库变成链接堆。

### 每个阶段

- 输出一份总纲更新。
- 明确自己的项目可以吸收哪些能力。
- 把行动项转成真实开发计划。

## 10. 最终目标

这套沉淀体系的最终目标不是让你拥有很多项目笔记，而是让你逐渐形成自己的技术判断：

- 看到一个功能，能判断它背后的通用问题。
- 看到一个架构，能判断它解决了什么复杂度。
- 看到一个优秀项目，能抽象出可迁移框架。
- 做自己的项目时，能直接拿这些框架指导设计。

也就是说，最后沉淀出来的不是“我看过哪些项目”，而是：

```text
我理解了哪些重要工程问题，
我知道优秀项目如何解决它们，
我能把这些方法迁移到自己的系统里。
```

## 行业痛点研究版补充

> 目标：把“优质项目学习沉淀操作手册”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

