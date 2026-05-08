#!/usr/bin/env python3
"""Search lightweight workbench session records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = REPO_ROOT / ".claude" / "sessions" / "index.json"


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
    return str(value).casefold()


def entry_matches(
    entry: dict[str, Any],
    *,
    project: str | None,
    keyword: str | None,
    status: str | None,
    task_type: str | None,
    text: str | None,
) -> bool:
    if project and normalize_text(entry.get("project")) != project.casefold():
        return False
    if status and normalize_text(entry.get("status")) != status.casefold():
        return False
    if task_type and normalize_text(entry.get("task_type")) != task_type.casefold():
        return False
    if keyword:
        keywords = entry.get("keywords", [])
        if keyword.casefold() not in {normalize_text(item) for item in keywords}:
            return False
    if text:
        haystack = " ".join(
            [
                normalize_text(entry.get("id")),
                normalize_text(entry.get("project")),
                normalize_text(entry.get("task_type")),
                normalize_text(entry.get("title")),
                normalize_text(entry.get("summary")),
                normalize_text(entry.get("keywords", [])),
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
        f"  task_type: {entry.get('task_type', '')}",
        f"  status: {entry.get('status', '')}",
        f"  created_at: {entry.get('created_at', '')}",
        f"  title: {entry.get('title', '')}",
        f"  summary: {entry.get('summary', '')}",
    ]
    keywords = entry.get("keywords", [])
    if keywords:
        lines.append(f"  keywords: {', '.join(str(item) for item in keywords)}")
    if verbose:
        entry_path = entry.get("entry_path")
        if entry_path:
            lines.append(f"  entry_path: {entry_path}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search .claude/sessions/index.json for historical work records."
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help=f"Path to session index JSON. Default: {DEFAULT_INDEX}",
    )
    parser.add_argument("--project", help="Exact project name match.")
    parser.add_argument("--keyword", help="Exact keyword/tag match.")
    parser.add_argument("--status", help="Exact status match.")
    parser.add_argument("--task-type", help="Exact task_type match.")
    parser.add_argument(
        "--text",
        help="Case-insensitive substring search across id/project/title/summary/keywords.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to show. Default: 10",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show additional fields such as entry_path.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.index.exists():
        parser.error(f"Session index not found: {args.index}")

    data = load_index(args.index)
    entries = data["entries"]
    matched = [
        entry
        for entry in entries
        if entry_matches(
            entry,
            project=args.project,
            keyword=args.keyword,
            status=args.status,
            task_type=args.task_type,
            text=args.text,
        )
    ]
    matched = sort_entries(matched)

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    shown = matched[: args.limit]
    print(f"matches: {len(matched)}")
    for entry in shown:
        print(format_entry(entry, args.verbose))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
