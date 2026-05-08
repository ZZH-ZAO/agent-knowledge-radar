# 通用问题：Permission & Sandbox

## 1. 问题定义

Permission & Sandbox 真正要解决的，不是“弹不弹一个确认框”，而是“Agent 在提出高风险动作时，系统怎样判断风险、怎样授权、怎样隔离执行、怎样留下可追踪证据”。

只要 Agent 能写文件、跑命令、访问网络、操作浏览器或调外部系统，权限和隔离就不再是附属功能，而是系统边界本身。

## 2. 为什么普通做法不够

很多系统在安全上最常见的偷懒方式是：

- 全靠人工确认
- 全靠命令黑名单
- 全靠模型自己“尽量小心”

这些办法短期有点用，但一旦工具复杂、路径多、环境乱、用户不总在线，就会迅速失效。真正难的不是提醒用户，而是让系统自己先建立稳定边界。

## 3. 典型方案结构

成熟 Permission & Sandbox 通常有这条链：

```text
Action Proposal
  -> Risk Classification
  -> Policy Match
  -> Confirmation Decision
  -> Sandbox / Isolation
  -> Execution
  -> Audit / Transcript
```

关键不是“有没有拦”，而是系统能不能解释：

- 为什么要拦
- 为什么这次可以放
- 放开后实际发生了什么

## 4. 成熟系统通常怎么做

### 4.1 先按动作风险分层

不是所有工具都一样危险。成熟系统通常会先分：

- 只读观察型
- 低风险状态修改
- 高风险副作用
- 外部系统写入

只有先把风险分层，后面的 allow / ask / deny 才能成立。

### 4.2 权限策略不能只看工具名

真正稳定的权限判断，通常同时看：

- tool category
- 参数内容
- 路径范围
- 当前运行环境
- 用户或组织策略

同样是 `bash`，执行 `ls` 和执行 `rm -rf` 显然不是一个级别；同样是写文件，写工作区内某个草稿和改系统路径也不是一个级别。

### 4.3 沙箱不是确认框的替代品，而是执行层边界

确认解决的是“用户是否同意”，沙箱解决的是“即使执行，也被限制在什么范围内”。这两层混在一起，系统最后既不安全，也不清晰。

### 4.4 审计必须记录原因和结果

真正有价值的审计不只是“用户点了允许”，还应该知道：

- 模型提议了什么
- 风险分类是什么
- 命中了哪条策略
- 是否进入沙箱
- 实际改了什么
- 结果有没有失败

否则权限系统很难被复盘，更难被优化。

## 5. 常见错误做法

### 5.1 只靠弹窗确认

这会把责任全部甩给用户，但不给用户足够判断依据，也不给系统留下可学习结构。

### 5.2 只靠危险字符串黑名单

黑名单能拦一部分显眼风险，但很难覆盖组合动作、路径逃逸、上下文变化和隐式副作用。

### 5.3 权限层和沙箱层彼此割裂

如果授权逻辑和执行隔离完全脱节，系统要么过度阻塞，要么过度信任。

## 6. 证据项目

### 6.1 anthropics/claude-code

它在公开产品层面已经把 settings、权限相关行为、hooks 和高风险动作边界当成正式能力面，说明这不是内部补丁，而是产品主线。

### 6.2 zzh/pico

本地源码已经能看出 approval policy、路径边界、只读模式、shell allowlist、secret shaped text 检查、resume 校验这些能力。这是很好的“轻量但正式”的证据。

### 6.3 现有行业资料

你沉淀的旧文档和面经里也已经不断出现 sandbox、permission、危险命令、secret scanning、组织策略这些关键词，说明这不是单项目附属问题。

## 7. Trade-off 与边界

### 7.1 安全治理越完整，行动摩擦越大

权限层、确认层、隔离层做得越重，用户感受到的 friction 也会变高。这是不可避免的 trade-off，所以真正要做的是“按风险分层”，而不是“一刀切全部收紧”。

### 7.2 不是所有场景都需要同样重的沙箱

本地个人只读分析、团队共享开发、企业生产环境，这三类场景需要的安全强度完全不同。好的系统应该支持策略层变化，而不是只有一个全局硬模式。

## 8. 我的项目行动项

- [ ] 给平台里的 shell、file write、network、external tool 统一补 `riskLevel` 和 `permissionPolicy` 视角。
- [ ] 后续项目沉淀时，固定抽取“路径边界 / approval policy / sandbox / audit trail”四类证据。
- [ ] 痛点页继续沉淀“高风险动作为什么容易失控”这类行业共性问题。
- [ ] 面试页增加“你怎么设计 Agent 的权限和沙箱边界”的标准回答框架。

## 自动回写补充

<!-- AUTO-WRITEBACK:anthropics-claude-code-permission-sandbox:START -->
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
<!-- AUTO-WRITEBACK:anthropics-claude-code-permission-sandbox:END -->
