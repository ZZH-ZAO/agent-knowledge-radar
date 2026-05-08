#!/usr/bin/env python3
"""
Migrate old .claude/docs cases into the new docs/external-projects structure.

The goal is not to copy the old tree blindly. Each legacy case becomes a
deep-distillation document with:
- source evidence from old user/agent docs
- what the case is really about
- oral answer
- engineering breakdown
- migration actions
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = ROOT / ".claude" / "docs"
LEGACY_INDEX = ROOT / "docs" / "legacy-migration" / "旧案例迁移规则与清单" / "legacy-case-migration-index.json"
OUTPUT_DIR = ROOT / "docs" / "external-projects" / "旧体系迁移项目样本"
TEMPLATE_DIR = ROOT / "docs" / "templates" / "旧体系共享模板"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_cases() -> list[dict[str, Any]]:
    data = json.loads(read_text(LEGACY_INDEX))
    return data.get("cases", [])


def load_index() -> dict[str, Any]:
    return json.loads(read_text(LEGACY_INDEX))


def path_from_legacy(value: str) -> Path:
    return ROOT / value.replace("/", "\\")


def collect_files(value: str) -> list[Path]:
    if not value:
        return []
    path = path_from_legacy(value)
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(p for p in path.rglob("*.md") if p.name.lower() != "readme.md")
    return []


def first_useful_paragraph(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("|") or stripped.startswith("---"):
            continue
        if stripped.startswith("- ") and len(lines) < 2:
            lines.append(stripped[2:])
        elif not stripped.startswith("- "):
            lines.append(stripped)
        if len(" ".join(lines)) > 260:
            break
    return " ".join(lines).strip()


def excerpt_from_files(files: list[Path], limit: int = 3) -> list[str]:
    excerpts = []
    for path in files[:limit]:
        text = read_text(path)
        paragraph = first_useful_paragraph(text)
        if paragraph:
            excerpts.append(f"- `{path.relative_to(ROOT).as_posix()}`：{paragraph[:380]}")
        else:
            excerpts.append(f"- `{path.relative_to(ROOT).as_posix()}`：旧文档存在，但需要继续人工提炼核心段落。")
    return excerpts


def profile_for(case: dict[str, Any]) -> dict[str, str]:
    types = " ".join(case.get("types", [])).lower()
    name = f"{case.get('id', '')} {case.get('name', '')}".lower()
    text = f"{types} {name}"
    if "testing" in text or "eval" in text or "quality" in text or "giskard" in text or "promptfoo" in text:
        return {
            "problem": "AI / Agent 系统如何证明输出质量，而不是只依赖一次看起来正确的生成结果。",
            "answer": "我会把它理解成质量治理问题：要把用例、评测、人工确认、失败分类和回归检查串起来，让模型输出从一次性结果变成可持续改进的质量闭环。",
            "action": "把该案例迁移到 Observability / Evaluation / Testing Agent 方案中，补充指标、失败分类和面试追问。",
        }
    if "rag" in text or "repository" in text or "retrieval" in text:
        return {
            "problem": "检索、仓库理解或垂直知识任务如何建立证据链，避免模型只靠参数记忆生成。",
            "answer": "我会把它理解成证据驱动的 Agent 工作流：先选择证据，再组织上下文，再生成结构化结果，最后用评估和人工回流校准。",
            "action": "把该案例补充到 RAG / Evidence / Report Generation 相关方案，并和面经项目回答联动。",
        }
    if "mcp" in text or "tool" in text or "browser" in text:
        return {
            "problem": "Agent 如何安全、可追踪地接入外部工具生态。",
            "answer": "我会把它理解成 Tool Runtime 问题：工具不是函数，而是带权限、状态、结果治理和审计要求的外部行动。",
            "action": "把该案例同步到 Tool Runtime / MCP Integration / Browser Tool Runtime 方案中。",
        }
    if "frontend" in text or "documentation" in text or "team knowledge" in text or "research" in text:
        return {
            "problem": "如何把团队知识、设计规范和输出质量要求变成可复用资产。",
            "answer": "我会把它理解成知识资产化问题：文档不只是说明，而是 Agent 能稳定读取、复用、校验和迭代的上下文资产。",
            "action": "把该案例迁移到 Frontend Design / Knowledge Distillation / Output Quality 方案中。",
        }
    if "memory" in text or "long-running" in text:
        return {
            "problem": "长链路 Agent 如何保留状态、记忆和任务连续性。",
            "answer": "我会把它理解成 Memory-first Workbench 问题：长期任务需要持久会话、记忆召回、任务恢复和多入口工作台。",
            "action": "把该案例补进 Memory System、Plugin / Skill 和 Productization 方案。",
        }
    return {
        "problem": "如何从旧体系项目案例中抽象出可迁移的 Agent 工程问题。",
        "answer": "我会先看它解决的真实问题，再看旧文档里的证据和实现建议，最后归并到当前 patterns 与平台行动项。",
        "action": "把该案例作为旧体系迁移样本，继续补充项目证据、通用问题和行动项。",
    }


def render_case(case: dict[str, Any]) -> str:
    files = collect_files(case.get("userDoc", "")) + collect_files(case.get("agentDoc", ""))
    extra_files = []
    if case.get("userDoc", "").endswith((".md", ".MD")):
        parent = path_from_legacy(case["userDoc"]).parent
        if parent.exists():
            extra_files = [p for p in sorted(parent.glob("*.md")) if p not in files and p.name.lower() != "readme.md"]
    files = files + extra_files
    profile = profile_for(case)
    source_lines = excerpt_from_files(files, 6)
    source_list = "\n".join(source_lines) if source_lines else "- 暂无可读旧文档，需要检查路径。"
    types = " / ".join(case.get("types", [])) or "待分类"
    related = "、".join(case.get("relatedPatterns", [])) or "待补充"
    title = case.get("name") or case.get("id")
    return f"""# 旧体系项目沉淀：{title}

> 来源：`.claude/docs`  
> 迁移日期：2026-05-04  
> 旧案例 ID：`{case.get('id')}`  
> 类型：{types}  
> 迁移优先级：{case.get('priority', 'unknown')}  
> 关联方案：{related}

## 1. 项目一句话

{case.get('coreValue', '旧体系中沉淀的项目案例，需要迁移到新知识平台继续学习。')}

## 2. 这件事到底考什么

{profile['problem']}

旧文档的价值不在于保留历史文件本身，而在于把里面的项目判断、架构分析、路线规划和模板沉淀，转成现在平台能继续索引、阅读、追问和行动的知识资产。

## 3. 口语版回答

{profile['answer']}

如果面试官追问“你为什么要迁移旧文档”，可以这样答：旧体系里已经有大量项目分析和模板，如果不迁移，新平台看到的只是新文档，会漏掉历史判断。迁移后它们会进入项目页、方案页和痛点页，继续参与平台的自动索引和深度阅读。

## 4. 旧文档证据

{source_list}

## 5. 可迁移的工程问题

- 这个案例对应的不是单个功能，而是 `{types}` 方向的工程问题。
- 它应该被归并到 `{related}` 等 patterns 中，而不是停留在旧目录。
- 如果旧文档里包含 roadmap、template、comparison 或 upgrade plan，应进一步拆成平台行动项。

## 6. 常见误区

- 只把旧文档复制到新目录，不做问题抽象。
- 只保留 README，不迁移 analysis、roadmap、template 和 comparison。
- 只把它当作历史材料，不让它进入平台索引。
- 迁移后不更新相关 patterns，导致知识仍然是孤立笔记。

## 7. Trade-off 与边界

旧文档迁移有两个边界：

- 不能无差别把所有旧文件平铺到新目录，否则目录会更乱。
- 不能只迁移摘要，否则会丢失旧文档里真正有价值的架构判断和行动建议。

所以当前采用“按案例生成深度沉淀文档 + 保留旧路径证据 + 后续逐步拆分专题”的方式。

## 8. 当前项目行动项

- [ ] {profile['action']}
- [ ] 检查旧文档中的 roadmap、template、comparison 是否需要拆成单独 pattern。
- [ ] 在平台中通过项目页阅读该案例，并根据内容补充痛点页证据。
- [ ] 后续不再向 `.claude/docs` 新增沉淀，新内容统一进入 `docs/` 新体系。

## 9. 面试官追问

**追问：旧文档迁移和简单归档有什么区别？**

答：归档只是保存文件，迁移是让旧知识重新进入当前平台的索引、阅读、方案抽象和行动项闭环。

**追问：怎么避免迁移后目录更乱？**

答：按案例收束到 `旧体系迁移项目样本`，用文档内部引用旧路径，不把旧目录结构原样复制出来。
"""


def migrate_cases() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    index = load_index()
    cases = index.get("cases", [])
    changed = 0
    for case in cases:
        if case.get("migratedTo"):
            continue
        case_id = case.get("id")
        if not case_id:
            continue
        output = OUTPUT_DIR / f"legacy-{case_id}.md"
        write_text(output, render_case(case))
        case["migratedTo"] = output.relative_to(ROOT).as_posix()
        changed += 1
    index["updatedAt"] = "2026-05-04"
    index["migrationStatus"] = "旧体系项目级文档已迁移到 docs/external-projects/旧体系迁移项目样本；旧 shared 模板已汇总到 docs/templates/旧体系共享模板。"
    write_text(LEGACY_INDEX, json.dumps(index, ensure_ascii=False, indent=2))
    readme = """# 旧体系迁移项目样本

这里存放从 `.claude/docs` 旧体系迁移过来的项目级沉淀。

规则：

- 不再向 `.claude/docs` 新增新沉淀。
- 旧文档不原样平铺复制，而是按项目案例生成深度沉淀。
- 每份文档保留旧路径证据，并补充口语版回答、工程拆解、误区、行动项和追问。
- 后续如果某个旧案例价值很高，再拆到更具体的 `patterns/` 或专题目录。
"""
    write_text(OUTPUT_DIR / "README.md", readme)
    return changed


def migrate_shared_templates() -> int:
    user_shared = LEGACY_ROOT / "user" / "shared"
    agent_shared = LEGACY_ROOT / "agent" / "shared"
    files = []
    if user_shared.exists():
        files.extend(p for p in sorted(user_shared.glob("*.md")) if p.name.lower() != "readme.md")
    if agent_shared.exists():
        files.extend(p for p in sorted(agent_shared.glob("*.md")) if p.name.lower() != "readme.md")
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 旧体系共享模板迁移",
        "",
        "这里收束 `.claude/docs/*/shared` 里的旧模板和 playbook。它们不作为项目样本，而是作为后续写作、评审、测试 Agent、输出质量控制和产品化设计的模板资产。",
        "",
        "## 模板清单",
        "",
    ]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        lines.append(f"### {path.stem}")
        lines.append("")
        lines.append(f"- 旧路径：`{rel}`")
        lines.append(f"- 摘要：{first_useful_paragraph(text)[:320] or '需要继续人工提炼。'}")
        lines.append("")
    write_text(TEMPLATE_DIR / "legacy-shared-templates-index.md", "\n".join(lines))
    return len(files)


def main() -> int:
    case_count = migrate_cases()
    template_count = migrate_shared_templates()
    print(f"Migrated legacy cases: {case_count}")
    print(f"Indexed shared templates: {template_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
