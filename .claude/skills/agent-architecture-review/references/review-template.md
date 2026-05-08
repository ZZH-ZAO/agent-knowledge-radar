# Review Template

Use this template when writing a full architecture review.

## 1. Overall Judgment

- What kind of system is this really?
- Is it a demo, a serious runtime, or a platform?
- What is the actual architectural center?

## 2. Runtime Spine

- entrypoint
- session state
- query loop
- tool result reinjection
- turn-end hooks

## 3. Layer-by-Layer Review

For each layer:

- what it is
- why it exists
- implementation points
- strengths
- tradeoffs
- scaling risks

Suggested layers:

- prompt/context
- tool runtime
- workflow orchestration
- RAG/retrieval
- memory
- multi-agent
- platform/operations

## 4. Most Valuable Ideas

- Which ideas are worth copying into other Agent projects?

## 5. Weaknesses and Risks

- What is still shallow, fragile, or overly heavy?

## 6. Final Advice

- What should the team strengthen next?
