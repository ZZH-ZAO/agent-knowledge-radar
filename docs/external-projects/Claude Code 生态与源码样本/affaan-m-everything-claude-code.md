# 项目沉淀：affaan-m/everything-claude-code

> 来源：https://github.com/affaan-m/everything-claude-code  
> 沉淀日期：2026-05-03  
> 推荐等级：High  
> 总分：92  
> 学习主题：ai-agents, anthropic, claude, claude-code, developer-tools, llm, mcp, productivity

## 1. 项目一句话

`everything-claude-code` 真正值得看的，不是它又整理了一堆 Claude Code 周边资源，而是它试图把 “AI coding agent 怎么从能跑，走到更稳、更快、更可治理” 这件事，沉淀成一套跨客户端、跨工作流、跨团队可复用的增强层。

如果说官方 `claude-code` 更像运行时本体，这个项目更像围绕运行时长出来的“操作系统层”: skills、memory、hooks、security、research workflow、团队协作约束、甚至插件和分发规范，都会被纳入同一套 agent harness 观念里。

## 1.1 为什么现在读

如果你现在已经不满足于“让 Agent 能调用工具”，而开始关心下面这些更像真实工程的问题，这个项目就很值得现在读：

- 为什么同一个 coding agent，在不同团队手里稳定性差这么多。
- 为什么很多 Agent 项目 demo 能跑，一进入长期使用就开始上下文发散、权限失控、输出风格漂移。
- 一个团队要怎么把 prompt、memory、skills、rules、hooks 这些分散资产收成可维护体系。

换句话说，这个项目适合补的是“Agent 使用层工程化”这块短板，而不是补某一个单点功能认知。

## 1.2 最容易误读什么

最容易把它误读成：

- Claude Code 资源大合集
- 一个很大的 prompt / rule / skill 仓库
- “别人调过的一套现成配置”

这些说法都不算错，但都偏浅。

真正该看的不是它收了多少东西，而是它在试图回答一个更重要的问题：

```text
当 Agent 真正进入高频研发流程后，怎样把零散经验沉淀成稳定可复用的工作系统？
```

## 1.3 一句话判断

这不是一个“功能型项目”，更像一个把 Agent 使用经验产品化、制度化、工作流化的外层增强系统样本。

## 2. 为什么值得学

- Radar 评分：总分 92；相关性 81；工程质量 100；学习价值 100；活跃度 95；稀缺性 81。
- GitHub 信号：stars=171939，forks=26654，language=JavaScript，license=MIT。
- 推荐理由：The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.；stars=171939，与当前 Agent 工程知识库主题存在可学习关联。

## 3. 核心场景

待人工补充：

- 用户是谁？
- 用户在什么场景下使用？
- 它替用户减少了什么复杂度？

## 4. 它解决的通用问题

初步判断：

- 围绕 外部工具生态接入、Agent Runtime / Coding Agent 设计、记忆系统与上下文治理、权限、沙箱与安全治理 提取通用问题、技术框架和当前项目行动项

后续阅读时，请进一步转换成通用问题，例如：

- Agent 如何统一接入外部工具生态？
- 高风险工具如何做权限、安全和审计？
- 多 Agent 如何分工、通信和合并结果？
- 长上下文、Memory、Prompt 如何治理？

## 5. 优秀技术和框架

待读源码和文档后补充：

- 架构分层：
- 核心 runtime：
- 数据模型：
- 插件/扩展：
- 权限/安全：
- 可观测性：
- UI/交互：
- 部署/分发：

## 6. 可迁移设计原则

待补充。请把项目做法抽象成“自己的项目也能复用”的原则。

## 7. 对我当前项目的行动项

- [ ] 现在就能做：
- [ ] 需要调研后做：
- [ ] 暂时不做但保留方向：

## 8. Radar 元数据

- topics: ai-agents, anthropic, claude, claude-code, developer-tools, llm, mcp, productivity
- root files: .agents, .claude, .claude-plugin, .codebuddy, .codex, .codex-plugin, .cursor, .env.example, .gemini, .github, .gitignore, .kiro, .markdownlint.json, .mcp.json, .npmignore, .opencode, .prettierrc, .tool-versions, .trae, .yarnrc.yml, AGENTS.md, CHANGELOG.md, CLAUDE.md, CODE_OF_CONDUCT.md, COMMANDS-QUICK-REF.md, CONTRIBUTING.md, EVALUATION.md, LICENSE, README.md, README.zh-CN.md, REPO-ASSESSMENT.md, RULES.md, SECURITY.md, SOUL.md, SPONSORING.md, SPONSORS.md, TROUBLESHOOTING.md, VERSION, WORKING-CONTEXT.md, agent.yaml, agents, assets, commands, commitlint.config.js, contexts, docs, ecc2, ecc_dashboard.py, eslint.config.js, examples, hooks, install.ps1, install.sh, legacy-command-shims, manifests, mcp-configs, package-lock.json, package.json, plugins, pyproject.toml, research, rules, schemas, scripts, skills, src, tests, the-longform-guide.md, the-security-guide.md, the-shortform-guide.md, yarn.lock
- pushed_at: 2026-04-30T16:25:17Z
- default_branch: main
- homepage: https://ecc.tools
- 风险/不足：暂无明显风险，仍需人工确认源码和文档质量

## 9. README 摘要摘录

```text
**Language:** English | [Português (Brasil)](docs/pt-BR/README.md) | [简体中文](README.zh-CN.md) | [繁體中文](docs/zh-TW/README.md) | [日本語](docs/ja-JP/README.md) | [한국어](docs/ko-KR/README.md) | [Türkçe](docs/tr/README.md)

# Everything Claude Code

![Everything Claude Code — the performance system for AI agent harnesses](assets/hero.png)

[![Stars](https://img.shields.io/github/stars/affaan-m/everything-claude-code?style=flat)](https://github.com/affaan-m/everything-claude-code/stargazers)
[![Forks](https://img.shields.io/github/forks/affaan-m/everything-claude-code?style=flat)](https://github.com/affaan-m/everything-claude-code/network/members)
[![Contributors](https://img.shields.io/github/contributors/affaan-m/everything-claude-code?style=flat)](https://github.com/affaan-m/everything-claude-code/graphs/contributors)
[![npm ecc-universal](https://img.shields.io/npm/dw/ecc-universal?label=ecc-universal%20weekly%20downloads&logo=npm)](https://www.npmjs.com/package/ecc-universal)
[![npm ecc-agentshield](https://img.shields.io/npm/dw/ecc-agentshield?label=ecc-agentshield%20weekly%20downloads&logo=npm)](https://www.npmjs.com/package/ecc-agentshield)
[![GitHub App Install](https://img.shields.
...
```

## 10. 证据链接

- README: https://github.com/affaan-m/everything-claude-code/blob/main/README.md
- Docs: https://github.com/affaan-m/everything-claude-code/tree/main/docs
- Source: https://github.com/affaan-m/everything-claude-code
- CHANGELOG: https://github.com/affaan-m/everything-claude-code/blob/main/CHANGELOG.md
- Examples: https://github.com/affaan-m/everything-claude-code/tree/main/examples

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“项目沉淀：affaan-m/everything-claude-code 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

### 1. 这件事到底考什么

这个项目真正考的，不是会不会给 Claude Code 配几个 rules 或 skills，而是你有没有意识到：

```text
Agent 的问题很多时候不在模型本身，
而在模型外面那一圈长期使用资产有没有被工程化。
```

也就是说，skills、memory、security、hooks、research workflow、团队规则这些东西，如果都只是散落在各处的“经验贴”，系统迟早会变得越来越脆。这个项目有价值，就在于它尝试把这些零散经验收束成一个能持续复用的 harness。

### 2. 口语版回答

如果让我用一句更像面试回答的话来讲，我会说：  
`everything-claude-code` 最值得学的不是某个 skill 本身，而是它把“怎么把 Agent 用稳”这件事拆成了很多可以治理的层，比如规则、记忆、权限、安全、研究流程和团队协作约束。很多项目会把这些东西混在 prompt 里糊过去，但这个项目是在把它们往系统资产上收。

### 3. 工程视角拆解

我会把它拆成四层：

- 使用层问题：为什么同样是 Claude Code / Codex / Cursor，有的人越用越稳，有的人越用越乱。
- 资产层收束：skills、rules、memory、hooks、security、plugins 等是不是被纳入统一治理。
- 工作流层固化：research-first、团队协作、提交规范、上下文使用方式有没有被写成可执行方法。
- 生态层兼容：它不是绑死一个客户端，而是试图形成跨 Agent 产品的增强层。

### 4. 常见误区

- 误区一：把它当“资源站”看，结果只记住它收集了很多配置，没有看到它在组织长期使用经验。
- 误区二：把 skill / rule 直接照搬到自己项目里，却没有补自己项目的边界、权限和团队约束。
- 误区三：以为 Agent 提效主要靠模型换代，而忽视外围工程资产对稳定性的影响。

### 5. Trade-off 与边界

这种系统化增强层的优点是复用性强、团队可传播、长期收益大；代价是前期整理成本高，而且一旦抽象过度，也容易把项目做成“规则越来越多，但真正落地的人越来越少”。

所以它更适合：

- 你已经有一段真实 Agent 使用经验
- 你开始遇到稳定性、团队协作、上下文治理问题
- 你希望把最佳实践沉淀成组织资产

如果你还停留在单人试玩阶段，直接照搬全套体系，反而容易让成本先于收益出现。

### 6. 当前项目行动项

- [ ] 给知识平台单独补一篇 “Agent 使用层工程化” 方案文档，把 skills / memory / rules / hooks / security 归成一个总问题。
- [ ] 在 Project Radar 的评分体系里增加“是否沉淀了可复用工作流资产”这一信号，不只看源码和 star。
- [ ] 回查自己的项目文档，凡是只写“用了什么能力”却没写“如何长期用稳”，都补一层外围工程资产分析。

### 7. 面试官追问

**追问：这个项目或方案最值得学习的不是功能，而是什么？**

答：最值得学习的是它把 Agent 的长期使用经验收成了系统资产。很多项目只在功能层做增强，但这个项目更像是在回答“怎么把 Agent 用稳、用久、用成团队能力”。

**追问：如果迁移到当前平台，第一步应该做什么？**

答：第一步不是抄它的 rules 或 skills，而是先把自己的项目分层，看看哪些问题属于 runtime，哪些属于长期使用资产，再决定该补文档、补 workflow，还是补治理约束。

## 行业痛点研究版补充

> 目标：把“项目沉淀：affaan-m/everything-claude-code”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

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

