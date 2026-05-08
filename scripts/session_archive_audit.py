#!/usr/bin/env python3
"""Audit archived session records for missing guardrails and weak metadata."""

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


def normalize_followup_items(entry: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for item in entry.get("followup_actions", []):
        if isinstance(item, str):
            items.append({"action": item, "status": "pending", "legacy": True})
            continue
        if isinstance(item, dict):
            normalized = dict(item)
            normalized["legacy"] = False
            items.append(normalized)
    return items


def audit_entry(entry: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    review = entry.get("promotion_review")
    if not isinstance(review, dict):
        issues.append("missing promotion_review")
    else:
        for key in ("skills_checked", "memory_checked", "docs_checked"):
            if review.get(key) is not True:
                issues.append(f"promotion_review.{key} is not true")
        decision = str(review.get("decision", "")).strip()
        if not decision:
            issues.append("promotion_review.decision is empty")

    if not str(entry.get("phase_report", "")).strip():
        issues.append("missing phase_report")

    derived_docs = entry.get("derived_docs", [])
    if not isinstance(derived_docs, list) or not derived_docs:
        issues.append("missing derived_docs")

    followup_items = normalize_followup_items(entry)
    if any(item.get("legacy") for item in followup_items):
        issues.append("contains legacy string followup_actions")

    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit .claude/sessions/index.json for session archive quality checks."
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help=f"Path to session index JSON. Default: {DEFAULT_INDEX}",
    )
    parser.add_argument(
        "--only-issues",
        action="store_true",
        help="Show only entries that have one or more audit issues.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.index.exists():
        parser.error(f"Session index not found: {args.index}")

    data = load_index(args.index)
    entries = data["entries"]

    issue_count = 0
    checked_count = 0
    for entry in entries:
        issues = audit_entry(entry)
        if args.only_issues and not issues:
            continue
        checked_count += 1
        print(f"- {entry.get('id', '<no-id>')}")
        print(f"  project: {entry.get('project', '')}")
        if issues:
            issue_count += len(issues)
            print("  audit: issues")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  audit: clean")

    print(f"entries_checked: {checked_count if args.only_issues else len(entries)}")
    print(f"issues_found: {issue_count}")
    return 0 if issue_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
