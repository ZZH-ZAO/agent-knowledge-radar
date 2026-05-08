# Codex Integration Guide

Agent Knowledge Radar 可以通过 MCP 协议同时被 Claude Code 和 Codex 使用。

## 传输模式

| 模式 | 命令 | 适用场景 |
|------|------|----------|
| stdio | `python scripts/mcp_server.py` | Claude Code、本地 CLI 工具 |
| SSE  | `python scripts/mcp_server.py --transport sse --port 8766` | Codex、远程客户端、Web UI |

## Claude Code 集成

已在 `.mcp.json` 中配置好，Claude Code 会自动启动 MCP server。可用的 10 个 tool：

- `search_knowledge` — 关键词搜索项目、方案、痛点、资料源、面经
- `get_project` — 获取项目详情
- `get_solution` — 获取方案详情
- `get_pain_point` — 获取痛点详情
- `list_projects` — 列出项目（支持分类/评分过滤）
- `list_solutions` — 列出所有方案
- `list_pain_points` — 列出痛点（支持严重度过滤）
- `get_related_entities` — 获取实体关联关系
- `get_interview_questions` — 获取面试题（支持按项目/方案过滤）
- `get_knowledge_stats` — 知识库统计信息

## Codex 集成（SSE 模式）

### 1. 启动 SSE Server

```bash
python scripts/mcp_server.py --transport sse --port 8766
```

服务启动后：
- SSE 端点：`http://127.0.0.1:8766/sse`
- 消息端点：`http://127.0.0.1:8766/messages/`

### 2. Codex 配置

在 `~/.codex/config.json` 中添加：

```json
{
  "mcpServers": {
    "agent-knowledge-radar": {
      "transport": "sse",
      "url": "http://127.0.0.1:8766/sse"
    }
  }
}
```

或通过命令行：

```bash
codex --mcp agent-knowledge-radar=http://127.0.0.1:8766/sse
```

### 3. 验证连接

```bash
# 测试 SSE 端点
curl -N http://127.0.0.1:8766/sse

# 测试工具调用（JSON-RPC）
curl -X POST http://127.0.0.1:8766/messages/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_knowledge_stats","arguments":{}}}'
```

## Python 依赖

```bash
pip install mcp>=1.0.0
```

注意：MCP SDK 需要支持 Rust 编译的 Python 环境（pydantic-core）。Windows 用户建议使用官方 Python 3.13+，msys64 Python 可能无法安装。

## 架构

```
┌─────────────┐     stdio      ┌──────────────────┐
│ Claude Code │ ──────────────→│                  │
└─────────────┘                │   MCP Server     │
                               │   (Python mcp)   │──→ data/knowledge-index.json
┌─────────────┐    HTTP/SSE    │                  │
│    Codex    │ ──────────────→│                  │
└─────────────┘                └──────────────────┘
```

核心逻辑在 `scripts/knowledge_tools.py`（纯 stdlib，无外部依赖），MCP Server 在 `scripts/mcp_server.py`。
