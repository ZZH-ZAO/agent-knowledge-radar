#!/usr/bin/env python3
"""Register or update a workbench session entry in .claude/sessions/index.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = REPO_ROOT / ".claude" / "sessions"
DEFAULT_INDEX = SESSIONS_DIR / "index.json"

REQUIRED_FIELDS = (
    "id",
    "created_at",
    "project",
    "task_type",
    "title",
    "summary",
    "status",
)

OPTIONAL_LIST_FIELDS = (
    "keywords",
    "related_cases",
    "source_paths",
    "derived_docs",
    "skill_promotions",
    "memory_promotions",
    "doc_promotions",
    "followup_actions",
)

ALLOWED_FOLLOWUP_STATUSES = {
    "pending",
    "completed",
    "needs-confirmation",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def has_non_empty_promotions(entry: dict[str, Any]) -> bool:
    return any(entry.get(field) for field in ("skill_promotions", "memory_promotions", "doc_promotions"))


def validate_promotion_review(entry: dict[str, Any], entry_path: Path) -> None:
    review = entry.get("promotion_review")
    if review is None:
        if has_non_empty_promotions(entry):
            return
        raise ValueError(
            f"Session entry {entry_path} must include 'promotion_review' when no promotion lists are populated"
        )
    if not isinstance(review, dict):
        raise ValueError(f"Field 'promotion_review' in {entry_path} must be an object")

    required_checks = ("skills_checked", "memory_checked", "docs_checked")
    for key in required_checks:
        if key not in review or not isinstance(review[key], bool):
            raise ValueError(
                f"Field 'promotion_review.{key}' in {entry_path} must be a boolean"
            )

    decision = review.get("decision")
    if not isinstance(decision, str) or not decision.strip():
        raise ValueError(
            f"Field 'promotion_review.decision' in {entry_path} must be a non-empty string"
        )

    if not all(review[key] for key in required_checks):
        raise ValueError(
            f"Field 'promotion_review' in {entry_path} must mark skills_checked, memory_checked, and docs_checked as true"
        )


def validate_entry(entry: dict[str, Any], entry_path: Path) -> None:
    missing = [field for field in REQUIRED_FIELDS if not entry.get(field)]
    if missing:
        raise ValueError(
            f"Session entry {entry_path} is missing required field(s): {', '.join(missing)}"
        )
    for key in OPTIONAL_LIST_FIELDS:
        if key in entry and not isinstance(entry[key], list):
            raise ValueError(f"Field '{key}' in {entry_path} must be a list")
    followup_actions = entry.get("followup_actions", [])
    for item in followup_actions:
        if isinstance(item, str):
            continue
        if not isinstance(item, dict):
            raise ValueError(
                f"Each follow-up item in {entry_path} must be a string or object"
            )
        action = item.get("action")
        if not isinstance(action, str) or not action.strip():
            raise ValueError(
                f"Each follow-up object in {entry_path} must contain a non-empty 'action' string"
            )
        status = item.get("status", "pending")
        if status not in ALLOWED_FOLLOWUP_STATUSES:
            raise ValueError(
                f"Invalid follow-up status in {entry_path}: {status}. "
                f"Allowed: {', '.join(sorted(ALLOWED_FOLLOWUP_STATUSES))}"
            )
    if "phase_report" in entry and not isinstance(entry["phase_report"], str):
        raise ValueError(f"Field 'phase_report' in {entry_path} must be a string")
    validate_promotion_review(entry, entry_path)


def make_index_entry(entry: dict[str, Any], entry_path: Path) -> dict[str, Any]:
    index_entry: dict[str, Any] = {
        "id": entry["id"],
        "created_at": entry["created_at"],
        "project": entry["project"],
        "task_type": entry["task_type"],
        "title": entry["title"],
        "summary": entry["summary"],
        "entry_path": str(entry_path),
        "status": entry["status"],
    }
    for key in OPTIONAL_LIST_FIELDS:
        values = entry.get(key, [])
        if values:
            index_entry[key] = values
    phase_report = entry.get("phase_report")
    if phase_report:
        index_entry["phase_report"] = phase_report
    promotion_review = entry.get("promotion_review")
    if promotion_review:
        index_entry["promotion_review"] = promotion_review
    return index_entry


def upsert_index(index_data: dict[str, Any], new_entry: dict[str, Any]) -> tuple[dict[str, Any], str]:
    entries = index_data.setdefault("entries", [])
    if not isinstance(entries, list):
        raise ValueError("Session index 'entries' must be a list")

    for i, existing in enumerate(entries):
        if isinstance(existing, dict) and existing.get("id") == new_entry["id"]:
            entries[i] = new_entry
            return index_data, "updated"

    entries.append(new_entry)
    entries.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
    return index_data, "added"


def resolve_entry_path(path_arg: str) -> Path:
    path = Path(path_arg)
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Register a .claude/sessions/entries/*.json file into the session index."
    )
    parser.add_argument(
        "entry",
        help="Path to a session entry JSON file.",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help=f"Path to session index JSON. Default: {DEFAULT_INDEX}",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    entry_path = resolve_entry_path(args.entry)
    if not entry_path.exists():
        parser.error(f"Session entry not found: {entry_path}")

    entry = load_json(entry_path)
    validate_entry(entry, entry_path)

    if args.index.exists():
        index_data = load_json(args.index)
    else:
        index_data = {
            "schema_version": 1,
            "description": "Lightweight index for workbench historical session records.",
            "entries": [],
        }

    new_index_entry = make_index_entry(entry, entry_path)
    index_data, action = upsert_index(index_data, new_index_entry)
    save_json(args.index, index_data)
    print(f"{action}: {entry['id']}")
    print(f"index: {args.index}")
    if entry.get("promotion_review"):
        print("promotion_review: recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
