# ByteDance--Auto_prd_test_agent Condensed Notes

## Summary

- Project name: ByteDance--Auto_prd_test_agent
- Project path: `D:\测开\ByteDance--Auto_prd_test_agent`
- Document type: agent
- Purpose: provide condensed reusable notes for future Agent analysis, especially when comparing vertical workflow testing systems against runtime-first Agent projects

## Classification

- Primary label: `vertical-workflow`
- Secondary label: `RAG-first`
- Secondary label: `human-in-the-loop`

## Core Identity

- PRD-to-test-case generation workflow product
- Streamlit workbench rather than general-purpose Agent runtime
- prompt-heavy and UI-centric orchestration
- local ChromaDB retrieval with Gemini/Qwen-backed generation
- includes human refinement and AI evaluator loop

## Strongest Layers

- prompt as SOP / procedure encoding
- RAG as constraint injection for generation
- human-in-the-loop editing loop
- evaluator / critic layer
- asset archival back into history cases

## Weakest Layers

- no formal function calling runtime
- no true tool schema / model-directed tool loop
- workflow mostly concentrated in `ui/main.py`
- memory is mostly session state + retrievable case storage, not learning memory
- RAG is lightweight vector retrieval plus LLM filtering, not full industrial retrieval architecture

## Implementation Signals

- `config/prompts.py`
  main control plane is in prompts
- `ui/main.py`
  orchestration center is the Streamlit UI layer
- `core/rag_engine.py`
  ChromaDB with `history_cases` and `company_knowledge`
- `core/llm_client.py`
  provider switching across Gemini and Qwen
- `core/evaluator.py`
  separate QA critic prompt path

## Reusable Lessons

- Vertical Agent systems often gain more from procedure encoding than from high autonomy
- In testing workflows, structured artifact output matters more than chat elegance
- “RAG for constraint” is a distinct and useful pattern from “RAG for QA”
- Human refinement plus AI critique is a strong pattern for quality-sensitive asset generation
- Storing historical artifacts is not yet the same as having a real memory system

## Recommended Reuse Scenarios

- analyzing test generation products
- designing domain-specific workflow agents
- comparing prompt-centric workflows against runtime-centric agents
- designing AI copilot workbenches where human review remains central
