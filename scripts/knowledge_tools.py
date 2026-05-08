"""Knowledge retrieval functions for Agent Knowledge Radar.

Pure stdlib module that loads data/knowledge-index.json and provides
search, filter, and detail retrieval functions used by both the MCP
server and other consumers.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "knowledge-index.json"

_cache: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _cache
    if _cache is None:
        _cache = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return _cache


def reload() -> dict[str, Any]:
    global _cache
    _cache = None
    return _load()


def _score_match(text: str, query: str) -> int:
    text_l = text.lower()
    query_l = query.lower()
    score = 0
    if query_l in text_l:
        score += 3
    for word in query_l.split():
        if word in text_l:
            score += 1
    return score


def _compact_project(p: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": p.get("id", ""),
        "name": p.get("name", ""),
        "summary": (p.get("oneLineVerdict") or p.get("summary") or "")[:200],
        "primaryCategory": p.get("primaryCategory", ""),
        "status": p.get("status", ""),
        "score": p.get("score"),
        "types": p.get("types", []),
        "relatedPatterns": p.get("relatedPatterns", []),
        "sourceFile": p.get("sourceFile", ""),
    }


def _compact_solution(s: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": s.get("id", ""),
        "title": s.get("title", ""),
        "problemDefinition": (s.get("problemDefinition") or "")[:200],
        "actions": s.get("actions", []),
        "sourceFile": s.get("sourceFile", ""),
    }


def _compact_pain_point(pp: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": pp.get("id", ""),
        "title": pp.get("title", ""),
        "topic": pp.get("topic", ""),
        "severity": pp.get("severity", ""),
        "industryPain": (pp.get("industryPain") or pp.get("solutionMethod") or "")[:200],
        "evidenceProjects": pp.get("evidenceProjects", []),
        "relatedSolution": pp.get("relatedSolution", ""),
        "actions": pp.get("actions", []),
    }


def _compact_source(src: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": src.get("id", ""),
        "title": src.get("title", ""),
        "sourceType": src.get("sourceType", ""),
        "evidenceStrength": src.get("evidenceStrength", ""),
        "summary": (src.get("summary") or "")[:200],
        "relatedPainPoints": src.get("relatedPainPoints", []),
        "relatedPatterns": src.get("relatedPatterns", []),
    }


def _compact_interview(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id", ""),
        "rawQuestion": item.get("rawQuestion", ""),
        "questionType": item.get("questionType", ""),
        "knowledgePoints": item.get("knowledgePoints", []),
        "relatedProjects": item.get("relatedProjects", []),
        "relatedPatterns": item.get("relatedPatterns", []),
        "recommendedAnswer": (item.get("recommendedAnswer") or "")[:300],
        "followUps": item.get("followUps", []),
    }


# --- Public API ---


def search_knowledge(query: str, kinds: list[str] | None = None, limit: int = 10) -> list[dict[str, Any]]:
    """Search across all entity types. Returns ranked results."""
    if not query.strip():
        return []
    data = _load()
    results: list[tuple[int, str, dict[str, Any]]] = []
    kind_set = set(kinds) if kinds else None

    def add(kind: str, text: str, compact: dict[str, Any]) -> None:
        if kind_set and kind not in kind_set:
            return
        score = _score_match(text, query)
        if score > 0:
            results.append((score, kind, compact))

    for p in data.get("projects", []):
        text = f"{p.get('name','')} {p.get('summary','')} {' '.join(p.get('types',[]))} {p.get('primaryCategory','')}"
        add("project", text, _compact_project(p))

    for s in data.get("solutions", []):
        text = f"{s.get('title','')} {s.get('problemDefinition','')} {' '.join(s.get('whyImportant',[]))}"
        add("solution", text, _compact_solution(s))

    for pp in data.get("painPoints", []):
        text = f"{pp.get('title','')} {pp.get('topic','')} {pp.get('industryPain','')} {pp.get('solutionMethod','')}"
        add("painPoint", text, _compact_pain_point(pp))

    for src in data.get("sources", []):
        text = f"{src.get('title','')} {src.get('summary','')} {src.get('sourceType','')}"
        add("source", text, _compact_source(src))

    for item in data.get("interviews", {}).get("items", []):
        text = f"{item.get('rawQuestion','')} {' '.join(item.get('knowledgePoints',[]))}"
        add("interview", text, _compact_interview(item))

    results.sort(key=lambda x: x[0], reverse=True)
    return [{"kind": kind, "score": score, **compact} for score, kind, compact in results[:limit]]


def get_project(project_id: str) -> dict[str, Any] | None:
    """Get full project details by ID."""
    data = _load()
    for p in data.get("projects", []):
        if p.get("id") == project_id:
            return {
                "id": p.get("id", ""),
                "name": p.get("name", ""),
                "url": p.get("url", ""),
                "summary": p.get("summary", ""),
                "oneLineVerdict": p.get("oneLineVerdict", ""),
                "primaryCategory": p.get("primaryCategory", ""),
                "businessScenario": p.get("businessScenario", ""),
                "biggestHighlight": p.get("biggestHighlight", ""),
                "status": p.get("status", ""),
                "score": p.get("score"),
                "types": p.get("types", []),
                "relatedPatterns": p.get("relatedPatterns", []),
                "nextActions": p.get("nextActions", []),
                "oralAnswer": p.get("oralAnswer", ""),
                "engineeringPitch": p.get("engineeringPitch", ""),
                "writebackSummary": p.get("writebackSummary", ""),
                "writebackTargets": p.get("writebackTargets", {}),
                "sourceFile": p.get("sourceFile", ""),
            }
    return None


def get_solution(solution_id: str) -> dict[str, Any] | None:
    """Get full solution details by ID."""
    data = _load()
    for s in data.get("solutions", []):
        if s.get("id") == solution_id:
            return {
                "id": s.get("id", ""),
                "title": s.get("title", ""),
                "problemDefinition": s.get("problemDefinition", ""),
                "whyImportant": s.get("whyImportant", []),
                "commonMistakes": s.get("commonMistakes", []),
                "maturePractices": s.get("maturePractices", []),
                "actions": s.get("actions", []),
                "sourceFile": s.get("sourceFile", ""),
            }
    return None


def get_pain_point(pain_point_id: str) -> dict[str, Any] | None:
    """Get full pain point details by ID."""
    data = _load()
    for pp in data.get("painPoints", []):
        if pp.get("id") == pain_point_id:
            return {
                "id": pp.get("id", ""),
                "title": pp.get("title", ""),
                "topic": pp.get("topic", ""),
                "severity": pp.get("severity", ""),
                "industryPain": pp.get("industryPain", ""),
                "solutionMethod": pp.get("solutionMethod", ""),
                "evidenceProjects": pp.get("evidenceProjects", []),
                "evidenceSources": pp.get("evidenceSources", []),
                "relatedSolution": pp.get("relatedSolution", ""),
                "commonPractices": pp.get("commonPractices", pp.get("maturePractices", [])),
                "dataSignals": pp.get("dataSignals", []),
                "commonMistakes": pp.get("commonMistakes", []),
                "evolutionRule": pp.get("evolutionRule", ""),
                "actions": pp.get("actions", []),
            }
    return None


def list_projects(category: str | None = None, min_score: int | None = None) -> list[dict[str, Any]]:
    """List projects with optional filters."""
    data = _load()
    projects = data.get("projects", [])
    if category:
        projects = [p for p in projects if category.lower() in (p.get("primaryCategory", "").lower() + " " + " ".join(p.get("types", [])).lower())]
    if min_score is not None:
        projects = [p for p in projects if (p.get("score") or 0) >= min_score]
    return [_compact_project(p) for p in projects]


def list_solutions() -> list[dict[str, Any]]:
    """List all solutions."""
    data = _load()
    return [_compact_solution(s) for s in data.get("solutions", [])]


def list_pain_points(severity: str | None = None) -> list[dict[str, Any]]:
    """List pain points with optional severity filter."""
    data = _load()
    pps = data.get("painPoints", [])
    if severity:
        pps = [pp for pp in pps if pp.get("severity", "").lower() == severity.lower()]
    return [_compact_pain_point(pp) for pp in pps]


def get_related_entities(entity_id: str) -> dict[str, Any]:
    """Get entities related to the given entity ID."""
    data = _load()
    related: dict[str, Any] = {"entityId": entity_id, "projects": [], "solutions": [], "painPoints": [], "interviews": []}

    for p in data.get("projects", []):
        if p.get("id") == entity_id:
            related["type"] = "project"
            for pid in p.get("relatedPatterns", []):
                related["solutions"].append({"id": pid, "title": pid})
            wb = p.get("writebackTargets", {})
            for pp_id in wb.get("painPoints", []):
                related["painPoints"].append({"id": pp_id, "title": pp_id})
            for int_id in wb.get("interviews", []):
                related["interviews"].append({"id": int_id})
            return related

    for s in data.get("solutions", []):
        if s.get("id") == entity_id:
            related["type"] = "solution"
            for p in data.get("projects", []):
                if entity_id in p.get("relatedPatterns", []):
                    related["projects"].append(_compact_project(p))
            return related

    for pp in data.get("painPoints", []):
        if pp.get("id") == entity_id:
            related["type"] = "painPoint"
            for proj_id in pp.get("evidenceProjects", []):
                for p in data.get("projects", []):
                    if p.get("id") == proj_id:
                        related["projects"].append(_compact_project(p))
            if pp.get("relatedSolution"):
                related["solutions"].append({"id": pp["relatedSolution"], "title": pp["relatedSolution"]})
            return related

    related["type"] = "unknown"
    return related


def get_interview_questions(project_id: str | None = None, pattern_id: str | None = None) -> list[dict[str, Any]]:
    """Get interview questions, optionally filtered by project or pattern."""
    data = _load()
    items = data.get("interviews", {}).get("items", [])
    if project_id:
        items = [i for i in items if project_id in i.get("relatedProjects", [])]
    if pattern_id:
        items = [i for i in items if pattern_id in i.get("relatedPatterns", [])]
    return [_compact_interview(i) for i in items]


def get_knowledge_stats() -> dict[str, Any]:
    """Return knowledge base statistics."""
    data = _load()
    projects = data.get("projects", [])
    return {
        "generatedAt": data.get("generatedAt", ""),
        "language": data.get("language", ""),
        "projects": len(projects),
        "solutions": len(data.get("solutions", [])),
        "painPoints": len(data.get("painPoints", [])),
        "sources": len(data.get("sources", [])),
        "interviews": data.get("interviews", {}).get("questionCount", 0),
        "searchIndex": len(data.get("searchIndex", [])),
        "highScoreProjects": len([p for p in projects if (p.get("score") or 0) >= 80]),
        "deepDistilled": len([p for p in projects if p.get("status") == "深度沉淀"]),
        "avgScore": round(sum(p.get("score") or 0 for p in projects) / len(projects)) if projects else 0,
    }
