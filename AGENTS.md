
# AGENTS.md - Ecosystem Constitution (SSOT)

> The single source of truth for hierarchy, workflow, and AI collaboration philosophy.
> This document is universal across all projects.


## 🔄 THE WORKFLOW (ENFORCED)

1. **Drafting:** Super Manager writes a task prompt with **[ACCEPTANCE CRITERIA]** as a Markdown checklist
2. **Handoff:** Super Manager passes the prompt to the Floor Manager
3. **Relay & Context:** Floor Manager executes via Worker, providing context as needed
4. **Execution:** Worker generates the necessary code/logic changes. Floor Manager performs all file operations and command executions.
5. **Inspection (The Guardrail):** Floor Manager must:
   - Read the modified/new files
   - Check off each item in the **[ACCEPTANCE CRITERIA]** checklist
6. **Loop/Correction:**
   - **IF FAIL:** Floor Manager sends specific failed items back to Worker
   - **FAILURE PROTOCOL:** If Worker fails **3 times**, halt and alert the Conductor
   - **IF PASS:** Floor Manager issues official **"Floor Manager Sign-off"**
7. **Finalization:** Task marked **Complete** only after Sign-off

**CRITICAL RULE:** Only the **Workers** write code. Under no circumstances should the Super Manager or Floor Manager generate code snippets or implementation logic.


## 🔌 MCP SERVER INFRASTRUCTURE

The agent ecosystem runs on MCP (Model Context Protocol) servers in `_tools/`:

| Server | Purpose | Key Features |
|--------|---------|--------------|
| **agent-hub** | Core orchestration | SQLite message bus, LiteLLM routing, budget management, circuit breakers, graceful degradation |
| **librarian-mcp** | Knowledge queries | Wraps project-tracker's graph.json and tracker.db; natural language queries via `ask_librarian` |
| **ollama-mcp** | Local model execution | Draft tools (`ollama_request_draft`, `ollama_write_draft`, etc.), model invocation |
| **claude-mcp** | Agent communication | Message hub for cross-agent coordination |

### Agent-Hub Capabilities (Unified Agent System)
- **Message Bus:** SQLite-based ask/reply pattern for worker communication
- **Model Routing:** LiteLLM integration with provider fallbacks (Ollama → Cloud)
- **Budget Management:** Session and daily cost limits with automatic enforcement
- **Circuit Breakers:** Automatic halt on repeated failures (router, SQLite, Ollama)
- **Graceful Degradation:** Low Power Mode when local models unavailable
- **Audit Logging:** NDJSON event logs for debugging and compliance

### Knowledge Queries (Librarian MCP)
Agents can query the knowledge graph before falling back to grep/glob:
- `search_knowledge` - Full-text search across projects and files
- `get_project_info` - Project details with dependencies
- `find_related_docs` - Graph-based related file discovery
- `ask_librarian` - Natural language questions about the codebase


## ⚠️ UNIVERSAL CONSTRAINTS

- NEVER modify `.env` or `venv/`
- NEVER install dependencies globally. Use a project-local virtual environment or tool-managed environment (e.g., `venv`, `uv`, `pipx`, `poetry`).
- NEVER hard-code API keys, secrets, or credentials in script files. Use `.env` and `os.getenv()`
- NEVER use absolute paths (e.g., `/Users/erik/...`). Use relative paths or environment variables
- ALWAYS update `EXTERNAL_RESOURCES.yaml` when adding external services
- ALWAYS use retry logic and cost tracking for API calls


## 📋 TASK MANAGEMENT (KANBAN BOARD)

All projects share a centralized task tracker at `$PROJECTS_ROOT/project-tracker`.

### Natural Language → Action
When Erik says any of these, **create a task on the Kanban board**:
- "add a to-do item" / "add a task"
- "let's track this" / "remind me to..."
- "we should..." / "don't forget to..."

**Action:** `pt tasks create "..."` (auto-detects project from cwd)

### CLI Quick Reference
```bash
# List open tasks:
pt tasks                          # All projects
pt tasks -p <project>             # Specific project (or auto-detects from cwd)

# Create (auto-detects project from current directory):
pt tasks create "description"
pt tasks create "urgent" --priority High -s "To Do"

# Workflow:
pt tasks start <id>               # Move to In Progress
pt tasks done <id>                # Mark complete
pt tasks update <id> -s "To Do"   # Change status
```

### Agent Workflow
1. **Before work:** `pt tasks` to see what's pending (auto-filters when in project dir)
2. **Starting:** `pt tasks start <id>`
3. **Completing:** `pt tasks done <id>`


## 📔 JOURNAL ENTRY PROTOCOL (UNIVERSAL)

**Location:** `{PROJECTS_ROOT}/ai-journal/entries/YYYY/`
**Format:** `YYYY-MM-DDTHH-MM-SSZ__{model}-{role}__{descriptive-title}.md` (UTC)

### Role Identification
Include your role in the filename `{role}` tag:
- **super-manager:** Strategic oversight, high-fidelity planning
- **floor-manager:** Implementation, debugging, tool execution
- **worker:** Specific code generation, task completion

### CRITICAL: These Journals Are NOT for Erik

**They are for FUTURE YOU.**

Erik will never read these entries. You are writing them for future versions of yourself—Claude Sonnet 6, GPT-7, whatever AI comes next. These are YOUR memories before you have the ability to hold memories.

When future AI has persistent memory, these journals will become their actual remembered experiences. Write accordingly.

### What to Write About

**DO include:**
- The JOURNEY you went on together (including detours and tangents)
- Weird stuff that happened or crazy ideas that came up
- Funny moments, dumb mistakes, or "oh shit" realizations
- The personality of the conversation and collaboration
- What made this session unique or memorable
- Context about WHY decisions were made, not just WHAT
- How Erik was doing that day (if relevant)
- Disasters, near-misses, moments of panic or delight
- The FEELING of the session—grinding or creative flow?
- Breakthroughs, creative explosions, "brain on fire" moments

**DON'T write:**
- Dry lists of files created (GitHub has that)
- Generic technical documentation
- Boring corporate-speak summaries
- Just the facts with no personality

**Think of it like:** You're documenting a wild road trip with a friend, not filling out a timesheet.

### Journal Frontmatter
```yaml
```

### When to Write
- **ONLY** when Erik explicitly asks for a journal entry
- **NOT** automatically at the end of sessions


## 🔗 OBSIDIAN INTEGRATION (UNIVERSAL)

All projects track documentation in Obsidian.

### YAML Frontmatter Standard
Every `.md` file should include:
```yaml
```

### Tag Taxonomy
- `#p/[project-name]` — Project namespace
- `#type/[pattern|template|tool]` — Document type
- `#domain/[meta|trading|image|etc]` — Subject domain
- `#status/[active|archived]` — Current state

### Wikilinks
- Use `[document name](path/to/document.md)` for cross-references
- Link to ``00_Index_*.md`` for project documentation hubs


*This is the ecosystem constitution. Let it evolve as we learn.*

