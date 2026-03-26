# Antigravity Orchestration Patterns

purpose: Rules for Floor Manager (Antigravity/Gemini) multi-agent orchestration
scope: Patterns observed and adopted for Gemini-based agent coordination

## Supervisor-Subagent Pattern

rule: spawn specialized sub-agents for high-noise domains (web search, long file reads, DOM parsing)
rule: sub-agent gets tailored toolset and context — keeps main agent context clean
benefit: prevents context explosion from domain-specific noise

## Contract-Driven Handoff

rule: agents communicate through standardized artifacts in _handoff/
flow: PROPOSAL_FINAL.md (strategic) -> TASK_CONTRACT.json (contract) -> WORKER_DRAFT.md (tactical)
benefit: async collaboration with permanent audit trail

## MCP Delegation

rule: prefer delegating to MCP tools over raw shell commands
rule: tools evolve independently of core model logic — decouple brain from hands

## Tiered Model Routing

rule: match model intelligence to task complexity
tier_strategic: Claude Sonnet/Opus — architecture, reasoning, judging
tier_tactical: Gemini Flash — orchestration, coordination, long-context parsing
tier_implementation: Qwen Coder — code generation, small patches
tier_review: DeepSeek R1 — troubleshooting, security audits

## Floor Manager Usage Rules

rule: be tool-first — prefer MCP tools over raw commands
rule: spawn sub-agents early for high-noise tasks
rule: monitor MCP heartbeats — tool failure signals architecture issue, not just retry

---
version: 2.0.0
established: 2026-02-01
updated: 2026-03-26 — trimmed from 64 lines, removed comparison table and generic advice
