# Ollama MCP Enhancement: Retry & Escalation Tracking

> **Type:** Technical Specification
> **Author:** Super Manager (Claude)
> **Date:** January 10, 2026
> **Target Project:** ollama-mcp (TypeScript)
> **Status:** Draft for Review

---

## Problem Statement

Currently, escalation protocol (3-Strike Rule) relies on Floor Manager following instructions:
- User must remember to say "stop if timeout"
- Floor Manager must remember to halt after 3 failures
- No structural enforcement - relies entirely on prompt compliance

**This is a single point of failure.** If the Floor Manager forgets or misinterprets, Workers can spin indefinitely.

---

## Proposed Solution

Add retry tracking and automatic escalation signaling to `ollama_run()` at the MCP level.

---

## Current State (server.ts)

```typescript
// Existing constants
const DEFAULT_TIMEOUT_MS = 120000; // 120s
const DEFAULT_CONCURRENCY = 3;
const MAX_CONCURRENCY = 8;

// Existing telemetry fields
logRun({
  timestamp: startTime,
  model,
  duration_ms: durationMs,
  exit_code: timedOut ? -1 : (code ?? -1),
  output_chars: stdout.length,
  timed_out: timedOut,
  batch_id: batchId,
  concurrency: concurrency,
});
```

---

## Proposed Changes

### 1. New Parameters for `ollama_run`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_retries` | number | 3 | Maximum retry attempts before escalation signal |
| `retry_count` | number | 0 | Current retry count (passed by caller) |
| `task_id` | string | undefined | Optional identifier to track retries across calls |

### 2. Enhanced Response Structure

**Current response:**
```typescript
{
  content: [{ type: "text", text: stdout }]
}
```

**Proposed response:**
```typescript
{
  content: [{ type: "text", text: stdout }],
  metadata: {
    timed_out: boolean,
    duration_ms: number,
    retry_count: number,
    escalate: boolean,        // TRUE when max_retries exceeded
    escalation_reason?: string // "timeout" | "error" | "max_retries_exceeded"
  }
}
```

### 3. Escalation Signaling Logic

```
IF timed_out AND retry_count >= max_retries:
  metadata.escalate = true
  metadata.escalation_reason = "max_retries_exceeded"

IF timed_out AND retry_count < max_retries:
  metadata.escalate = false
  // Floor Manager can retry

IF NOT timed_out:
  metadata.escalate = false
  // Success - no escalation needed
```

### 4. Enhanced Telemetry

Add to `runs.jsonl`:
```typescript
logRun({
  // ... existing fields ...
  task_id: taskId,
  retry_count: retryCount,
  max_retries: maxRetries,
  escalate: shouldEscalate,
  escalation_reason: reason,
});
```

---

## Usage Example (Floor Manager Perspective)

```
// First attempt
ollama_run({
  model: "deepseek-r1",
  prompt: "...",
  timeout: 120000,
  max_retries: 3,
  retry_count: 0,
  task_id: "global-rules-1a"
})

// Response if timeout:
{
  content: [{ type: "text", text: "..." }],
  metadata: {
    timed_out: true,
    retry_count: 0,
    escalate: false  // Can still retry
  }
}

// After 3rd timeout:
{
  content: [{ type: "text", text: "..." }],
  metadata: {
    timed_out: true,
    retry_count: 3,
    escalate: true,  // MUST STOP
    escalation_reason: "max_retries_exceeded"
  }
}
```

---

## Circuit Breaker Pattern (Future Enhancement)

Track failure rates per model across tasks:

```typescript
// In-memory or file-based tracking
modelHealth: {
  "deepseek-r1": {
    recent_failures: 3,
    recent_successes: 1,
    circuit_state: "half-open" | "open" | "closed"
  }
}
```

When circuit is "open", all requests to that model immediately return:
```typescript
{
  metadata: {
    escalate: true,
    escalation_reason: "circuit_open",
    message: "Model deepseek-r1 has failed 5 consecutive tasks. Circuit breaker open."
  }
}
```

**This is a v2 feature** - focus on basic retry/escalation first.

---

## Implementation Phases

### Phase 1: Core Retry Tracking (Minimal Change)
- Add `retry_count` parameter
- Add `escalate` field to response
- Update telemetry logging

### Phase 2: Task ID Persistence
- Add `task_id` parameter
- Track retries across calls for same task
- Store in telemetry for analytics

### Phase 3: Circuit Breaker (v2)
- Track model health across tasks
- Automatic circuit opening/closing
- Dashboard for model reliability metrics

---

## Why This Matters

| Without Enhancement | With Enhancement |
|---------------------|------------------|
| Floor Manager must remember "stop if timeout" | MCP signals when to stop |
| Escalation is prompt-based (fragile) | Escalation is structural (enforced) |
| No visibility into retry patterns | Telemetry shows all retry attempts |
| Floor Manager can ignore rules | `escalate: true` is undeniable signal |

---

## Acceptance Criteria

- [ ] `ollama_run` accepts `max_retries` parameter (default: 3)
- [ ] `ollama_run` accepts `retry_count` parameter (default: 0)
- [ ] Response includes `metadata.escalate` boolean
- [ ] Response includes `metadata.escalation_reason` when escalating
- [ ] Telemetry logs retry_count and escalate fields
- [ ] Floor Manager can rely on `escalate: true` to know when to halt

---

## Open Questions

1. **Who increments retry_count?**
   - Option A: Caller (Floor Manager) tracks and passes
   - Option B: MCP tracks internally by task_id
   - **Recommendation:** Option A for Phase 1 (simpler), Option B for Phase 2

2. **What happens if max_retries=0?**
   - Never escalate? Always escalate on first failure?
   - **Recommendation:** 0 means "no limit" (backward compatible)

3. **Should escalation be a hard block or just a signal?**
   - Hard block: MCP refuses to run after max_retries
   - Signal: MCP runs but flags escalate=true
   - **Recommendation:** Signal only - Floor Manager decides action

---

## Related Documents

- [AGENTS](../../../../AGENTS.md) - 3-Strike Escalation Rule
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - Timeout patterns
- [learning-loop-pattern](../../../../writing/Documents/patterns/learning-loop-pattern.md) - Structural enforcement rationale

---

*This spec is ready for Conductor review before implementation.*

## Related Documentation

- [Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md) - prompt engineering
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [Safety Systems](patterns/safety-systems.md) - security
