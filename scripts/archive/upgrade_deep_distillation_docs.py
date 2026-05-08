#!/usr/bin/env python3
"""
Upgrade existing distillation docs with interview-knowledge-base style sections.

This is intentionally conservative: it does not replace the original distillation.
It appends a "深度学习版补充" section to docs that have not already been upgraded.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [
    ROOT / "docs" / "external-projects",
    ROOT / "docs" / "patterns",
    ROOT / "docs" / "source-research",
    ROOT / "docs" / "platform",
]


PROFILE_BY_KEYWORD = [
    (
        ["tool-runtime", "mcp", "chromedevtools", "工具"],
        {
            "exam": "这里真正考察的不是会不会调用一个 API，而是能不能把 Agent 对外部世界的行动放进可治理的执行管线。",
            "answer": "我会把工具调用理解成 Agent Runtime 的行动边界。成熟系统不能只关心函数能不能执行，还要关心输入协议、权限分级、执行隔离、结果压缩、错误恢复和审计回放。否则模型一旦误调工具，风险会直接落到真实文件、浏览器、网络或业务系统上。",
            "mistake": "把 MCP 或 Tool Calling 当成普通 API wrapper，只写 schema，不写权限、结果治理和失败恢复。",
            "tradeoff": "治理越完整，接入成本越高；但如果工具有副作用，前期省掉治理，后期会以安全事故、上下文爆炸和不可复现的形式还回来。",
            "action": "给每个工具补齐 riskLevel、permission、resultPolicy、auditTrail，并在平台中把相关项目和工具治理 pattern 关联起来。",
        },
    ),
    (
        ["memory", "context", "上下文", "记忆"],
        {
            "exam": "这里考察的是能不能把长链路任务里的上下文当成工程资源管理，而不是把所有历史都塞给模型。",
            "answer": "我会把 Memory 理解成上下文治理系统，而不是聊天记录。它至少要解决作用域、生命周期、存储、召回、注入和隐私边界。真正有价值的记忆不是越多越好，而是能在正确时间召回正确证据，并减少重复读取和重复推理。",
            "mistake": "把 memory 做成无差别追加日志，导致上下文越来越大、旧信息污染新任务。",
            "tradeoff": "记忆越结构化，维护成本越高；但没有结构化，模型长期任务会反复读取、遗忘关键约束，甚至引用过期事实。",
            "action": "把任务摘要、文件摘要、面试弱点、项目行动项分层存储，并给每类记忆定义 freshness 校验。",
        },
    ),
    (
        ["plugin", "skill", "multi-agent", "everything-claude-code", "插件"],
        {
            "exam": "这里考察的是 Agent 能力如何从一次性 prompt 变成可安装、可复用、可治理的资产。",
            "answer": "我会把 Plugin / Skill 理解成能力资产化机制。它不是简单放一段提示词，而是把经验、工具、规则、触发条件和边界打包，让 Agent 在类似任务中稳定复用。多 Agent 则进一步把复杂任务拆给不同角色，但必须有上下文交接、结果合并和回收机制。",
            "mistake": "把 skill 当成 prompt 片段，把 multi-agent 当成多开几个模型，缺少任务边界和结果验收。",
            "tradeoff": "能力资产越多，发现、选择和冲突治理越重要；否则会从能力增强变成上下文噪声。",
            "action": "为知识平台沉淀固定 skill：项目沉淀、面经追问、前端视觉生成、痛点诊断，并记录适用场景和禁用场景。",
        },
    ),
    (
        ["permission", "sandbox", "observability", "安全", "可观测"],
        {
            "exam": "这里考察的是 Agent 系统从 demo 走向可用产品时，如何处理风险、审计和可复现。",
            "answer": "我会把权限、沙箱和可观测性看成 Agent 产品化的底座。模型输出不稳定，工具又可能有副作用，所以系统必须知道什么动作能自动执行，什么动作要确认，出错以后如何回放，用户如何知道 Agent 做过什么。",
            "mistake": "只做功能成功路径，不记录失败、拒绝、审批和执行证据。",
            "tradeoff": "严格治理会降低一些自动化速度，但能换来用户信任、问题定位和企业场景可落地。",
            "action": "在项目雷达和平台中把安全治理作为评分维度，沉淀项目时必须记录其权限、沙箱和审计设计。",
        },
    ),
    (
        ["frontend", "design", "workbench", "gpt-image", "draw-ui", "前端", "视觉"],
        {
            "exam": "这里考察的是能不能把前端审美要求变成可执行的工程规则，而不是只说高级、现代、好看。",
            "answer": "我会把前端风格控制理解成设计上下文工程。对知识平台来说，重点不是营销式视觉，而是长期可读、可扫描、可追溯。所以我会用 DESIGN.md 固化规则，用 UI mockup 固定目标，用截图对照校准实现，最后把反复出现的问题回写成设计规范。",
            "mistake": "把所有页面做成卡片堆，或者用 GPT Image 生成一张漂亮图后不做真实页面校验。",
            "tradeoff": "视觉生成能提升探索效率，但不能替代 React/CSS、响应式、中文长文本和可访问性这些真实工程约束。",
            "action": "为项目页、方案页、痛点页分别建立页面 inventory、文档阅读结构和截图校验清单。",
        },
    ),
    (
        ["provider", "productization", "radar", "平台", "产品化"],
        {
            "exam": "这里考察的是一个 Agent 原型如何变成长期可维护的平台，而不是一次性脚本。",
            "answer": "我会把产品化理解成把安装、配置、模型差异、权限、安全、文档、反馈和升级都纳入工程系统。Project Radar 也是同样逻辑，它不是搜索器，而是发现、评分、候选、沉淀、抽象和行动项的学习闭环。",
            "mistake": "只关注模型效果和功能 demo，忽略配置、版本、治理、用户反馈和长期维护成本。",
            "tradeoff": "产品化会让早期开发变慢，但它能避免系统在内容、依赖、模型和用户场景变多后失控。",
            "action": "把平台中的项目、方案、痛点、面试官、视觉生成全部接到统一索引，让沉淀自动反哺页面展示。",
        },
    ),
]

DEFAULT_PROFILE = {
    "exam": "这里考察的是能不能从一个具体项目或技术点里抽象出通用工程问题，而不是停留在功能介绍。",
    "answer": "我的沉淀方法是先识别它解决的真实问题，再看成熟项目如何拆解，再抽象成可迁移框架，最后落到当前项目行动项。这样文档不是摘要，而是可以复述、追问和迁移的学习资产。",
    "mistake": "只写项目有什么功能，不写为什么这么做、什么场景适合、有什么边界。",
    "tradeoff": "写深度文档会比摘要更慢，但它能沉淀判断力，后续面试、设计和开发都能复用。",
    "action": "补齐问题定义、口语版回答、工程取舍、面试官追问和当前项目行动项。",
}


def profile_for(path: Path, text: str) -> dict[str, str]:
    key = f"{path.as_posix().lower()} {text[:2000].lower()}"
    for keywords, profile in PROFILE_BY_KEYWORD:
        if any(keyword.lower() in key for keyword in keywords):
            return profile
    return DEFAULT_PROFILE


def append_deep_section(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "## 深度学习版补充" in text or "# 深度沉淀写作规范" in text:
        return False
    profile = profile_for(path, text)
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), path.stem)
    addition = f"""

## 深度学习版补充

> 学习目标：读完这部分后，不只是知道“{title} 做了什么”，而是能讲清它背后的工程问题、适用边界、常见误区和对当前平台的迁移路径。

### 1. 这件事到底考什么

{profile["exam"]}

如果只回答功能点，说明还停留在“看过项目”的层面；如果能回答问题来源、工程约束、取舍和行动项，才说明这份沉淀真正进入了自己的方法论。

### 2. 口语版回答

{profile["answer"]}

这段回答可以直接用于复盘、面试或方案评审。它的结构是：先定义问题，再讲工程边界，最后落到可迁移做法。

### 3. 工程视角拆解

可以按四层来理解：

- 问题层：这个设计到底在解决什么不稳定、不可控或不可复用的问题。
- 机制层：它用了哪些结构、协议、运行时、文档或流程来解决。
- 证据层：有哪些 README、源码、指标、案例或平台行为能证明它不是口号。
- 迁移层：它对 `claude-code-sourcemap`、知识平台、Project Radar 或面试训练有什么可执行启发。

### 4. 常见误区

{profile["mistake"]}

另一个常见误区是只把优秀项目当作模板照抄。真正应该学的是它为什么这样拆分，以及这个拆分在自己的场景里是否仍然成立。

### 5. Trade-off 与边界

{profile["tradeoff"]}

判断一个方案是否成熟，不是看它有没有更多能力，而是看它有没有明确说明代价、适用场景和不适用场景。

### 6. 当前项目行动项

- [ ] {profile["action"]}
- [ ] 把这份文档中的通用问题同步到对应 `docs/patterns/` 文档，避免停留在单项目笔记。
- [ ] 在平台详情页中保留“口语版回答、工程拆解、误区、行动项”，让它能直接用于学习和面试表达。

### 7. 面试官追问

**追问：这个项目或方案最值得学习的不是功能，而是什么？**

答：最值得学习的是它如何把一个模糊问题变成可治理的工程结构。功能只是表层，真正可迁移的是它的边界划分、执行流程、证据链和取舍。

**追问：如果迁移到当前平台，第一步应该做什么？**

答：第一步不是照搬实现，而是把它抽象成平台中的一个通用问题，补齐文档、索引、行动项和验证方式，让后续沉淀能自动进入平台展示。
"""
    path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = []
    for root in TARGET_DIRS:
        for path in sorted(root.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            if append_deep_section(path):
                changed.append(path)
    print(f"Updated {len(changed)} docs")
    for path in changed:
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
