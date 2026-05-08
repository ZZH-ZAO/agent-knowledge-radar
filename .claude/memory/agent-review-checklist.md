# Agent Review Checklist

Use this checklist when reviewing an Agent, coding assistant, or LLM application.
以后做 Agent 项目评审时，优先按这份清单检查，不要只凭感觉。

## Runtime

- Is there a clear main execution loop?
- 有没有清晰的主执行循环？
- Is the system centered on the loop rather than the raw model API?
- 系统中心是不是 query loop，而不是裸模型 API？
- Are turn boundaries, stop conditions, and reinjection paths clear?
- turn 边界、停止条件、结果回注路径是否清楚？

## Prompt and Context

- Are stable rules separated from dynamic runtime context?
- 稳定规则和动态上下文是否拆开？
- Are attachments or temporary reminders handled separately from long-lived instructions?
- attachment 或临时提醒是否和长期指令分开？
- Is prompt design cache-aware and debuggable?
- Prompt 是否考虑缓存命中，并且便于调试？

## Tool Runtime

- Are tools defined with clear schemas and boundaries?
- 工具是否有明确 schema 和能力边界？
- Is there a unified orchestration layer?
- 是否有统一工具编排层？
- Are permissions handled centrally?
- 权限是否集中处理？
- Is concurrency treated intentionally?
- 并发是否是有意识设计的，而不是顺手 `Promise.all`？
- Are tool results converted back into a unified session protocol?
- 工具结果是否回到统一会话协议里？

## Workflow

- Is there orchestration at the single-turn level?
- 单轮层面有没有编排？
- Is there session-level governance such as compaction or restore?
- 会话层面有没有 compact、restore 这类治理？
- Are background jobs modeled explicitly?
- 背景任务是不是显式建模的？
- Is multi-agent coordination a first-class workflow instead of an afterthought?
- 多 Agent 协调是不是一等 workflow，而不是后来拼上的？

## RAG and Retrieval

- What kinds of knowledge are being retrieved?
- 取回的知识到底分哪几类？
- Are rule retrieval, memory retrieval, tool retrieval, and external retrieval separated when needed?
- 规则检索、记忆检索、工具检索、外部检索在需要时有没有区分？
- Is the retrieval design appropriate to the data scale and structure?
- 检索方案是否匹配当前数据规模和结构？

## Memory

- Is there more than one memory layer?
- 有没有多层 memory，而不是单一存储？
- What gets written to memory and why?
- 什么被写进 memory，为什么写？
- Are recall conditions defined?
- recall 条件是否明确？
- Is there consolidation, pruning, or conflict handling?
- 有没有 consolidation、裁剪、冲突处理？

## Multi-Agent

- Is there a clear coordinator or responsibility center?
- 有没有 coordinator 或责任中心？
- Do worker results flow back through a structured protocol?
- worker 结果有没有通过结构化协议回流？
- Are interruption, resume, and status visibility considered?
- 中断、恢复、状态可见性是否被考虑？

## Platform and Operations

- Are feature flags or rollout gates in place where risk is high?
- 高风险能力有没有 feature flag 或 rollout gate？
- Is telemetry or error visibility present?
- 有没有 telemetry、错误可见性？
- Are cache and cost considerations visible in the architecture?
- 架构里有没有明确考虑缓存和成本？

## Final Judgment

- What is this system genuinely strong at?
- 这个系统真正强在哪？
- What is still demo-level?
- 哪些部分还停留在 demo 水平？
- What should be built next, and what should wait?
- 下一步应该补什么，什么应该先别做？
