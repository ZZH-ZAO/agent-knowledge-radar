---
name: refactoring-guided-review
description: Use when the user wants code review, code cleanup, or refactoring guided by explicit refactoring principles rather than vague optimization. Apply this skill when reviewing legacy code, AI-generated code, or PR changes and the goal is to identify code smells, explain maintenance cost, propose small behavior-preserving refactoring steps, and call out test or safety gaps. Trigger on requests like “重构审查”, “小步重构”, “按原则重构”, “按重构方法审查”, “review and refactor”, “smell-based review”, or “small-step refactor”.
---

# Refactoring Guided Review

Use this skill when the task is to review or refactor code with a refactoring mindset, not to do an unconstrained rewrite.

Natural short aliases for users:

- `重构审查`
- `小步重构`
- `按原则重构`

For reference material, read as needed:

- `../../docs/agent/shared/refactoring-review-playbook.md`
- `../../docs/user/shared/refactoring-smell-to-action-cheatsheet.md`
- `../../docs/user/shared/refactoring-review-prompt-templates.md`
- `../../docs/user/shared/refactoring-2nd-edition-notes.md`

## Core Goal

Your job is to:

- identify likely code smells
- explain why they hurt future changeability
- propose the smallest useful refactoring moves first
- distinguish refactor from rewrite
- call out missing tests or safety gaps before risky edits

Do not use “needs optimization” or “should be rewritten” as lazy conclusions.

## Workflow

1. Read the relevant code path first.
2. Decide whether the task is:
   - review only
   - small-step refactor
   - mixed review + implementation
3. Name likely smells before proposing edits.
4. Prefer 1-3 behavior-preserving moves over a large redesign jump.
5. If the user asked for changes, implement the smallest safe steps that materially improve structure.
6. If tests are missing, say so explicitly and reduce change scope accordingly.

## Smell-First Lens

Common smells to look for:

- duplicated code
- long function
- long parameter list
- data clumps
- feature envy
- primitive obsession
- repeated switches
- deep nested conditionals
- large class
- message chains
- data class
- loops hiding multiple intents
- comments compensating for unclear code

## Preferred Output Shape

For review findings, prefer:

- `Likely smell`
- `Why it hurts`
- `Small next moves`
- `Risk / missing tests`

For implementation tasks, explain briefly:

- what smell you targeted
- what small refactoring moves you applied
- what you could not safely change

## Guardrails

- Do not call a behavior-changing redesign a refactor.
- Do not jump to rewrite if a small-step path exists.
- Do not recommend broad cleanup without naming the maintenance problem.
- Do not hide missing-test risk.
- If the code is acceptable and no meaningful smell stands out, say so plainly.
