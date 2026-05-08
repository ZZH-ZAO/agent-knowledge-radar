#!/usr/bin/env python3
"""
Local bridge server for the knowledge platform.

Purpose:
- keep the existing Distill Desk button working
- expose Agent-friendly APIs so external agents can ask the platform
  to ingest, analyze, and distill projects directly
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXTERNAL_DIR = DOCS / "external-projects"
SOURCE_LIBRARY_DIR = DOCS / "source-library" / "用户提供文档"
PATTERN_WRITEBACK_DIR = DOCS / "patterns" / "总纲与方法论" / "分析回写草稿"
PAINPOINT_WRITEBACK_DIR = DOCS / "pain-points" / "分析回写草稿"
INTERVIEW_WRITEBACK_BANK = DOCS / "interviews" / "analysis-writeback-question-bank.json"
WRITEBACK_PACKAGE_DIR = DOCS / "project-radar" / "writeback-packages"
TMP_DISTILL_DIR = ROOT / "tmp" / "distill-desk"
DEFAULT_PORT = 8765


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_slug() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def ensure_dirs() -> None:
    (EXTERNAL_DIR / "待分类项目池").mkdir(parents=True, exist_ok=True)
    SOURCE_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    PATTERN_WRITEBACK_DIR.mkdir(parents=True, exist_ok=True)
    PAINPOINT_WRITEBACK_DIR.mkdir(parents=True, exist_ok=True)
    INTERVIEW_WRITEBACK_BANK.parent.mkdir(parents=True, exist_ok=True)
    WRITEBACK_PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DISTILL_DIR.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"^https?://", "", lowered)
    lowered = lowered.replace("\\", "-").replace("/", "-")
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff._-]+", "-", lowered)
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


def run_command(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "command": subprocess.list2cmdline(args),
    }


def run_build_index() -> dict[str, Any]:
    return run_command([sys.executable, str(ROOT / "scripts" / "build_knowledge_index.py")])


def find_existing_project_doc(repo: str) -> Path | None:
    filename = f"{repo_slug(repo)}.md"
    for path in EXTERNAL_DIR.rglob(filename):
        if path.name.lower() != "readme.md":
            return path
    return None


def default_project_doc(repo: str) -> Path:
    return EXTERNAL_DIR / "待分类项目池" / f"{repo_slug(repo)}.md"


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def relative_to_root(path_value: str) -> str:
    if not path_value:
        return ""
    path = Path(path_value)
    if not path.is_absolute():
        return path_value.replace("\\", "/")
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def save_task_record(payload: dict[str, Any], note_lines: list[str]) -> Path:
    ensure_dirs()
    task_path = TMP_DISTILL_DIR / f"distill-task-{now_slug()}.md"
    outputs = payload.get("outputs") or []
    lines = [
        "# 沉淀台待执行任务",
        "",
        f"- 创建时间：{now_text()}",
        "",
        "## 任务定义",
        "",
        f"来源：{payload.get('source', '')}",
        f"来源类型：{payload.get('sourceType', '')}",
        f"沉淀目标：{payload.get('goal', '')}",
        f"写法偏向：{payload.get('style', '')}",
        f"希望产出：{'、'.join(outputs) if outputs else '项目沉淀文档'}",
        f"额外要求：{payload.get('extraNotes', '') or '无'}",
        "",
        "## 说明",
        "",
    ]
    lines.extend(f"- {item}" for item in note_lines)
    lines.append("")
    return write_text(task_path, "\n".join(lines))


def build_local_project_markdown(
    *,
    source: str,
    payload: dict[str, Any],
    ingest_result: dict[str, Any] | None,
) -> str:
    name = Path(source).name or source
    focus = (payload.get("ingestFocus") or "").strip()
    summary = ""
    tree = ""
    cache_file = ""
    if ingest_result:
        summary = (ingest_result.get("summary") or "").strip()
        tree = (ingest_result.get("tree") or "").strip()
        cache_file = ingest_result.get("output_file") or ""
        if len(tree) > 4000:
            tree = tree[:4000].rstrip() + "\n..."
    outputs = "、".join(payload.get("outputs") or ["项目沉淀文档"])
    return f"""# 项目沉淀：{name}

> 来源：{source}  
> 沉淀日期：{datetime.now().strftime("%Y-%m-%d")}  
> 来源类型：本地项目  
> 目标产出：{outputs}

## 1. 项目一句话

这是一个待深入阅读的本地项目样本。当前平台已经为它建立了第一版沉淀草稿，方便后续围绕源码结构、运行链路、通用问题和工程启发继续深挖。

## 2. 为什么值得学

- 它来自你的本地工作区，通常比外部项目更适合直接回写成自己的工程动作。
- 平台已经把“源码理解 -> 项目沉淀 -> 索引更新”这条链路打通，后续可以继续补强 patterns、pain points 和面试表达。
- 当前聚焦目录：{focus or "整个仓库"}。

## 3. 核心场景

- 适合做自研项目复盘。
- 适合抽取 Agent Runtime / Tool Runtime / Memory / Prompt / Observability 等共性做法。
- 适合继续延伸成面试表达、方案抽象和平台行动项。

## 4. 它解决的通用问题

- 当前待补：先基于目录结构和关键源码判断它真正解决的工程问题。
- 后续要重点追问：它是怎么组织运行链路、怎么处理状态、怎么处理工具副作用、怎么把结果沉淀为可复用资产。

## 5. 优秀技术和框架

- 待补：架构分层
- 待补：核心 runtime
- 待补：数据流与状态流
- 待补：观测与恢复
- 待补：产品化接口

## 6. 可迁移设计原则

- 先把项目事实讲清楚，再抽象成通用问题。
- 先有证据链，再下结论。
- 先沉淀结构和边界，再沉淀亮点。

## 7. 对我当前项目的行动项

- [ ] 根据源码补齐“项目一句话 / 核心场景 / 最大亮点”
- [ ] 从关键模块里抽取 3-5 个可迁移工程原则
- [ ] 回写到方案页、痛点页和面试页

## 8. Gitingest 理解输入

{f'''### 8.1 Summary

```text
{summary or '暂无'}
```

### 8.2 Directory Tree

```text
{tree or '暂无'}
```

### 8.3 Cache

- ingest cache: {cache_file or '暂无'}
''' if ingest_result else '当前没有启用 Gitingest，可重新执行并勾选“项目理解增强”。'}

## 9. 证据链接

- 本地路径：`{source}`
"""


def build_source_note_markdown(payload: dict[str, Any]) -> str:
    source = payload.get("source", "")
    outputs = "、".join(payload.get("outputs") or ["资料源登记"])
    return f"""# 资料源登记：{source}

> 记录时间：{datetime.now().strftime("%Y-%m-%d")}  
> 来源类型：{payload.get("sourceType", "article")}  
> 目标产出：{outputs}

## 1. 这份资料是什么

这是平台收到的一份外部资料源登记草稿，后续可以继续补成项目沉淀、方案抽象、痛点证据或面试素材。

## 2. 为什么值得收进平台

- 它可能提供外部证据、写法样本、设计思路或案例细节。
- 平台会先把它纳入资料源，再决定是否升级成更高价值的沉淀文档。

## 3. 你下一步应该怎么看

- 先判断它更像项目样本、方案证据、行业痛点证据，还是面试表达素材。
- 再决定回写到 `external-projects`、`patterns`、`pain-points` 或 `interviews`。

## 4. 当前备注

{payload.get("extraNotes", "暂无")}

## 5. 来源链接

- {source}
"""


def run_ingest(payload: dict[str, Any]) -> dict[str, Any]:
    from ingest_repo import build_cache_path, run_ingest as execute_ingest

    source = str(payload.get("source", "")).strip()
    if not source:
        raise ValueError("source 不能为空")
    source_type = str(payload.get("sourceType", "local")).strip() or "local"
    focus = str(payload.get("focus") or payload.get("ingestFocus") or "").strip()
    include = payload.get("include") or []
    exclude = payload.get("exclude") or []
    branch = payload.get("branch") or None
    normalized_source = normalize_ingest_source(source, source_type)
    result = execute_ingest(
        normalized_source,
        focus=focus,
        include_patterns=include,
        exclude_patterns=exclude,
        branch=branch,
    )
    output_file = build_cache_path(normalized_source, focus, include, exclude)
    output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        **result,
        "output_file": str(output_file),
    }


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


def distill_github_project(payload: dict[str, Any]) -> dict[str, Any]:
    repo = parse_github_repo(str(payload.get("source", "")).strip())
    command = [
        sys.executable,
        str(ROOT / "scripts" / "project_radar.py"),
        "distill",
        repo,
        "--refresh",
        "--force",
    ]
    if payload.get("useGitingest"):
        command.append("--use-ingest")
        focus = str(payload.get("ingestFocus") or "").strip()
        if focus:
            command.extend(["--ingest-focus", focus])
    result = run_command(command)
    if not result["ok"]:
        raise RuntimeError(result["stderr"] or result["stdout"] or "project_radar distill 执行失败")
    output_file = find_existing_project_doc(repo) or default_project_doc(repo)
    index_result = run_build_index()
    return {
        "repo": repo,
        "output_file": str(output_file),
        "command": result["command"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "index_result": index_result,
    }


def distill_local_project(payload: dict[str, Any]) -> dict[str, Any]:
    source = str(payload.get("source", "")).strip()
    if not source:
        raise ValueError("source 不能为空")
    ingest_result = run_ingest(payload) if payload.get("useGitingest") else None
    output_file = EXTERNAL_DIR / "待分类项目池" / f"{slugify(source)}.md"
    markdown = build_local_project_markdown(source=source, payload=payload, ingest_result=ingest_result)
    write_text(output_file, markdown)
    task_file = save_task_record(
        payload,
        [
            "当前来源是本地项目，平台已先生成一版项目沉淀草稿。",
            f"项目草稿：{output_file}",
            f"Gitingest 缓存：{ingest_result['output_file']}" if ingest_result else "本次未启用 Gitingest。",
        ],
    )
    index_result = run_build_index()
    return {
        "output_file": str(output_file),
        "task_file": str(task_file),
        "ingest_result": ingest_result,
        "index_result": index_result,
    }


def distill_source_note(payload: dict[str, Any]) -> dict[str, Any]:
    source = str(payload.get("source", "")).strip()
    if not source:
        raise ValueError("source 不能为空")
    output_file = SOURCE_LIBRARY_DIR / f"{slugify(source)}.md"
    write_text(output_file, build_source_note_markdown(payload))
    task_file = save_task_record(
        payload,
        [
            "当前来源不是 GitHub 仓库，平台先把它登记为资料源草稿。",
            f"资料源草稿：{output_file}",
            "后续可以继续升级为项目沉淀、方案文档、痛点证据或面试素材。",
        ],
    )
    index_result = run_build_index()
    return {
        "output_file": str(output_file),
        "task_file": str(task_file),
        "index_result": index_result,
    }


def handle_distill(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_dirs()
    source_type = str(payload.get("sourceType", "github")).strip() or "github"
    if source_type == "github":
        result = distill_github_project(payload)
        return {
            "status": "ok",
            "message": "GitHub 项目沉淀完成",
            "outputFile": result["output_file"],
            "command": result["command"],
            "indexCommand": result["index_result"]["command"],
            "indexOk": result["index_result"]["ok"],
        }
    if source_type == "local":
        result = distill_local_project(payload)
        return {
            "status": "ok",
            "message": "本地项目草稿已生成",
            "outputFile": result["output_file"],
            "taskFile": result["task_file"],
            "ingestCache": result["ingest_result"]["output_file"] if result["ingest_result"] else "",
            "indexCommand": result["index_result"]["command"],
            "indexOk": result["index_result"]["ok"],
        }
    result = distill_source_note(payload)
    return {
        "status": "ok",
        "message": "资料源草稿已生成",
        "outputFile": result["output_file"],
        "taskFile": result["task_file"],
        "indexCommand": result["index_result"]["command"],
        "indexOk": result["index_result"]["ok"],
    }


def handle_analyze_project(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_dirs()
    source_type = str(payload.get("sourceType", "github")).strip() or "github"
    use_ingest = bool(payload.get("useGitingest", False))
    auto_writeback = bool(payload.get("autoWriteback", True))
    if source_type == "github":
        distill_result = distill_github_project(payload)
        draft_path = Path(distill_result["output_file"])
        markdown = draft_path.read_text(encoding="utf-8") if draft_path.exists() else ""
        parsed = parse_analysis(markdown)
        ingest_cache = ""
        if use_ingest:
            try:
                ingest_result = run_ingest(
                    {
                        "source": payload.get("source", ""),
                        "sourceType": "github",
                        "focus": payload.get("ingestFocus", ""),
                    }
                )
                ingest_cache = ingest_result.get("output_file", "")
            except Exception as exc:  # noqa: BLE001
                ingest_cache = f"ingest failed: {exc}"
        result = {
            "status": "ok",
            "project": {
                "source": payload.get("source", ""),
                "repo": distill_result["repo"],
                "draftFile": str(draft_path),
                "ingestCache": ingest_cache,
            },
            "analysis": parsed,
            "raw": {"markdown": markdown},
        }
        if auto_writeback:
            result["writeback"] = build_analysis_writeback(result)
        return result

    if source_type == "local":
        local_result = distill_local_project(payload)
        draft_path = Path(local_result["output_file"])
        markdown = draft_path.read_text(encoding="utf-8")
        parsed = parse_analysis(markdown)
        result = {
            "status": "ok",
            "project": {
                "source": payload.get("source", ""),
                "repo": "",
                "draftFile": str(draft_path),
                "ingestCache": local_result["ingest_result"]["output_file"] if local_result["ingest_result"] else "",
            },
            "analysis": parsed,
            "raw": {"markdown": markdown},
        }
        if auto_writeback:
            result["writeback"] = build_analysis_writeback(result)
        return result

    note_result = distill_source_note(payload)
    draft_path = Path(note_result["output_file"])
    markdown = draft_path.read_text(encoding="utf-8")
    parsed = parse_analysis(markdown)
    result = {
        "status": "ok",
        "project": {
            "source": payload.get("source", ""),
            "repo": "",
            "draftFile": str(draft_path),
            "ingestCache": "",
        },
        "analysis": parsed,
        "raw": {"markdown": markdown},
    }
    if auto_writeback:
        result["writeback"] = build_analysis_writeback(result)
    return result


def merge_interview_bank(item: dict[str, Any]) -> Path:
    if INTERVIEW_WRITEBACK_BANK.exists():
        try:
            bank = json.loads(INTERVIEW_WRITEBACK_BANK.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            bank = {}
    else:
        bank = {}
    items = bank.get("items") or []
    items = [entry for entry in items if entry.get("id") != item.get("id")]
    items.append(item)
    bank["items"] = items
    bank["questionCount"] = len(items)
    INTERVIEW_WRITEBACK_BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return INTERVIEW_WRITEBACK_BANK


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


def load_knowledge_index() -> dict[str, Any]:
    return read_json(ROOT / "data" / "knowledge-index.json")


def find_index_project(project: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    index = load_knowledge_index()
    projects = index.get("projects") if isinstance(index.get("projects"), list) else []
    if not isinstance(projects, list):
        return {}
    draft_file = relative_to_root(str(project.get("draftFile") or ""))
    repo = str(project.get("repo") or "").strip().lower()
    title = str(analysis.get("title") or "").strip().lower()
    source = str(project.get("source") or "").strip().lower()
    for item in projects:
        if not isinstance(item, dict):
            continue
        source_file = str(item.get("sourceFile") or "").replace("\\", "/").lower()
        item_url = str(item.get("url") or "").lower()
        item_name = str(item.get("name") or "").strip().lower()
        item_id = str(item.get("id") or "").strip().lower()
        if draft_file and source_file == draft_file.lower():
            return item
        if repo and (repo in item_url or repo_slug(repo) == item_id):
            return item
        if source and source in item_url:
            return item
        if title and title in item_name:
            return item
    return {}


def normalize_lines(items: list[str]) -> list[str]:
    cleaned: list[str] = []
    for item in items:
        line = str(item).strip()
        if not line:
            continue
        if line not in cleaned:
            cleaned.append(line)
    return cleaned


def snippet(text: str, limit: int = 220) -> str:
    compact = re.sub(r"\s+", " ", text or "").strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "?"


def map_pattern_targets(index_project: dict[str, Any], analysis: dict[str, Any]) -> list[dict[str, Any]]:
    known_order = [
        "agent-runtime",
        "tool-runtime",
        "mcp-integration",
        "memory-system",
        "permission-sandbox",
        "observability-patterns",
        "provider-abstraction-patterns",
        "productization-patterns",
    ]
    direct = index_project.get("relatedPatterns") if isinstance(index_project.get("relatedPatterns"), list) else []
    direct_ids = [str(item).strip() for item in direct if str(item).strip()]
    combined = " ".join(
        str(analysis.get(key) or "")
        for key in [
            "title",
            "oneLine",
            "whyWorthStudying",
            "coreScenario",
            "generalProblems",
            "technicalFrameworks",
            "designPrinciples",
            "oneLineDetail",
            "whyWorthStudyingDetail",
            "coreScenarioDetail",
            "generalProblemsDetail",
            "technicalFrameworksDetail",
            "designPrinciplesDetail",
        ]
    ).lower()
    heuristic_rules = {
        "agent-runtime": ["agent runtime", "coding agent", "subagent", "resume", "checkpoint", "runtime", "终端", "任务"],
        "tool-runtime": ["tool runtime", "tool", "command", "shell", "patch", "artifact", "工具", "命令", "副作用"],
        "mcp-integration": ["mcp", "model context protocol", "server", "tool registry"],
        "memory-system": ["memory", "context", "retrieval", "summary", "freshness", "记忆", "上下文"],
        "permission-sandbox": ["permission", "sandbox", "approval", "risk", "audit", "安全", "权限", "审计"],
        "observability-patterns": ["trace", "report", "benchmark", "eval", "recovery", "telemetry", "可观测", "评测"],
        "provider-abstraction-patterns": ["provider", "model adapter", "capability", "多模型", "模型切换"],
        "productization-patterns": ["product", "workflow", "settings", "hooks", "platform", "平台化", "产品化"],
    }
    selected: list[str] = []
    reasons: dict[str, str] = {}
    for pattern_id in known_order:
        if pattern_id in direct_ids:
            selected.append(pattern_id)
            reasons[pattern_id] = "来自项目已有 relatedPatterns"
    for pattern_id, keywords in heuristic_rules.items():
        if pattern_id in selected:
            continue
        if any(keyword.lower() in combined for keyword in keywords):
            selected.append(pattern_id)
            reasons[pattern_id] = f"命中关键词：{', '.join(keywords[:3])}"
    return [{"id": item, "reason": reasons.get(item, "自动映射")} for item in selected]


def map_pain_point_targets(pattern_targets: list[dict[str, Any]], analysis: dict[str, Any]) -> list[dict[str, Any]]:
    selected: list[str] = []
    reasons: dict[str, str] = {}
    pattern_to_pain = {
        "tool-runtime": "tool-result-context-overload",
        "mcp-integration": "mcp-ecosystem-governance",
        "memory-system": "memory-context-staleness-and-bloat",
        "agent-runtime": "runtime-recovery-and-eval-gap",
        "observability-patterns": "runtime-recovery-and-eval-gap",
        "provider-abstraction-patterns": "provider-differences-pollute-runtime",
        "productization-patterns": "agent-productization-gap",
    }
    for item in pattern_targets:
        pain_id = pattern_to_pain.get(str(item.get("id") or ""))
        if pain_id and pain_id not in selected:
            selected.append(pain_id)
            reasons[pain_id] = f"来自 pattern {item.get('id')}"
    combined = " ".join(
        str(analysis.get(key) or "")
        for key in ["generalProblemsDetail", "technicalFrameworksDetail", "designPrinciplesDetail", "title"]
    ).lower()
    keyword_rules = {
        "tool-result-context-overload": ["artifact", "tool result", "截图", "trace", "上下文", "summary"],
        "mcp-ecosystem-governance": ["mcp", "server", "registry", "扩展生态"],
        "memory-context-staleness-and-bloat": ["memory", "freshness", "stale", "context", "记忆"],
        "runtime-recovery-and-eval-gap": ["resume", "checkpoint", "trace", "benchmark", "eval", "恢复"],
        "agent-productization-gap": ["product", "workflow", "settings", "产品化", "平台"],
        "project-learning-stays-as-notes": ["distill", "knowledge", "学习", "沉淀"],
    }
    for pain_id, keywords in keyword_rules.items():
        if pain_id in selected:
            continue
        if any(keyword.lower() in combined for keyword in keywords):
            selected.append(pain_id)
            reasons[pain_id] = f"命中关键词：{', '.join(keywords[:3])}"
    return [{"id": item, "reason": reasons.get(item, "自动映射")} for item in selected]


def append_or_replace_block(path: Path, section_title: str, block_id: str, block_markdown: str) -> Path:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    start_marker = f"<!-- AUTO-WRITEBACK:{block_id}:START -->"
    end_marker = f"<!-- AUTO-WRITEBACK:{block_id}:END -->"
    block = f"{start_marker}\n{block_markdown.rstrip()}\n{end_marker}"
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub(block, text)
    else:
        if text and section_title not in text:
            text = text.rstrip() + f"\n\n{section_title}\n"
        updated = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(updated, encoding="utf-8")
    return path


def build_pattern_block(*, source_project_id: str, title: str, source: str, draft_file: str, reason: str, evidence: str, practice: str, action: str) -> str:
    return (
        f"### {title}\n\n"
        f"- 命中原因：{reason}\n"
        f"- 来源项目：`{source_project_id}`\n"
        f"- 项目地址：{source}\n"
        f"- 草稿文件：`{draft_file}`\n\n"
        f"#### 新增证据项目\n\n{evidence}\n\n"
        f"#### 项目里的具体做法\n\n{practice}\n\n"
        f"#### 对当前平台的直接启发\n\n- {action}\n"
    )


def build_pain_block(*, source_project_id: str, title: str, reason: str, evidence: str, practice: str, signals: list[str], action: str) -> str:
    signal_lines = "\n".join(f"- {item}" for item in signals) or "- 暂无新增信号"
    return (
        f"### {title}\n\n"
        f"- 命中原因：{reason}\n"
        f"- 证据项目：`{source_project_id}`\n\n"
        f"#### 新增证据项目\n\n{evidence}\n\n"
        f"#### 优秀做法补充\n\n{practice}\n\n"
        f"#### 新增数据信号\n\n{signal_lines}\n\n"
        f"#### 当前动作候选\n\n- {action}\n"
    )


def build_interview_items(*, source_project_id: str, title: str, one_line: str, why: str, scenario: str, problems: str, frameworks: str, principles: str, actions: list[str], related_patterns: list[str], pain_points: list[str]) -> list[dict[str, Any]]:
    lead_action = actions[0] if actions else "先把这个项目的设计做法映射回自己的工程动作"
    shared = {
        "knowledgePoints": normalize_lines([title, *related_patterns, *pain_points]),
        "relatedProjects": [source_project_id],
        "relatedPatterns": related_patterns,
        "evidenceSource": title,
    }
    return [
        {
            "id": f"analysis-{source_project_id}-intro",
            "rawQuestion": f"如果让你用一两分钟介绍 {title}，你会怎么讲？",
            "questionType": "项目介绍版",
            **shared,
            "recommendedAnswer": f"我会先把它定义成：{one_line}。然后讲它为什么值得现在看：{why}。最后落到真实业务场景 {scenario}，说明它不是功能堆砌，而是在回答 {problems} 这类工程问题。",
            "followUps": [
                f"这个项目最适合的业务场景是什么？{scenario}",
                f"如果只保留一个最大亮点，你会保留什么？{frameworks}",
            ],
        },
        {
            "id": f"analysis-{source_project_id}-deep-dive",
            "rawQuestion": f"{title} 具体是怎么把这些能力做进去的，而不是只停留在概念上？",
            "questionType": "深挖版",
            **shared,
            "recommendedAnswer": f"不要只说它有什么功能，要按步骤讲：先回答通用问题 {problems}，再说项目里的具体做法 {frameworks}，最后补上它为什么能成立的设计原则 {principles}。",
            "followUps": [
                f"如果你照着做，第一步会先补哪一层？{lead_action}",
                "这个项目里哪一部分最像真正的 runtime，而不是 demo？",
            ],
        },
        {
            "id": f"analysis-{source_project_id}-tradeoff",
            "rawQuestion": f"{title} 这种做法的代价和边界是什么？",
            "questionType": "trade-off 版",
            **shared,
            "recommendedAnswer": f"我会先承认它不是零成本方案。它的价值在于把 {problems} 这类问题收进工程结构里，但代价通常是接入成本、治理成本和更多显式规则。真正该讲清楚的是：为什么这个代价在当前场景下值得付。",
            "followUps": [
                "什么场景下你不会照搬它？",
                "如果要做轻量版，你会砍掉哪一层，保留哪一层？",
            ],
        },
        {
            "id": f"analysis-{source_project_id}-pain-point",
            "rawQuestion": f"{title} 对行业里的普遍痛点给了什么证据和启发？",
            "questionType": "行业痛点版",
            **shared,
            "recommendedAnswer": f"我不会把它讲成单项目功能，而会把它当成行业证据：它说明 {problems} 不是抽象讨论，而是现实系统必须处理的主线。它给出的具体做法是 {frameworks}，对我当前项目最直接的动作是 {lead_action}。",
            "followUps": [
                f"它补强了哪些 pain points？{', '.join(pain_points) if pain_points else '待映射'}",
                "除了这个项目，还有哪些样本能互相印证？",
            ],
        },
    ]


def persist_writeback_package(package: dict[str, Any]) -> Path:
    source_project_id = str(package.get("sourceProjectId") or slugify(package.get("sourceTitle") or "writeback"))
    return write_json(WRITEBACK_PACKAGE_DIR / f"{source_project_id}.json", package)


def build_analysis_writeback(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_dirs()
    project = (payload.get("project") if isinstance(payload.get("project"), dict) else {}) or {}
    analysis = (payload.get("analysis") if isinstance(payload.get("analysis"), dict) else {}) or {}
    title = str(analysis.get("title") or "项目分析结果")
    source = str(project.get("source") or "unknown")
    source_project_id = slugify(str(project.get("repo") or title or source))
    draft_file = relative_to_root(str(project.get("draftFile") or ""))
    one_line = str(analysis.get("oneLine") or "待补充")
    why = str(analysis.get("whyWorthStudying") or "待补充")
    scenario = str(analysis.get("coreScenario") or "待补充")
    problems = str(analysis.get("generalProblems") or "待补充")
    frameworks = str(analysis.get("technicalFrameworks") or "待补充")
    principles = str(analysis.get("designPrinciples") or "待补充")
    problems_detail = str(analysis.get("generalProblemsDetail") or problems or "待补充")
    frameworks_detail = str(analysis.get("technicalFrameworksDetail") or frameworks or "待补充")
    principles_detail = str(analysis.get("designPrinciplesDetail") or principles or "待补充")
    actions = normalize_lines(analysis.get("actions") if isinstance(analysis.get("actions"), list) else [])
    rebuild_index = bool(payload.get("rebuildIndex", True))
    index_project = find_index_project(project, analysis)
    pattern_targets = map_pattern_targets(index_project, analysis)
    pain_targets = map_pain_point_targets(pattern_targets, analysis)

    pattern_file_map = {
        "agent-runtime": DOCS / "patterns" / "Agent Runtime 核心运行时框架" / "agent-runtime-patterns.md",
        "tool-runtime": DOCS / "patterns" / "Tool 与 MCP 工具体系" / "tool-runtime-patterns.md",
        "mcp-integration": DOCS / "patterns" / "Tool 与 MCP 工具体系" / "mcp-integration-patterns.md",
        "memory-system": DOCS / "patterns" / "Memory Plugin Multi-Agent 扩展能力" / "memory-system-patterns.md",
        "permission-sandbox": DOCS / "patterns" / "安全治理与可观测性" / "permission-sandbox-patterns.md",
        "observability-patterns": DOCS / "patterns" / "安全治理与可观测性" / "observability-patterns.md",
        "provider-abstraction-patterns": DOCS / "patterns" / "产品化与平台工程" / "provider-abstraction-patterns.md",
        "productization-patterns": DOCS / "patterns" / "产品化与平台工程" / "productization-patterns.md",
    }
    pain_file_map = {
        "tool-result-context-overload": DOCS / "pain-points" / "tool-result-context-overload.md",
        "mcp-ecosystem-governance": DOCS / "pain-points" / "mcp-ecosystem-governance.md",
        "memory-context-staleness-and-bloat": DOCS / "pain-points" / "memory-context-staleness-and-bloat.md",
        "runtime-recovery-and-eval-gap": DOCS / "pain-points" / "runtime-recovery-and-eval-gap.md",
        "provider-differences-pollute-runtime": DOCS / "pain-points" / "行业共性痛点总纲.md",
        "agent-productization-gap": DOCS / "pain-points" / "agent-productization-gap.md",
        "project-learning-stays-as-notes": DOCS / "pain-points" / "行业共性痛点总纲.md",
    }

    pattern_impacts: list[dict[str, Any]] = []
    for target in pattern_targets:
        pattern_id = str(target.get("id") or "")
        target_path = pattern_file_map.get(pattern_id)
        if not target_path or not target_path.exists():
            continue
        practice = snippet(frameworks_detail, 500)
        action = actions[0] if actions else "把这个项目的做法映射成当前平台的可执行动作"
        append_or_replace_block(
            target_path,
            "## 自动回写补充",
            f"{source_project_id}-{pattern_id}",
            build_pattern_block(
                source_project_id=source_project_id,
                title=title,
                source=source,
                draft_file=draft_file or "unknown",
                reason=str(target.get("reason") or "自动映射"),
                evidence=snippet(problems_detail, 500),
                practice=practice,
                action=action,
            ),
        )
        pattern_impacts.append(
            {
                "id": pattern_id,
                "reason": str(target.get("reason") or "自动映射"),
                "evidence": snippet(problems_detail, 240),
                "practice": practice,
                "action": action,
                "targetFile": str(target_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )

    default_signals = normalize_lines(
        [
            f"关注项目 {title} 是否提供了工程证据，而不是只有概念。",
            f"关注 {title} 是否给出了可复用步骤、治理边界和后续动作。",
            f"后续可把 {title} 的动作项转成平台里的可验证指标或检查项。",
        ]
    )
    pain_impacts: list[dict[str, Any]] = []
    for target in pain_targets:
        pain_id = str(target.get("id") or "")
        target_path = pain_file_map.get(pain_id)
        if not target_path or not target_path.exists():
            continue
        action = actions[0] if actions else "把这个项目里的做法转成当前平台下一步动作"
        append_or_replace_block(
            target_path,
            "## 自动回写补充",
            f"{source_project_id}-{pain_id}",
            build_pain_block(
                source_project_id=source_project_id,
                title=title,
                reason=str(target.get("reason") or "自动映射"),
                evidence=snippet(problems_detail, 500),
                practice=snippet(frameworks_detail or principles_detail, 500),
                signals=default_signals,
                action=action,
            ),
        )
        pain_impacts.append(
            {
                "id": pain_id,
                "reason": str(target.get("reason") or "自动映射"),
                "evidenceProject": title,
                "practice": snippet(frameworks_detail or principles_detail, 240),
                "signals": default_signals,
                "action": action,
                "targetFile": str(target_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )

    interview_items = build_interview_items(
        source_project_id=source_project_id,
        title=title,
        one_line=one_line,
        why=why,
        scenario=scenario,
        problems=problems,
        frameworks=frameworks,
        principles=principles,
        actions=actions,
        related_patterns=[item["id"] for item in pattern_impacts],
        pain_points=[item["id"] for item in pain_impacts],
    )
    for interview_item in interview_items:
        merge_interview_bank(interview_item)
    interview_path = INTERVIEW_WRITEBACK_BANK
    writeback_targets = {
        "patterns": [item["id"] for item in pattern_impacts],
        "painPoints": [item["id"] for item in pain_impacts],
        "interviews": [item["id"] for item in interview_items],
    }
    writeback_reasoning = merge_unique_texts(
        [str(item.get("reason") or "") for item in pattern_impacts],
        [str(item.get("reason") or "") for item in pain_impacts],
        limit=8,
    )
    status = "completed"
    if not pattern_impacts and not pain_impacts and not interview_items:
        status = "skipped"
    elif not pattern_impacts or not pain_impacts:
        status = "partial"
    timestamp = now_text()

    package = {
        "sourceProjectId": source_project_id,
        "sourceTitle": title,
        "sourceRepo": str(project.get("repo") or ""),
        "sourceFile": draft_file,
        "source": source,
        "createdAt": timestamp,
        "updatedAt": timestamp,
        "writebackStatus": status,
        "projectSummary": {
            "oneLine": one_line,
            "whyWorthStudying": why,
            "coreScenario": scenario,
        },
        "generalProblems": {
            "summary": problems,
            "detail": problems_detail,
        },
        "solutionPatterns": pattern_impacts,
        "painPointLinks": pain_impacts,
        "interviewAngles": [
            {
                "questionType": item.get("questionType", ""),
                "prompt": item.get("rawQuestion", ""),
                "answer": item.get("recommendedAnswer", ""),
                "followUps": item.get("followUps", []),
                "evidenceSource": item.get("evidenceSource", title),
            }
            for item in interview_items
        ],
        "patterns": pattern_impacts,
        "painPoints": pain_impacts,
        "interviews": interview_items,
        "currentActions": actions,
        "writebackTargets": writeback_targets,
        "writebackReasoning": writeback_reasoning,
        "writebackSummary": f"已把 {title} 的沉淀结果回写到 {len(pattern_impacts)} 个 patterns、{len(pain_impacts)} 个 pain-points，并生成 {len(interview_items)} 条面试资产。",
    }
    package_path = persist_writeback_package(package)
    index_result = run_build_index() if rebuild_index else {"ok": True, "command": "", "stdout": "", "stderr": "", "returncode": 0}
    return {
        "status": "ok",
        "packageFile": str(package_path),
        "patternFiles": [item["targetFile"] for item in pattern_impacts],
        "painPointFiles": [item["targetFile"] for item in pain_impacts],
        "interviewFile": str(interview_path),
        "writebackSummary": package["writebackSummary"],
        "writebackStatus": status,
        "writebackUpdatedAt": timestamp,
        "writebackTargets": writeback_targets,
        "writebackReasoning": writeback_reasoning,
        "indexCommand": index_result["command"],
        "indexOk": index_result["ok"],
    }


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "KnowledgePlatformBridge/1.0"

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(
                200,
                {
                    "status": "ok",
                    "service": "knowledge-platform-bridge",
                    "time": now_text(),
                    "port": self.server.server_address[1],
                },
            )
            return
        self._send_json(404, {"status": "error", "message": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
            if parsed.path == "/api/distill":
                result = handle_distill(payload)
                self._send_json(200, result)
                return
            if parsed.path == "/api/ingest-repo":
                result = run_ingest(payload)
                preview = {
                    "summary": (result.get("summary") or "")[:1200],
                    "tree": (result.get("tree") or "")[:2000],
                }
                self._send_json(
                    200,
                    {
                        "status": "ok",
                        "message": "仓库理解完成",
                        "source": result.get("source"),
                        "ingestSource": result.get("ingest_source"),
                        "outputFile": result.get("output_file"),
                        "summaryLength": result.get("summary_length"),
                        "treeLength": result.get("tree_length"),
                        "contentLength": result.get("content_length"),
                        "preview": preview,
                    },
                )
                return
            if parsed.path == "/api/analyze-project":
                result = handle_analyze_project(payload)
                self._send_json(200, result)
                return
            if parsed.path == "/api/writeback-analysis":
                result = build_analysis_writeback(payload)
                self._send_json(200, result)
                return
            self._send_json(404, {"status": "error", "message": "Not found"})
        except ValueError as exc:
            self._send_json(400, {"status": "error", "message": str(exc)})
        except RuntimeError as exc:
            self._send_json(500, {"status": "error", "message": str(exc)})
        except Exception as exc:  # noqa: BLE001
            self._send_json(500, {"status": "error", "message": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("请求体不是合法 JSON") from exc
        if not isinstance(data, dict):
            raise ValueError("请求体必须是 JSON object")
        return data

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    ensure_dirs()
    port = int(os.environ.get("KNOWLEDGE_PLATFORM_BRIDGE_PORT", str(DEFAULT_PORT)))
    server = ThreadingHTTPServer(("127.0.0.1", port), BridgeHandler)
    print(f"Knowledge platform bridge listening on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
