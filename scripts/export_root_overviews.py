#!/usr/bin/env python3
"""Generate root-level Chinese overview files for development progress and follow-up actions."""

from __future__ import annotations

import re
from pathlib import Path

from followup_actions import DEFAULT_INDEX, DEFAULT_MARKDOWN, load_index, render_markdown_zh


REPO_ROOT = Path(__file__).resolve().parents[1]
INTERNAL_REPORT = (
    REPO_ROOT
    / ".claude"
    / "docs"
    / "user"
    / "claude-code-sourcemap"
    / "workbench-development-report.md"
)
ROOT_DEV_REPORT = REPO_ROOT / "DEVELOPMENT-REPORT.md"

PHASE_TITLE_ZH = {
    "Autonomous Execution Rule And Reporting Standard": "持续执行规则与阶段报告标准",
    "Core Skill Feedback Loop Upgrade": "核心技能反馈回路升级",
    "Skill Library Entry Map": "技能库统一入口",
    "Session Promotion Traceability": "Session 反哺追踪",
    "Workbench Navigation Reinforcement": "工作台导航补强",
    "Followup Actions Unified View": "Follow-up 统一检索视图",
    "Root Follow-up Overview": "根目录 Follow-up 总览页",
    "Follow-up Status Layering": "Follow-up 状态分层",
    "Root Chinese Auto-Generated Overviews": "根目录中文自动总览",
    "Root Overview Localization Hardening": "根目录总览中文化加固",
    "Session Promotion Review Guardrail": "Session 反哺审核护栏",
    "Session Archive Audit View": "Session 归档巡检视图",
    "Case Advice Entry Point": "案例建议入口",
    "Awesome AI Research Writing Case Intake": "awesome-ai-research-writing 案例沉淀",
    "Research Writing Cheatsheet Extraction": "科研写作速查表抽取",
    "Research Writing Task Router": "科研写作任务路由器",
    "Research Writing Starter Template Library": "科研写作起手模板库",
    "Browser Harness Web Intake": "browser-harness 网页归档接入",
}

PHASE_GOAL_ZH = {
    "Autonomous Execution Rule And Reporting Standard": "把持续执行和阶段报告固化成默认工作方式。",
    "Core Skill Feedback Loop Upgrade": "把核心 Agent 技能升级成可反哺、可演进的方法资产。",
    "Skill Library Entry Map": "给技能库增加统一入口和路由说明。",
    "Session Promotion Traceability": "让 session 归档能追踪它反哺了哪些 skills、memory 和 docs。",
    "Workbench Navigation Reinforcement": "把 workbench 关键资产接入现有索引，提升可发现性。",
    "Followup Actions Unified View": "把 follow-up 从散落的 JSON 字段变成统一可检索视图。",
    "Root Follow-up Overview": "让根目录直接可见 follow-up 总览，而不是只能跑命令查看。",
    "Follow-up Status Layering": "让 follow-up 支持待处理、已完成、待确认三类状态。",
    "Root Chinese Auto-Generated Overviews": "把根目录两个总览文件改成中文自动生成版本。",
    "Root Overview Localization Hardening": "修正导出链路中的乱码与中英混杂问题，让根目录总览稳定输出可读中文。",
    "Session Promotion Review Guardrail": "把 session 反哺检查从软约定升级成结构化归档护栏，让每次归档都留下显式审核证据。",
    "Session Archive Audit View": "增加一个轻量巡检命令，用来统一扫描 session 归档是否满足当前护栏要求。",
    "Case Advice Entry Point": "增加一个轻量建议入口，把案例库直接转成面向新项目问题的可回链建议。",
    "Awesome AI Research Writing Case Intake": "把 awesome-ai-research-writing 作为知识资产型案例沉淀进工作台，并扩展相应的案例路由能力。",
    "Research Writing Cheatsheet Extraction": "把上游大 README 抽成可直接使用的中文科研写作速查表，减少未来重复查阅成本。",
    "Research Writing Task Router": "把科研写作案例从被动参考升级成可执行入口，让自然语言任务能直接映射到 prompt 或 skill 路线。",
    "Research Writing Starter Template Library": "给科研写作路由再补一层可复制的起手话术模板，减少每次从零组织请求的成本。",
    "Browser Harness Web Intake": "把 browser-harness 以网页证据方式沉淀进案例库，即使当前会话无法本地克隆，也先保留其可复用的浏览器基座设计经验。",
}

STATUS_ZH = {
    "verified": "已验证",
    "complete": "已完成",
    "completed": "已完成",
    "in progress": "进行中",
    "pending": "待处理",
    "needs-confirmation": "待确认",
}

PROGRESS_ZH = {
    "autonomous execution skill, report template, and stable memory rule have all been created and updated": "autonomous execution skill、阶段报告模板和稳定 memory 规则都已创建并更新。",
    "all 4 core skills have been updated with reusable metadata and case feedback sections": "4 个核心技能都已补齐可复用元数据和案例反馈区块。",
    "a root `README.md` has been added under `.claude/skills/`": "`.claude/skills/` 下已经增加根级 `README.md` 入口。",
    "workflow, template, registration script, Hermes session entry, and `index.json` have all been updated and verified": "工作流文档、模板、注册脚本、Hermes session 条目和 `index.json` 都已更新并验证。",
    "shared and case-local navigation docs have been updated to expose the workbench assets": "共享导航文档和案例本地导航文档都已更新，workbench 资产已经暴露出来。",
    "`scripts/followup_actions.py` has been created, connected to the workflow doc, and verified with default and project-specific queries": "`scripts/followup_actions.py` 已创建并接入工作流文档，还完成了默认查询和按项目查询验证。",
    "the script now writes a root Markdown overview, and `FOLLOWUP-ACTIONS.md` has been generated and verified": "脚本现在可以写出根目录 Markdown 总览，`FOLLOWUP-ACTIONS.md` 已生成并验证。",
    "the schema, template, Hermes example, registration script, retrieval script, and root overview now support follow-up statuses, and status filters have been verified": "schema、模板、Hermes 示例、注册脚本、检索脚本和根目录总览现在都支持 follow-up 状态，而且状态过滤已验证通过。",
    "the export flow now generates both root overview files in Chinese, and the generated files have been verified through content anchors and timestamps": "导出流程现在可以生成两个中文根目录总览文件，并已通过内容锚点和时间戳完成验证。",
    "the root overview exporter and follow-up renderer have been rewritten with clean Chinese mappings, and both generated root files now stay readable and consistent": "根目录总览导出器与 follow-up 渲染器已经重写为干净的中文映射，两份根目录生成文件现在可读且一致。",
    "the workflow, template, registration script, and Hermes session example now all support a structured `promotion_review` guardrail": "工作流、模板、注册脚本和 Hermes session 示例现在都支持结构化 `promotion_review` 审核护栏。",
    "a dedicated `session_archive_audit.py` script now checks session archive guardrails, and the workflow doc includes it as part of the verification path": "专用的 `session_archive_audit.py` 脚本现在可以检查 session 归档护栏，工作流文档也已把它纳入验证路径。",
    "a dedicated `case_advisor.py` script now recommends skills, memory, shared docs, and matching historical cases with explicit evidence signals": "专用的 `case_advisor.py` 脚本现在可以推荐技能、memory、共享文档和匹配的历史案例，并给出明确依据。",
    "the awesome-ai-research-writing case has been cloned, analyzed, archived into docs and sessions, and added as a knowledge-asset reference in the case library": "awesome-ai-research-writing 已完成克隆、分析、归档，并作为知识资产型参考案例加入案例库。",
    "a Chinese quick-reference page has been extracted from the upstream README, linked into the case folder, and added to the archived derived docs": "已经从上游 README 抽出中文速查页，接入案例目录，并加入归档产物列表。",
    "a dedicated `research_writing_router.py` entry point now maps writing task sentences to prompt and skill routes with supporting case docs": "专用的 `research_writing_router.py` 入口现在可以把写作任务句子映射到 prompt 和 skill 路线，并带出支撑案例文档。",
    "a dedicated starter-template script and Chinese template-library doc now provide copyable first-message scaffolds for common research-writing tasks": "已经补齐专用起手模板脚本和中文模板库文档，可直接提供常见科研写作任务的可复制首条消息。",
    "browser-harness has been archived through web analysis, linked into the case library, prepared for session registration, and added to the case-advice retrieval metadata": "browser-harness 已通过网页分析完成归档，已接入案例库、补齐 session 归档准备，并进入案例建议检索元数据。",
}

REMAINING_ZH = {
    "apply the reporting rule to ongoing workbench upgrade phases": "把这套报告规则继续应用到后续 workbench 升级阶段。",
    "optionally extend the same structure to secondary skills and add a shared skills index if the library grows further": "如果技能库继续扩张，可以再把同样的结构扩展到次级技能，并补更完整的共享索引。",
    "optionally link this map from other top-level indexes if cross-entry navigation becomes more important": "如果跨入口导航变得更重要，可以把这个技能地图再链接到更多顶层索引。",
    "none for this phase": "本阶段暂时无剩余事项。",
    "keep follow-up fields maintained as new sessions are archived": "后续新增 session 归档时，继续维护 follow-up 字段。",
    "refresh the root view whenever follow-up data changes": "每次 follow-up 数据变化后，重新刷新根目录视图。",
    "keep new follow-up items maintained with explicit statuses": "后续新增 follow-up 时，继续保持显式状态字段。",
    "re-run the export script whenever the internal report or session index changes": "每次内部报告或 session 索引发生变化后，重新执行导出脚本。",
    "use the cleaned exporter as the default refresh path for future root overview updates": "后续根目录总览更新时，统一使用清理后的导出器作为默认刷新入口。",
    "backfill the same structure into future sessions by default as new archive entries are created": "后续新增 session 归档时，默认沿用同样的结构化审核字段。",
    "extend the same audit if future archive rules add more required cross-checks": "如果后续归档规则继续增加，再把相同的巡检逻辑扩展进去。",
    "improve suggestion quality further as more case entries and richer metadata are added": "随着案例条目和元数据继续丰富，再进一步提升建议质量。",
    "reuse this case when future tasks involve prompt libraries, skill onboarding, or knowledge-asset packaging": "后续遇到 prompt 资源库、skill 上手指南或知识资产打包类项目时，优先复用这个案例。",
    "reuse this extraction pattern when future knowledge repositories deserve a direct-use cheat sheet": "后续遇到值得直接使用的知识仓库时，继续复用这种速查表抽取模式。",
    "extend the route dictionary if future writing workflows reveal missing task patterns": "如果后续写作工作流暴露新的任务模式，再继续扩展路由词典。",
    "add more scenario templates if future usage reveals gaps between route selection and practical invocation": "如果后续使用中发现路由和真实调用之间还有空档，再继续补充更多场景模板。",
    "retry a local clone and add a source-code-deep pass when GitHub connectivity becomes available": "等 GitHub 连通性恢复后，补做一次本地克隆和源码级深挖分析。",
}


def extract_section(block: str, heading: str) -> str:
    pattern = rf"^### {re.escape(heading)}\n\n(.*?)(?=^### |\Z)"
    match = re.search(pattern, block, flags=re.M | re.S)
    return match.group(1).strip() if match else ""


def extract_status_fields(block: str) -> dict[str, str]:
    section = extract_section(block, "Current Status")
    result = {"status": "", "progress": "", "remaining": ""}
    if not section:
        return result
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Status:"):
            result["status"] = stripped.split(":", 1)[1].strip().strip("`")
        elif stripped.startswith("- Progress:"):
            result["progress"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Remaining:"):
            result["remaining"] = stripped.split(":", 1)[1].strip()
    return result


def parse_internal_report(text: str) -> list[dict[str, str]]:
    matches = list(re.finditer(r"^## Phase: (.+)$", text, flags=re.M))
    phases: list[dict[str, str]] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        goal = extract_section(block, "Goal")
        status_fields = extract_status_fields(block)
        phases.append(
            {
                "title_en": title,
                "title_zh": PHASE_TITLE_ZH.get(title, title),
                "goal": goal,
                **status_fields,
            }
        )
    return phases


def translate_status(text: str) -> str:
    return STATUS_ZH.get(text, text or "其他")


def translate_goal(phase: dict[str, str]) -> str:
    return PHASE_GOAL_ZH.get(phase["title_en"], phase["goal"])


def translate_progress(text: str) -> str:
    return PROGRESS_ZH.get(text, text)


def translate_remaining(text: str) -> str:
    return REMAINING_ZH.get(text, text)


def build_dev_report_markdown(phases: list[dict[str, str]]) -> str:
    counts = {"已验证": 0, "已完成": 0, "进行中": 0, "其他": 0}
    for phase in phases:
        zh_status = translate_status(phase["status"])
        if zh_status in counts:
            counts[zh_status] += 1
        else:
            counts["其他"] += 1

    lines = [
        "# 开发记录总览",
        "",
        "## 说明",
        "",
        "- 项目：`claude-code-sourcemap`",
        f"- 自动生成来源：`{INTERNAL_REPORT}`",
        "- 用途：在仓库根目录提供便于快速阅读的中文开发进度总览",
        "",
        "## 当前统计",
        "",
        f"- 阶段总数：`{len(phases)}`",
        f"- 已验证：`{counts['已验证']}`",
        f"- 已完成：`{counts['已完成']}`",
        f"- 进行中：`{counts['进行中']}`",
        "",
        "## 阶段概览",
        "",
    ]

    for idx, phase in enumerate(phases, start=1):
        lines.extend(
            [
                f"### 阶段 {idx}：{phase['title_zh']}",
                "",
                f"- 当前状态：`{translate_status(phase['status'])}`",
                f"- 英文阶段名：`{phase['title_en']}`",
            ]
        )
        goal_text = translate_goal(phase)
        if goal_text:
            lines.append(f"- 目标摘要：{goal_text}")
        if phase["progress"]:
            lines.append(f"- 当前进度：{translate_progress(phase['progress'])}")
        if phase["remaining"]:
            lines.append(f"- 剩余事项：{translate_remaining(phase['remaining'])}")
        lines.append("")

    lines.extend(
        [
            "## 详细记录入口",
            "",
            f"- 内部长报告：`{INTERNAL_REPORT}`",
            f"- 根目录 follow-up 总览：`{DEFAULT_MARKDOWN}`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    report_text = INTERNAL_REPORT.read_text(encoding="utf-8")
    phases = parse_internal_report(report_text)
    ROOT_DEV_REPORT.write_text(
        build_dev_report_markdown(phases) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    index_data = load_index(DEFAULT_INDEX)
    entries = index_data["entries"]
    DEFAULT_MARKDOWN.write_text(
        render_markdown_zh(entries, DEFAULT_INDEX) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"development_report: {ROOT_DEV_REPORT}")
    print(f"followup_overview: {DEFAULT_MARKDOWN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
