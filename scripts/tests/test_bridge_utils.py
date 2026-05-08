"""Tests for bridge_utils pure utility functions."""

import sys
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_utils import (
    extract_sections,
    merge_unique_texts,
    normalize_lines,
    parse_analysis,
    parse_github_repo,
    slugify,
)


class TestSlugify:
    def test_basic(self):
        assert slugify("hello world") == "hello-world"

    def test_chinese(self):
        result = slugify("项目沉淀")
        assert "项目沉淀" in result

    def test_url(self):
        result = slugify("https://github.com/owner/repo")
        assert "github" in result.lower()
        assert "/" not in result

    def test_empty_fallback(self):
        result = slugify("")
        assert result.startswith("draft-")

    def test_special_chars(self):
        result = slugify("hello@world#!test")
        assert "@" not in result
        assert "#" not in result
        assert "!" not in result


class TestParseGithubRepo:
    def test_full_url(self):
        assert parse_github_repo("https://github.com/owner/repo") == "owner/repo"

    def test_url_with_git_suffix(self):
        assert parse_github_repo("https://github.com/owner/repo.git") == "owner/repo"

    def test_short_form(self):
        assert parse_github_repo("owner/repo") == "owner/repo"

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            parse_github_repo("not-a-repo")


class TestExtractSections:
    def test_basic_sections(self):
        md = "# Title\n\n## Section 1\n\nContent 1\n\n## Section 2\n\nContent 2"
        sections = extract_sections(md)
        assert "Section 1" in sections
        assert "Section 2" in sections
        assert "Content 1" in sections["Section 1"]
        assert "Content 2" in sections["Section 2"]

    def test_no_sections(self):
        md = "# Title\n\nSome content without sections"
        sections = extract_sections(md)
        assert "_root" in sections

    def test_empty(self):
        sections = extract_sections("")
        assert "_root" in sections


class TestParseAnalysis:
    def test_full_markdown(self):
        md = """# Test Project

## 项目一句话

This is a test project.

## 为什么值得学

Because it tests things.

## 核心场景

Testing scenarios.

## 它解决的通用问题

How to test properly.

## 优秀技术和框架

pytest, unittest

## 可迁移设计原则

Test early, test often.

## 对我当前项目的行动项

- [ ] Write more tests
- [ ] Add CI
"""
        result = parse_analysis(md)
        assert result["title"] == "Test Project"
        assert "test project" in result["oneLine"].lower()
        assert len(result["actions"]) == 2

    def test_empty_markdown(self):
        result = parse_analysis("")
        assert result["title"] == ""
        assert result["oneLine"] == ""
        assert result["actions"] == []


class TestNormalizeLines:
    def test_basic(self):
        assert normalize_lines(["a", "b", "c"]) == ["a", "b", "c"]

    def test_dedup(self):
        assert normalize_lines(["a", "b", "a", "c"]) == ["a", "b", "c"]

    def test_strips_whitespace(self):
        assert normalize_lines(["  a  ", " b ", "c"]) == ["a", "b", "c"]

    def test_skips_empty(self):
        assert normalize_lines(["a", "", "b", "  "]) == ["a", "b"]


class TestMergeUniqueTexts:
    def test_basic_merge(self):
        result = merge_unique_texts(["a", "b"], ["c", "d"])
        assert result == ["a", "b", "c", "d"]

    def test_dedup_across_groups(self):
        result = merge_unique_texts(["a", "b"], ["b", "c"])
        assert result == ["a", "b", "c"]

    def test_with_limit(self):
        result = merge_unique_texts(["a", "b"], ["c", "d"], limit=2)
        assert len(result) == 2
        assert result == ["a", "b"]

    def test_empty_groups(self):
        result = merge_unique_texts([], [], [])
        assert result == []
