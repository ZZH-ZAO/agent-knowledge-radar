#!/usr/bin/env python3
"""MCP Server for Agent Knowledge Radar.

Exposes the knowledge base as MCP tools for Claude Code (stdio)
and Codex (HTTP/SSE).

Usage:
  python scripts/mcp_server.py                        # stdio mode (Claude Code)
  python scripts/mcp_server.py --transport sse --port 8766  # SSE mode (Codex)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Ensure scripts/ is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

import knowledge_tools as kt

server = Server("agent-knowledge-radar")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_knowledge",
            description="搜索知识库中的项目、方案、痛点、资料源和面经。返回匹配结果列表，按相关度排序。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "kinds": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["project", "solution", "painPoint", "source", "interview"]},
                        "description": "限定搜索类型，留空搜索全部",
                    },
                    "limit": {"type": "integer", "description": "返回结果数量上限", "default": 10},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_project",
            description="获取项目的完整详情，包括摘要、标签、关联方案、行动项、口语版回答和工程讲法。",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "项目 ID"},
                },
                "required": ["project_id"],
            },
        ),
        types.Tool(
            name="get_solution",
            description="获取方案的完整详情，包括问题定义、为什么重要、成熟做法、常见误区和行动项。",
            inputSchema={
                "type": "object",
                "properties": {
                    "solution_id": {"type": "string", "description": "方案 ID"},
                },
                "required": ["solution_id"],
            },
        ),
        types.Tool(
            name="get_pain_point",
            description="获取痛点的完整详情，包括行业现象、证据项目、成熟做法、数据信号和演化规律。",
            inputSchema={
                "type": "object",
                "properties": {
                    "pain_point_id": {"type": "string", "description": "痛点 ID"},
                },
                "required": ["pain_point_id"],
            },
        ),
        types.Tool(
            name="list_projects",
            description="列出所有项目，可按分类和最低评分过滤。返回项目摘要列表。",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "按分类过滤（如 'Agent Runtime', 'MCP'）"},
                    "min_score": {"type": "integer", "description": "最低评分过滤"},
                },
            },
        ),
        types.Tool(
            name="list_solutions",
            description="列出所有方案方法，返回方案摘要列表。",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="list_pain_points",
            description="列出所有行业痛点，可按严重度过滤。",
            inputSchema={
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["high", "medium", "low"], "description": "按严重度过滤"},
                },
            },
        ),
        types.Tool(
            name="get_related_entities",
            description="获取实体的关联关系。传入项目/方案/痛点的 ID，返回它关联的其他实体。",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_id": {"type": "string", "description": "实体 ID（项目、方案或痛点）"},
                },
                "required": ["entity_id"],
            },
        ),
        types.Tool(
            name="get_interview_questions",
            description="获取面试题，可按项目或方案过滤。返回题目、推荐答案和追问方向。",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "按项目 ID 过滤"},
                    "pattern_id": {"type": "string", "description": "按方案 ID 过滤"},
                },
            },
        ),
        types.Tool(
            name="get_knowledge_stats",
            description="返回知识库统计信息：项目数、方案数、痛点数、平均评分等。",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    result = None

    if name == "search_knowledge":
        result = kt.search_knowledge(
            query=arguments.get("query", ""),
            kinds=arguments.get("kinds"),
            limit=arguments.get("limit", 10),
        )
    elif name == "get_project":
        result = kt.get_project(arguments.get("project_id", ""))
    elif name == "get_solution":
        result = kt.get_solution(arguments.get("solution_id", ""))
    elif name == "get_pain_point":
        result = kt.get_pain_point(arguments.get("pain_point_id", ""))
    elif name == "list_projects":
        result = kt.list_projects(
            category=arguments.get("category"),
            min_score=arguments.get("min_score"),
        )
    elif name == "list_solutions":
        result = kt.list_solutions()
    elif name == "list_pain_points":
        result = kt.list_pain_points(severity=arguments.get("severity"))
    elif name == "get_related_entities":
        result = kt.get_related_entities(arguments.get("entity_id", ""))
    elif name == "get_interview_questions":
        result = kt.get_interview_questions(
            project_id=arguments.get("project_id"),
            pattern_id=arguments.get("pattern_id"),
        )
    elif name == "get_knowledge_stats":
        result = kt.get_knowledge_stats()
    else:
        result = {"error": f"Unknown tool: {name}"}

    text = json.dumps(result, ensure_ascii=False, indent=2)
    return [types.TextContent(type="text", text=text)]


async def run_stdio() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


async def run_sse(host: str, port: int) -> None:
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route, Mount
    import uvicorn

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
            await server.run(streams[0], streams[1], server.create_initialization_options())

    starlette_app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    print(f"MCP SSE server listening on http://{host}:{port}")
    print(f"  SSE endpoint: http://{host}:{port}/sse")
    print(f"  Messages endpoint: http://{host}:{port}/messages/")

    config = uvicorn.Config(starlette_app, host=host, port=port, log_level="info")
    srv = uvicorn.Server(config)
    await srv.serve()


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Knowledge Radar MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="Transport mode")
    parser.add_argument("--host", default="127.0.0.1", help="SSE host")
    parser.add_argument("--port", type=int, default=8766, help="SSE port")
    args = parser.parse_args()

    if args.transport == "sse":
        asyncio.run(run_sse(args.host, args.port))
    else:
        asyncio.run(run_stdio())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
