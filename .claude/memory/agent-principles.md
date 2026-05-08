# Agent Principles

These are the stable design principles we want to reuse when analyzing or designing Agent systems.
这些是以后分析和设计 Agent 系统时，优先复用的稳定原则。

## Core Principles

- Treat an Agent as a runtime system, not just a prompt plus tools.
- 把 Agent 当成运行时系统，不要只当成 prompt 加工具。
- Find the main query loop before analyzing anything else.
- 在分析任何东西前，先找到主 query loop。
- Prompt engineering is context supply engineering, not just wording.
- Prompt 工程本质上是上下文供给工程，不只是措辞优化。
- Tool calling is primarily a side-effect governance problem.
- Tool calling 首先是副作用治理问题，其次才是调用问题。
- Workflow should be understood across multiple time scales, not as a single happy-path flowchart.
- Workflow 要按多个时间尺度理解，而不是只看一张 happy path 流程图。
- Memory is not chat history; it is a governed, layered knowledge system.
- Memory 不是聊天记录，而是受治理的分层知识系统。
- RAG should start from retrieval needs and knowledge types, not from a vector database.
- RAG 应该从“需要取回什么知识”出发，而不是先上向量库。
- Multi-agent systems should be organized around responsibility, result flow, and coordination, not just spawning more models.
- 多 Agent 要围绕责任、结果回流和协调关系来设计，而不是多开几个模型。
- Cost, caching, rollout, and observability are architecture concerns, not afterthoughts.
- 成本、缓存、灰度发布、可观测性都属于架构问题，不是上线后再补的东西。

## Review Heuristics

- Ask what the real center of the system is.
- 先问这个系统真正的中心是什么。
- Separate stable mechanisms from optional product features.
- 区分稳定底座和可选产品特性。
- Explain why a design exists, not just where it is implemented.
- 要解释“为什么这样设计”，不只是“在哪实现”。
- Always compare current design to a simpler alternative.
- 永远拿当前设计和更简单的替代方案做比较。
- Surface tradeoffs, failure modes, and maturity level.
- 明确说出取舍、失败模式和成熟度。

## Design Heuristics

- Build runtime stability before advanced feature breadth.
- 先把 runtime 稳定性做好，再追求高级 feature 的广度。
- Add complexity only when a real bottleneck appears.
- 只有在真实瓶颈出现时再增加复杂度。
- Prefer explicit state boundaries over hidden implicit behavior.
- 优先做显式状态边界，而不是隐藏的隐式行为。
- Prefer unified message and result protocols over ad hoc returns.
- 优先统一的消息和结果协议，而不是零散返回值。
- Prefer recoverable and inspectable systems over clever but opaque ones.
- 优先可恢复、可检查的系统，而不是看起来聪明但不透明的系统。
