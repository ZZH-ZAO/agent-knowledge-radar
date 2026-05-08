#!/usr/bin/env python3
"""
Repo ingestion wrapper for the knowledge platform.

Uses gitingest to normalize a GitHub repo or local directory into:
- summary
- directory tree
- concatenated file content

The result is cached to tmp/ingest-cache as JSON so later distillation
steps can reuse the same normalized input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "tmp" / "ingest-cache"
TEXT_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".css",
    ".scss",
    ".html",
    ".xml",
    ".sh",
    ".ps1",
    ".java",
    ".go",
    ".rs",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".sql",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^https?://", "", value)
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "ingest"


def normalize_source(source: str) -> str:
    source = source.strip()
    if not source:
        raise SystemExit("source is required")
    return source


def build_cache_path(source: str, focus: str, include_patterns: list[str], exclude_patterns: list[str]) -> Path:
    fingerprint = hashlib.sha1(
        json.dumps(
            {
                "source": source,
                "focus": focus,
                "include": include_patterns,
                "exclude": exclude_patterns,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:12]
    name = f"{slugify(source)}-{fingerprint}.json"
    return CACHE_DIR / name


def run_ingest(
    source: str,
    *,
    focus: str = "",
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    branch: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    try:
        from gitingest import ingest
    except ImportError as exc:
        raise SystemExit(
            "gitingest is not installed. Run `python -m pip install gitingest` first."
        ) from exc

    actual_source = source
    if focus:
        if source.startswith("http://") or source.startswith("https://"):
            actual_source = source.rstrip("/") + "/" + focus.strip("/").replace("\\", "/")
        else:
            actual_source = str((Path(source) / focus).resolve())

    include_arg: str | set[str] | None = set(include_patterns or []) or None
    exclude_arg: str | set[str] | None = set(exclude_patterns or []) or None
    auth_token = token or os.environ.get("GITHUB_TOKEN")

    summary, tree, content = ingest(
        actual_source,
        include_patterns=include_arg,
        exclude_patterns=exclude_arg,
        branch=branch,
        token=auth_token,
    )

    local_path = Path(actual_source)
    if local_path.exists() and "Error reading file with 'cp936'" in content:
        tree = build_local_tree(local_path)
        content = build_local_content(local_path)
        summary = build_local_summary(local_path, content)

    return {
        "source": source,
        "ingest_source": actual_source,
        "focus": focus,
        "include_patterns": include_patterns or [],
        "exclude_patterns": exclude_patterns or [],
        "branch": branch,
        "summary": summary,
        "tree": tree,
        "content": content,
        "summary_length": len(summary),
        "tree_length": len(tree),
        "content_length": len(content),
        "ingested_at": datetime.now().isoformat(timespec="seconds"),
    }


def iter_local_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "dist", "build", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.stat().st_size > 1024 * 1024:
            continue
        files.append(path)
    files.sort()
    return files


def build_local_tree(root: Path) -> str:
    lines = ["Directory structure:", f"{root.name}/"]
    for path in iter_local_files(root):
        rel = path.relative_to(root)
        indent = "    " * (len(rel.parts) - 1)
        lines.append(f"{indent}{rel.as_posix()}")
    return "\n".join(lines)


def read_text_fallback(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "utf-16"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def build_local_content(root: Path) -> str:
    chunks: list[str] = []
    for path in iter_local_files(root):
        rel = path.relative_to(root).as_posix()
        chunks.append("================================================")
        chunks.append(f"FILE: {rel}")
        chunks.append("================================================")
        chunks.append(read_text_fallback(path))
        chunks.append("")
    return "\n".join(chunks)


def build_local_summary(root: Path, content: str) -> str:
    file_count = len(iter_local_files(root))
    token_estimate = max(1, len(content) // 4)
    return (
        f"Directory: {root}\n"
        f"Files analyzed: {file_count}\n\n"
        f"Estimated tokens: {round(token_estimate / 1000, 1)}k\n"
        "Note: local UTF-8 fallback reader was used to avoid Windows cp936 decode issues."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize a repo with gitingest.")
    parser.add_argument("source", help="GitHub URL / owner-repo URL / local directory")
    parser.add_argument("--focus", default="", help="Optional subdirectory focus")
    parser.add_argument("--include", action="append", default=[], help="Include glob pattern")
    parser.add_argument("--exclude", action="append", default=[], help="Exclude glob pattern")
    parser.add_argument("--branch", default=None, help="Optional branch for remote repo")
    parser.add_argument("--output", default="", help="Optional JSON output path")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    source = normalize_source(args.source)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    result = run_ingest(
        source,
        focus=args.focus,
        include_patterns=args.include,
        exclude_patterns=args.exclude,
        branch=args.branch,
    )

    output_path = Path(args.output).resolve() if args.output else build_cache_path(source, args.focus, args.include, args.exclude)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.stdout:
      print(json.dumps({**result, "output_file": str(output_path)}, ensure_ascii=False, indent=2))
    else:
      print(f"Wrote {output_path}")
      print(f"Summary length: {result['summary_length']}")
      print(f"Tree length: {result['tree_length']}")
      print(f"Content length: {result['content_length']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
