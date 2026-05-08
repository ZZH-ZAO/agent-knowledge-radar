# RepoMind Analysis Notes

## Summary

- Project name: RepoMind
- Project path: `D:\repomind`
- Document type: agent
- Purpose: provide condensed reusable notes for analyzing future repository-intelligence or security-agent products against RepoMind

## Classification

- Primary label: `vertical-workflow`
- Secondary label: `team-knowledge`
- Secondary label: `tool-runtime`
- Secondary label: `platform-expansion`

## Core Identity

RepoMind is a productized repository-intelligence platform, not a general-purpose agent runtime.

Strong identity:

- repo/profile chat over GitHub assets
- agentic CAG for code understanding
- GitHub live-snapshot tool use
- verification-first security scanning
- product surfaces for cache, budgets, share links, false-positive review, fix verification

## Strongest Layers

### Unified query pipeline

- `src/lib/services/query-pipeline.ts`
- one shared pipeline for streaming and non-streaming
- stages:
  - file pruning
  - AI file selection
  - file fetch with token budget
  - context assembly
  - streamed answer generation
- emits structured `StreamUpdate` events instead of raw token-only streaming

### Toolized GitHub evidence

- `src/lib/gemini.ts`
- tool declarations for commits, PRs, issues, releases, workflow runs, contributors, languages, dependency alerts, file history, ref compare
- model can enrich code answers with live GitHub evidence
- explicit per-function GitHub call cap and transparency note when sampling is used

### Agentic CAG instead of classic RAG

- primary retrieval pattern is:
  - file tree
  - LLM file selection
  - raw file-context injection
- better fit for codebase structure than naive chunk-vector retrieval
- weak for long-term org KB or cross-project semantic reuse

### Productized streaming contract

- `src/app/api/chat/repo/route.ts`
- `src/app/api/chat/profile/route.ts`
- newline-delimited JSON / SSE-style event flow
- event types:
  - `status`
  - `files`
  - `tool`
  - `content`
  - `complete`
  - `error`
- route layer also persists `ChatRun.partialText` / `finalText`

### Security verification workflow

- `src/lib/services/security-service.ts`
- `src/lib/services/security-verification.ts`
- deterministic detection is not enough
- findings pass verification gate before report inclusion
- type-specific verification:
  - dependency advisory / OSV checks
  - source-sink-sanitizer logic for code issues
  - placeholder / production-context logic for secrets/config
- specialized Supabase authz/RLS evidence analysis
- optional LLM adjudication is conservative and layered on top, not primary truth source

## Memory Notes

Memory is distributed across layers:

- conversation memory
  - `ChatConversation.messages`
- run-state memory
  - `ChatRun.status`, `partialText`, `finalText`, `errorMessage`
- query reuse memory
  - query -> selected files
  - query + files -> answer
  - latest answer short-circuit
- infra cache memory
  - file, tree, repo metadata, repo full context, commit snapshots
- security business memory
  - scans, finding verification records, false-positive submissions, share links, fix verification runs

Key lesson:

- do not reduce memory to chat history only
- product agents need run memory, cache memory, and business-process memory

## Prompt Notes

- `src/lib/prompt-builder.ts`
- prompt responsibilities:
  - topic scope enforcement
  - code-over-docs evidence policy
  - strict output structure
  - visual routing contract
  - external/web snapshot coordination
- prompt is product-governance heavy, not just persona-heavy

## Cache / Budget / Isolation Notes

- `src/lib/cache.ts`
- multi-layer cache with public/private namespace separation
- anonymous vs authenticated cache and tool budgets
- anonymous cache admission is more conservative
- repo/profile tool budgets handled separately
- security scan cache is revision-aware and config-aware

Key productization lesson:

- cost control and tenant isolation are first-class design layers in serious agent products

## Workflow Layers

### Single-turn loop

- select files
- fetch context
- answer
- invoke tools when needed
- continue reasoning

### Streaming-process orchestration

- emits phase status, file list, tool activity, answer chunks, completion metadata

### Session/run orchestration

- `ChatConversation`
- `ChatRun`
- supports partial persistence and later restoration / inspection

### Security workflow orchestration

- scan config
- revision resolution
- cache lookup
- scan
- verification gate
- result storage
- share / false-positive / fix-verification downstream flows

## Reusable Lessons

### What to copy

- build one unified repo-query pipeline for both streaming and non-streaming
- treat GitHub metadata as live evidence tools, not only background decoration
- use agentic CAG for repository analysis before reaching for classic vector RAG
- stream structured process events, not tokens only
- separate conversation memory from run-state memory
- put a verification gate between scanner detection and report publication
- make caching namespace-aware and revision-aware

### What to watch

- file-selection quality is a major bottleneck
- prompt is large and rule-heavy
- cache architecture raises consistency/debug complexity
- approach is optimized for repo intelligence, not general knowledge platforms
- security verification logic can become expensive to maintain

## Best Reuse Scenarios

- GitHub repository analysis products
- code intelligence assistants
- repo/profile chat systems that need evidence-backed answers
- security review products with false-positive pressure
- agent products that need strong cache/budget/streaming discipline
