#!/usr/bin/env python3
"""
Project Radar: discover, score, and prepare distillation drafts for high-value projects.

First version goals:
- Add a GitHub repo manually.
- Discover GitHub repos by keyword/topic.
- Score candidates with transparent heuristics.
- Render docs/project-radar/candidates.md.
- Create a single-project distillation draft.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RADAR_DIR = DOCS / "project-radar"
EXTERNAL_DIR = DOCS / "external-projects"
PATTERNS_DIR = DOCS / "patterns"
CACHE_DIR = ROOT / "tmp" / "ingest-cache"

CONFIG_PATH = RADAR_DIR / "radar-config.json"
DATA_PATH = RADAR_DIR / "candidates.json"
CANDIDATES_MD = RADAR_DIR / "candidates.md"
LOG_MD = RADAR_DIR / "discovery-log.md"

GITHUB_API = "https://api.github.com"


@dataclass
class RepoRef:
    owner: str
    repo: str

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repo}"

    @property
    def html_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs() -> None:
    RADAR_DIR.mkdir(parents=True, exist_ok=True)
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    (EXTERNAL_DIR / "待分类项目池").mkdir(parents=True, exist_ok=True)
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def ingest_cache_path(full_name: str) -> Path:
    safe = safe_filename(full_name)
    matches = sorted(CACHE_DIR.glob(f"{safe}-*.json"))
    if matches:
        return matches[-1]
    return CACHE_DIR / f"{safe}.json"


def load_ingest_cache(full_name: str) -> dict[str, Any] | None:
    path = ingest_cache_path(full_name)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_config() -> dict[str, Any]:
    return load_json(CONFIG_PATH, {})


def load_data() -> dict[str, Any]:
    return load_json(DATA_PATH, {"version": 1, "updated_at": None, "candidates": {}})


def save_data(data: dict[str, Any]) -> None:
    data["updated_at"] = utc_now()
    save_json(DATA_PATH, data)


def parse_repo(value: str) -> RepoRef:
    value = value.strip()
    patterns = [
        r"github\.com[:/](?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+)",
        r"^(?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            repo = match.group("repo").removesuffix(".git")
            return RepoRef(match.group("owner"), repo)
    raise SystemExit(f"Cannot parse GitHub repo from: {value}")


def github_request(path_or_url: str) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{GITHUB_API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "claude-code-sourcemap-project-radar",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API error {exc.code} for {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error for {url}: {exc}") from exc


def fetch_text_url(url: str) -> str:
    headers = {"User-Agent": "claude-code-sourcemap-project-radar"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_repo_metadata(ref: RepoRef) -> dict[str, Any]:
    repo = github_request(f"/repos/{ref.full_name}")
    root_files = fetch_root_files(ref)
    readme = fetch_readme(ref)
    return {
        "full_name": repo.get("full_name", ref.full_name),
        "owner": ref.owner,
        "repo": ref.repo,
        "html_url": repo.get("html_url", ref.html_url),
        "description": repo.get("description") or "",
        "topics": repo.get("topics") or [],
        "language": repo.get("language") or "",
        "stars": repo.get("stargazers_count") or 0,
        "forks": repo.get("forks_count") or 0,
        "watchers": repo.get("watchers_count") or 0,
        "open_issues": repo.get("open_issues_count") or 0,
        "license": (repo.get("license") or {}).get("spdx_id") or "",
        "homepage": repo.get("homepage") or "",
        "default_branch": repo.get("default_branch") or "main",
        "created_at": repo.get("created_at") or "",
        "updated_at": repo.get("updated_at") or "",
        "pushed_at": repo.get("pushed_at") or "",
        "archived": bool(repo.get("archived")),
        "disabled": bool(repo.get("disabled")),
        "root_files": root_files,
        "readme_excerpt": readme[:5000],
        "readme_length": len(readme),
        "fetched_at": utc_now(),
    }


def fetch_root_files(ref: RepoRef) -> list[str]:
    try:
        contents = github_request(f"/repos/{ref.full_name}/contents")
    except SystemExit:
        return []
    if not isinstance(contents, list):
        return []
    return sorted(item.get("name", "") for item in contents if item.get("name"))


def fetch_readme(ref: RepoRef) -> str:
    try:
        readme = github_request(f"/repos/{ref.full_name}/readme")
    except SystemExit:
        return ""
    download_url = readme.get("download_url")
    if download_url:
        try:
            return fetch_text_url(download_url)
        except Exception:
            return ""
    content = readme.get("content")
    if content:
        try:
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except Exception:
            return ""
    return ""


def discover_repos(query: str, limit: int) -> list[RepoRef]:
    encoded = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(limit),
        }
    )
    result = github_request(f"/search/repositories?{encoded}")
    refs: list[RepoRef] = []
    for item in result.get("items", []):
        full_name = item.get("full_name")
        if full_name:
            refs.append(parse_repo(full_name))
    return refs


def has_any(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword.lower() in lowered)


def days_since(date_text: str) -> int | None:
    if not date_text:
        return None
    try:
        dt = datetime.fromisoformat(date_text.replace("Z", "+00:00"))
    except ValueError:
        return None
    delta = datetime.now(timezone.utc) - dt
    return max(0, delta.days)


def clamp(value: float, low: int = 0, high: int = 100) -> int:
    return int(max(low, min(high, round(value))))


def score_candidate(meta: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    keywords = config.get("priority_keywords") or []
    text = " ".join(
        [
            meta.get("full_name", ""),
            meta.get("description", ""),
            " ".join(meta.get("topics") or []),
            meta.get("readme_excerpt", ""),
        ]
    )
    keyword_hits = has_any(text, keywords)
    relevance = 25 + keyword_hits * 8
    lowered_text = text.lower()
    if "agentic coding" in lowered_text or "coding tool" in lowered_text:
        relevance += 18
    if "terminal" in lowered_text and "code" in lowered_text:
        relevance += 8
    relevance = clamp(relevance)

    root = {name.lower() for name in meta.get("root_files") or []}
    root_joined = " ".join(root)
    quality = 20
    if meta.get("readme_length", 0) > 800:
        quality += 18
    if meta.get("license") or "license.md" in root or "license" in root:
        quality += 10
    if "docs" in root_joined or "doc" in root_joined:
        quality += 12
    if "examples" in root_joined or "example" in root_joined:
        quality += 10
    if ".github" in root:
        quality += 8
    if "test" in root_joined or "tests" in root_joined:
        quality += 8
    if "changelog" in root_joined or "release" in root_joined:
        quality += 8
    if "plugins" in root:
        quality += 8
    if "security.md" in root:
        quality += 6
    engineering_quality = clamp(quality)

    learning_terms = [
        "architecture",
        "runtime",
        "framework",
        "plugin",
        "mcp",
        "memory",
        "sandbox",
        "permission",
        "multi-agent",
        "agent",
        "examples",
        "docs",
        "sdk",
    ]
    learning_hits = has_any(text, learning_terms)
    learning_value = 25 + learning_hits * 7
    if "plugins" in root:
        learning_value += 12
    if "examples" in root:
        learning_value += 8
    if "changelog.md" in root:
        learning_value += 8
    if "security.md" in root:
        learning_value += 6
    if meta.get("stars", 0) >= 10000 and ("agent" in lowered_text or "llm" in lowered_text):
        learning_value += 10
    learning_value = clamp(learning_value)

    pushed_days = days_since(meta.get("pushed_at", ""))
    if pushed_days is None:
        activity = 35
    elif pushed_days <= 30:
        activity = 95
    elif pushed_days <= 90:
        activity = 82
    elif pushed_days <= 180:
        activity = 68
    elif pushed_days <= 365:
        activity = 52
    else:
        activity = 35
    if meta.get("archived") or meta.get("disabled"):
        activity = min(activity, 20)

    stars = meta.get("stars") or 0
    novelty = 45
    if stars >= 10000:
        novelty += 15
    elif stars >= 1000:
        novelty += 10
    elif stars >= 100:
        novelty += 5
    novelty += min(25, keyword_hits * 3)
    if "demo" in text.lower() and stars < 500:
        novelty -= 15
    novelty = clamp(novelty)

    weights = config.get("scoring") or {}
    score = (
        relevance * float(weights.get("relevance", 0.3))
        + engineering_quality * float(weights.get("engineering_quality", 0.25))
        + learning_value * float(weights.get("learning_value", 0.2))
        + activity * float(weights.get("activity", 0.15))
        + novelty * float(weights.get("novelty", 0.1))
    )

    total = clamp(score)
    thresholds = config.get("thresholds") or {}
    must = int(thresholds.get("must_distill", 85))
    worth = int(thresholds.get("worth_distill", 70))
    brief = int(thresholds.get("brief_card", 55))
    if total >= must:
        level = "High"
        next_action = "distill"
    elif total >= worth:
        level = "High"
        next_action = "distill"
    elif total >= brief:
        level = "Medium"
        next_action = "watch"
    else:
        level = "Low"
        next_action = "skip"

    return {
        "total": total,
        "level": level,
        "next_action": next_action,
        "dimensions": {
            "relevance": relevance,
            "engineering_quality": engineering_quality,
            "learning_value": learning_value,
            "activity": activity,
            "novelty": novelty,
        },
        "signals": {
            "keyword_hits": keyword_hits,
            "learning_hits": learning_hits,
            "pushed_days": pushed_days,
            "root_files": meta.get("root_files", [])[:30],
        },
    }


def upsert_candidate(data: dict[str, Any], meta: dict[str, Any], source: str, query: str = "") -> None:
    config = load_config()
    full_name = meta["full_name"]
    existing = data["candidates"].get(full_name, {})
    score = score_candidate(meta, config)
    data["candidates"][full_name] = {
        **existing,
        **meta,
        "source": source,
        "query": query,
        "score": score,
        "updated_in_radar_at": utc_now(),
    }


def render_candidates(data: dict[str, Any]) -> None:
    candidates = list(data.get("candidates", {}).values())
    candidates.sort(key=lambda item: item.get("score", {}).get("total", 0), reverse=True)

    lines = [
        "# Project Radar 候选池",
        "",
        "> 用途：记录自动发现或手动加入的优质项目候选。  ",
        "> 工作流：先进入候选池，评分和人工确认后再深度沉淀。  ",
        f"> 最后更新：{data.get('updated_at') or utc_now()}",
        "",
        "## 候选项目",
        "",
    ]
    if not candidates:
        lines.extend(
            [
                "暂无候选项目。运行下面命令添加：",
                "",
                "```powershell",
                "python scripts/project_radar.py add https://github.com/anthropics/claude-code",
                "python scripts/project_radar.py discover --query \"coding agent\"",
                "```",
                "",
            ]
        )
    for item in candidates:
        score = item.get("score", {})
        dims = score.get("dimensions", {})
        lines.extend(
            [
                f"### {item.get('full_name')}",
                "",
                f"- URL: {item.get('html_url')}",
                f"- 主题: {', '.join(item.get('topics') or []) or '待补充'}",
                f"- 来源: {item.get('source', 'unknown')}"
                + (f" / `{item.get('query')}`" if item.get("query") else ""),
                f"- 推荐等级: {score.get('level', 'Unknown')}",
                f"- 总分: {score.get('total', 0)}",
                f"- 维度: relevance={dims.get('relevance')}, engineering={dims.get('engineering_quality')}, learning={dims.get('learning_value')}, activity={dims.get('activity')}, novelty={dims.get('novelty')}",
                f"- 推荐理由: {build_recommendation(item)}",
                f"- 核心价值: {build_core_value(item)}",
                f"- 风险/不足: {build_risks(item)}",
                f"- 建议沉淀角度: {build_distill_angle(item)}",
                f"- 下一步动作: {score.get('next_action', 'watch')}",
                "",
            ]
        )
    CANDIDATES_MD.write_text("\n".join(lines), encoding="utf-8")


def build_recommendation(item: dict[str, Any]) -> str:
    desc = item.get("description") or "README/描述待补充"
    stars = item.get("stars") or 0
    return f"{desc}；stars={stars}，与当前 Agent 工程知识库主题存在可学习关联。"


def build_core_value(item: dict[str, Any]) -> str:
    text = " ".join(
        [
            item.get("description", ""),
            " ".join(item.get("topics") or []),
            item.get("readme_excerpt", ""),
        ]
    ).lower()
    values = []
    mapping = [
        ("mcp", "外部工具生态接入"),
        ("agent", "Agent Runtime / Coding Agent 设计"),
        ("memory", "记忆系统与上下文治理"),
        ("plugin", "插件化和能力包设计"),
        ("sandbox", "权限、沙箱与安全治理"),
        ("multi-agent", "多 Agent 协作"),
        ("observability", "可观测性和工程化"),
    ]
    for keyword, value in mapping:
        if keyword in text:
            values.append(value)
    return "、".join(dict.fromkeys(values)) or "待人工阅读 README 后补充"


def build_risks(item: dict[str, Any]) -> str:
    risks = []
    if item.get("archived"):
        risks.append("项目已归档")
    root = {name.lower() for name in item.get("root_files") or []}
    if not item.get("license") and "license.md" not in root and "license" not in root:
        risks.append("license 信号不足")
    if item.get("readme_length", 0) < 800:
        risks.append("README 信息较少")
    pushed_days = item.get("score", {}).get("signals", {}).get("pushed_days")
    if pushed_days is not None and pushed_days > 365:
        risks.append("最近一年活跃度较低")
    return "；".join(risks) or "暂无明显风险，仍需人工确认源码和文档质量"


def build_distill_angle(item: dict[str, Any]) -> str:
    values = build_core_value(item)
    if values.startswith("待人工"):
        return "先做项目速览，再判断是否进入通用问题库"
    return f"围绕 {values} 提取通用问题、技术框架和当前项目行动项"


def append_log(message: str) -> None:
    if not LOG_MD.exists():
        LOG_MD.write_text("# Project Radar 发现日志\n\n## 日志\n\n", encoding="utf-8")
    content = LOG_MD.read_text(encoding="utf-8")
    if "暂无日志。" in content:
        content = content.replace("暂无日志。\n", "")
    content += f"- {utc_now()} {message}\n"
    LOG_MD.write_text(content, encoding="utf-8")


def add_repo(args: argparse.Namespace) -> None:
    ensure_dirs()
    data = load_data()
    ref = parse_repo(args.repo)
    meta = fetch_repo_metadata(ref)
    upsert_candidate(data, meta, "manual", "")
    save_data(data)
    render_candidates(data)
    append_log(f"手动添加 `{ref.full_name}`，score={data['candidates'][ref.full_name]['score']['total']}")
    print(f"Added {ref.full_name}: score={data['candidates'][ref.full_name]['score']['total']}")


def init_project(args: argparse.Namespace) -> None:
    ensure_dirs()
    if not CONFIG_PATH.exists():
        save_json(
            CONFIG_PATH,
            {
                "default_topics": {
                    "agent-runtime": [
                        "agent runtime",
                        "coding agent",
                        "developer agent",
                        "llm tools",
                        "tool calling",
                        "mcp",
                        "multi-agent",
                    ]
                },
                "scoring": {
                    "relevance": 0.3,
                    "engineering_quality": 0.25,
                    "learning_value": 0.2,
                    "activity": 0.15,
                    "novelty": 0.1,
                },
                "thresholds": {"must_distill": 85, "worth_distill": 70, "brief_card": 55},
                "priority_keywords": ["agent", "mcp", "tool calling", "memory", "plugin", "sandbox", "llm"],
            },
        )
    if not DATA_PATH.exists():
        save_data({"version": 1, "updated_at": None, "candidates": {}})
    if not CANDIDATES_MD.exists():
        render_candidates(load_data())
    if not LOG_MD.exists():
        LOG_MD.write_text("# Project Radar 发现日志\n\n## 日志\n\n", encoding="utf-8")
    append_log("初始化 Project Radar 目录和基础文件")
    print("Project Radar initialized.")


def discover(args: argparse.Namespace) -> None:
    ensure_dirs()
    config = load_config()
    queries: list[str] = []
    if args.query:
        queries.append(args.query)
    if args.topic:
        topic_queries = (config.get("default_topics") or {}).get(args.topic)
        if not topic_queries:
            raise SystemExit(f"Unknown topic `{args.topic}`. Available: {', '.join((config.get('default_topics') or {}).keys())}")
        queries.extend(topic_queries)
    if not queries:
        raise SystemExit("Use --query or --topic.")

    data = load_data()
    seen = 0
    for query in queries:
        refs = discover_repos(query, args.limit)
        for ref in refs:
            meta = fetch_repo_metadata(ref)
            upsert_candidate(data, meta, "keyword", query)
            seen += 1
    save_data(data)
    render_candidates(data)
    append_log(f"关键词发现完成 queries={queries}，repos={seen}")
    print(f"Discovered/updated {seen} candidates.")


def rescore(args: argparse.Namespace) -> None:
    ensure_dirs()
    config = load_config()
    data = load_data()
    for item in data.get("candidates", {}).values():
        item["score"] = score_candidate(item, config)
        item["updated_in_radar_at"] = utc_now()
    save_data(data)
    render_candidates(data)
    append_log("重新评分候选池")
    print(f"Rescored {len(data.get('candidates', {}))} candidates.")


def list_candidates(args: argparse.Namespace) -> None:
    data = load_data()
    candidates = list(data.get("candidates", {}).values())
    candidates.sort(key=lambda item: item.get("score", {}).get("total", 0), reverse=True)
    min_score = args.min_score
    count = 0
    for item in candidates:
        total = item.get("score", {}).get("total", 0)
        if total < min_score:
            continue
        count += 1
        print(f"{total:3} {item.get('score', {}).get('level', 'Unknown'):6} {item.get('full_name')} {item.get('html_url')}")
    if count == 0:
        print("No candidates matched.")


def status(args: argparse.Namespace) -> None:
    data = load_data()
    candidates = list(data.get("candidates", {}).values())
    buckets = {"High": 0, "Medium": 0, "Low": 0, "Unknown": 0}
    for item in candidates:
        level = item.get("score", {}).get("level", "Unknown")
        buckets[level] = buckets.get(level, 0) + 1
    drafts = sorted(EXTERNAL_DIR.rglob("*.md")) if EXTERNAL_DIR.exists() else []
    pattern_docs = sorted(PATTERNS_DIR.rglob("*.md")) if PATTERNS_DIR.exists() else []
    pattern_docs = [p for p in pattern_docs if p.name.lower() != "readme.md"]
    print(f"Candidates: {len(candidates)}")
    print(f"High: {buckets.get('High', 0)}  Medium: {buckets.get('Medium', 0)}  Low: {buckets.get('Low', 0)}")
    print(f"External project drafts: {len([p for p in drafts if p.name.lower() != 'readme.md'])}")
    print(f"Pattern docs: {len(pattern_docs)}")
    print(f"Updated at: {data.get('updated_at') or 'never'}")


def safe_filename(full_name: str) -> str:
    return full_name.lower().replace("/", "-").replace("_", "-")


def distillation_output_path(full_name: str) -> Path:
    return EXTERNAL_DIR / "待分类项目池" / f"{safe_filename(full_name)}.md"


def existing_distillation_path(full_name: str) -> Path | None:
    filename = f"{safe_filename(full_name)}.md"
    for path in EXTERNAL_DIR.rglob(filename):
        if path.name.lower() != "readme.md":
            return path
    return None


def run_ingest_for_repo(ref: RepoRef, focus: str = "") -> dict[str, Any]:
    from ingest_repo import build_cache_path, run_ingest

    source = ref.html_url
    try:
        result = run_ingest(source, focus=focus)
    except Exception as exc:  # noqa: BLE001
        result = {
            "source": source,
            "ingest_source": source,
            "focus": focus,
            "summary": f"Gitingest failed: {exc}",
            "tree": "",
            "content": "",
            "summary_length": 0,
            "tree_length": 0,
            "content_length": 0,
            "ingested_at": utc_now(),
            "error": str(exc),
        }
    cache_path = build_cache_path(source, focus, [], [])
    cache_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result["output_file"] = str(cache_path)
    return result


def distill(args: argparse.Namespace) -> None:
    ensure_dirs()
    data = load_data()
    ref = parse_repo(args.repo)
    full_name = ref.full_name
    item = data.get("candidates", {}).get(full_name)
    if not item or args.refresh:
        meta = fetch_repo_metadata(ref)
        upsert_candidate(data, meta, "manual", "")
        save_data(data)
        render_candidates(data)
        item = data["candidates"][full_name]

    output = existing_distillation_path(full_name) or distillation_output_path(full_name)
    if output.exists() and not args.force:
        raise SystemExit(f"{output} already exists. Use --force to overwrite.")

    ingest_data = None
    if args.use_ingest:
        ingest_data = run_ingest_for_repo(ref, args.ingest_focus)
    else:
        ingest_data = load_ingest_cache(full_name)
    content = build_distillation_draft(item, ingest_data)
    output.write_text(content, encoding="utf-8")
    append_log(f"生成沉淀草稿 `{output.relative_to(ROOT)}`")
    print(f"Wrote {output}")


def distill_all(args: argparse.Namespace) -> None:
    ensure_dirs()
    data = load_data()
    candidates = list(data.get("candidates", {}).values())
    candidates.sort(key=lambda item: item.get("score", {}).get("total", 0), reverse=True)
    written = 0
    skipped = 0
    for item in candidates:
        total = item.get("score", {}).get("total", 0)
        if total < args.min_score:
            continue
        full_name = item.get("full_name")
        if not full_name:
            continue
        output = existing_distillation_path(full_name) or distillation_output_path(full_name)
        if output.exists() and not args.force:
            skipped += 1
            continue
        output.write_text(build_distillation_draft(item), encoding="utf-8")
        append_log(f"批量生成沉淀草稿 `{output.relative_to(ROOT)}`")
        written += 1
        if args.limit and written >= args.limit:
            break
    print(f"Wrote {written} drafts. Skipped {skipped} existing drafts.")


def build_distillation_draft(item: dict[str, Any], ingest_data: dict[str, Any] | None = None) -> str:
    score = item.get("score", {})
    dims = score.get("dimensions", {})
    topics = ", ".join(item.get("topics") or []) or "待补充"
    root_files = ", ".join(item.get("root_files") or [])
    branch = item.get("default_branch") or "main"
    readme_excerpt = item.get("readme_excerpt", "").strip()
    if len(readme_excerpt) > 1200:
        readme_excerpt = readme_excerpt[:1200].rstrip() + "\n..."
    ingest_summary = ""
    ingest_tree = ""
    ingest_path = ""
    if ingest_data:
        ingest_summary = (ingest_data.get("summary") or "").strip()
        ingest_tree = (ingest_data.get("tree") or "").strip()
        ingest_path = ingest_data.get("output_file") or str(ingest_cache_path(item.get("full_name", "")))
        if len(ingest_tree) > 4000:
            ingest_tree = ingest_tree[:4000].rstrip() + "\n..."

    return f"""# 项目沉淀：{item.get('full_name')}

> 来源：{item.get('html_url')}  
> 沉淀日期：{datetime.now().strftime('%Y-%m-%d')}  
> 推荐等级：{score.get('level', 'Unknown')}  
> 总分：{score.get('total', 0)}  
> 学习主题：{topics}

## 1. 项目一句话

{item.get('description') or '待人工阅读 README 后补充。'}

## 2. 为什么值得学

- Radar 评分：总分 {score.get('total', 0)}；相关性 {dims.get('relevance')}；工程质量 {dims.get('engineering_quality')}；学习价值 {dims.get('learning_value')}；活跃度 {dims.get('activity')}；稀缺性 {dims.get('novelty')}。
- GitHub 信号：stars={item.get('stars')}，forks={item.get('forks')}，language={item.get('language') or 'unknown'}，license={item.get('license') or 'unknown'}。
- 推荐理由：{build_recommendation(item)}

## 3. 核心场景

待人工补充：

- 用户是谁？
- 用户在什么场景下使用？
- 它替用户减少了什么复杂度？

## 4. 它解决的通用问题

初步判断：

- {build_distill_angle(item)}

后续阅读时，请进一步转换成通用问题，例如：

- Agent 如何统一接入外部工具生态？
- 高风险工具如何做权限、安全和审计？
- 多 Agent 如何分工、通信和合并结果？
- 长上下文、Memory、Prompt 如何治理？

## 5. 优秀技术和框架

待读源码和文档后补充：

- 架构分层：
- 核心 runtime：
- 数据模型：
- 插件/扩展：
- 权限/安全：
- 可观测性：
- UI/交互：
- 部署/分发：

## 6. 可迁移设计原则

待补充。请把项目做法抽象成“自己的项目也能复用”的原则。

## 7. 对我当前项目的行动项

- [ ] 现在就能做：
- [ ] 需要调研后做：
- [ ] 暂时不做但保留方向：

## 8. Radar 元数据

- topics: {topics}
- root files: {root_files or 'unknown'}
- pushed_at: {item.get('pushed_at') or 'unknown'}
- default_branch: {branch}
- homepage: {item.get('homepage') or 'none'}
- 风险/不足：{build_risks(item)}

## 9. Gitingest 理解输入

{f'''### 9.1 Summary

```text
{ingest_summary}
```

### 9.2 Directory Tree

```text
{ingest_tree}
```

### 9.3 Cache

- ingest cache: {ingest_path}
''' if ingest_summary or ingest_tree else '当前还没有 Gitingest 输入，后续可用 `python scripts\\project_radar.py distill owner/repo --use-ingest` 补充。'}

## 10. README 摘要摘录

```text
{readme_excerpt or 'README 暂未获取。'}
```

## 11. 证据链接

- README: {item.get('html_url')}/blob/{branch}/README.md
- Docs: {item.get('html_url')}/tree/{branch}/docs
- Source: {item.get('html_url')}
- CHANGELOG: {item.get('html_url')}/blob/{branch}/CHANGELOG.md
- Examples: {item.get('html_url')}/tree/{branch}/examples
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Discover, score, and distill high-value projects.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Create Project Radar directories and base files if missing.")
    init_cmd.set_defaults(func=init_project)

    add_cmd = sub.add_parser("add", help="Add one GitHub repo to the candidate pool.")
    add_cmd.add_argument("repo", help="GitHub URL or owner/repo.")
    add_cmd.set_defaults(func=add_repo)

    discover_cmd = sub.add_parser("discover", help="Discover GitHub repos by query or configured topic.")
    discover_cmd.add_argument("--query", help="GitHub search query.")
    discover_cmd.add_argument("--topic", help="Configured topic from radar-config.json.")
    discover_cmd.add_argument("--limit", type=int, default=10, help="Max repos per query.")
    discover_cmd.set_defaults(func=discover)

    score_cmd = sub.add_parser("score", help="Re-score all candidates.")
    score_cmd.set_defaults(func=rescore)

    list_cmd = sub.add_parser("list", help="List candidates.")
    list_cmd.add_argument("--min-score", type=int, default=0)
    list_cmd.set_defaults(func=list_candidates)

    status_cmd = sub.add_parser("status", help="Show Project Radar summary.")
    status_cmd.set_defaults(func=status)

    distill_cmd = sub.add_parser("distill", help="Create a single-project distillation draft.")
    distill_cmd.add_argument("repo", help="GitHub URL or owner/repo.")
    distill_cmd.add_argument("--refresh", action="store_true", help="Fetch latest metadata before drafting.")
    distill_cmd.add_argument("--use-ingest", action="store_true", help="Run gitingest before drafting.")
    distill_cmd.add_argument("--ingest-focus", default="", help="Optional subdirectory focus for gitingest.")
    distill_cmd.add_argument("--force", action="store_true", help="Overwrite existing draft.")
    distill_cmd.set_defaults(func=distill)

    distill_all_cmd = sub.add_parser("distill-all", help="Create distillation drafts for high-score candidates.")
    distill_all_cmd.add_argument("--min-score", type=int, default=80)
    distill_all_cmd.add_argument("--limit", type=int, default=0, help="Max drafts to write; 0 means no limit.")
    distill_all_cmd.add_argument("--force", action="store_true", help="Overwrite existing drafts.")
    distill_all_cmd.set_defaults(func=distill_all)

    return parser


def main(argv: list[str] | None = None) -> int:
    ensure_dirs()
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
