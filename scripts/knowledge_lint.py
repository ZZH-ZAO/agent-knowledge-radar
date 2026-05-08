#!/usr/bin/env python3
"""
Knowledge health checks for the local Agent knowledge platform.

This is a guardrail against the knowledge base becoming a link dump:
- projects should connect to patterns or actions
- pain points should have evidence and mature practices
- sources should connect to pain points or patterns
- docs should contain action items or industry-pain-point structure
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = ROOT / "data" / "knowledge-index.json"
REPORT = ROOT / "data" / "knowledge-lint-report.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_issue(issues: list[dict[str, str]], severity: str, kind: str, target: str, message: str) -> None:
    issues.append({"severity": severity, "kind": kind, "target": target, "message": message})


def lint_projects(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    for project in data.get("projects", []):
        target = project.get("sourceFile") or project.get("id", "")
        if not project.get("relatedPatterns"):
            add_issue(issues, "warning", "project", target, "项目没有关联方案，后续阅读时难以抽象成通用框架。")
        if not project.get("nextActions"):
            add_issue(issues, "warning", "project", target, "项目没有行动项，容易停留在读书笔记。")
        if not project.get("summary"):
            add_issue(issues, "warning", "project", target, "项目缺少摘要。")


def lint_solutions(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    projects_text = " ".join(
        " ".join(project.get("relatedPatterns", [])) + " " + project.get("content", "")
        for project in data.get("projects", [])
    ).lower()
    for solution in data.get("solutions", []):
        target = solution.get("sourceFile") or solution.get("id", "")
        if not solution.get("problemDefinition"):
            add_issue(issues, "warning", "solution", target, "方案缺少问题定义。")
        if not solution.get("actions"):
            add_issue(issues, "warning", "solution", target, "方案缺少当前项目行动项。")
        if solution.get("id", "").lower() not in projects_text and solution.get("title", "").lower() not in projects_text:
            add_issue(issues, "info", "solution", target, "暂未发现项目明确引用该方案，可后续补关联。")


def lint_pain_points(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    project_ids = {project.get("id") for project in data.get("projects", [])}
    for pain_point in data.get("painPoints", []):
        target = pain_point.get("id", "")
        if not pain_point.get("industryPain"):
            add_issue(issues, "error", "painPoint", target, "痛点缺少行业痛点定义。")
        if not pain_point.get("evidenceSources"):
            add_issue(issues, "warning", "painPoint", target, "痛点缺少来源类型。")
        if not pain_point.get("maturePractices"):
            add_issue(issues, "warning", "painPoint", target, "痛点缺少优秀项目共性做法。")
        missing = [pid for pid in pain_point.get("evidenceProjects", []) if pid not in project_ids]
        if missing:
            add_issue(issues, "warning", "painPoint", target, f"痛点引用了不存在的项目：{', '.join(missing)}")


def lint_sources(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    for source in data.get("sources", []):
        target = source.get("sourceFile") or source.get("id", "")
        if source.get("evidenceStrength") not in {"high", "medium", "low"}:
            add_issue(issues, "warning", "source", target, "资料源缺少证据强度。")
        if not source.get("relatedPainPoints") and not source.get("relatedPatterns"):
            add_issue(issues, "warning", "source", target, "资料源没有关联痛点或方案，可能还没有进入自动进化链路。")
        if not source.get("actions"):
            add_issue(issues, "info", "source", target, "资料源没有当前项目行动项。")


def lint_docs(issues: list[dict[str, str]]) -> None:
    for path in sorted(DOCS.rglob("*.md")):
        if path.name.lower() == "readme.md" or path.name.startswith("DIRECTORY"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        target = path.relative_to(ROOT).as_posix()
        if not re.search(r"^##\s+(\d+\.\s+)?行业痛点研究版补充\s*$", text, flags=re.MULTILINE):
            add_issue(issues, "warning", "doc", target, "文档缺少行业痛点研究版补充。")
        if "- [ ]" not in text and "当前项目行动项" not in text:
            add_issue(issues, "info", "doc", target, "文档没有显式行动项。")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when errors are found.")
    args = parser.parse_args()

    if not INDEX.exists():
        raise SystemExit("Missing data/knowledge-index.json. Run scripts/build_knowledge_index.py first.")

    data = read_json(INDEX)
    issues: list[dict[str, str]] = []
    lint_projects(data, issues)
    lint_solutions(data, issues)
    lint_pain_points(data, issues)
    lint_sources(data, issues)
    lint_docs(issues)

    summary = {
        "total": len(issues),
        "errors": sum(1 for issue in issues if issue["severity"] == "error"),
        "warnings": sum(1 for issue in issues if issue["severity"] == "warning"),
        "info": sum(1 for issue in issues if issue["severity"] == "info"),
    }
    report = {"summary": summary, "issues": issues}
    write_json(REPORT, report)

    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"Errors={summary['errors']} Warnings={summary['warnings']} Info={summary['info']}")
    for issue in issues[:20]:
        print(f"[{issue['severity']}] {issue['kind']} {issue['target']} - {issue['message']}")

    if args.strict and summary["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
