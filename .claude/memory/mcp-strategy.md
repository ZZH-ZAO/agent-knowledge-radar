# MCP Strategy

This file captures how we want to think about MCP for Agent projects.
这个文件沉淀的是：以后我们应该怎样判断 MCP 什么时候值得上、怎么上、上到什么程度。

## Core View

MCP should not be treated as “more tools for free”.
It should be treated as a standardized capability boundary between the Agent runtime and external systems.

中文理解：

- MCP 不是“白送更多工具”
- 它更像 Agent runtime 和外部能力之间的标准边界层

## When MCP Is Most Valuable

- the project needs many external tools or resources
- 项目需要接很多外部工具或资源
- tool sources are heterogeneous
- 工具来源很异构
- the team wants plug-in style extensibility
- 团队想做插件式扩展
- multiple Agents or sessions should share a common tool ecosystem
- 多个 Agent 或会话想共享同一个工具生态
- resources, prompts, and tools should be discovered through a common protocol
- 资源、prompt、tools 都希望通过统一协议被发现

## When MCP Is Not Necessary Yet

- the project only has a few simple local tools
- 项目现在只有少量简单本地工具
- there is no need for external capability discovery
- 还不需要外部能力发现
- the team is still stabilizing the core runtime
- 团队还在稳核心 runtime
- the real bottleneck is prompt, workflow, or permissions, not tool integration scale
- 真实瓶颈在 prompt、workflow、permissions，而不是工具接入规模

## Recommended MCP Categories

### Repo Analysis MCP

Use for:

- file search
- 文件搜索
- symbol lookup
- 符号查找
- code graph queries
- 代码图查询
- repository understanding
- 仓库理解

### Docs and Knowledge MCP

Use for:

- querying architecture docs
- 查询架构文档
- querying internal design references
- 查询内部设计参考
- surfacing stable engineering guidance
- 取回稳定工程方法论

### External Research MCP

Use for:

- official documentation lookup
- 官方文档检索
- standards or API references
- 标准或 API 参考
- ecosystem research
- 生态研究

### Environment or Task MCP

Use for:

- browser automation
- 浏览器自动化
- issue tracker access
- issue tracker 接入
- deployment or CI data
- 部署或 CI 数据
- team communication systems
- 团队沟通系统

## MCP Design Rules

- Do not expose dangerous capabilities without a permission model.
- 没有权限模型时，不要暴露危险能力。
- Keep MCP tool results compatible with the same session protocol as local tools.
- MCP 工具结果尽量和本地工具使用同一会话协议。
- Separate “resource lookup” from “side-effecting tools” whenever possible.
- 尽量把“资源查询”和“有副作用工具”分开。
- Prefer a small number of well-governed MCP servers over many ad hoc integrations.
- 优先少量治理良好的 MCP server，而不是大量零散接入。
- Document what each MCP server is for, who should use it, and what risks it introduces.
- 每个 MCP server 都应该说明用途、适用人群和风险。

## Recommended Adoption Order

1. stabilize core runtime
   先稳核心 runtime
2. add local tool governance
   再把本地工具治理做好
3. introduce MCP for one or two high-value external capability domains
   先只接 1 到 2 类高价值外部能力
4. add discovery, filtering, and permission refinements
   再补发现、筛选、权限细化
5. expand to team or platform-wide MCP ecosystems
   最后才扩成团队或平台级 MCP 生态

## Evaluation Questions

- Does MCP solve a scaling problem, or is it just adding novelty?
- MCP 解决的是规模问题，还是只是增加新鲜感？
- Which external capabilities truly need standardization?
- 哪些外部能力真的值得标准化？
- What permissions and auditability are required?
- 需要什么权限和审计能力？
- Should this be a tool, a resource, or both?
- 这个能力应该建成 tool、resource，还是两者都有？
- Will multiple agents or sessions benefit from the same integration?
- 多个 agent 或会话会不会从这次接入中共同受益？
