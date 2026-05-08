# Case Library Workflow

## Summary

- Project name: Agent research workbench
- Project path: `D:\claude-code-sourcemap\.claude`
- Document type: workflow note
- Purpose: define how project analysis should now be persisted as a repeatable case-library process instead of a one-off output

## Standard Workflow

1. Read the target project as a system.
2. Judge whether it is mainly:
   - a runtime
   - a platform expansion
   - a vertical workflow system
   - a memory or RAG system
   - a multi-agent coordination system
3. Write a deep user-facing document into `.claude/docs/user/`.
4. Write a compressed agent-facing document into `.claude/docs/agent/`.
5. Add folder-level `README.md` files inside the project folders so readers can navigate the local case bundle quickly.
6. Update the case-library index so future work can retrieve the case correctly.

## Shared Templates Workflow

When several project cases repeatedly point to the same reusable pattern:

1. Extract the cross-project lesson into `.claude/docs/user/shared/`.
2. Add or update `shared/README.md` so the template stays discoverable.
3. Link the template from relevant project case folders or the main index when useful.

## What The User-Facing Doc Should Do

- explain the project in lecture style
- define important technical terms
- answer why the design works
- explain tradeoffs and failure cases
- help the human reader actually learn the pattern

## What The Agent-Facing Doc Should Do

- compress the project into reusable judgment notes
- identify strong layers and weak layers
- identify reusable patterns
- identify what future project types should compare against this case

## Minimum Metadata For Every Case

- Project name
- Project path
- Document type
- Purpose

## Recommended Additional Metadata

- Primary classification label
- Core architectural identity
- Strongest engineering layers
- Important tradeoffs
- Recommended reuse scenarios
