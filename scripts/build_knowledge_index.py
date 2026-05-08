#!/usr/bin/env python3
"""
Build a structured knowledge index for the visual platform.

Input:
- docs/external-projects/**/*.md
- docs/patterns/*.md
- docs/project-radar/candidates.json

Output:
- data/knowledge-index.json
- apps/knowledge-platform/src/data/knowledge-index.json, if the app exists
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXTERNAL = DOCS / "external-projects"
PATTERNS = DOCS / "patterns"
PAIN_POINTS_DIR = DOCS / "pain-points"
SOURCE_LIBRARY = DOCS / "source-library"
ENGINEERING_LOGIC_DOC = DOCS / "platform" / "可视化知识平台规格" / "engineering-logic-route-framework.md"
RADAR_DATA = DOCS / "project-radar" / "candidates.json"
LEGACY_INDEX = DOCS / "legacy-migration" / "旧案例迁移规则与清单" / "legacy-case-migration-index.json"
CURRENT_PROJECT = DOCS / "source-research" / "当前项目沉淀与路线" / "current-project-distillation.md"
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "knowledge-index.json"
APP_OUTPUT = ROOT / "apps" / "knowledge-platform" / "src" / "data" / "knowledge-index.json"
INTERVIEW_BANK = DOCS / "interviews" / "question-bank.json"
INTERVIEW_BANK_GLOB = "*-question-bank.json"
WRITEBACK_PACKAGE_DIR = DOCS / "project-radar" / "writeback-packages"


TYPE_KEYWORDS = {
    "Agent Runtime": ["agent runtime", "coding agent", "ai agent", "agent 平台", "agent runtime"],
    "MCP": ["mcp", "model context protocol"],
    "Tool Runtime": ["tool runtime", "工具", "tool calling", "tool use"],
    "Memory": ["memory", "记忆"],
    "Plugin / Skill": ["plugin", "skill", "插件", "skills"],
    "Permission / Sandbox": ["permission", "sandbox", "权限", "沙箱"],
    "Multi-Agent": ["multi-agent", "多 agent", "协作"],
    "Provider": ["provider", "多模型", "llm providers"],
    "Productization": ["productization", "产品化", "治理", "release", "security"],
    "Observability": ["observability", "telemetry", "trace", "可观测"],
    "Frontend Design": ["frontend", "前端", "design.md", "设计", "ui", "界面", "视觉", "风格"],
    "Workbench UI": ["dashboard", "admin", "工作台", "后台", "数据面板", "shadcn", "tremor", "blocks"],
    "AI Frontend Generation": ["gpt image", "gpt-image", "mockup", "screenshot", "visual generation", "frontend reconstruction", "ui mockup"],
}


PAIN_POINT_SEEDS = [
    {
        "id": "tool-result-context-overload",
        "title": "工具结果太大，容易打爆上下文",
        "topic": "Tool Runtime",
        "severity": "high",
        "industryPain": "Agent 接入浏览器、仓库、数据库、日志、RAG 和外部系统后，工具返回值往往比模型上下文更大、更脏、更难压缩。行业内的共性难题不是“怎么调用工具”，而是怎么让工具结果可摘要、可追溯、可二次查询，并且不把上下文预算一次性烧光。",
        "evidenceSources": ["GitHub 项目", "旧体系文档", "源码/README 设计原则"],
        "evidenceProjects": [
            "chromedevtools-chrome-devtools-mcp",
            "legacy-browser-harness",
            "legacy-langgraph-mcp-agents",
            "legacy-repomind",
        ],
        "solutionMethod": "使用摘要、结构化结果和 artifact reference 分层返回，避免把截图、trace、heap snapshot 等大对象直接塞进上下文。",
        "maturePractices": [
            "把大结果拆成 summary、structuredData、artifactRefs 三层，让模型先读摘要，必要时再追查细节。",
            "为截图、trace、日志、仓库片段建立 reference over value 机制，避免大对象直接进入上下文。",
            "给工具结果增加 nextActions，让 Agent 能继续查询而不是一次性吞掉所有信息。",
        ],
        "dataSignals": [
            "直接证据项目包含 Chrome DevTools MCP、browser-harness、repomind 等工具密集型项目。",
            "判断指标包括单次 tool result token 数、artifact 引用比例、follow-up 查询成功率、上下文截断次数。",
        ],
        "evolutionRule": "每次新增工具型项目时，检查它是否处理大结果、artifact、分页、摘要和 follow-up query；如果有成熟做法，就回写到 Tool Runtime 痛点。",
        "commonMistakes": ["直接返回大段 JSON", "截图和 trace 直接进入模型上下文", "没有 follow-up tool 让 Agent 继续查询细节"],
        "actions": ["给 tool result 增加 summary、structuredData、artifactRefs、nextActions 字段", "在评分中加入 artifact-aware 信号"],
    },
    {
        "id": "mcp-ecosystem-governance",
        "title": "MCP 工具生态接入后难治理",
        "topic": "MCP Integration",
        "severity": "high",
        "industryPain": "MCP 让 Agent 能快速接入外部工具，但行业共性痛点也随之出现：server 来源复杂、权限粒度不同、工具质量参差不齐、安装和生命周期难治理。真正的问题不是能不能连上 MCP，而是如何把开放生态纳入统一的 Tool Registry、权限策略和审计体系。",
        "evidenceSources": ["GitHub 项目", "官方/生态文档", "旧体系文档"],
        "evidenceProjects": [
            "chromedevtools-chrome-devtools-mcp",
            "aaif-goose-goose",
            "anthropics-claude-code",
            "legacy-deer-flow",
            "legacy-adk-python",
            "legacy-ms-agent",
            "legacy-langgraph-mcp-agents",
        ],
        "solutionMethod": "将 MCP 工具纳入统一 Tool Registry，补充 category、riskLevel、stateful、artifactPolicy、permission mapping 和生命周期管理。",
        "maturePractices": [
            "用 Tool Registry 统一登记 builtin、plugin、MCP 三类工具来源。",
            "给工具补充 riskLevel、permission、stateful、artifactPolicy、owner、installSource 等治理元数据。",
            "把工具发现、权限映射、执行审计、卸载升级纳入生命周期，而不是只做连接配置。",
        ],
        "dataSignals": [
            "证据项目覆盖 Claude Code、Goose、ADK、MS Agent、LangGraph MCP Agents 等不同 MCP 接入方式。",
            "判断指标包括 MCP server 数量、工具权限等级覆盖率、失败调用可追踪率、未分类高风险工具数量。",
        ],
        "evolutionRule": "每次 Project Radar 发现 MCP 项目时，先进入候选池评分，再抽取它的工具发现、权限、安装、审计做法，用来更新 MCP Integration 痛点和 patterns。",
        "commonMistakes": ["把 MCP 当 API wrapper", "不区分只读工具和高风险工具", "没有安装、校验和安全扫描"],
        "actions": ["给 MCP 工具增加 source=builtin/plugin/mcp", "为 MCP extension 建立安装、校验、文档和安全扫描流程"],
    },
    {
        "id": "provider-differences-pollute-runtime",
        "title": "多模型 Provider 差异容易污染 Agent Runtime",
        "topic": "Provider Abstraction",
        "severity": "medium",
        "industryPain": "大模型应用接入多个 provider 后，工具调用协议、流式事件、上下文长度、视觉能力、错误格式、价格和限流策略都会不同。行业共性痛点是 provider 差异会不断渗透业务代码，最后 Runtime 变成一堆模型分支，难以维护和替换。",
        "evidenceSources": ["GitHub 项目", "旧体系文档", "平台产品化资料"],
        "evidenceProjects": [
            "aaif-goose-goose",
            "anthropics-claude-code",
            "legacy-arcreel",
            "legacy-claude-code",
        ],
        "solutionMethod": "使用 Provider Interface、Capability Metadata、Unified Message 和 Event Normalizer 隔离模型差异。",
        "maturePractices": [
            "用统一 Provider Interface 隔离模型厂商差异。",
            "用 capability metadata 声明 tool calling、vision、streaming、context length、reasoning 等能力。",
            "把 provider 原始事件归一化成平台内部事件，避免 UI、Agent loop 和工具层直接依赖厂商返回。",
        ],
        "dataSignals": [
            "证据项目包括 Goose、Claude Code、ArcReel 等需要多模型或多 provider 的系统。",
            "判断指标包括 provider 分支数量、能力声明覆盖率、模型替换改动文件数、provider-specific bug 数量。",
        ],
        "evolutionRule": "每次沉淀支持多模型的项目时，提取它如何描述 capability、事件、错误和配置，并同步到 Provider Abstraction 痛点。",
        "commonMistakes": ["业务逻辑里到处写 provider 分支", "直接暴露模型原始返回", "默认所有模型能力一样"],
        "actions": ["为模型 provider 定义统一接口", "声明 tool calling、vision、streaming、context length 等 capability"],
    },
    {
        "id": "memory-context-staleness-and-bloat",
        "title": "上下文膨胀与过期记忆会同时拖垮 Agent",
        "topic": "Memory System",
        "severity": "high",
        "industryPain": "长链路 Agent 很容易一边把上下文越堆越大，一边继续引用已经过期的旧结论。行业共性痛点并不是单纯的 token 不够，而是没有把 task summary、recent files、file summary、episodic notes、durable memory 和 freshness 校验分开治理，结果就是成本上升、重复读取增多、旧信息污染当前任务。",
        "evidenceSources": ["GitHub 项目", "自研项目源码", "用户提供文档", "平台沉淀文档"],
        "evidenceProjects": [
            "zzh-pico",
            "anthropics-claude-code",
            "current-project",
            "legacy-repomind",
        ],
        "solutionMethod": "把 memory 当成上下文治理系统，而不是聊天记录。至少分清 working memory、file summaries、episodic notes、durable memory，并给可失效内容补 freshness / invalidation 机制；在注入 prompt 时再按预算和优先级裁剪。",
        "maturePractices": [
            "把当前任务摘要、最近文件、文件级摘要、事件性笔记和长期知识拆层保存，而不是塞进一个大 memory。",
            "为 file summary 建 freshness 校验和失效机制，文件变了就主动淘汰旧摘要。",
            "Relevant memory 只按需召回少量高相关内容，并限制每条 note 的注入预算，避免单条长笔记挤占整个 prompt。",
            "把老的 read_file 和 tool output 优先压缩成摘要或 reference，而不是完整回放。",
        ],
        "dataSignals": [
            "可观测信号包括 prompt 压缩率、重复读取次数、memory hit rate、旧摘要失效率和 current request 保留率。",
            "pico 的实验材料表明：结构化 memory 能让重复读取从 8 次降到 3 次，平均 tool steps 从 0.67 降到 0.25，准确率从 66.7% 提升到 100%。",
            "context stress matrix 还可以持续观察 full prompt chars、raw prompt chars、compression ratio 和 current request preserved rate。",
        ],
        "evolutionRule": "每次发现带记忆能力的优质项目时，优先抽取它的 memory scope、freshness rule、retrieval rule 和 injection order；如果有明确失效机制或实验指标，就回写到 Memory System 痛点和 patterns。",
        "commonMistakes": ["把 memory 做成无限追加日志", "只有召回，没有 freshness 校验", "把旧工具输出整段塞回 prompt", "把聊天历史误当成长期知识"],
        "actions": ["给平台项目页补 memory_scope / freshness_rule / retrieval_rule / injection_rule 视角", "后续自动沉淀时优先抽取 summary invalidation、durable promotion、retrieval ranking 三类信号"],
    },
    {
        "id": "runtime-recovery-and-eval-gap",
        "title": "很多 Agent 能跑，但缺少恢复协议和评估闭环",
        "topic": "Observability",
        "severity": "high",
        "industryPain": "大量 Agent 项目能完成单次演示，但一旦任务中断、工作区变化、工具副作用需要复盘，系统就很难回答“还能不能继续信任当前状态”。行业共性痛点不是没有日志，而是没有把 checkpoint、task state、trace、report、failure taxonomy 和 benchmark 聚合成一套运行合同。",
        "evidenceSources": ["GitHub 项目", "自研项目源码", "平台模式文档"],
        "evidenceProjects": [
            "zzh-pico",
            "anthropics-claude-code",
            "aaif-goose-goose",
            "current-project",
        ],
        "solutionMethod": "把恢复、审计和评估当成 Runtime 主链的一部分：运行时拆出 task_state / checkpoint / trace / report，恢复时校验 freshness 和 runtime identity，评估时同时看 pass rate、cost、duration、security events 和 failure categories。",
        "maturePractices": [
            "把 session、task state、trace、report 分开落盘，避免所有运行信息混成一个大对象。",
            "恢复时优先判断旧状态是否仍然可信，而不是简单回放聊天记录。",
            "为失败建立 taxonomy，例如 missing_artifact、budget_exceeded、verifier_failed、failure_stop_reason。",
            "评估不能只看 pass rate，还要同时看 attempts、tool steps、cache hit、duration 和 security event。",
        ],
        "dataSignals": [
            "可观测信号包括 stop_reason_counts、tool_status_counts、security_event_counts、avg_attempts、avg_tool_steps、avg_run_duration_ms 和 cache_hit_rate。",
            "pico 已经把 benchmark artifact 和 run artifact 分开聚合，这意味着可以同时比较结果质量和运行代价。",
        ],
        "evolutionRule": "每次沉淀带 benchmark、trace 或 resume 能力的项目时，抽取它的 artifact split、recovery validation、failure taxonomy 和 cost metrics；如果具备固定评估合同，就同步补到 Observability 与 Agent Runtime 痛点。",
        "commonMistakes": ["把 resume 理解成重新读取旧消息", "只有终端输出，没有结构化 trace", "只报 pass rate，不报 attempts / duration / failure category", "日志和评估结果混在一起"],
        "actions": ["把平台痛点页的证据项目和数据信号与 runtime 恢复、评估闭环显式关联", "后续前端增加 artifact split / metrics coverage / failure taxonomy 的展示字段"],
    },
    {
        "id": "project-learning-stays-as-notes",
        "title": "项目学习容易停留在读书笔记",
        "topic": "Knowledge Distillation",
        "severity": "medium",
        "industryPain": "学习优秀项目时，常见问题是收藏很多链接、摘要很多功能，但没有把它们转化成可迁移的工程问题和自己的行动项。对 Agent 项目尤其严重，因为项目变化快、术语多、实现差异大，如果没有沉淀框架，学习很快会碎片化。",
        "evidenceSources": ["你的旧文档", "面经知识库", "GitHub 项目", "优质博客", "论文"],
        "evidenceProjects": [
            "current-project",
            "legacy-awesome-ai-research-writing",
            "legacy-computer-fundamentals",
            "legacy-fireworks-tech-graph",
            "legacy-shared",
        ],
        "solutionMethod": "固定执行：单项目沉淀 -> 通用问题 -> 技术框架 -> 行动项，确保学习能反哺自己的项目。",
        "maturePractices": [
            "把每个项目拆成项目事实、行业痛点、技术框架、可迁移原则、当前项目行动项。",
            "用 patterns 承接多个项目的共性，避免知识停留在单项目笔记。",
            "把面经追问接到项目沉淀上，让学习内容能转成表达能力。",
        ],
        "dataSignals": [
            "当前平台已有 28 个项目样本、15 个方案框架、6 个行业痛点。",
            "判断指标包括每个项目关联 pattern 数、每个痛点证据项目数、行动项完成率、面试题覆盖率。",
        ],
        "evolutionRule": "每次新增项目、博客、论文或用户文档时，必须产出至少一个通用问题、一个成熟做法和一个当前项目行动项；构建索引后自动刷新平台。",
        "commonMistakes": ["只写项目功能列表", "没有抽象通用问题", "没有行动项"],
        "actions": ["每次深度沉淀后至少更新一个 patterns 文档", "每份文档必须包含当前项目行动项"],
    },
    {
        "id": "agent-productization-gap",
        "title": "Agent 原型难以进入产品化",
        "topic": "Productization",
        "severity": "high",
        "industryPain": "Agent demo 通常能在单机、单用户、单场景下跑通，但一旦进入产品化，就会遇到安装、配置、权限、审计、跨平台、模型切换、失败恢复、团队协作和升级维护问题。行业共性痛点是 Agent 原型很容易展示能力，却很难成为可长期使用的平台。",
        "evidenceSources": ["GitHub 项目", "官方产品仓库", "旧体系文档", "平台规格文档"],
        "evidenceProjects": [
            "aaif-goose-goose",
            "anthropics-claude-code",
            "legacy-claude-code",
            "legacy-hermes-agent",
            "legacy-repomind",
            "legacy-agentset",
            "legacy-arcreel",
        ],
        "solutionMethod": "把安装、更新、跨平台、配置、治理、安全、反馈和文档当成正式工程问题，而不是上线前补丁。",
        "maturePractices": [
            "从第一天就把配置层、权限层、日志层、版本发布和反馈入口当成产品能力设计。",
            "把单次 Agent 执行升级成 workspace、session、history、policy、extension 的平台对象。",
            "用文档、examples、release notes、CI 和安全治理降低长期使用成本。",
        ],
        "dataSignals": [
            "证据项目覆盖 Claude Code、Goose、Hermes、RepoMind、AgentSet、ArcReel 等产品化程度不同的 Agent 系统。",
            "判断指标包括安装成功率、跨平台 issue 数、失败可复现率、配置项清晰度、release 频率、用户反馈闭环。",
        ],
        "evolutionRule": "每次沉淀成熟 Agent 项目时，检查它是否解决安装、配置、权限、日志、团队协作、更新和文档问题，并更新 Productization 痛点。",
        "commonMistakes": ["只关注模型和工具", "忽略 Windows/PowerShell/代理/私有模型", "没有 release/security/governance"],
        "actions": ["维护 CHANGELOG 和 release checklist", "补齐 security、governance、maintainers 文档", "提前设计配置层和企业策略入口"],
    },
    {
        "id": "agent-ui-style-drift",
        "title": "Agent 生成前端容易风格漂移",
        "topic": "Frontend Design Control",
        "severity": "medium",
        "industryPain": "LLM / Agent 生成前端时，普遍会出现审美口径不稳定、页面风格漂移、中文长文本溢出、生成图和真实 DOM 脱节的问题。痛点本质不是 CSS 不会写，而是缺少可执行、可校验、可回写的设计上下文工程。",
        "evidenceSources": ["GitHub 项目", "旧体系文档", "视觉生成项目", "当前平台 DESIGN.md"],
        "evidenceProjects": [
            "voltagent-awesome-design-md",
            "current-project",
            "legacy-fireworks-tech-graph",
            "legacy-shared",
        ],
        "solutionMethod": "将 UI 风格要求沉淀为版本化的 DESIGN.md / FRONTEND_RULES.md，并在前端任务中稳定注入上下文。",
        "maturePractices": [
            "用 DESIGN.md 固化布局、信息密度、颜色、圆角、禁用模式和中文界面规则。",
            "用 mockup / screenshot 作为视觉目标，但最终必须落到真实 React/CSS 和响应式校验。",
            "把每次页面优化中稳定下来的规则回写设计文档，形成设计记忆。",
        ],
        "dataSignals": [
            "证据项目包括 awesome-design-md、draw-ui、Fireworks Tech Graph 和当前平台。",
            "判断指标包括截图回归问题数、中文溢出问题数、设计规则覆盖率、页面风格一致性。",
        ],
        "evolutionRule": "每次发现优质前端风格项目或完成平台页面优化后，把可复用规则回写 DESIGN.md，并更新 Frontend Design Control 痛点。",
        "commonMistakes": ["只在聊天里临时描述风格", "只说现代高级但没有具体规则", "没有说明卡片、间距、颜色、动效和禁忌"],
        "actions": ["为 apps/knowledge-platform 新增 DESIGN.md", "把中文界面规范、信息密度和布局节奏写成可执行前端规则"],
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug_from_path(path: Path) -> str:
    return path.stem.lower()


def title_from_markdown(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if not match:
        return fallback
    return match.group(1).strip()


def section(text: str, heading: str) -> str:
    pattern = rf"^##\s+\d*\.?\s*{re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def heading_block(text: str, *headings: str) -> str:
    for heading in headings:
        pattern = rf"^(##|###)\s+\d*\.?\s*{re.escape(heading)}\s*$"
        match = re.search(pattern, text, flags=re.MULTILINE)
        if not match:
            continue
        current_level = 2 if match.group(1) == "##" else 3
        start = match.end()
        next_pattern = rf"^#{{1,{current_level}}}\s+"
        next_match = re.search(next_pattern, text[start:], flags=re.MULTILINE)
        end = start + next_match.start() if next_match else len(text)
        return text[start:end].strip()
    return ""


def first_paragraph(text: str) -> str:
    cleaned = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped or stripped.startswith(">"):
            continue
        if stripped.startswith("- ") or stripped.startswith("#"):
            continue
        cleaned.append(stripped)
        if len(" ".join(cleaned)) > 180:
            break
    return " ".join(cleaned).strip()


def list_items(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ] "):
            items.append(stripped[6:].strip())
        elif stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def first_nonempty_list(*sections: str) -> list[str]:
    for value in sections:
        items = list_items(value)
        if items:
            return items
    return []


def first_nonempty_section(text: str, *headings: str) -> str:
    for heading in headings:
        value = section(text, heading)
        if value.strip():
            return value
    return ""


def extract_named_section(text: str, headings: list[str]) -> str:
    for heading in headings:
        value = section(text, heading)
        if value.strip():
            return value.strip()
    return ""


def infer_types(text: str) -> list[str]:
    lowered = text.lower()
    types = []
    for label, keywords in TYPE_KEYWORDS.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            types.append(label)
    return types or ["未分类"]


PRIMARY_TYPE_ORDER = [
    "Agent Runtime",
    "Tool Runtime",
    "MCP",
    "Memory",
    "Permission / Sandbox",
    "Multi-Agent",
    "Provider",
    "Productization",
    "Observability",
    "Frontend Design",
    "Workbench UI",
    "AI Frontend Generation",
    "Plugin / Skill",
]


def choose_primary_category(types: list[str]) -> str:
    for label in PRIMARY_TYPE_ORDER:
        if label in types:
            return label
    return types[0] if types else "未分类"


def normalize_inline(text: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", text)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]+)\*", r"\1", value)
    value = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\t\r\n")


def first_sentence(text: str) -> str:
    cleaned = normalize_inline(text)
    if not cleaned:
        return ""
    match = re.split(r"(?<=[。！？!?])\s+", cleaned, maxsplit=1)
    return match[0].strip()


def extract_business_scenario(text: str) -> str:
    scenario_section = first_nonempty_section(text, "核心场景", "核心使用场景")
    scenario_items = list_items(scenario_section)
    if scenario_items:
        return normalize_inline(scenario_items[0])
    paragraph = first_paragraph(scenario_section)
    return first_sentence(paragraph) or "待补充具体业务场景"


def extract_biggest_highlight(text: str) -> str:
    sentence = first_sentence(first_nonempty_section(text, "项目一句话"))
    if sentence:
        return sentence
    why_section = first_nonempty_section(text, "为什么这个项目值得拿去面试", "为什么值得学", "为什么值得看")
    why_items = list_items(why_section)
    if why_items:
        return normalize_inline(why_items[0])
    return first_sentence(first_paragraph(why_section)) or "待补充最大亮点"


def extract_one_line_verdict(text: str, fallback: str) -> str:
    verdict = first_sentence(first_nonempty_section(text, "项目一句话"))
    return verdict or fallback


def extract_why_read_now(text: str) -> str:
    why_section = first_nonempty_section(text, "为什么这个项目值得拿去面试", "为什么值得学", "为什么值得继续做")
    why_items = list_items(why_section)
    if why_items:
        return normalize_inline(why_items[0])
    return first_sentence(first_paragraph(why_section)) or "待补充推荐理由"


def extract_oral_answer(text: str) -> str:
    oral = heading_block(text, "一分钟讲法", "口语版回答", "口语版讲法")
    return first_paragraph(oral) or first_sentence(oral)


def extract_engineering_pitch(text: str) -> str:
    pitch = heading_block(text, "三分钟工程讲法", "工程视角拆解", "工程讲法")
    return first_paragraph(pitch) or first_sentence(pitch)


def extract_source_url(text: str) -> str:
    match = re.search(r"https?://[^\s)]+", text)
    return match.group(0) if match else ""


def status_for_project(text: str) -> str:
    if "待人工补充" in text or "待补充" in text:
        return "草稿"
    return "深度沉淀"


def load_radar_scores() -> dict[str, dict[str, Any]]:
    if not RADAR_DATA.exists():
        return {}
    data = json.loads(read_text(RADAR_DATA))
    result = {}
    for full_name, item in data.get("candidates", {}).items():
        key = full_name.lower().replace("/", "-").replace("_", "-")
        result[key] = item
    return result


def load_legacy_cases() -> list[dict[str, Any]]:
    if not LEGACY_INDEX.exists():
        return []
    data = json.loads(read_text(LEGACY_INDEX))
    return data.get("cases", [])


def load_writeback_packages() -> dict[str, dict[str, Any]]:
    if not WRITEBACK_PACKAGE_DIR.exists():
        return {}
    packages: dict[str, dict[str, Any]] = {}
    for path in sorted(WRITEBACK_PACKAGE_DIR.glob("*.json")):
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        package_id = str(payload.get("sourceProjectId") or path.stem)
        packages[package_id] = payload
    return packages


def build_pain_point_rollups(writebacks: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    rollups: dict[str, dict[str, Any]] = {}
    for package in writebacks.values():
        title = str(package.get("sourceTitle") or package.get("sourceProjectId") or "").strip()
        updated_at = str(package.get("updatedAt") or package.get("createdAt") or "").strip()
        for item in package.get("painPoints", []) or []:
            pain_id = str(item.get("id") or "").strip()
            if not pain_id:
                continue
            rollup = rollups.setdefault(
                pain_id,
                {
                    "projects": [],
                    "practices": [],
                    "signals": [],
                    "updatedAt": "",
                },
            )
            if title and title not in rollup["projects"]:
                rollup["projects"].append(title)
            practice = str(item.get("practice") or "").strip()
            if practice and practice not in rollup["practices"]:
                rollup["practices"].append(practice)
            for signal in item.get("signals", []) or []:
                signal_text = str(signal).strip()
                if signal_text and signal_text not in rollup["signals"]:
                    rollup["signals"].append(signal_text)
            if updated_at:
                rollup["updatedAt"] = updated_at
    return rollups


def merge_unique_lists(*groups: list[str]) -> list[str]:
    merged: list[str] = []
    for group in groups:
        for item in group:
            text = str(item).strip()
            if text and text not in merged:
                merged.append(text)
    return merged


def build_projects() -> list[dict[str, Any]]:
    radar = load_radar_scores()
    legacy_cases = load_legacy_cases()
    writebacks = load_writeback_packages()
    projects = []

    def writeback_view(project_id: str) -> tuple[dict[str, list[str]], str, str, str, list[str]]:
        package = writebacks.get(project_id, {})
        targets = {
            "patterns": [item.get("id", "") for item in package.get("patterns", []) if item.get("id")],
            "painPoints": [item.get("id", "") for item in package.get("painPoints", []) if item.get("id")],
            "interviews": [item.get("id", "") for item in package.get("interviews", []) if item.get("id")],
        }
        return (
            targets,
            str(package.get("writebackSummary", "")),
            str(package.get("writebackStatus", "none")),
            str(package.get("updatedAt", "") or package.get("createdAt", "")),
            [str(item).strip() for item in package.get("writebackReasoning", []) if str(item).strip()],
        )

    current_path = CURRENT_PROJECT
    if current_path.exists():
        text = read_text(current_path)
        current_types = ["Agent Runtime", "Knowledge Platform", "Project Radar"]
        current_summary = first_paragraph(section(text, "项目一句话")) or "Claude Code sourcemap 研究基座与 Agent 工程知识库。"
        current_targets, current_summary_text, current_writeback_status, current_writeback_updated_at, current_writeback_reasoning = writeback_view("current-project")
        projects.append(
            {
                "id": "current-project",
                "name": "claude-code-sourcemap",
                "url": "",
                "summary": current_summary,
                "types": current_types,
                "primaryCategory": choose_primary_category(current_types),
                "businessScenario": extract_business_scenario(text),
                "biggestHighlight": extract_biggest_highlight(text),
                "oneLineVerdict": extract_one_line_verdict(text, current_summary),
                "whyReadNow": extract_why_read_now(text),
                "oralAnswer": extract_oral_answer(text),
                "engineeringPitch": extract_engineering_pitch(text),
                "status": "深度沉淀",
                "score": 100,
                "sourceFile": str(current_path.relative_to(ROOT)).replace("\\", "/"),
                "relatedPatterns": infer_related_patterns(text),
                "writebackTargets": current_targets,
                "writebackSummary": current_summary_text,
                "writebackStatus": current_writeback_status,
                "writebackUpdatedAt": current_writeback_updated_at,
                "writebackReasoning": current_writeback_reasoning,
                "nextActions": first_nonempty_list(
                    section(text, "下一步行动项"),
                    section(text, "当前项目行动项"),
                    section(text, "对当前知识平台的行动项"),
                    section(text, "当前行动项"),
                    section(text, "当前项目的启发"),
                ),
                "content": text,
            }
        )

    for path_item in sorted(EXTERNAL.rglob("*.md")):
        if path_item.name.lower() == "readme.md":
            continue
        text = read_text(path_item)
        project_id = slug_from_path(path_item)
        radar_item = radar.get(project_id, {})
        writeback_targets, writeback_summary, writeback_status, writeback_updated_at, writeback_reasoning = writeback_view(project_id)
        project_summary = first_paragraph(section(text, "项目一句话")) or radar_item.get("description", "")
        project_types = infer_types(text)
        projects.append(
            {
                "id": project_id,
                "name": title_from_markdown(text, project_id).replace("项目沉淀：", ""),
                "url": extract_source_url(text),
                "summary": project_summary,
                "types": project_types,
                "primaryCategory": choose_primary_category(project_types),
                "businessScenario": extract_business_scenario(text),
                "biggestHighlight": extract_biggest_highlight(text),
                "oneLineVerdict": extract_one_line_verdict(text, project_summary),
                "whyReadNow": extract_why_read_now(text),
                "oralAnswer": extract_oral_answer(text),
                "engineeringPitch": extract_engineering_pitch(text),
                "status": status_for_project(text),
                "score": radar_item.get("score", {}).get("total"),
                "sourceFile": str(path_item.relative_to(ROOT)).replace("\\", "/"),
                "relatedPatterns": infer_related_patterns(text),
                "writebackTargets": writeback_targets,
                "writebackSummary": writeback_summary,
                "writebackStatus": writeback_status,
                "writebackUpdatedAt": writeback_updated_at,
                "writebackReasoning": writeback_reasoning,
                "nextActions": first_nonempty_list(
                    section(text, "对我当前项目的行动项"),
                    section(text, "对当前知识平台的行动项"),
                    section(text, "当前项目行动项"),
                    section(text, "当前行动项"),
                    section(text, "给当前项目的启发"),
                    section(text, "我们应该怎么做"),
                ),
                "scenarioSection": extract_named_section(text, ["核心场景", "核心使用场景"]),
                "problemSection": extract_named_section(text, ["它解决的通用问题", "通用问题"]),
                "solutionSection": extract_named_section(text, ["这个项目具体怎么做", "优秀技术和框架", "技术和框架"]),
                "frameworkSection": extract_named_section(text, ["优秀技术和框架", "技术框架"]),
                "principleSection": extract_named_section(text, ["可迁移设计原则", "设计原则"]),
                "actionSection": extract_named_section(text, ["对我当前项目的行动项", "对当前知识平台的行动项", "当前项目行动项"]),
                "tradeoffSection": extract_named_section(text, ["Trade-off 与边界", "Trade-off", "代价和边界", "边界"]),
                "content": text,
            }
        )

    known_ids = {project["id"] for project in projects}
    for case in legacy_cases:
        case_id = f"legacy-{case.get('id', '').lower().replace('_', '-')}"
        if not case.get("id") or case.get("migratedTo") or case_id in known_ids:
            continue
        projects.append(
            {
                "id": case_id,
                "name": case.get("name", case.get("id", case_id)),
                "url": case.get("url", ""),
                "summary": case.get("coreValue", ""),
                "types": case.get("types", ["旧体系待迁移"]),
                "primaryCategory": choose_primary_category(case.get("types", ["旧体系待迁移"])),
                "businessScenario": case.get("scenario", "") or "待从旧文档补充业务场景",
                "biggestHighlight": case.get("coreValue", "") or "待从旧文档补充最大亮点",
                "oneLineVerdict": case.get("coreValue", "") or case.get("name", case_id),
                "whyReadNow": "这是旧体系里的高价值样本，适合优先迁移进新的项目概述与详情体系。",
                "oralAnswer": "",
                "engineeringPitch": "",
                "status": "旧体系待迁移",
                "score": None,
                "sourceFile": case.get("userDoc", ""),
                "relatedPatterns": case.get("relatedPatterns", []),
                "writebackTargets": {"patterns": [], "painPoints": [], "interviews": []},
                "writebackSummary": "",
                "writebackStatus": "none",
                "writebackUpdatedAt": "",
                "writebackReasoning": [],
                "nextActions": [
                    "读取旧 user/agent 两份沉淀",
                    "迁移为 docs/external-projects 下的单项目沉淀",
                    "更新至少一个 docs/patterns 通用问题文档",
                ],
                "content": case.get("agentSummary", "") or case.get("userSummary", "") or case.get("coreValue", ""),
            }
        )

    return projects


def build_solutions() -> list[dict[str, Any]]:
    solutions = []
    for path in sorted(PATTERNS.rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = read_text(path)
        solution_id = slug_from_path(path).replace("-patterns", "")
        problem_definition = first_paragraph(
            first_nonempty_section(
                text,
                "问题定义",
                "这件事在项目里到底考什么",
                "这件事到底考什么",
            )
        ) or first_paragraph(text)
        solutions.append(
            {
                "id": solution_id,
                "title": title_from_markdown(text, solution_id).replace("通用问题：", ""),
                "problemDefinition": problem_definition,
                "whyImportant": list_items(section(text, "为什么重要")),
                "commonMistakes": list_items(section(text, "常见错误做法")),
                "maturePractices": list_items(section(text, "成熟系统通常怎么做")),
                "actions": first_nonempty_list(
                    section(text, "我的项目行动项"),
                    section(text, "当前项目行动项"),
                    section(text, "当前行动项"),
                    section(text, "给当前项目的启发"),
                    section(text, "我们应该怎么做"),
                ),
                "structureSection": extract_named_section(text, ["典型方案结构", "方案结构"]),
                "practiceSection": extract_named_section(text, ["成熟系统通常怎么做", "常见步骤", "成熟做法"]),
                "mistakeSection": extract_named_section(text, ["常见错误做法", "常见误区"]),
                "actionSection": extract_named_section(text, ["我的项目行动项", "当前项目行动项", "当前行动项", "我们应该怎么做"]),
                "sourceFile": str(path.relative_to(ROOT)).replace("\\", "/"),
                "content": text,
            }
        )
    return solutions


def build_pain_points(projects: list[dict[str, Any]], solutions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    known_projects = {project["id"] for project in projects}
    known_solutions = {solution["title"]: solution["id"] for solution in solutions}
    writeback_rollups = build_pain_point_rollups(load_writeback_packages())
    pain_point_docs = {}
    if PAIN_POINTS_DIR.exists():
        for path in PAIN_POINTS_DIR.rglob("*.md"):
            if path.name.lower() == "readme.md":
                continue
            pain_point_docs[path.stem] = {
                "content": read_text(path),
                "sourceFile": str(path.relative_to(ROOT)).replace("\\", "/"),
            }
    pain_points = []
    for seed in PAIN_POINT_SEEDS:
        item = dict(seed)
        rollup = writeback_rollups.get(seed["id"], {})
        item["evidenceProjects"] = [pid for pid in seed["evidenceProjects"] if pid in known_projects]
        item["relatedSolution"] = known_solutions.get(seed["topic"], seed["topic"].lower().replace(" ", "-"))
        item["content"] = pain_point_docs.get(seed["id"], {}).get("content", "")
        item["sourceFile"] = pain_point_docs.get(seed["id"], {}).get("sourceFile", "")
        item["commonPractices"] = merge_unique_lists(
            item.get("maturePractices", []),
            rollup.get("practices", []),
        )
        item["dataSignals"] = merge_unique_lists(
            item.get("dataSignals", []),
            rollup.get("signals", []),
        )
        item["evidenceProjectCount"] = len(item["evidenceProjects"]) + len(rollup.get("projects", []))
        item["lastUpdatedFromProjects"] = rollup.get("projects", [])
        if rollup.get("updatedAt"):
            item["lastUpdatedAt"] = rollup.get("updatedAt")
        pain_points.append(item)
    return pain_points


def source_type_from_path(path: Path) -> str:
    try:
        rel = path.relative_to(SOURCE_LIBRARY)
    except ValueError:
        return "资料源"
    parts = rel.parts
    if len(parts) > 1:
        return parts[0]
    return "资料源入口"


def evidence_strength_for(source_type: str, related_pain_points: list[str], related_patterns: list[str], text: str) -> str:
    score = 0
    if source_type in {"GitHub 优质项目", "论文研究资料"}:
        score += 2
    if source_type in {"优质技术博客", "用户提供文档"}:
        score += 1
    if related_pain_points:
        score += 1
    if related_patterns:
        score += 1
    lowered = text.lower()
    if any(token in lowered for token in ["evidence", "benchmark", "实验", "数据", "案例", "源码", "README"]):
        score += 1
    if score >= 5:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def recommended_use_for(source_type: str, evidence_strength: str, related_pain_points: list[str], related_patterns: list[str]) -> str:
    if evidence_strength == "high" and related_pain_points:
        return "优先补强行业痛点和方案文档，再决定是否升级成单项目深度沉淀。"
    if evidence_strength == "high":
        return "优先进入深度沉淀，补充证据链、可迁移框架和当前项目行动项。"
    if related_patterns:
        return "先作为方案或模式的补充证据使用，后续根据价值再升级。"
    if source_type == "用户提供文档":
        return "先用于面试、痛点证据或当前项目行动项，再决定是否公开沉淀。"
    return "先留在资料源池观察，等出现更多关联痛点或方案后再升级。"


def build_sources() -> list[dict[str, Any]]:
    if not SOURCE_LIBRARY.exists():
        return []
    sources = []
    for path in sorted(SOURCE_LIBRARY.rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = read_text(path)
        source_id = "source-" + slug_from_path(path)
        source_type = source_type_from_path(path)
        related_pain_points = infer_related_pain_points(text)
        related_patterns = infer_related_patterns(text)
        evidence_strength = evidence_strength_for(source_type, related_pain_points, related_patterns, text)
        sources.append(
            {
                "id": source_id,
                "title": title_from_markdown(text, path.stem),
                "sourceType": source_type,
                "evidenceStrength": evidence_strength,
                "summary": first_paragraph(text),
                "sourceFile": str(path.relative_to(ROOT)).replace("\\", "/"),
                "relatedPainPoints": related_pain_points,
                "relatedPatterns": related_patterns,
                "recommendedUse": recommended_use_for(source_type, evidence_strength, related_pain_points, related_patterns),
                "actions": list_items(section(text, "当前项目行动项")) or list_items(section(text, "我们应该怎么做")),
                "valueSection": extract_named_section(text, ["资料价值判断", "这份资料为什么值得看", "为什么值得读"]),
                "insightSection": extract_named_section(text, ["可提炼观点", "核心启发", "这份资料具体说透了什么"]),
                "writebackSection": extract_named_section(text, ["可回写主题", "回写建议", "可以反哺哪些主题"]),
                "content": text,
            }
        )
    return sources


def infer_related_pain_points(text: str) -> list[str]:
    lowered = text.lower()
    mapping = {
        "tool-result-context-overload": ["tool", "工具", "上下文", "artifact"],
        "mcp-ecosystem-governance": ["mcp", "工具生态"],
        "provider-differences-pollute-runtime": ["provider", "多模型"],
        "project-learning-stays-as-notes": ["沉淀", "知识", "学习", "读书笔记"],
        "agent-productization-gap": ["产品化", "平台", "release", "治理"],
        "agent-ui-style-drift": ["前端", "design", "视觉", "ui"],
    }
    return [pid for pid, keys in mapping.items() if any(key.lower() in lowered for key in keys)]


def infer_related_patterns(text: str) -> list[str]:
    lowered = text.lower()
    mapping = {
        "agent-runtime": ["agent runtime", "coding agent", "runtime", "subagent", "checkpoint", "resume"],
        "tool-runtime": ["tool runtime", "tool", "artifact", "command", "shell", "patch"],
        "mcp-integration": ["mcp", "model context protocol", "tool registry", "mcp server"],
        "memory-system": ["memory", "retrieval", "freshness", "summary", "context"],
        "permission-sandbox": ["permission", "sandbox", "approval", "risk", "audit"],
        "observability-patterns": ["trace", "report", "benchmark", "eval", "telemetry", "observability"],
        "provider-abstraction-patterns": ["provider", "model adapter", "capability", "multi-model"],
        "productization-patterns": ["productization", "workflow", "settings", "hooks", "platform"],
        "plugin-system": ["plugin", "skill", "extension"],
        "multi-agent": ["multi-agent", "subagent", "delegation"],
    }
    return [pattern_id for pattern_id, keys in mapping.items() if any(key.lower() in lowered for key in keys)]


def build_interview_seed(projects: list[dict[str, Any]], solutions: list[dict[str, Any]], pain_points: list[dict[str, Any]]) -> dict[str, Any]:
    if INTERVIEW_BANK.exists():
        bank = json.loads(read_text(INTERVIEW_BANK))
        merged_items = list(bank.get("items", []))
        seen_ids = {item.get("id") for item in merged_items}
        for path in sorted(INTERVIEW_BANK.parent.glob(INTERVIEW_BANK_GLOB)):
            if path == INTERVIEW_BANK:
                continue
            extra_bank = json.loads(read_text(path))
            for item in extra_bank.get("items", []):
                item_id = item.get("id")
                if item_id and item_id not in seen_ids:
                    merged_items.append(item)
                    seen_ids.add(item_id)
        bank["items"] = merged_items
        bank["questionCount"] = len(merged_items)
        return bank
    return {
        "questionCount": 6,
        "items": [
            {
                "id": "tool-runtime-project-question",
                "rawQuestion": "你怎么理解 Tool Runtime？它和普通函数调用有什么区别？",
                "questionType": "项目追问",
                "knowledgePoints": ["Tool Runtime", "MCP Integration", "Permission"],
                "relatedProjects": ["chromedevtools-chrome-devtools-mcp", "current-project"],
                "relatedPatterns": ["tool-runtime", "mcp-integration"],
                "recommendedAnswer": "先定义 Tool Runtime 是模型影响外部世界的执行管线，再结合本项目 docs/patterns/Tool 与 MCP 工具体系/tool-runtime-patterns.md，说明 schema、权限、执行、结果归一化和 telemetry，最后引用 Chrome DevTools MCP 的 artifact reference 设计。",
                "followUps": ["如果工具返回结果很大怎么办？", "如何区分只读工具和高风险工具？"],
            },
            {
                "id": "project-radar-design-question",
                "rawQuestion": "你为什么要做 Project Radar？它解决了什么问题？",
                "questionType": "项目追问",
                "knowledgePoints": ["Project Radar", "Knowledge Distillation"],
                "relatedProjects": ["current-project"],
                "relatedPatterns": ["agent-engineering-framework"],
                "recommendedAnswer": "说明它不是 GitHub 搜索器，而是发现、评分、候选池、沉淀、patterns 更新的学习闭环，解决项目学习停留在收藏链接的问题。",
                "followUps": ["评分维度怎么设计？", "怎么避免低质量项目污染知识库？"],
            },
            {
                "id": "mcp-integration-question",
                "rawQuestion": "如果让你的平台接入 MCP 工具生态，你会怎么设计？",
                "questionType": "系统设计",
                "knowledgePoints": ["MCP", "Tool Registry", "Permission Mapping"],
                "relatedProjects": ["chromedevtools-chrome-devtools-mcp", "aaif-goose-goose"],
                "relatedPatterns": ["mcp-integration", "tool-runtime"],
                "recommendedAnswer": "用 External Capability -> MCP Server -> Tool Discovery -> Tool Registry -> Permission Mapping -> Result Summary -> Artifact Reference -> Telemetry 这条链路回答，并说明 Goose 与 Chrome DevTools MCP 的不同角色。",
                "followUps": ["MCP server 有状态怎么办？", "OAuth 和权限如何处理？"],
            },
        ],
        "memory": {
            "focus": "围绕当前项目、外部优秀 Agent 项目和 patterns 进行项目深挖。",
            "answerStyle": "定义问题 -> 为什么重要 -> 当前项目实践 -> 外部项目证据 -> trade-off 和下一步。",
            "weakSpots": [],
        },
    }


def compact_text(text: str, limit: int = 2400) -> str:
    cleaned = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:limit]


def search_item(
    *,
    entity_id: str,
    kind: str,
    title: str,
    summary: str,
    source_file: str,
    tags: list[str],
    context: str,
    content: str,
) -> dict[str, Any]:
    return {
        "id": f"{kind}-{entity_id}",
        "entityId": entity_id,
        "kind": kind,
        "title": title,
        "summary": summary,
        "sourceFile": source_file,
        "tags": tags,
        "context": context,
        "searchableText": compact_text(content),
    }


def build_search_index(
    projects: list[dict[str, Any]],
    solutions: list[dict[str, Any]],
    pain_points: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    engineering_logic: dict[str, Any],
    interviews: dict[str, Any],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for project in projects:
        items.append(
            search_item(
                entity_id=project["id"],
                kind="project",
                title=project["name"],
                summary=project.get("summary", ""),
                source_file=project.get("sourceFile", ""),
                tags=project.get("types", []) + project.get("relatedPatterns", []),
                context="项目样本：适合看它解决了什么行业痛点、用了什么工程做法、能给当前项目什么启发。",
                content=project.get("content", ""),
            )
        )
    for solution in solutions:
        items.append(
            search_item(
                entity_id=solution["id"],
                kind="solution",
                title=solution["title"],
                summary=solution.get("problemDefinition", ""),
                source_file=solution.get("sourceFile", ""),
                tags=solution.get("maturePractices", [])[:4],
                context="方案框架：适合从多个项目里抽象通用问题、成熟做法和行动项。",
                content=solution.get("content", ""),
            )
        )
    for pain_point in pain_points:
        items.append(
            search_item(
                entity_id=pain_point["id"],
                kind="painPoint",
                title=pain_point["title"],
                summary=pain_point.get("industryPain") or pain_point.get("solutionMethod", ""),
                source_file=pain_point.get("sourceFile", "scripts/build_knowledge_index.py"),
                tags=[pain_point.get("topic", ""), pain_point.get("severity", "")] + pain_point.get("evidenceSources", []),
                context="行业痛点：适合看业内普遍问题、证据来源、优秀项目共性做法和当前项目行动项。",
                content=" ".join(
                    [
                        pain_point.get("industryPain", ""),
                        pain_point.get("solutionMethod", ""),
                        " ".join(pain_point.get("maturePractices", [])),
                        " ".join(pain_point.get("commonPractices", [])),
                        " ".join(pain_point.get("commonMistakes", [])),
                        " ".join(pain_point.get("actions", [])),
                    ]
                ),
            )
        )
    for source in sources:
        items.append(
            search_item(
                entity_id=source["id"],
                kind="source",
                title=source["title"],
                summary=source.get("summary", ""),
                source_file=source.get("sourceFile", ""),
                tags=[source.get("sourceType", ""), source.get("evidenceStrength", "")] + source.get("relatedPainPoints", []) + source.get("relatedPatterns", []),
                context="资料源：适合判断外部资料能补强哪个痛点、方案或行动项。",
                content=source.get("content", ""),
            )
        )
    items.append(
        search_item(
            entity_id="engineering-logic",
            kind="solution",
            title=engineering_logic.get("title", "工程逻辑"),
            summary=engineering_logic.get("summary", ""),
            source_file=engineering_logic.get("sourceFile", ""),
            tags=["工程逻辑", "方法论", "项目决策"] + engineering_logic.get("currentFocus", []),
            context="工程逻辑：适合把项目、方案、痛点和资料源收束成真实项目的设计顺序与验证逻辑。",
            content=engineering_logic.get("content", ""),
        )
    )
    for interview in interviews.get("items", []):
        items.append(
            search_item(
                entity_id=interview["id"],
                kind="interview",
                title=interview["rawQuestion"],
                summary=interview.get("recommendedAnswer", ""),
                source_file="docs/interviews/question-bank.json",
                tags=interview.get("knowledgePoints", []) + interview.get("relatedPatterns", []),
                context="面试题：适合把项目沉淀、行业痛点和方案框架转成可表达答案。",
                content=" ".join([interview.get("recommendedAnswer", ""), " ".join(interview.get("followUps", []))]),
            )
        )
    return items


def build_engineering_logic(
    projects: list[dict[str, Any]],
    solutions: list[dict[str, Any]],
    pain_points: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    if not ENGINEERING_LOGIC_DOC.exists():
        return {
            "title": "工程逻辑",
            "summary": "把项目、方案、痛点和资料源收束成真实项目的工程主链路。",
            "sourceFile": "",
            "stages": [],
            "routeMap": [],
            "currentFocus": [],
            "riskBoundaries": [],
            "validationChecklist": [],
            "recommendedOrder": [],
            "actions": [],
            "content": "",
        }
    text = read_text(ENGINEERING_LOGIC_DOC)
    route_map = [
        {"title": "发现阶段", "route": "雷达 / 资料源", "purpose": "找高质量项目和资料，判断是否值得进入沉淀。", "output": "候选项目 / 候选资料 / 优先级"},
        {"title": "沉淀阶段", "route": "项目", "purpose": "把单个项目转成可学习、可迁移的深度文档。", "output": "单项目沉淀 / 可迁移原则 / 行动项"},
        {"title": "抽象阶段", "route": "方案", "purpose": "把多个项目收束为通用技术框架。", "output": "问题定义 / 成熟做法 / 可迁移框架"},
        {"title": "诊断阶段", "route": "痛点", "purpose": "抽出行业共性难题、误区、数据信号和解决路径。", "output": "行业痛点 / 证据来源 / 解法"},
        {"title": "决策阶段", "route": "工程逻辑", "purpose": "决定做项目时的设计顺序、风险边界和验证方法。", "output": "默认顺序 / 风险边界 / 验证清单"},
        {"title": "表达阶段", "route": "面经 / 面试官", "purpose": "把学习和实践结果转成复盘、汇报和面试表达。", "output": "推荐回答 / 追问链 / 表达素材"},
    ]
    return {
        "title": title_from_markdown(text, "工程逻辑"),
        "summary": first_paragraph(section(text, "路由一句话")) or first_paragraph(text),
        "sourceFile": str(ENGINEERING_LOGIC_DOC.relative_to(ROOT)).replace("\\", "/"),
        "stages": [{"title": item["title"], "route": item["route"], "purpose": item["purpose"]} for item in route_map],
        "routeMap": route_map,
        "currentFocus": [
            f"项目样本 {len(projects)} 个",
            f"方案框架 {len(solutions)} 个",
            f"行业痛点 {len(pain_points)} 个",
            f"资料源 {len(sources)} 个",
        ],
        "riskBoundaries": list_items(section(text, "风险边界")),
        "validationChecklist": list_items(section(text, "验证清单")),
        "recommendedOrder": list_items(section(text, "默认执行顺序")),
        "actions": first_nonempty_list(
            section(text, "当前项目行动项"),
            section(text, "我们应该怎么做"),
        ),
        "content": text,
    }


def main() -> int:
    projects = build_projects()
    solutions = build_solutions()
    pain_points = build_pain_points(projects, solutions)
    sources = build_sources()
    engineering_logic = build_engineering_logic(projects, solutions, pain_points, sources)
    interviews = build_interview_seed(projects, solutions, pain_points)
    search_index = build_search_index(projects, solutions, pain_points, sources, engineering_logic, interviews)
    data = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "language": "zh-CN",
        "projects": projects,
        "solutions": solutions,
        "painPoints": pain_points,
        "sources": sources,
        "searchIndex": search_index,
        "engineeringLogic": engineering_logic,
        "interviews": interviews,
    }
    write_json(OUTPUT, data)
    if APP_OUTPUT.parent.exists():
        write_json(APP_OUTPUT, data)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    if APP_OUTPUT.parent.exists():
        print(f"Wrote {APP_OUTPUT.relative_to(ROOT)}")
    print(
        f"Projects={len(projects)} Solutions={len(solutions)} PainPoints={len(pain_points)} "
        f"Sources={len(sources)} SearchItems={len(search_index)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
