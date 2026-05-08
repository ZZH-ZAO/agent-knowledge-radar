#!/usr/bin/env python3
"""
Append the new industry-pain-point research structure to existing docs.

The goal is to make older docs match the user's current target shape:
industry pain -> evidence sources -> mature practices -> data signals ->
inspiration -> actions -> evolution rule.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [
    ROOT / "docs" / "external-projects",
    ROOT / "docs" / "patterns",
    ROOT / "docs" / "source-research",
    ROOT / "docs" / "platform",
    ROOT / "docs" / "project-radar",
    ROOT / "docs" / "interviews",
    ROOT / "docs" / "pain-points",
    ROOT / "docs" / "source-library",
    ROOT / "docs" / "templates",
    ROOT / "docs" / "legacy-migration",
]


PROFILES = [
    (
        ["mcp", "tool", "工具", "browser", "devtools"],
        {
            "pain": "Agent 接入外部工具后，行业共性痛点是权限、结果大小、执行副作用、工具质量和可观测性会同时失控。优秀项目不会把工具当普通函数，而会把它放进 Tool Runtime / MCP Integration 的治理管线。",
            "sources": "GitHub 工具型项目、MCP server、旧体系工具文档、源码 README、浏览器自动化案例。",
            "practice": "共性做法是 Tool Registry + Permission Mapping + Result Summary + Artifact Reference + Audit Trail，把调用、权限、结果和追踪拆开治理。",
            "signals": "可观察信号包括工具数量、权限等级覆盖率、单次结果 token 数、artifact 引用比例、失败调用可复现率。",
            "action": "把该文档关联到 Tool Runtime / MCP 行业痛点，并检查是否能补充工具权限、结果治理或审计行动项。",
        },
    ),
    (
        ["memory", "context", "上下文", "记忆"],
        {
            "pain": "长链路 Agent 的行业共性痛点是上下文会膨胀、记忆会过期、历史会污染当前任务。问题本质不是存更多内容，而是治理作用域、生命周期、召回和注入。",
            "sources": "长运行 Agent 项目、Memory 系统设计、旧体系会话文档、RAG 和上下文工程资料。",
            "practice": "共性做法是 Scope + Lifecycle + Storage + Retrieval + Injection + Freshness Check，把记忆从聊天记录升级成可治理资产。",
            "signals": "可观察信号包括重复读取次数、上下文截断次数、过期记忆命中率、任务恢复成功率。",
            "action": "把该文档关联到 Memory / Context 行业痛点，并补充记忆分层、刷新和注入规则。",
        },
    ),
    (
        ["provider", "model", "模型", "多模型"],
        {
            "pain": "多模型系统的行业共性痛点是 provider 的能力、事件、错误、价格和上下文限制不同，差异会渗透业务代码，污染 Agent Runtime。",
            "sources": "多 provider Agent 项目、模型平台文档、产品化案例、旧体系 provider 分析。",
            "practice": "共性做法是 Provider Interface + Capability Metadata + Event Normalizer + Config Layer，把厂商差异隔离在适配层。",
            "signals": "可观察信号包括 provider 分支数量、能力声明覆盖率、模型替换改动范围、provider-specific bug 数。",
            "action": "把该文档关联到 Provider Abstraction 行业痛点，并补充能力声明、事件归一化和配置边界。",
        },
    ),
    (
        ["frontend", "design", "视觉", "ui", "gpt-image"],
        {
            "pain": "AI 生成前端的行业共性痛点是风格漂移、中文长文本溢出、生成图和真实 DOM 脱节，以及设计规则无法复用。",
            "sources": "前端风格项目、AI UI 生成项目、DESIGN.md、截图对照经验、旧体系前端设计文档。",
            "practice": "共性做法是 DESIGN.md + UI Mockup + React/CSS Implementation + Screenshot Review + Rule Feedback，把审美要求变成可执行工程规则。",
            "signals": "可观察信号包括页面风格不一致次数、中文溢出问题数、截图回归问题数、设计规则覆盖率。",
            "action": "把该文档关联到 Frontend Design Control 行业痛点，并把可复用视觉规则回写 DESIGN.md。",
        },
    ),
    (
        ["interview", "面经", "八股", "面试"],
        {
            "pain": "面试准备的共性痛点是知识和项目脱节：八股会背，但不能结合项目、外部证据、trade-off 和行动项回答。",
            "sources": "用户面经、旧知识库、项目沉淀、patterns、面试官追问记录。",
            "practice": "共性做法是把每道题转成定义问题、项目实践、外部证据、取舍边界、追问链和薄弱点记忆。",
            "signals": "可观察信号包括题目覆盖率、项目关联率、追问命中率、薄弱点重复出现次数。",
            "action": "把该文档关联到面试官自动进化流程，并补充可追问问题、推荐回答和薄弱点更新规则。",
        },
    ),
    (
        ["radar", "source", "资料", "沉淀", "知识", "project"],
        {
            "pain": "项目学习的行业共性痛点是资料很多但难以转化：收藏链接、摘要功能、缺少证据和行动项，最终不能反哺自己的项目。",
            "sources": "GitHub、优质博客、论文、用户文档、旧体系沉淀、Project Radar 候选池。",
            "practice": "共性做法是 Source Intake + Scoring + Candidate Pool + Distillation + Pain Point Update + Pattern Update，把资料源接进知识进化闭环。",
            "signals": "可观察信号包括资料源数量、进入深度沉淀比例、每个痛点证据来源数、patterns 更新次数、行动项完成率。",
            "action": "把该文档关联到资料源自动进化流程，并检查它能否补强某个行业痛点或 pattern。",
        },
    ),
]

DEFAULT_PROFILE = {
    "pain": "这里对应的行业共性痛点是：大模型和 Agent 项目复杂度上升后，单点功能无法解决长期学习、治理、验证和产品化问题。",
    "sources": "GitHub 项目、优质博客、论文、用户文档、旧体系沉淀和当前项目实践。",
    "practice": "共性做法是先识别行业痛点，再收集证据，再抽象成熟做法，最后转成当前项目行动项。",
    "signals": "可观察信号包括证据来源数量、关联项目数量、关联 patterns 数量、行动项数量和后续更新次数。",
    "action": "把该文档补充到行业痛点、patterns 或资料源自动进化流程中，避免停留在静态笔记。",
}


def profile_for(path: Path, text: str) -> dict[str, str]:
    key = f"{path.as_posix().lower()} {text[:4000].lower()}"
    for keywords, profile in PROFILES:
        if any(keyword.lower() in key for keyword in keywords):
            return profile
    return DEFAULT_PROFILE


def title_for(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def append_industry_section(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "## 行业痛点研究版补充" in text:
        return False
    profile = profile_for(path, text)
    title = title_for(path, text)
    addition = f"""

## 行业痛点研究版补充

> 目标：把“{title}”从单篇资料或单个项目笔记，升级成能服务行业痛点研究、优秀做法抽象和当前项目行动的学习资产。

### 1. 它对应的行业痛点

{profile["pain"]}

判断它是不是值得持续沉淀，不看它是否新奇，而看它能不能解释一个反复出现的行业问题，并能不能给当前项目带来可执行改变。

### 2. 可作为证据的来源类型

{profile["sources"]}

后续如果新增 GitHub、优质博客、论文或你提供的文档，都应该先判断它能否补强这一类证据，而不是直接堆进知识库。

### 3. 优秀项目或资料的共性做法

{profile["practice"]}

这里真正要学的不是表层功能名，而是成熟项目如何划分边界、控制风险、组织证据、形成可复用流程。

### 4. 数据支撑与判断信号

{profile["signals"]}

这些信号用于避免主观判断。后续平台应该让痛点页自动展示证据项目数、来源类型、关联方案数和行动项数量。

### 5. 给当前项目的启发

这份文档应该反哺 `claude-code-sourcemap` 的三个位置：

- 项目页：说明它作为样本值得学习什么。
- 痛点页：说明它补强了哪个 Agent / 大模型行业共性问题。
- 方案页：说明它能沉淀成什么可迁移框架。

### 6. 当前项目行动项

- [ ] {profile["action"]}
- [ ] 检查它是否需要更新 `docs/pain-points/` 的行业痛点说明。
- [ ] 检查它是否需要更新 `docs/patterns/` 的通用技术框架。
- [ ] 如果它来自外部资料，把它登记到 `docs/source-library/` 或 Project Radar 候选池。

### 7. 自动进化规则

每次新增相关资料后，按以下顺序更新：

```text
资料源
  -> 行业痛点
  -> 证据项目/资料
  -> 共性做法
  -> 数据支撑
  -> 当前项目行动项
  -> 面试官追问
```
"""
    path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed: list[Path] = []
    for root in TARGET_DIRS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            if append_industry_section(path):
                changed.append(path)
    print(f"Updated {len(changed)} docs")
    for path in changed:
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
