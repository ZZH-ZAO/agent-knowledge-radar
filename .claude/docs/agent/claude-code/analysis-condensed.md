# Claude Code Condensed Notes

## Project Summary

- Project name: `claude-code`
- Project path: `D:\claude-code`
- Document type: `agent`
- Purpose: compressed reusable notes for future architectural comparison and design recall

## System Type

- platform-expansion agent system
- Claude Code style runtime extended toward product/platform capabilities

## Real Architectural Character

- shares a similar runtime family with `claude-code-sourcemap`
- but its center of gravity is no longer just runtime clarity
- its main question is how a working agent runtime becomes a governed product platform

## Strongest Design Areas

### 1. Feature gating maturity

- build-time feature flags
- runtime GrowthBook gates
- staged rollout and remote kill-switch thinking
- repeated emphasis on safe activation rather than unconditional exposure

Evidence:

- `src/assistant/gate.ts`
- `src/bridge/bridgeEnabled.ts`
- `src/bootstrap/state.ts`
- `src/cli/print.ts`

### 2. Persistent / proactive agent direction

- `KAIROS`
- `PROACTIVE`
- `SleepTool`
- tick/background/session-continuation thinking

Evidence:

- `src/assistant/gate.ts`
- `src/cli/print.ts`
- `src/utils/sessionStorage.ts`
- `src/utils/systemPrompt.ts`

### 3. Team memory as infrastructure

- memory moves beyond user preferences
- team-shared knowledge pathing and file hooks
- starts treating memory as organizational asset infrastructure

Evidence:

- `src/utils/sessionFileAccessHooks.ts`

### 4. Remote control and multi-instance coordination

- bridge mode
- remote session control
- pipes / UDS / peer messaging
- moves toward an agent control-plane model

Evidence:

- `src/bridge/bridgeApi.ts`
- `src/bridge/bridgeEnabled.ts`
- `src/cli/remoteIO.ts`
- `src/utils/udsClient.ts`
- `src/utils/udsMessaging.ts`

### 5. Product-layer observability

- Sentry
- OpenTelemetry
- Langfuse
- GrowthBook

Evidence:

- `src/utils/sentry.ts`
- `src/utils/telemetry/instrumentation.ts`
- `src/utils/telemetry/sessionTracing.ts`
- `package.json`

### 6. Safety and governance

- classifier-based approval logic
- fail-closed orientation
- runtime kill-switches
- rollout-aware capability isolation

Evidence:

- `src/utils/permissions/yoloClassifier.ts`
- `src/cli/handlers/autoMode.ts`
- `src/utils/settings/settings.ts`
- `src/utils/settings/types.ts`

## Main Reusable Lessons

- Treat advanced agent features as rollout and governance problems, not only implementation problems.
- Persistent agents require pacing, interruption, and permission design, not just background loops.
- Team memory becomes infrastructure once multiple humans and sessions share it.
- Remote control and multi-instance communication push an agent from runtime into control-plane territory.
- Observability and feature gating are first-class architecture concerns in serious agent products.

## Best Use As A Reference

- studying how a runtime becomes a platform
- designing feature-flag-heavy agent systems
- exploring persistent / proactive / remote-control agent directions
- thinking about team memory and product governance after core runtime is already stable
