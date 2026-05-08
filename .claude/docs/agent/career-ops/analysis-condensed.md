# career-ops Condensed Notes

## Project Summary

- Project name: `career-ops`
- Project path: `D:\career-ops`
- Document type: `agent`
- Purpose: compressed notes for future agent reuse and fast architectural recall

## System Type

- Not a general Agent runtime
- Not a model-platform architecture
- A vertical agentic workflow system built on top of Claude Code / OpenCode style hosts

## Real Center

- The center is the career workflow pipeline, not the base query loop
- Main flow:
  - ingest JD/URL
  - extract JD
  - classify archetype
  - evaluate A-F/G
  - generate report
  - generate PDF
  - append tracker artifacts

## Strongest Design Areas

### 1. Prompt as domain operating procedure

- `CLAUDE.md`
- `modes/_shared.md`
- `modes/*.md`
- `batch/batch-prompt.md`

These prompts act as:

- domain rules
- workflow instructions
- tool reliability policy
- writing constraints
- output contracts

### 2. Workflow orchestration

- single-offer evaluation
- auto-pipeline
- portal scan
- pipeline inbox
- batch parallel workers
- tracker merge and integrity checks

This is the main product strength.

### 3. Data contract

- `DATA_CONTRACT.md`
- explicit separation between user layer and system layer
- supports personalization plus safe updates

This is unusually mature for an Agent application.

## Tooling Philosophy

- Relies on host Agent tools rather than implementing a new tool runtime
- But has strong tool governance at the domain layer:
  - Playwright for real verification
  - WebFetch as fallback
  - WebSearch for comp/culture/research
  - explicit rule against parallel Playwright workers

## Memory Pattern

- No heavy memory runtime
- Uses explicit file-based long-term context:
  - `cv.md`
  - `article-digest.md`
  - `config/profile.yml`
  - `modes/_profile.md`
  - tracker and follow-up files

This is a pragmatic, transparent memory design for a sensitive personal-data domain.

## Multi-Agent Pattern

- Practical parallel-worker design
- headless workers with self-contained prompts
- suitable because each offer is naturally separable
- not a coordinator/swarm/social-agent design

## What This Project Teaches

- You can build a strong Agent product without building a full Agent runtime
- Borrow the host Agent runtime and go deep on:
  - domain prompts
  - workflow
  - data contract
  - output pipeline
  - HITL boundaries

## Main Reusable Lessons

- For vertical Agent products, workflow depth often matters more than runtime novelty
- Data-contract separation is critical when user assets and auto-updatable system logic coexist
- Prompt can function as a domain operating manual
- “Good enough” multi-agent should match task decomposition, not hype
