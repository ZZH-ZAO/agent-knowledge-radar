"""Pure utility functions extracted from knowledge_platform_bridge.py.

This module has no external dependencies (stdlib only) so tests can import
it without needing FastAPI/pydantic/uvicorn installed.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_slug() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"^https?://", "", lowered)
    lowered = lowered.replace("\\", "-").replace("/", "-")
    lowered = re.sub(r"[^a-z0-9一-鿿._-]+", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-._")
    return lowered or f"draft-{now_slug()}"


def repo_slug(repo: str) -> str:
    return repo.lower().replace("/", "-").replace("_", "-")


def parse_github_repo(source: str) -> str:
    value = source.strip()
    patterns = [
        r"github\.com[:/](?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+)",
        r"^(?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, value, re.IGNORECASE)
        if match:
            repo = match.group("repo").removesuffix(".git")
            return f"{match.group('owner')}/{repo}"
    raise ValueError(f"无法解析 GitHub 仓库：{source}")


def repo_to_url(repo: str) -> str:
    return f"https://github.com/{repo}"


def normalize_ingest_source(source: str, source_type: str) -> str:
    if source_type == "github":
        repo = parse_github_repo(source)
        return repo_to_url(repo)
    return source.strip()


def extract_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "_root"
    sections[current] = []
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def pick_section(sections: dict[str, str], keywords: list[str]) -> str:
    for key, value in sections.items():
        lowered = key.lower()
        if any(keyword.lower() in lowered for keyword in keywords):
            return value
    return ""


def first_meaningful_line(text: str) -> str:
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            continue
        if line.startswith("- [ ]"):
            return line[5:].strip()
        if line.startswith("- "):
            return line[2:].strip()
        return line
    return ""


def list_from_section(text: str) -> list[str]:
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- [ ]"):
            items.append(line[5:].strip())
        elif line.startswith("- "):
            items.append(line[2:].strip())
    return items


def clean_section_text(text: str) -> str:
    return text.strip()


def parse_analysis(markdown: str) -> dict[str, Any]:
    sections = extract_sections(markdown)
    title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""
    one_line = pick_section(sections, ["项目一句话"])
    why = pick_section(sections, ["为什么值得", "为什么值得学"])
    scenarios = pick_section(sections, ["核心场景"])
    problems = pick_section(sections, ["通用问题", "它解决的通用问题"])
    frameworks = pick_section(sections, ["优秀技术", "技术和框架"])
    principles = pick_section(sections, ["设计原则", "可迁移设计原则"])
    actions = pick_section(sections, ["行动项", "对我当前项目"])
    return {
        "title": title,
        "oneLine": first_meaningful_line(one_line),
        "whyWorthStudying": first_meaningful_line(why),
        "coreScenario": first_meaningful_line(scenarios),
        "generalProblems": first_meaningful_line(problems),
        "technicalFrameworks": first_meaningful_line(frameworks),
        "designPrinciples": first_meaningful_line(principles),
        "oneLineDetail": clean_section_text(one_line),
        "whyWorthStudyingDetail": clean_section_text(why),
        "coreScenarioDetail": clean_section_text(scenarios),
        "generalProblemsDetail": clean_section_text(problems),
        "technicalFrameworksDetail": clean_section_text(frameworks),
        "designPrinciplesDetail": clean_section_text(principles),
        "actions": list_from_section(actions),
        "sections": sections,
    }


def normalize_lines(items: list[str]) -> list[str]:
    cleaned: list[str] = []
    for item in items:
        line = str(item).strip()
        if not line:
            continue
        if line not in cleaned:
            cleaned.append(line)
    return cleaned


def merge_unique_texts(*groups: list[str], limit: int | None = None) -> list[str]:
    merged: list[str] = []
    for group in groups:
        for item in group:
            line = str(item).strip()
            if not line or line in merged:
                continue
            merged.append(line)
            if limit is not None and len(merged) >= limit:
                return merged
    return merged


def snippet(text: str, limit: int = 220) -> str:
    compact = re.sub(r"\s+", " ", text or "").strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "?"


def relative_to_root(path_value: str, root: Path) -> str:
    if not path_value:
        return ""
    path = Path(path_value)
    if not path.is_absolute():
        return path_value.replace("\\", "/")
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
