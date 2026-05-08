#!/usr/bin/env python3
"""Route research-writing tasks to prompts, skills, and supporting assets."""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = REPO_ROOT / ".claude" / "docs" / "user" / "awesome-ai-research-writing"
CASE_ANALYSIS = CASE_ROOT / "analysis.md"
CASE_BORROW = CASE_ROOT / "what-to-borrow-for-this-workbench.md"
CASE_CHEATSHEET = CASE_ROOT / "research-writing-skill-cheatsheet-zh.md"
CASE_README = CASE_ROOT / "README.md"

SKILL_20 = "20-ml-paper-writing"
SKILL_DOC_COAUTHORING = "doc-coauthoring"
SKILL_DOCX = "docx"
SKILL_HUMANIZER = "humanizer"
SKILL_CANVAS = "canvas-design"

PROMPT_ZH_TO_EN = "中转英"
PROMPT_EN_TO_ZH = "英转中"
PROMPT_ZH_TO_ZH = "中转中"
PROMPT_SHRINK = "缩写"
PROMPT_EXPAND = "扩写"
PROMPT_POLISH_EN = "英文论文润色"
PROMPT_POLISH_ZH = "中文论文润色"
PROMPT_LOGIC = "逻辑检查"
PROMPT_REVIEWER = "论文整体以 Reviewer 视角进行审视"
PROMPT_DEAI_LATEX = "去 AI 味（LaTeX 英文）"
PROMPT_DEAI_WORD = "去 AI 味（Word 中文）"

ROUTES = [
    {
        "id": "draft_from_repo",
        "label": "从 repo 起草论文",
        "keywords": {"repo", "仓库", "起稿", "起草", "论文初稿", "从零写论文", "写论文", "conference template"},
        "recommended": [f"Skill: {SKILL_20}"],
        "prepare": [
            "repo 路径",
            "实验结果目录或 results 摘要",
            "目标会议",
            "一句话核心贡献",
        ],
        "outputs": [
            "论文骨架",
            "章节初稿",
            "模板化会议稿目录",
        ],
    },
    {
        "id": "template_setup",
        "label": "按会议模板开新稿或迁移会模板",
        "keywords": {"模板", "neurips", "iclr", "icml", "acl", "aaai", "colm", "换会", "改投", "迁移模板"},
        "recommended": [f"Skill: {SKILL_20}"],
        "prepare": [
            "目标会议名称",
            "现有稿件路径（若是迁移）",
            "新稿放置目录",
        ],
        "outputs": [
            "新模板工程",
            "迁移后的稿件",
            "投稿前格式检查点",
        ],
    },
    {
        "id": "zh_to_en",
        "label": "中文草稿转英文论文段落",
        "keywords": {"中转英", "中文转英文", "翻成英文", "英文段落", "摘要翻译", "方法翻译", "写成英文"},
        "recommended": [f"Prompt: {PROMPT_ZH_TO_EN}", f"Prompt: {PROMPT_POLISH_EN}"],
        "prepare": [
            "中文草稿",
            "是否保留 LaTeX 公式",
            "目标语气或目标会议风格",
        ],
        "outputs": [
            "英文论文段落",
            "中文对照",
            "进一步可润色的英文版本",
        ],
    },
    {
        "id": "en_abstract_polish",
        "label": "英文摘要或英文段落润色",
        "keywords": {"英文摘要", "英文abstract", "abstract", "润色英文", "改英文", "顶会论文", "英文润色"},
        "recommended": [f"Prompt: {PROMPT_POLISH_EN}", f"Prompt: {PROMPT_LOGIC}"],
        "prepare": [
            "英文摘要或英文段落",
            "目标会议或目标语气",
            "如果有的话，当前最担心的问题",
        ],
        "outputs": [
            "更学术、更流畅的英文摘要",
            "逻辑或表达改进建议",
        ],
    },
    {
        "id": "en_to_zh",
        "label": "英文论文快速转中文理解",
        "keywords": {"英转中", "英文转中文", "看懂论文", "翻成中文", "latex 翻译"},
        "recommended": [f"Prompt: {PROMPT_EN_TO_ZH}"],
        "prepare": [
            "英文 LaTeX 片段",
        ],
        "outputs": [
            "中文直译说明",
        ],
    },
    {
        "id": "zh_polish",
        "label": "中文论文重写或润色",
        "keywords": {"中转中", "中文润色", "中文重写", "中文论文", "正式一点"},
        "recommended": [f"Prompt: {PROMPT_ZH_TO_ZH}", f"Prompt: {PROMPT_POLISH_ZH}"],
        "prepare": [
            "中文草稿",
            "零散要点或当前段落",
        ],
        "outputs": [
            "更正式、更连贯的中文论文段落",
        ],
    },
    {
        "id": "shrink_expand",
        "label": "英文段落缩写或扩写",
        "keywords": {"缩写", "压缩字数", "扩写", "补充一点", "写短一点", "写长一点"},
        "recommended": [f"Prompt: {PROMPT_SHRINK}", f"Prompt: {PROMPT_EXPAND}"],
        "prepare": [
            "英文 LaTeX 段落",
            "希望压缩或增强的重点",
        ],
        "outputs": [
            "缩写版或扩写版",
            "修改说明",
        ],
    },
    {
        "id": "logic_review",
        "label": "逻辑检查或审稿人视角挑刺",
        "keywords": {"逻辑", "审稿", "reviewer", "挑刺", "论证", "不严谨", "检查论文"},
        "recommended": [f"Prompt: {PROMPT_LOGIC}", f"Prompt: {PROMPT_REVIEWER}"],
        "prepare": [
            "目标段落、章节或全文 PDF",
            "目标会议（如果要审稿视角）",
        ],
        "outputs": [
            "逻辑问题清单",
            "审稿式意见",
            "修稿建议",
        ],
    },
    {
        "id": "related_work",
        "label": "补引用或写 Related Work",
        "keywords": {"related work", "补引用", "引文", "citation", "bibtex", "相关工作"},
        "recommended": [f"Skill: {SKILL_20}"],
        "prepare": [
            "主题关键词",
            "想对比的方法或论文",
            "目标会议或论文段落位置",
        ],
        "outputs": [
            "引用建议",
            "related work 草稿",
            "待核实的引用点",
        ],
    },
    {
        "id": "coauthoring",
        "label": "按阶段协作写章节",
        "keywords": {"协作写", "分阶段", "写一章", "introduction", "methods", "experiments", "章节"},
        "recommended": [f"Skill: {SKILL_DOC_COAUTHORING}"],
        "prepare": [
            "当前要写的章节",
            "上下文与已有材料",
            "不确定点",
        ],
        "outputs": [
            "澄清问题",
            "章节草稿",
            "读者测试后的改进建议",
        ],
    },
    {
        "id": "deai",
        "label": "去 AI 味或提高自然度",
        "keywords": {"去ai", "去 ai", "ai味", "ai 味", "humanize", "像人写的", "自然一点"},
        "recommended": [f"Skill: {SKILL_HUMANIZER}", f"Prompt: {PROMPT_DEAI_LATEX}", f"Prompt: {PROMPT_DEAI_WORD}"],
        "prepare": [
            "待修改段落或全文",
            "当前是 LaTeX 英文还是 Word 中文",
        ],
        "outputs": [
            "更自然的人类写作风格版本",
        ],
    },
    {
        "id": "word_docx",
        "label": "处理 Word 模板或修订痕迹",
        "keywords": {"word", "docx", "修订", "tracked changes", "模板文档", "期刊模板"},
        "recommended": [f"Skill: {SKILL_DOCX}"],
        "prepare": [
            ".docx 模板或现有文档",
            "要替换的标题、作者、摘要、正文内容",
        ],
        "outputs": [
            "符合模板的 Word 稿件",
            "带修订痕迹的修改结果",
        ],
    },
    {
        "id": "figure_diagram",
        "label": "生成框架图、概念图或方法图",
        "keywords": {"框架图", "概念图", "方法图", "figure", "caption", "图标题", "示意图", "canvas"},
        "recommended": [f"Skill: {SKILL_CANVAS}", f"Skill: {SKILL_20}"],
        "prepare": [
            "图的用途",
            "结构层次",
            "关键元素和想突出的对比点",
        ],
        "outputs": [
            ".png / .pdf 图",
            "caption 文案",
        ],
    },
]


def score_route(task: str, route: dict[str, object]) -> tuple[int, list[str]]:
    text = task.casefold()
    matched = [keyword for keyword in route["keywords"] if keyword.casefold() in text]
    return len(matched), sorted(matched)


def choose_routes(task: str, limit: int) -> list[tuple[int, list[str], dict[str, object]]]:
    scored = []
    for route in ROUTES:
        score, matched = score_route(task, route)
        if score > 0:
            scored.append((score, matched, route))
    scored.sort(key=lambda item: (-item[0], str(item[2]["label"])))
    if scored:
        return scored[:limit]
    fallback = next(route for route in ROUTES if route["id"] == "draft_from_repo")
    return [(0, [], fallback)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Route a research-writing task to the best prompt/skill path."
    )
    parser.add_argument(
        "--task",
        required=True,
        help="A natural-language research-writing task, such as '我要改英文摘要' or '帮我按 NeurIPS 模板起稿'.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum number of route suggestions to show. Default: 3",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    results = choose_routes(args.task, args.limit)

    print("# Research Writing Route")
    print()
    print(f"- task: {args.task}")
    print(f"- quick_reference: {CASE_CHEATSHEET}")
    print(f"- case_readme: {CASE_README}")
    print()

    print("## Suggested Routes")
    for idx, (score, matched, route) in enumerate(results, start=1):
        print(f"### Route {idx}: {route['label']}")
        print()
        print(f"- matched_keywords: {', '.join(matched) if matched else 'fallback'}")
        print(f"- confidence: {'high' if score >= 2 else 'medium' if score == 1 else 'fallback'}")
        print("- recommended_assets:")
        for item in route["recommended"]:
            print(f"  - {item}")
        print("- prepare_inputs:")
        for item in route["prepare"]:
            print(f"  - {item}")
        print("- expected_outputs:")
        for item in route["outputs"]:
            print(f"  - {item}")
        print("- supporting_case_docs:")
        print(f"  - {CASE_ANALYSIS}")
        print(f"  - {CASE_CHEATSHEET}")
        print(f"  - {CASE_BORROW}")
        print()

    print("## Usage Hint")
    print("- 如果你已经知道自己要处理的是一小段文本，优先走 Prompt。")
    print("- 如果任务跨 repo、模板、章节或 Word 文件，优先走 Skill。")
    print("- 如果还拿不准，先读速查表，再回看案例分析。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
