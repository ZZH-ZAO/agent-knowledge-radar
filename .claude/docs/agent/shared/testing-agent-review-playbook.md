# Testing Agent Review Playbook

## Summary

- Project name: shared
- Project path: `D:\claude-code-sourcemap\.claude\docs\agent\shared`
- Document type: agent
- Purpose: provide a compact reusable review playbook for future agents analyzing testing-oriented Agent systems such as PRD-to-test-case, test design copilots, and testing knowledge workbenches

## Core Classification Heuristic

When reviewing a testing-oriented Agent project, first decide which of these it really is:

- `generator-tool`
  mostly one-shot case generation with light UI
- `vertical-workflow`
  testing workflow system with retrieval, refinement, and review
- `testing-knowledge-system`
  workflow + persistent case assets + quality closure + regression
- `runtime-first`
  rare for testing systems; only use if the project is primarily building a general-purpose agent runtime

Most testing projects that look like “agents” are actually `vertical-workflow` systems first.

## Seven-Layer Review Frame

Always review across these seven layers:

1. product interaction
2. workflow orchestration
3. retrieval and evidence
4. generation and evaluation
5. memory and assets
6. quality and verification
7. platform governance

If the analysis only lists features and does not cover these layers, it is incomplete.

## Layer Questions

### 1. Product Interaction

Check:

- Is this a chat shell or a real workbench?
- Can the user inspect evidence, refine outputs, and review failures?
- Are outputs artifacts or only chat responses?

Strong signals:

- structured editable case output
- evidence panel
- evaluator panel
- bad-case review surface

### 2. Workflow Orchestration

Check:

- Is orchestration trapped in the UI layer?
- Are stage boundaries explicit?
- Are there stable input/output contracts?

Strong signals:

- service/workflow layer exists
- generate / refine / evaluate / archive stages are separated
- batch or worker decomposition is possible

### 3. Retrieval and Evidence

Check:

- Is retrieval only semantic?
- Are business keywords and logic/rule keywords used?
- Is rerank present?
- Can the system explain why retrieved items were selected?

Strong signals:

- hybrid retrieval
- evidence assembly
- rerank score breakdown
- visible source attribution

### 4. Generation and Evaluation

Check:

- Does the system support generate -> refine -> evaluate?
- Is output structured and contract-bound?
- Is evaluator only for display, or also for system writeback?

Strong signals:

- explanation + structured artifact separation
- evaluator with structured report
- evaluation writeback for learning/triage

### 5. Memory and Assets

Check:

- Does the system distinguish session memory, case memory, and learning memory?
- Are good cases promoted into reusable assets?
- Are bad cases preserved as negative examples?

Strong signals:

- historical case store
- golden cases
- template extraction
- async asset/memory updates

### 6. Quality and Verification

Check:

- Are there retrieval metrics?
- Are there bad-case records?
- Is there a regression benchmark suite?
- Is there a verification-first mindset?

Strong signals:

- Recall/Precision + Rule Recall + Noise Rate
- bad-case lifecycle
- benchmark reruns after changes

### 7. Platform Governance

Check:

- Are risky new retrieval/generation behaviors gated?
- Are experiments observable?
- Can the team rollback feature changes safely?

Strong signals:

- feature flags
- experiment groups
- metrics by strategy/version

## Retrieval-Specific Review Notes

Testing systems should not be judged with generic RAG criteria alone.

In addition to semantic relevance, review whether retrieval preserves:

- rule recall
- edge-case recall
- module/domain match
- source authority
- version freshness

If a project only reports semantic similarity or top-k hit rate, the review is shallow.

## Rerank Review Notes

Good rerank for testing systems should score along three bands:

- relevance
- test value
- knowledge trust

Useful dimensions:

- `query_relevance`
- `module_match`
- `testcase_usefulness`
- `rule_strength`
- `edge_case_density`
- `source_authority`
- `version_freshness`
- `human_acceptance`

Do not overprescribe all eight for first-version implementation; but expect at least a minimal explicit scoring frame.

## Bad-Case Review Notes

Always ask whether bad cases are first-class objects.

Minimum taxonomy:

- retrieval bad-case
- rerank bad-case
- generation bad-case
- evaluation bad-case
- workflow bad-case

Strong signals:

- bad-case review UI
- severity
- status lifecycle
- root cause guess
- promote to regression set

## Minimal Metrics Pack

For a mature-enough testing workflow system, expect at least:

- `Recall@20`
- `Precision@5`
- `Rule Recall@10`
- `Noise Rate@10`
- `Human Acceptance Rate`

If these do not exist, note the lack of quality governance explicitly.

## Borrow Map For Recommendations

Use these projects as recommendation anchors:

- `ByteDance--Auto_prd_test_agent`
  for PRD-to-test-case workbench, refinement loop, evaluator seed
- `career-ops`
  for workflow-first design and data contracts
- `fault-diagnosis`
  for evidence transparency and report-style delivery
- `repomind`
  for verification-first, bad-case lifecycle, and regression culture
- `deer-flow`
  for app/runtime layering and async memory asset updates
- `claude-code`
  for feature flags, observability, and platform rollout discipline

## Final Review Shortcut

A testing Agent project is becoming mature when it shifts from:

- “Can it generate test cases?”

to:

- “Can it retrieve the right rules?”
- “Can it explain its evidence?”
- “Can humans refine it effectively?”
- “Can it evaluate itself?”
- “Can it retain bad cases?”
- “Can it regression-test improvements?”
- “Can it become a team testing knowledge system?”
