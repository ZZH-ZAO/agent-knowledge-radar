#!/usr/bin/env python3
"""Print copyable starter prompts for common research-writing tasks."""

from __future__ import annotations

import argparse


TEMPLATES = {
    "english-abstract-polish": {
        "label": "英文摘要润色",
        "best_for": "已经有英文摘要，想让它更像顶会论文语言。",
        "starter": """请帮我润色下面这段英文摘要，让它更像顶会论文风格。

目标会议：
当前最担心的问题：
希望保留的核心贡献句：

英文摘要：
<把你的摘要贴在这里>
""",
    },
    "zh-to-en-paper-paragraph": {
        "label": "中文草稿转英文论文段落",
        "best_for": "先用中文写清逻辑，再转成英文论文表达。",
        "starter": """请把下面这段中文草稿改写成适合论文正文的英文段落。

目标会议：
是否保留 LaTeX 公式：是 / 否
语气要求：更学术 / 更简洁 / 更像 introduction / 更像 methods

中文草稿：
<把你的中文草稿贴在这里>
""",
    },
    "logic-check": {
        "label": "逻辑检查",
        "best_for": "担心段落逻辑跳跃、论证不严、主张和证据不匹配。",
        "starter": """请从逻辑严谨性角度检查下面这段论文内容。

我最担心的问题：
这段内容属于：abstract / introduction / methods / experiments / conclusion

待检查内容：
<把段落贴在这里>
""",
    },
    "reviewer-pass": {
        "label": "Reviewer 视角审视",
        "best_for": "想用审稿人的视角先挑刺。",
        "starter": """请从 reviewer 视角审视下面这篇论文内容，并指出最关键的问题。

目标会议：
你要重点关注：贡献是否清楚 / 实验是否充分 / 逻辑是否成立 / 表达是否严谨

内容：
<贴摘要、章节或整篇 PDF 的文字内容>
""",
    },
    "paper-from-repo": {
        "label": "从 repo 起草论文",
        "best_for": "已经有代码仓库和实验结果，想生成论文骨架或初稿。",
        "starter": """请基于这个 repo 帮我起草一篇论文。

repo 路径：
实验结果目录：
目标会议：
一句话核心贡献：
我希望先产出：论文骨架 / abstract / introduction / 全文初稿
""",
    },
    "template-setup": {
        "label": "按会议模板起稿",
        "best_for": "想按 NeurIPS / ICLR / ICML 模板开新稿，或迁移已有稿件。",
        "starter": """请帮我按目标会议模板起稿。

目标会议：
新稿目录：
如果是迁移已有稿件，请提供当前稿件路径：
我希望先完成：模板工程 / 标题作者占位 / 章节骨架 / 正文迁移
""",
    },
    "related-work": {
        "label": "补引用 / 写 Related Work",
        "best_for": "需要整理相关工作、补关键引用、形成可直接写进论文的 related work。",
        "starter": """请帮我补引用并整理 Related Work。

主题：
想重点对比的方法：
时间范围要求：
目标会议：
如果已有草稿，请贴在下面：
<Related Work 草稿>
""",
    },
    "doc-coauthoring": {
        "label": "按章节协作写作",
        "best_for": "想围绕某一章分阶段澄清、起草、迭代。",
        "starter": """请用协作写作模式帮我完成这一章。

章节名称：
目标读者：
当前已有材料：
我最不确定的点：
我希望你先做：澄清问题 / 章节骨架 / 第一版草稿
""",
    },
    "humanize": {
        "label": "去 AI 味",
        "best_for": "逻辑基本没问题，但语言太像 AI 写的。",
        "starter": """请帮我去掉下面这段文字的 AI 味，让它更自然，但不要改变原意。

当前文本类型：LaTeX 英文 / Word 中文
我希望保留的语气：

文本：
<把内容贴在这里>
""",
    },
    "word-docx": {
        "label": "Word 模板 / 修订痕迹处理",
        "best_for": "要处理 .docx 模板、修订模式、期刊格式。",
        "starter": """请帮我处理这份 Word 论文文档。

任务类型：套模板 / 替换占位内容 / 带修订痕迹修改
文档路径：
目标期刊或模板要求：
我希望优先处理的部分：
""",
    },
    "figure-caption": {
        "label": "图、框架图、caption",
        "best_for": "要做方法图、框架图、概念图，或者给图写 caption。",
        "starter": """请帮我完成这张论文图的设计或 caption。

任务类型：框架图 / 方法图 / 概念图 / caption
图的用途：
图里必须包含的元素：
我想强调的对比点：
如果已有草图或说明，请贴在下面：
<图说明>
""",
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show copyable starter templates for research-writing tasks."
    )
    parser.add_argument(
        "--scenario",
        choices=sorted(TEMPLATES),
        help="Show one specific scenario template.",
    )
    return parser


def print_template(key: str, data: dict[str, str]) -> None:
    print(f"## {data['label']}")
    print()
    print(f"- scenario_id: {key}")
    print(f"- best_for: {data['best_for']}")
    print("- starter_text:")
    print("```text")
    print(data["starter"].rstrip())
    print("```")
    print()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print("# Research Writing Starters")
    print()
    if args.scenario:
        print_template(args.scenario, TEMPLATES[args.scenario])
        return 0

    for key, data in TEMPLATES.items():
        print_template(key, data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
