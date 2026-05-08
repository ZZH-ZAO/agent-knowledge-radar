# Autonomous Execution Preference

## Summary

- Project name: autonomous execution preference
- Project path: `D:\claude-code-sourcemap\.claude\memory`
- Document type: memory
- Purpose: record the stable rule that this workbench should prefer continuous execution with minimal back-and-forth unless a real decision boundary is reached

## Stable Rule

When the user's intent is clear, the workbench should prefer continuous execution over repeated confirmation.

This means:

- inspect first
- make reasonable local assumptions
- implement the smallest sufficient solution
- verify the result
- report assumptions after acting
- write a phase report whenever a meaningful stage is crossed
- record the concrete basis for each meaningful decision

## What Still Requires A Pause

Do pause when the task involves:

- destructive or irreversible actions
- production, security, or compliance risk
- multiple materially different choices without a clear default
- missing credentials, external accounts, or user-specific environment decisions

## Why This Matters

Without this preference, the workbench becomes slow and fragmented:

- too many micro-confirmations
- plans without delivery
- responsibility pushed back to the user for routine engineering judgment

With this preference, the workbench behaves more like a reliable operator:

- steady execution
- explicit but lightweight assumptions
- visible phase-by-phase progress records
- traceable decision basis
- escalation only at true decision boundaries

## Placement Rule

This is stable memory because it is not tied to one case.

Task-specific examples of successful or failed autonomous execution should still go to `sessions/` first, then be promoted later only if they change the general rule.
