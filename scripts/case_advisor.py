#!/usr/bin/env python3
"""Generate evidence-backed suggestions from the workbench case library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = REPO_ROOT / ".claude" / "sessions" / "index.json"
SKILLS_ROOT = REPO_ROOT / ".claude" / "skills"
MEMORY_ROOT = REPO_ROOT / ".claude" / "memory"
DOCS_ROOT = REPO_ROOT / ".claude" / "docs" / "user" / "shared"

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}

PROJECT_TYPE_HINTS: dict[str, dict[str, Any]] = {
    "team-knowledge": {
        "description": "Focus on curated know-how, reusable task assets, onboarding, and knowledge packaging rather than runtime depth.",
        "skills": [
            "agent-research-workbench",
            "agent-feature-roadmap",
        ],
        "memory": [
            "memory-operating-model.md",
            "agent-project-triage.md",
            "project-preferences.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {"knowledge", "library", "prompt", "skill", "onboarding", "workflow", "asset"},
    },
    "runtime-first": {
        "description": "Focus on engine loop, run state, tool continuation, and execution stability.",
        "skills": [
            "agent-research-workbench",
            "agent-architecture-review",
        ],
        "memory": [
            "agent-project-triage.md",
            "agent-principles.md",
            "agent-patterns.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {"runtime", "loop", "engine", "execution", "state", "subagent"},
    },
    "platform-expansion": {
        "description": "Focus on governance, platform maturity, rollout, and capability surface.",
        "skills": [
            "agent-platform-design",
            "agent-feature-roadmap",
        ],
        "memory": [
            "agent-project-triage.md",
            "agent-principles.md",
            "project-preferences.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {"platform", "governance", "rollout", "workspace", "product"},
    },
    "vertical-workflow": {
        "description": "Focus on domain workflow packaging, procedure design, and end-to-end delivery shape.",
        "skills": [
            "agent-research-workbench",
            "agent-platform-design",
        ],
        "memory": [
            "agent-project-triage.md",
            "agent-principles.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {"workflow", "domain", "report", "sop", "procedure"},
    },
    "tool-runtime": {
        "description": "Focus on skills, MCP, adapters, plugins, and capability substrate design.",
        "skills": [
            "agent-platform-design",
            "agent-architecture-review",
        ],
        "memory": [
            "mcp-strategy.md",
            "agent-patterns.md",
            "agent-principles.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {
            "tool",
            "mcp",
            "plugin",
            "adapter",
            "skills",
            "sandbox",
            "browser",
            "cdp",
            "harness",
            "substrate",
        },
    },
    "memory-first": {
        "description": "Focus on memory schema, extraction, injection, and long-term knowledge hygiene.",
        "skills": [
            "agent-research-workbench",
            "agent-platform-design",
        ],
        "memory": [
            "memory-operating-model.md",
            "agent-principles.md",
            "agent-patterns.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {"memory", "session", "retrieval", "history", "knowledge"},
    },
    "evidence-first": {
        "description": "Focus on retrieval, evidence grounding, verification, and source-backed outputs.",
        "skills": [
            "agent-architecture-review",
            "agent-feature-roadmap",
        ],
        "memory": [
            "agent-principles.md",
            "agent-review-checklist.md",
        ],
        "docs": [
            "agent-project-classification-map.md",
        ],
        "tokens": {"evidence", "rag", "verification", "source", "retrieval"},
    },
}

GOAL_HINTS: dict[str, dict[str, Any]] = {
    "analyze": {
        "skills": ["agent-architecture-review"],
        "memory": ["agent-project-triage.md", "agent-review-checklist.md"],
        "tokens": {"analyze", "review", "architecture", "understand"},
    },
    "design": {
        "skills": ["agent-platform-design"],
        "memory": ["agent-principles.md", "agent-patterns.md"],
        "tokens": {"design", "build", "platform", "architecture"},
    },
    "roadmap": {
        "skills": ["agent-feature-roadmap"],
        "memory": ["project-preferences.md", "agent-principles.md"],
        "tokens": {"roadmap", "priority", "plan", "sequence"},
    },
    "knowledge": {
        "skills": ["agent-research-workbench"],
        "memory": ["memory-operating-model.md", "agent-project-triage.md"],
        "tokens": {"knowledge", "case", "library", "memory", "reuse"},
    },
    "continuous-execution": {
        "skills": ["autonomous-delivery-default"],
        "memory": ["autonomous-execution-preference.md"],
        "tokens": {"continuous", "autonomous", "execution", "phase", "report"},
    },
}

CASE_TAGS: dict[str, set[str]] = {
    "2026-04-27-awesome-ai-research-writing-analysis": {
        "team-knowledge",
        "vertical-workflow",
        "research-writing",
        "prompt-library",
        "skills-adoption",
        "knowledge",
        "workflow",
        "asset",
    },
    "awesome-ai-research-writing": {
        "team-knowledge",
        "vertical-workflow",
        "research-writing",
        "prompt-library",
        "skills-adoption",
        "knowledge",
        "workflow",
        "asset",
    },
    "2026-04-22-hermes-agent-analysis": {
        "runtime-first",
        "memory-first",
        "tool-runtime",
        "knowledge",
        "continuous-execution",
        "workbench",
        "session-search",
        "skills",
        "mcp",
        "long-running-agent",
    },
    "hermes-agent": {
        "runtime-first",
        "memory-first",
        "tool-runtime",
        "knowledge",
        "continuous-execution",
        "workbench",
        "session-search",
        "skills",
        "mcp",
        "long-running-agent",
    },
    "2026-04-28-browser-harness-analysis": {
        "tool-runtime",
        "runtime-first",
        "browser-control",
        "browser-harness",
        "cdp",
        "interaction-skills",
        "domain-skills",
        "substrate",
        "self-healing-helpers",
    },
    "browser-harness": {
        "tool-runtime",
        "runtime-first",
        "browser-control",
        "browser-harness",
        "cdp",
        "interaction-skills",
        "domain-skills",
        "substrate",
        "self-healing-helpers",
    },
}


def load_index(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Session index must be a JSON object.")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Session index must contain an 'entries' list.")
    return data


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in (match.group(0).lower() for match in TOKEN_RE.finditer(text))
        if token not in STOPWORDS
    }


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(normalize_text(item) for item in value.values())
    return str(value)


def build_query_tokens(project_type: str | None, goal: str | None, text: str | None) -> set[str]:
    tokens: set[str] = set()
    if project_type:
        tokens.add(project_type)
        tokens.update(PROJECT_TYPE_HINTS.get(project_type, {}).get("tokens", set()))
    if goal:
        tokens.add(goal)
        tokens.update(GOAL_HINTS.get(goal, {}).get("tokens", set()))
    if text:
        tokens.update(tokenize(text))
    return tokens


def entry_tokens(entry: dict[str, Any]) -> set[str]:
    tokens = tokenize(
        " ".join(
            [
                normalize_text(entry.get("id")),
                normalize_text(entry.get("project")),
                normalize_text(entry.get("task_type")),
                normalize_text(entry.get("title")),
                normalize_text(entry.get("summary")),
                normalize_text(entry.get("keywords", [])),
                normalize_text(entry.get("related_cases", [])),
                normalize_text(entry.get("skill_promotions", [])),
                normalize_text(entry.get("memory_promotions", [])),
                normalize_text(entry.get("doc_promotions", [])),
            ]
        )
    )
    tokens.update(CASE_TAGS.get(str(entry.get("id")), set()))
    tokens.update(CASE_TAGS.get(str(entry.get("project")), set()))
    return tokens


def score_entry(entry: dict[str, Any], query_tokens: set[str]) -> tuple[int, list[str]]:
    tokens = entry_tokens(entry)
    overlaps = sorted(query_tokens & tokens)
    score = len(overlaps) * 3

    project = str(entry.get("project", "")).lower()
    if project in query_tokens:
        score += 4
    if str(entry.get("task_type", "")).lower() in query_tokens:
        score += 2
    return score, overlaps


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def resolve_paths(filenames: list[str], root: Path) -> list[Path]:
    paths = []
    for filename in dedupe_keep_order(filenames):
        path = root / filename
        if path.exists():
            paths.append(path)
    return paths


def recommend_skills(project_type: str | None, goal: str | None) -> list[Path]:
    names: list[str] = []
    if goal:
        names.extend(GOAL_HINTS.get(goal, {}).get("skills", []))
    if project_type:
        names.extend(PROJECT_TYPE_HINTS.get(project_type, {}).get("skills", []))
    return resolve_paths([f"{name}\\SKILL.md" for name in names], SKILLS_ROOT)


def recommend_memory(project_type: str | None, goal: str | None) -> list[Path]:
    names: list[str] = []
    if goal:
        names.extend(GOAL_HINTS.get(goal, {}).get("memory", []))
    if project_type:
        names.extend(PROJECT_TYPE_HINTS.get(project_type, {}).get("memory", []))
    return resolve_paths(names, MEMORY_ROOT)


def recommend_shared_docs(project_type: str | None) -> list[Path]:
    names: list[str] = []
    if project_type:
        names.extend(PROJECT_TYPE_HINTS.get(project_type, {}).get("docs", []))
    return resolve_paths(names, DOCS_ROOT)


def format_case(entry: dict[str, Any], score: int, overlaps: list[str]) -> list[str]:
    lines = [
        f"- Case: {entry.get('id', '<no-id>')}",
        f"  project: {entry.get('project', '')}",
        f"  score: {score}",
        f"  why_matched: {', '.join(overlaps) if overlaps else '(broad fallback match)'}",
        f"  summary: {entry.get('summary', '')}",
    ]
    derived_docs = entry.get("derived_docs", [])
    if derived_docs:
        lines.append("  suggested_docs:")
        for path in derived_docs[:3]:
            lines.append(f"    - {path}")
    promotions = entry.get("skill_promotions", []) + entry.get("memory_promotions", []) + entry.get("doc_promotions", [])
    if promotions:
        lines.append("  reusable_signals:")
        for item in promotions[:3]:
            lines.append(f"    - {item}")
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Suggest reusable cases, skills, memory, and docs for a new project question."
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help=f"Path to session index JSON. Default: {DEFAULT_INDEX}",
    )
    parser.add_argument(
        "--project-type",
        choices=sorted(PROJECT_TYPE_HINTS),
        help="Primary project type for the new analysis target.",
    )
    parser.add_argument(
        "--goal",
        choices=sorted(GOAL_HINTS),
        help="Current goal, such as analyze, design, roadmap, knowledge, or continuous-execution.",
    )
    parser.add_argument(
        "--text",
        help="Free-form problem statement used for keyword matching.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum number of case suggestions to show. Default: 3",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.index.exists():
        parser.error(f"Session index not found: {args.index}")
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    if not args.project_type and not args.goal and not args.text:
        parser.error("Provide at least one of --project-type, --goal, or --text")

    data = load_index(args.index)
    query_tokens = build_query_tokens(args.project_type, args.goal, args.text)

    scored: list[tuple[int, list[str], dict[str, Any]]] = []
    for entry in data["entries"]:
        score, overlaps = score_entry(entry, query_tokens)
        if score > 0:
            scored.append((score, overlaps, entry))

    scored.sort(key=lambda item: (-item[0], str(item[2].get("created_at", ""))), reverse=False)

    skills = recommend_skills(args.project_type, args.goal)
    memory_docs = recommend_memory(args.project_type, args.goal)
    shared_docs = recommend_shared_docs(args.project_type)

    print("# Case Advice")
    print()
    if args.project_type:
        print(f"- project_type: {args.project_type}")
        print(f"- project_type_focus: {PROJECT_TYPE_HINTS[args.project_type]['description']}")
    if args.goal:
        print(f"- goal: {args.goal}")
    if args.text:
        print(f"- problem: {args.text}")
    print(f"- query_tokens: {', '.join(sorted(query_tokens))}")
    print()

    print("## Recommended Skills")
    if skills:
        for path in skills:
            print(f"- {path}")
    else:
        print("- No skill recommendation for the current input.")
    print()

    print("## Recommended Memory")
    if memory_docs:
        for path in memory_docs:
            print(f"- {path}")
    else:
        print("- No memory recommendation for the current input.")
    print()

    print("## Recommended Shared Docs")
    if shared_docs:
        for path in shared_docs:
            print(f"- {path}")
    else:
        print("- No shared doc recommendation for the current input.")
    print()

    print("## Suggested Historical Cases")
    if scored:
        for score, overlaps, entry in scored[: args.limit]:
            for line in format_case(entry, score, overlaps):
                print(line)
    else:
        print("- No strong historical case match yet. Fall back to the recommended skills and memory docs above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
