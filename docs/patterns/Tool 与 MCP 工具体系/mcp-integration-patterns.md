# 通用问题：MCP Integration

## 1. 问题定义

MCP Integration 要解决的，不是“Agent 能不能接一个外部 server”，而是“外部能力进入系统以后，怎样被纳入统一注册、统一权限、统一执行和统一结果治理”。

真正难的地方从来不是连上，而是接进来以后还能不能继续被平台掌控。

## 2. 为什么普通做法不够

很多项目把 MCP 理解成“比 function calling 更标准一点的 wrapper”。这会很快遇到四类问题：

- 工具来源越来越多，平台根本不知道谁是谁
- 不同 server 结果格式不统一
- 高风险工具和只读工具混在一起
- 安装、升级、认证、重试、生命周期都没人管

所以 MCP 真正带来的，不只是能力扩展，也会把治理问题成倍放大。

## 3. 典型方案结构

成熟 MCP Integration 通常至少分成下面几层：

```text
External Capability
  -> MCP Server
  -> Discovery / Registry
  -> Auth / Transport
  -> Tool Mapping
  -> Permission Mapping
  -> Execution Context
  -> Result Policy
  -> Audit / Telemetry
```

这里最重要的是，MCP 不应该直接绕过平台自己的 Tool Runtime。正确姿势是“通过 MCP 接入，仍然在平台内部治理”。

## 4. 成熟系统通常怎么做

### 4.1 先统一工具身份，而不是先追求接得多

一个成熟平台第一件事不是“接了多少 MCP server”，而是能不能明确：

- 这个工具从哪来
- 它属于什么 category
- 它风险多高
- 它是不是 stateful
- 它结果应该怎么返回

否则工具数量一旦变多，平台就会迅速失去判断力。

### 4.2 把 MCP 工具映射回统一 Tool Registry

MCP 是接入协议，不是平台本体。真正稳的做法，是把 MCP 工具继续映射回平台自己的 Tool Registry，让 builtin、plugin、MCP 三类工具在同一治理视角下可比较、可过滤、可审计。

### 4.3 对重资产结果做 artifact-aware 治理

浏览器、trace、截图、日志、文件片段这类结果，不能直接把原始大块内容塞进模型。成熟系统会优先：

- summary
- structuredData
- artifactRefs
- follow-up tool

MCP 如果没有结果治理，越开放只会越乱。

### 4.4 外部环境有状态时，要补生命周期管理

有些 MCP server 不是静态查询器，而是长期环境的一部分，比如浏览器、远程服务、daemon、会话型工具。只要它有长期状态，平台就必须管理：

- start
- status
- restart
- stop
- stale session handling

### 4.5 安装和认证不是附属问题

真正要进产品或团队环境时，MCP 很快会遇到：

- OAuth
- token / secret
- headers
- install source
- 版本兼容
- 重试与错误恢复

如果这些层没设计好，MCP 就会从扩展能力变成维护负担。

## 5. 常见错误做法

### 5.1 把 MCP 当 API wrapper

这样做最开始最轻，但一旦 server 多起来，平台就没有自己的控制面。

### 5.2 让每个 MCP server 自己定义返回格式

短期看自由，长期看等于放弃统一结果治理。

### 5.3 不区分只读工具和高风险工具

如果 MCP 工具统一被当成“只是外部能力”，权限模型一定会失真。

### 5.4 不做安装、校验和安全扫描

扩展生态一旦进入团队使用，这部分迟早会变成正式问题。

## 6. 证据项目

### 6.1 ChromeDevTools/chrome-devtools-mcp

它说明 MCP 不只是“接进能力”，还要重新包装结果、管理状态、同时服务 Agent 和 CLI。

### 6.2 aaif-goose/goose

它说明 MCP extension 一旦进入平台，就不再是单个 server 问题，而是生态治理问题。

### 6.3 anthropics/claude-code

官方文档里 MCP、connectors、settings、tool search、OAuth 这些能力都在产品层被公开，说明这不是边缘补丁，而是正式接入面。

## 7. Trade-off 与边界

### 7.1 接入越标准，治理成本越高

你会多写发现、认证、权限、结果归一化、安装校验、版本治理。但这不是额外负担，而是开放生态必须支付的成本。

### 7.2 并不是所有平台都需要一开始就做重 MCP 治理

如果还是单团队、少量工具、短周期实验，可以先轻做；但只要目标是平台化或生态化，就必须尽早把 MCP 视为正式扩展层。

## 8. 我的项目行动项

- [ ] 给平台工具注册表增加 `source=builtin/plugin/mcp`，并补 `riskLevel / stateful / artifactPolicy` 字段。
- [ ] 在项目沉淀模板中固定抽取 MCP 工具的安装方式、认证方式、结果策略和生命周期策略。
- [ ] 在痛点页持续回写“MCP 接入以后难治理”的证据项目和数据信号。
- [ ] 后续自动沉淀链路里，把 MCP 识别从“提到关键词”升级成结构化抽取。

## 自动回写补充

<!-- AUTO-WRITEBACK:anthropics-claude-code-mcp-integration:START -->
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
<!-- AUTO-WRITEBACK:anthropics-claude-code-mcp-integration:END -->
