# Project Structure Standards

> **Purpose:** Establish consistent directory structure and file placement across all projects  
> **Last Updated:** January 15, 2026

---

## Core Principle

**Convention over configuration** - Projects should follow a predictable structure so anyone (human or AI) can navigate them instantly.

---

## Standard Directory Structure

### Python Projects

```
project-name/
├── venv/                      # Virtual environment (in project root)
├── scripts/                   # All executable scripts
│   ├── script1.py
│   ├── script2.py
│   └── utils/                # Script utilities
├── data/                      # Data files, databases
├── Documents/                      # Documentation
├── templates/                 # Templates (if applicable)
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── TODO.md                    # Task tracking
└── .gitignore                # Ignore venv/, data/, etc.
```

**Key rules:**
- ✅ **Virtual environment in root:** `venv/` at top level (see [[VENV_LOCATION_STANDARD]])
- ✅ **Scripts in scripts/:** All executable code in `scripts/`
- ✅ **Data isolated:** `data/` for all data files
- ✅ **Documentation clear:** `Documents/` for detailed docs (see [[DOCUMENTATION_HYGIENE]])

### Web Projects (React/Next.js)

```
project-name/
├── node_modules/             # Dependencies (gitignored)
├── src/                      # Source code
│   ├── components/
│   ├── pages/
│   └── utils/
├── public/                   # Static assets
├── scripts/                  # Build scripts, utilities
├── Documents/                     # Documentation
├── package.json              # Node dependencies
├── README.md
├── TODO.md
└── .gitignore
```

### Hybrid Projects (Python Backend + React Frontend)

```
project-name/
├── venv/                     # Python virtual environment
├── backend/                  # Python/FastAPI backend
├── frontend/                 # React frontend
├── scripts/                  # Deployment, utilities
├── data/                     # Databases, local data
├── Documents/                     # Documentation
├── requirements.txt          # Python dependencies
├── README.md
├── TODO.md
└── .gitignore
```

---

## Documentation Structure

**Standard docs layout:**

```
Documents/
├── README.md               # Docs index (Grand Central Station) - See [[DOCUMENTATION_HYGIENE]]
├── ARCHITECTURE.md         # Core Architecture (at root of Documents/)
├── OPERATIONS.md           # Core Operations (at root of Documents/)
├── DATA_MODEL.md           # Core Data Model (at root of Documents/)
├── guides/                 # How-to guides
├── reference/              # Reference docs
├── safety/                 # Safety systems
└── archives/               # Historical docs (See [[ARCHIVE_POLICY]])
```

---

## Portability Rule

- **NEVER** use absolute paths (e.g., `/USER_HOME/...`) in scripts or configs.
- **ALWAYS** use relative paths or environment variables like `PROJECT_ROOT` to ensure the project is portable across different machines and environments (RunPod, CI/CD).
- **Rule of Thumb:** If the path starts with `/USER_HOME/`, it's a bug.

---

## Code Review Standards

Code reviews are critical for maintaining quality. **All** reviews **MUST** adhere to the following:

- [ ] Active code review exists in project root (follows `CODE_REVIEW_{REVIEWER}_{VERSION}.md` naming)
- [ ] Previous reviews archived in `Documents/archives/reviews/`
- [ ] All reviews include a **Definition of Done (DoD)** - See [[CODE_REVIEW_PROMPT]]
- [ ] Review IDs present in frontmatter for traceability - See [[WARDEN_LOG]]

---

## Master Compliance Checklist

**Every project MUST meet these requirements to be considered "scaffolded":**

- [ ] **`00_Index_[ProjectName].md`** - Obsidian index with status tags.
- [ ] **`AGENTS.md`** - Universal source of truth for AI agents (DoD, Tech Stack).
- [ ] **`CLAUDE.md`** - Project-specific AI instructions.
- [ ] **`.cursorrules`** - Behavioral configuration for Cursor AI.
- [ ] **`TODO.md`** - Task tracking following [[TODO_FORMAT_STANDARD]].
- [ ] **`Documents/`** directory - Centralized documentation following this standard.

---

*See also: [[PROJECT_KICKOFF_GUIDE]] for new projects and [[CODE_QUALITY_STANDARDS]] for quality rules.*

## Related Documentation

- [[CODE_REVIEW_ANTI_PATTERNS]] - code review
- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure
- [[architecture_patterns]] - architecture
- [[cloud_gpu_setup]] - cloud GPU
- [[dashboard_architecture]] - dashboard/UI
- [[database_schema]] - database design
- [[adult_business_compliance]] - adult industry
- [[ai_model_comparison]] - AI models
- [[database_setup]] - database
- [[deployment_patterns]] - deployment
