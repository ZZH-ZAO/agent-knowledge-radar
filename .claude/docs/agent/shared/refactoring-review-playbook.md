# Refactoring Review Playbook

## Summary

- Project name: shared refactoring review playbook
- Project path: `D:\claude-code-sourcemap\.claude\docs\agent\shared`
- Document type: agent
- Purpose: provide compact reusable notes for reviewing code with a refactoring mindset derived from Refactoring, 2nd Edition

## Use When

- reviewing legacy code or AI-generated code
- deciding whether a change should be a refactor or a behavior change
- proposing small safe improvement steps instead of vague rewrite advice

## Core Lens

- Refactoring means improving internal structure without changing observable behavior.
- Prefer many small behavior-preserving steps over one large redesign jump.
- Use tests or another reliable safety net before recommending risky structural changes.
- Judge code by changeability, not by aesthetic preference alone.

## Smell-First Review

Look for named signals rather than generic discomfort:

- duplicated code
- long function
- long parameter list
- global data
- mutable data
- divergent change
- shotgun surgery
- feature envy
- data clumps
- primitive obsession
- repeated switches
- loops that hide intent
- large class
- message chains
- middle man
- data class
- refused bequest
- comments compensating for confusing code

## Suggestion Pattern

When you report a finding, prefer this structure:

1. name the likely smell
2. explain the maintenance cost it creates
3. propose 1-3 small refactoring moves
4. mention the safety requirement or test gap

Example shape:

- Likely smell: `long function`
- Cost: mixes multiple responsibilities and makes future edits risky
- Small moves: `Extract Function`, `Split Phase`, `Slide Statements`
- Safety note: add characterization tests around current outputs before editing

## Common Move Mapping

- `long function`
  - `Extract Function`
  - `Split Phase`
  - `Replace Temp with Query`
- `duplicated code`
  - `Extract Function`
  - `Move Function`
  - `Combine Functions into Class` or `Transform`
- `data clumps` or `long parameter list`
  - `Introduce Parameter Object`
  - `Preserve Whole Object`
- `primitive obsession`
  - `Replace Primitive with Object`
  - `Encapsulate Record`
- `feature envy`
  - `Move Function`
  - `Move Field`
- `divergent change`
  - `Extract Class`
  - `Move Function`
  - `Split Phase`
- `shotgun surgery`
  - gather behavior with `Move Function` / `Move Field`
  - consider `Extract Superclass` or better ownership boundaries
- `repeated switches`
  - `Replace Conditional with Polymorphism`
  - `Introduce Special Case`
- `deep nested conditionals`
  - `Replace Nested Conditional with Guard Clauses`
  - `Decompose Conditional`
- `large class`
  - `Extract Class`
  - `Move Function`
  - `Move Field`
- `message chains`
  - `Hide Delegate`
  - `Move Function`
- `data class`
  - move behavior closer to the data
  - consider `Encapsulate Record`
- `loops hiding multiple intents`
  - `Split Loop`
  - `Replace Loop with Pipeline`
- tangled parsing + formatting + calculation
  - `Split Phase`
  - `Combine Functions into Class` or `Transform`

## Review Wording Heuristic

Prefer wording like:

- likely smell
- maintenance cost
- smallest next moves
- safety gap

Avoid wording like:

- "bad code"
- "needs rewrite"
- "not elegant"

## Fast Output Shape

For each finding, output:

- `Likely smell`
- `Why it hurts`
- `Small next moves`
- `Risk / missing tests`

## Refactor vs Rewrite

Bias toward refactoring when:

- current behavior is mostly correct
- there is at least partial test coverage
- the structure is ugly but still understandable in slices
- value can be unlocked incrementally

Bias toward larger redesign only when:

- behavior is not trustworthy
- structure cannot be safely changed in small steps
- dependencies are too entangled to isolate
- the team accepts higher migration risk explicitly

## Guardrails

- Do not call a behavior-changing redesign a refactor.
- Do not recommend a huge rewrite when a sequence of small moves is available.
- Do not ignore missing tests when proposing structural change.
- Do not describe code as bad without naming the concrete maintenance problem.

## Source Basis

- `D:\claude-code-sourcemap\重构-改善既有代码的设计[第2版].pdf`
- core themes: behavior preservation, small steps, smell detection, test-backed change, refactoring catalog
