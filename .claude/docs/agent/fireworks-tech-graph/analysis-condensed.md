# fireworks-tech-graph Condensed Notes

## Summary

- Project name: fireworks-tech-graph
- Project path: `D:\fireworks-tech-graph`
- Document type: agent
- Purpose: provide condensed reusable notes for future agents when they need a reference for technical-diagram generation skills
- Primary label: `team-knowledge`

## What It Is

`fireworks-tech-graph` is a Claude Code skill for generating production-quality technical diagrams from natural language and exporting them as SVG + PNG.

It is not an Agent runtime or workflow product.

Better classification:

- visualization skill
- technical documentation support asset
- diagram-generation knowledge package

## Core System Shape

Main layers in the repo:

- `SKILL.md`: trigger rules, workflow, diagram taxonomy, layout rules, shape vocabulary, arrow semantics
- `references/`: style specs, icons, SVG layout guidance
- `templates/`: starter SVG templates by diagram type
- `fixtures/`: regression cases for stable sample-grade outputs
- `scripts/`: generation, validation, export, batch testing

Inference:

- this is closer to a small generation framework than a plain prompt collection
- output quality is controlled through rules + fixtures + scripts, not only model wording

## Strongest Lessons

- Treat technical diagrams as a structured generation task, not as ad hoc art output.
- Separate visual style from semantic diagram vocabulary.
- Encode node meaning with consistent shapes and edge meaning with consistent arrow semantics.
- Add validation and regression fixtures so AI-generated artifacts stay stable over time.

## Strong Layers

- style system for diagrams
- semantic node/arrow vocabulary
- AI/Agent domain-specific diagram patterns
- SVG validation and export workflow
- reusable templates plus fixture-driven regression

## Reuse When

- building AI-assisted diagram generation workflows
- adding standardized visualization output to documentation or architecture workbenches
- turning diagram production into a repeatable team capability
- documenting Agent, RAG, memory, or tool-call systems with consistent visuals

## Main Tradeoff

- much more structured and reusable than manual prompt-only diagram generation
- but less flexible than full manual design tools such as Figma or draw.io
- still depends on good input descriptions and `rsvg-convert` availability

## Comparison Anchor

Use this case when the main question is:

- how to make an Agent reliably generate polished technical diagrams as a reusable capability

Do not use this case when the main question is:

- how an Agent runtime loop works
- how multi-agent orchestration is implemented
- how a domain workflow product is architected

## Source Basis

- local repo `D:\fireworks-tech-graph`
- `README.md`
- `SKILL.md`
- `package.json`
- `scripts/README.md`
- `references/`
- `fixtures/`
- `templates/`
