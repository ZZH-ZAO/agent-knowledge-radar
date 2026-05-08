"""Tests for knowledge_tools retrieval functions."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import knowledge_tools as kt


@pytest.fixture(autouse=True)
def reload_data():
    kt.reload()


class TestSearchKnowledge:
    def test_returns_results(self):
        results = kt.search_knowledge("Agent")
        assert len(results) > 0
        assert all("kind" in r for r in results)

    def test_filter_by_kind(self):
        results = kt.search_knowledge("Agent", kinds=["project"])
        assert all(r["kind"] == "project" for r in results)

    def test_limit(self):
        results = kt.search_knowledge("Agent", limit=2)
        assert len(results) <= 2

    def test_empty_query(self):
        results = kt.search_knowledge("")
        assert len(results) == 0

    def test_no_match(self):
        results = kt.search_knowledge("xyznonexistent123")
        assert len(results) == 0


class TestGetProject:
    def test_existing_project(self):
        proj = kt.get_project("current-project")
        assert proj is not None
        assert proj["name"] == "claude-code-sourcemap"
        assert "id" in proj
        assert "summary" in proj

    def test_nonexistent_project(self):
        assert kt.get_project("nonexistent-id") is None


class TestGetSolution:
    def test_returns_dict(self):
        solutions = kt.list_solutions()
        if solutions:
            first = kt.get_solution(solutions[0]["id"])
            assert first is not None
            assert "title" in first

    def test_nonexistent(self):
        assert kt.get_solution("nonexistent") is None


class TestGetPainPoint:
    def test_returns_dict(self):
        pps = kt.list_pain_points()
        if pps:
            first = kt.get_pain_point(pps[0]["id"])
            assert first is not None
            assert "title" in first
            assert "severity" in first

    def test_nonexistent(self):
        assert kt.get_pain_point("nonexistent") is None


class TestListProjects:
    def test_all(self):
        projects = kt.list_projects()
        assert len(projects) > 0

    def test_filter_category(self):
        projects = kt.list_projects(category="Agent Runtime")
        assert all("Agent Runtime" in (p.get("primaryCategory", "") + " " + " ".join(p.get("types", []))).lower() or
                   "agent" in " ".join(p.get("types", [])).lower()
                   for p in projects)

    def test_filter_min_score(self):
        projects = kt.list_projects(min_score=80)
        assert all((p.get("score") or 0) >= 80 for p in projects)


class TestListPainPoints:
    def test_all(self):
        pps = kt.list_pain_points()
        assert len(pps) > 0

    def test_filter_severity(self):
        high = kt.list_pain_points(severity="high")
        assert all(pp.get("severity") == "high" for pp in high)


class TestGetRelatedEntities:
    def test_project_relations(self):
        related = kt.get_related_entities("current-project")
        assert related["type"] == "project"
        assert "solutions" in related

    def test_unknown_entity(self):
        related = kt.get_related_entities("nonexistent")
        assert related["type"] == "unknown"


class TestGetInterviewQuestions:
    def test_all(self):
        questions = kt.get_interview_questions()
        assert len(questions) > 0

    def test_filter_by_project(self):
        questions = kt.get_interview_questions(project_id="current-project")
        for q in questions:
            assert "current-project" in q.get("relatedProjects", [])


class TestGetKnowledgeStats:
    def test_returns_stats(self):
        stats = kt.get_knowledge_stats()
        assert stats["projects"] > 0
        assert stats["solutions"] > 0
        assert "avgScore" in stats
        assert "generatedAt" in stats
