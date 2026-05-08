#!/usr/bin/env python3
"""List session follow-up actions that still need attention."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = REPO_ROOT / ".claude" / "sessions" / "index.json"
DEFAULT_MARKDOWN = REPO_ROOT / "FOLLOWUP-ACTIONS.md"
DEFAULT_STATUSES = ("pending", "completed", "needs-confirmation")

STATUS_ZH = {
    "pending": "待处理",
    "completed": "已完成",
    "needs-confirmation": "待确认",
    "completed-session": "已完成",
}

TITLE_ZH = {
    "Initial Hermes Agent case study and workbench borrowing analysis": "Hermes Agent 初始案例研究与 workbench 借鉴分析",
}

ACTION_ZH = {
    "Continue connecting session workflow to skill and memory feedback checks": "继续把 session 工作流与 skill、memory 的反馈检查连接得更紧密。",
}

NOTES_ZH = {
    "The workflow now records promotions, but future sessions still need stronger default checks and automation.": "当前工作流已经记录 promotion，但后续 session 仍需要更强的默认检查与自动化。",
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


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(normalize_text(item) for item in value.values())
    return str(value).casefold()


def normalize_followup_item(item: Any) -> dict[str, str]:
    if isinstance(item, str):
        return {
            "action": item,
            "status": "pending",
            "owner": "",
            "notes": "",
        }
    if isinstance(item, dict):
        return {
            "action": str(item.get("action", "")).strip(),
            "status": str(item.get("status", "pending")).strip() or "pending",
            "owner": str(item.get("owner", "")).strip(),
            "notes": str(item.get("notes", "")).strip(),
        }
    return {
        "action": str(item),
        "status": "pending",
        "owner": "",
        "notes": "",
    }


def translate_title(text: str) -> str:
    return TITLE_ZH.get(text, text)


def translate_action(text: str) -> str:
    return ACTION_ZH.get(text, text)


def translate_notes(text: str) -> str:
    return NOTES_ZH.get(text, text)


def translate_status(text: str) -> str:
    return STATUS_ZH.get(text, text)


def get_followup_items(entry: dict[str, Any]) -> list[dict[str, str]]:
    items = [normalize_followup_item(item) for item in entry.get("followup_actions", [])]
    return [item for item in items if item.get("action")]


def has_matching_followup_status(
    entry: dict[str, Any],
    status_filter: str | None,
) -> bool:
    items = get_followup_items(entry)
    if not items:
        return False
    if not status_filter:
        return True
    return any(item.get("status") == status_filter for item in items)


def matches(
    entry: dict[str, Any],
    project: str | None,
    text: str | None,
    status_filter: str | None,
) -> bool:
    if not has_matching_followup_status(entry, status_filter):
        return False
    if project and normalize_text(entry.get("project")) != project.casefold():
        return False
    if text:
        haystack = " ".join(
            [
                normalize_text(entry.get("id")),
                normalize_text(entry.get("project")),
                normalize_text(entry.get("title")),
                normalize_text(entry.get("summary")),
                normalize_text(entry.get("followup_actions", [])),
                normalize_text(entry.get("skill_promotions", [])),
                normalize_text(entry.get("memory_promotions", [])),
                normalize_text(entry.get("doc_promotions", [])),
            ]
        )
        if text.casefold() not in haystack:
            return False
    return True


def sort_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        entries,
        key=lambda item: normalize_text(item.get("created_at")),
        reverse=True,
    )


def format_entry(entry: dict[str, Any], verbose: bool) -> str:
    lines = [
        f"- {entry.get('id', '<no-id>')}",
        f"  project: {entry.get('project', '')}",
        f"  title: {entry.get('title', '')}",
        f"  status: {entry.get('status', '')}",
    ]
    phase_report = entry.get("phase_report")
    if phase_report:
        lines.append(f"  phase_report: {phase_report}")
    entry_path = entry.get("entry_path")
    if entry_path:
        lines.append(f"  entry_path: {entry_path}")
    lines.append("  followup_actions:")
    for item in get_followup_items(entry):
        suffix = f" [{item['status']}]"
        owner = f" owner={item['owner']}" if item.get("owner") else ""
        lines.append(f"    - {item['action']}{suffix}{owner}")
        if verbose and item.get("notes"):
            lines.append(f"      notes: {item['notes']}")
    if verbose:
        for label in ("skill_promotions", "memory_promotions", "doc_promotions"):
            values = entry.get(label, [])
            if values:
                lines.append(f"  {label}:")
                for item in values:
                    lines.append(f"    - {item}")
    return "\n".join(lines)


def render_markdown(entries: list[dict[str, Any]], source_index: Path) -> str:
    status_counts = {status: 0 for status in DEFAULT_STATUSES}
    for entry in entries:
        for item in get_followup_items(entry):
            status = item.get("status", "pending")
            status_counts[status] = status_counts.get(status, 0) + 1
    lines = [
        "# Follow-up Actions Overview",
        "",
        "## Summary",
        "",
        f"- Source index: `{source_index}`",
        f"- Total entries with follow-up actions: `{len(entries)}`",
        f"- Pending items: `{status_counts.get('pending', 0)}`",
        f"- Completed items: `{status_counts.get('completed', 0)}`",
        f"- Needs-confirmation items: `{status_counts.get('needs-confirmation', 0)}`",
        "- Purpose: show currently recorded follow-up actions in one root-level Markdown view",
        "",
    ]
    if not entries:
        lines.extend(
            [
                "## Current State",
                "",
                "No follow-up actions are currently recorded in the session index.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "## Current Items",
            "",
        ]
    )
    for entry in entries:
        lines.extend(
            [
                f"### {entry.get('id', '<no-id>')}",
                "",
                f"- Project: `{entry.get('project', '')}`",
                f"- Title: {entry.get('title', '')}",
                f"- Status: `{entry.get('status', '')}`",
            ]
        )
        phase_report = entry.get("phase_report")
        if phase_report:
            lines.append(f"- Phase report: `{phase_report}`")
        entry_path = entry.get("entry_path")
        if entry_path:
            lines.append(f"- Entry path: `{entry_path}`")
        lines.append("- Follow-up actions:")
        for item in get_followup_items(entry):
            lines.append(f"  - [{item['status']}] {item['action']}")
            if item.get("owner"):
                lines.append(f"    - owner: {item['owner']}")
            if item.get("notes"):
                lines.append(f"    - notes: {item['notes']}")
        for label, title in (
            ("skill_promotions", "Skill promotions"),
            ("memory_promotions", "Memory promotions"),
            ("doc_promotions", "Doc promotions"),
        ):
            values = entry.get(label, [])
            if values:
                lines.append(f"- {title}:")
                for item in values:
                    lines.append(f"  - {item}")
        lines.append("")
    return "\n".join(lines)


def render_markdown_zh(entries: list[dict[str, Any]], source_index: Path) -> str:
    status_counts = {status: 0 for status in DEFAULT_STATUSES}
    grouped: dict[str, list[tuple[dict[str, Any], dict[str, str]]]] = {
        status: [] for status in DEFAULT_STATUSES
    }
    for entry in entries:
        for item in get_followup_items(entry):
            status = item.get("status", "pending")
            status_counts[status] = status_counts.get(status, 0) + 1
            grouped.setdefault(status, []).append((entry, item))

    lines = [
        "# 后续动作总览",
        "",
        "## 说明",
        "",
        f"- 来源索引：`{source_index}`",
        f"- 含后续动作的记录数：`{len(entries)}`",
        f"- 待处理：`{status_counts.get('pending', 0)}`",
        f"- 已完成：`{status_counts.get('completed', 0)}`",
        f"- 待确认：`{status_counts.get('needs-confirmation', 0)}`",
        "- 用途：在仓库根目录集中展示当前 session 中记录的后续动作",
        "",
    ]
    if not entries:
        lines.extend(
            [
                "## 当前状态",
                "",
                "当前没有记录任何后续动作。",
                "",
            ]
        )
        return "\n".join(lines)

    for status in DEFAULT_STATUSES:
        title = translate_status(status)
        lines.extend([f"## {title}", ""])
        items = grouped.get(status, [])
        if not items:
            lines.extend(["当前无此状态的后续动作。", ""])
            continue
        for entry, item in items:
            lines.extend(
                [
                    f"### {entry.get('id', '<no-id>')}",
                    "",
                    f"- 项目：`{entry.get('project', '')}`",
                    f"- 标题：{translate_title(str(entry.get('title', '')))}",
                    f"- Session 状态：`{translate_status(str(entry.get('status', '')) or 'completed-session')}`",
                    f"- 后续动作：{translate_action(item.get('action', ''))}",
                ]
            )
            if item.get("owner"):
                lines.append(f"- 负责人：`{item['owner']}`")
            if item.get("notes"):
                lines.append(f"- 备注：{translate_notes(item['notes'])}")
            phase_report = entry.get("phase_report")
            if phase_report:
                lines.append(f"- 阶段报告：`{phase_report}`")
            entry_path = entry.get("entry_path")
            if entry_path:
                lines.append(f"- 条目路径：`{entry_path}`")
            lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List session follow-up actions from .claude/sessions/index.json."
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help=f"Path to session index JSON. Default: {DEFAULT_INDEX}",
    )
    parser.add_argument("--project", help="Exact project name match.")
    parser.add_argument(
        "--text",
        help="Case-insensitive substring search across follow-up fields.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of matching entries to show. Default: 20",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show promotion fields alongside follow-up actions.",
    )
    parser.add_argument(
        "--status",
        choices=DEFAULT_STATUSES,
        help="Filter follow-up items by status.",
    )
    parser.add_argument(
        "--markdown-out",
        type=Path,
        help="Write a Markdown overview file for the matched follow-up items.",
    )
    parser.add_argument(
        "--write-root-md",
        action="store_true",
        help=f"Write the root Markdown overview to {DEFAULT_MARKDOWN}.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.index.exists():
        parser.error(f"Session index not found: {args.index}")
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    data = load_index(args.index)
    matched = [
        entry
        for entry in data["entries"]
        if matches(
            entry,
            project=args.project,
            text=args.text,
            status_filter=args.status,
        )
    ]
    matched = sort_entries(matched)

    print(f"matches: {len(matched)}")
    for entry in matched[: args.limit]:
        print(format_entry(entry, args.verbose))

    markdown_target: Path | None = None
    markdown_renderer = render_markdown
    if args.write_root_md:
        markdown_target = DEFAULT_MARKDOWN
        markdown_renderer = render_markdown_zh
    elif args.markdown_out:
        markdown_target = args.markdown_out

    if markdown_target is not None:
        markdown_entries = matched[: args.limit]
        markdown = markdown_renderer(markdown_entries, args.index)
        markdown_target.parent.mkdir(parents=True, exist_ok=True)
        markdown_target.write_text(markdown + "\n", encoding="utf-8", newline="\n")
        print(f"markdown: {markdown_target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
