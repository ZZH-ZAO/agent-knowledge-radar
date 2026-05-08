# Hermes Agent Condensed Notes

## Project Summary

- Project name: `hermes-agent`
- Project path: `D:\hermes-agent`
- Document type: `agent`
- Purpose: compressed reusable notes for future comparison and design work

## System Type

- long-running general-purpose agent workbench
- memory-first and multi-surface agent system
- mixes product use, infrastructure concerns, and research/training support

## Real Architectural Character

- not just a CLI coding assistant
- not just a messaging bot
- not just a research harness
- combines CLI, gateway, TUI, ACP, memory, skills, cron, delegation, MCP, remote environments, and RL-oriented data paths into one substrate

## Strongest Design Areas

### 1. Multi-surface entry model

- CLI
- messaging gateway
- Ink TUI + Python JSON-RPC backend
- ACP editor integration

Evidence:

- `cli.py`
- `gateway/run.py`
- `ui-tui/`
- `tui_gateway/`
- `acp_adapter/`

### 2. Memory-first architecture

- builtin + external memory provider model
- fenced memory-context injection
- persistent session store
- FTS5 cross-session search

Evidence:

- `agent/memory_manager.py`
- `tools/memory_tool.py`
- `hermes_state.py`

### 3. Skills as growing assets

- large skill library
- Skills Hub browse/search/install workflow
- skills positioned as reusable procedural memory

Evidence:

- `skills/`
- `optional-skills/`
- `hermes_cli/skills_hub.py`
- `README.md`

### 4. Long-running agent direction

- scheduled automation
- cross-platform continuity
- persistent / remote terminal backends
- cloud-capable environments

Evidence:

- `cron/scheduler.py`
- `gateway/platforms/`
- `tools/environments/`
- `README.md`

### 5. Formal delegation

- isolated child agents
- restricted child toolsets
- concurrency / timeout / depth governance
- side-effect and memory-write blocking for children

Evidence:

- `tools/delegate_tool.py`

### 6. Unified tool and MCP expansion

- central tool registry / toolsets
- MCP as formal external capability bus
- stdio + HTTP MCP support
- reconnect, sanitization, sampling support

Evidence:

- `model_tools.py`
- `toolsets.py`
- `tools/registry.py`
- `tools/mcp_tool.py`

### 7. Research-ready runtime

- trajectory generation
- trajectory compression
- Atropos environment integration
- RL/eval support sharing the same tool-calling substrate

Evidence:

- `batch_runner.py`
- `trajectory_compressor.py`
- `environments/`
- `tinker-atropos/`

## Main Reusable Lessons

- A serious long-running agent needs more than a chat loop: it needs memory, search, scheduling, and environment persistence.
- Multiple UX surfaces can share one agent substrate if session, config, and tool layers are kept unified.
- Skills are more powerful when treated as installable procedural assets rather than static prompt text.
- Delegation should be governed by isolation, depth limits, and restricted side effects, not only by spawn mechanics.
- If future training or eval matters, build trajectory capture and environment hooks into the runtime early.

## Best Use As A Reference

- designing long-running personal or team agents
- building memory-first agent systems
- combining CLI + messaging + editor surfaces on one runtime
- studying how product usage and RL/eval pipelines can share a common agent substrate
