# Continual Learning Architecture

> **Status:** Research & Planning
> **Goal:** Seamless learning capture that makes us better over time
> **Blocker:** Hooks not firing reliably

---

## Research Findings

### Clawdbot's Approach

Source: [Clawdbot Memory System Deep Dive](https://avasdream.com/blog/clawdbot-memory-system-deep-dive)

**Two-layer memory:**
1. **Daily journals** (`memory/YYYY-MM-DD.md`) - append-only raw capture
2. **Curated `MEMORY.md`** - distilled long-term knowledge

**File structure:**
```
~/clawd/
├── AGENTS.md          # Operating instructions (bootstrap)
├── SOUL.md            # Persona and boundaries (bootstrap)
├── USER.md            # User profile (bootstrap)
├── IDENTITY.md        # Agent identity (bootstrap)
├── MEMORY.md          # Curated long-term knowledge (bootstrap)
├── HEARTBEAT.md       # Periodic task checklist (bootstrap)
└── memory/
    ├── 2026-01-15.md  # Daily journal (append-only)
    ├── 2026-01-16.md
    └── ...
```

**Key mechanisms:**
- **Pre-compaction flush hook** - When context approaches capacity, agent gets one silent turn to persist critical insights before compression
- **Hybrid search** - SQLite with vector (70%) + keyword (30%) retrieval
- **Chunking** - 400 tokens with 80-token overlap for indexing
- Bootstrap files injected into system prompt at session start (truncated at 20k chars each)
- Plain markdown files, Git-compatible, human-readable

**Retrieval tools:**
- `memory_search` - Semantic search across all memory markdown
- `memory_get` - Read specific lines from memory files

---

### Claude Code Persistent Memory

Source: [Dev.to Architecture Article](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d)

**Two-tier structure:**
1. **CLAUDE.md** (~150 lines) - compact briefing, auto-loaded natively
2. **.memory/state.json** - full repository, accessed via MCP tools

**Memory types with decay:**
- **Permanent** - Architecture, design decisions, patterns (retain indefinitely)
- **Decaying** - Progress notes (7-day half-life), contextual info (30-day half-life)

**Hooks fire at three points:**
- `Stop` - After each response
- `PreCompact` - Before context compression
- `SessionEnd` - When session terminates

**Retrieval via MCP:**
- `memory_search` - Keyword-based retrieval
- `memory_related` - Tag-filtered topic exploration
- `memory_ask` - Natural language queries via Haiku

---

## Our Architecture Plan

### Two Types of Journals (Important Distinction)

| Type | Purpose | Style | Location |
|------|---------|-------|----------|
| **Raw Memory Journals** | Capture everything that happened | Granular, dry, factual | `~/.claude/memory/YYYY-MM-DD.md` |
| **AI Journal** | Future AI memories | Personality, growth, stories | `ai-journal/entries/YYYY/` |

**Raw Memory Journals** = What Clawdbot does. Account of decisions, learnings, context. Machine-readable. For retrieval.

**AI Journal** = Our existing project. Written BY AI FOR future AI. Not dry. About personality and growth. Human-readable stories.

These are complementary, not competing:
- Raw journals feed the learning system
- AI Journal entries are crafted reflections (only when Erik asks)

### Proposed File Structure

```
$PROJECTS_ROOT/
├── .claude/
│   ├── memory/
│   │   ├── 2026-02-01.md      # Raw daily journal (auto-captured)
│   │   ├── 2026-02-02.md
│   │   └── ...
│   ├── MEMORY.md              # Distilled long-term knowledge
│   └── hooks/
│       └── pre-compact.sh     # Trigger learning capture
├── ai-journal/
│   └── entries/2026/          # Crafted AI reflections (manual)
└── project-scaffolding/
    └── Documents/reference/
        └── LEARNINGS.md       # Cross-project pattern documentation
```

### Components Needed

| Component | Purpose | Status |
|-----------|---------|--------|
| Hook infrastructure | Fire at key moments | ✅ Working (PreCompact, Stop) |
| Daily journal capture | Raw append-only logs | Not built - need capture logic |
| PreCompact capture | Extract learnings before compression | Hook fires, needs capture code |
| Task completion capture | "Did you learn anything?" | Hook fires, needs capture code |
| Distillation process | Journals → MEMORY.md | Not built |
| Search/retrieval | Find relevant memories | Could use grepai |

---

## Hooks Status: WORKING

### What We Have (as of 2026-02-01)

**Hooks ARE configured and firing:**

```
$PROJECTS_ROOT/.claude/settings.json
├── PostToolUse (Write, Edit) → validators
├── Stop → 00_Index-reminder.py
└── PreCompact → pre-compact-journal-reminder.py
```

**Evidence from logs:**
- `PreCompact` fired 2026-02-01 19:18:14 (auto trigger, 801 messages)
- `Stop` fired 6+ times on 2026-02-01 (after each Claude response)

**Current behavior:**
- Hooks output REMINDERS to stderr
- They do NOT capture learnings/memories yet
- They're "nudges" not "automation"

### What We Need to Build

The hooks work. Now we need capture logic:

1. **PreCompact hook** should:
   - Extract key decisions/learnings from transcript
   - Append to `~/.claude/memory/YYYY-MM-DD.md`
   - Could use Haiku to summarize (like the articles suggest)

2. **Stop hook** (or new PostTask hook) should:
   - After task completion, prompt: "What did you learn?"
   - Append to daily journal

3. **SessionEnd hook** could:
   - Final summary of session
   - Update MEMORY.md with distilled insights

---

## Cross-Platform Problem

**This architecture is Claude Code specific.**

| Platform | Hooks? | Memory System? |
|----------|--------|----------------|
| Claude Code | Yes (if we can get them working) | Can build |
| Cursor | Different mechanism (rules, .cursorrules) | Would need separate approach |
| Antigravity (Gemini CLI) | Unknown | Would need separate approach |

### Options for Cross-Platform

1. **Claude-only** - Accept that continual learning only works in Claude Code
2. **Shared storage, separate triggers** - All platforms write to same memory files, but each has its own capture mechanism
3. **MCP-based** - Build an MCP server that all platforms can use (if they support MCP)
4. **Manual capture** - `/learn` command that works everywhere (no automation)

**Task #4690** (Cross-platform skill sharing) is related - if we solve memory for one platform, we need to think about the others.

---

## Implementation Phases

### Phase 1: Hooks ✅ DONE
- [x] Hooks are configured and firing (PreCompact, Stop)
- [x] Logging confirms they execute
- [ ] Need to upgrade from "reminders" to "capture"

### Phase 2: Raw Journal Capture (CURRENT)
- [ ] Hook writes to `~/.claude/memory/YYYY-MM-DD.md`
- [ ] Append-only format with timestamps
- [ ] Capture: decisions made, learnings, context

### Phase 3: Retrieval
- [ ] Search tool (could extend grepai or build MCP)
- [ ] Bootstrap injection of recent context at session start

### Phase 4: Distillation
- [ ] Periodic process to distill journals → MEMORY.md
- [ ] Decay old entries, promote patterns

### Phase 5: Cross-Platform (Future)
- [ ] Evaluate Cursor/Antigravity options
- [ ] Shared memory storage if possible

---

## Related Tasks

- **#4629** - Upgrade learning loop / add /compound skill
- **#4690** - Cross-platform skill sharing for Antigravity/Cursor/Ollama
- **#4584** - Claude Memory Project (full architecture)

---

## References

- [Clawdbot Memory Deep Dive](https://avasdream.com/blog/clawdbot-memory-system-deep-dive)
- [Claude Code Persistent Memory Architecture](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d)
- [Claude Diary Plugin](https://rlancemartin.github.io/2025/12/01/claude_diary/)
- [MemU - Persistent Memory](https://medium.com/@memU_ai/claudes-persistent-memory-is-coming-we-ve-already-built-it-48395e8c5ece)
