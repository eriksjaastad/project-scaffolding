# Project Structure Standards

> **Purpose:** Establish consistent directory structure and file placement across all projects  
> **Last Updated:** December 30, 2025

---

## Core Principle

**Convention over configuration** - Projects should follow a predictable structure so anyone (human or AI) can navigate them instantly.

---

## Standard Directory Structure

### Python Projects

```
project-name/
├── venv/                      # Virtual environment (in root)
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
- ✅ **Virtual environment in root:** `venv/` at top level
- ✅ **Scripts in scripts/:** All executable code in `scripts/`
- ✅ **Data isolated:** `data/` for all data files
- ✅ **Documentation clear:** `Documents/` for detailed docs

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

**Key rules:**
- ✅ **Standard React structure:** Follow Create React App / Next.js conventions
- ✅ **Scripts separate:** Build scripts in `scripts/`, source in `src/`
- ✅ **Documentation clear:** `Documents/` for detailed docs

### Hybrid Projects (Python Backend + React Frontend)

```
project-name/
├── venv/                     # Python virtual environment
├── backend/                  # Python/FastAPI backend
│   ├── api/
│   ├── db/
│   └── utils/
├── frontend/                 # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── scripts/                  # Deployment, utilities
├── data/                     # Databases, local data
├── Documents/                     # Documentation
├── requirements.txt          # Python dependencies
├── README.md
├── TODO.md
└── .gitignore
```

---

## Virtual Environment Location

### Python Projects

**Rule:** Virtual environment MUST be in project root as `venv/`

**Why:**
- Standard Python convention
- Easy to find and activate
- Clear separation from code
- Consistent across all projects

**Correct:**
```
project-name/
├── venv/           ← Virtual environment here
├── scripts/        ← Code here
└── requirements.txt
```

**Incorrect:**
```
project-name/
└── scripts/
    ├── venv/       ← ❌ NO - Don't bury venv in scripts
    └── code.py
```

**Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add to .gitignore
echo "venv/" >> .gitignore
```

### Node.js Projects

**Rule:** `node_modules/` in project root (standard)

```
project-name/
├── node_modules/   ← Dependencies here
├── src/            ← Code here
└── package.json
```

---

## Scripts Directory

**Rule:** All executable scripts go in `scripts/`

**What belongs in scripts/:**
- ✅ CLI tools
- ✅ Utility scripts
- ✅ Automation scripts
- ✅ Deployment scripts
- ✅ Data processing scripts

**What doesn't belong in scripts/:**
- ❌ Virtual environment (goes in root)
- ❌ Data files (goes in `data/`)
- ❌ Documentation (goes in `Documents/`)
- ❌ Configuration (goes in root or dedicated config dir)

**Example:**
```
scripts/
├── backup.py           # Backup utility
├── deploy.sh           # Deployment script
├── process_data.py     # Data processing
└── utils/              # Shared utilities
    ├── logger.py
    └── helpers.py
```

---

## Documentation Structure

**Standard docs layout:**

```
Documents/
├── README.md               # Docs index
├── core/                   # Core documentation
│   ├── ARCHITECTURE.md
│   ├── OPERATIONS.md
│   └── DATA_MODEL.md
├── guides/                 # How-to guides
│   ├── SETUP.md
│   └── DEPLOYMENT.md
├── reference/              # Reference docs
│   ├── API.md
│   └── CLI.md
├── safety/                 # Safety systems
│   └── DISASTER_RECOVERY.md
└── archives/               # Historical docs
    └── sessions/
```

---

## Data Directory

**Rule:** All data files in `data/`

**What goes in data/:**
- ✅ SQLite databases
- ✅ JSON/CSV files
- ✅ Local caches
- ✅ Generated files

**Structure:**
```
data/
├── databases/
│   └── tracker.db
├── cache/
│   └── temp_data.json
└── generated/
    └── reports/
```

**Important:**
- Always gitignore `data/` unless explicitly needed in repo
- Document data structure in `Documents/core/DATA_MODEL.md`
- Provide sample data in `data/samples/` if needed

---

## Configuration Files

**Location:** Project root (for discoverability)

**Standard config files:**
```
project-name/
├── .env                    # Environment variables (gitignored)
├── .env.example            # Example env vars (committed)
├── .gitignore              # Git ignore rules
├── .cursorrules            # Cursor AI rules
├── requirements.txt        # Python dependencies
├── package.json            # Node dependencies
├── pytest.ini              # Test configuration
└── README.md               # Project overview
```

**⚠️ Portability Rule:**
- **NEVER** use absolute paths (e.g., `/USER_HOME/...`) in scripts or configs.
- **ALWAYS** use relative paths or environment variables like `PROJECT_ROOT` to ensure the project is portable across different machines and environments (RunPod, CI/CD).
- **Rule of Thumb:** If the path starts with `/USER_HOME/`, it's a bug.

---

## Templates

**Location:** `templates/` in root

**When to use:**
- Projects that generate files
- Scaffolding tools
- Email/report templates
- Configuration templates

**Example:**
```
templates/
├── README.md.template
├── TODO.md.template
├── email_template.html
└── report_template.md
```

---

## Testing

**Python:**
```
tests/
├── __init__.py
├── test_core.py
├── test_utils.py
└── fixtures/
    └── sample_data.json
```

**JavaScript:**
```
src/
├── components/
│   ├── Button.jsx
│   └── Button.test.jsx    # Co-located tests
└── utils/
    ├── helpers.js
    └── helpers.test.js
```

---

## .gitignore Essentials

**Always ignore:**
```gitignore
# Virtual environments
venv/
env/
.venv/
node_modules/

# Data and caches
data/
*.db
*.sqlite
__pycache__/
.pytest_cache/
.coverage

# Environment and secrets
.env
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Examples from Real Projects

### image-workflow (Python)
```
image-workflow/
├── venv/                  ✅ Venv in root
├── scripts/               ✅ Scripts separate
│   ├── backup/
│   ├── crop/
│   └── utils/
├── data/                  ✅ Data isolated
└── Documents/             ✅ Docs clear
```

### Trading Projects (Python)
```
Trading Projects/
├── venv/                  ✅ Venv in root
├── scripts/               ✅ Scripts organized
│   ├── daily/
│   ├── weekly/
│   └── models/
└── data/
    └── databases/
```

### project-tracker (Python)
```
project-tracker/
├── venv/                  ✅ Venv in root (FIXED!)
├── scripts/               ✅ CLI tool here
│   ├── pt.py
│   ├── db/
│   └── discovery/
├── dashboard/             ✅ Web UI separate
└── data/                  ✅ Database here
```

---

## Migration Guide

### Moving venv from scripts/ to root

If you have an existing project with venv in the wrong place:

```bash
# Move virtual environment
mv scripts/venv ./venv

# Update launcher scripts
# Change: scripts/venv/bin/python
# To:     venv/bin/python

# Update .gitignore
echo "venv/" >> .gitignore

# Test that everything still works
source venv/bin/activate
python scripts/your_script.py
```

---

## When to Deviate

**It's okay to deviate when:**
- Framework conventions dictate different structure (e.g., Django, Flask)
- Project has unique requirements (e.g., monorepo)
- Third-party tools expect specific layout

**But document deviations in README.md!**

---

## 📋 Master Compliance Checklist (The One Checklist)

**Every project I touch MUST meet these requirements to be considered "scaffolded".**

### Project Types & Exclusions
- **Coding Projects (Python/Node/Go):** Full scaffolding mandatory (Indexes, Agents, Tests, Requirements).
- **Non-Coding Projects (Writing/Research/Builds):** Light scaffolding mandatory (Indexes, README, TODO). Excluded from `requirements.txt` and `tests/` audits.

### Mandatory Files (Root Level)
- [ ] **`00_Index_[ProjectName].md`** - Obsidian index with YAML frontmatter and status tags.
- [ ] **`AGENTS.md`** - Universal source of truth for AI agents (DoD, Tech Stack, Constraints).
- [ ] **`CLAUDE.md`** - Project-specific AI instructions and validation commands.
- [ ] **`requirements.txt`** (for Python) or **`package.json`** (for Node) - Mandatory for all coding projects.
- [ ] **`.cursorrules`** - Behavioral configuration for Cursor AI.
- [ ] **`.cursorignore`** - Context window filtering (ignore node_modules, logs, etc.).
- [ ] **`TODO.md`** - Task tracking following the [standard format](TODO_FORMAT_STANDARD.md).
- [ ] **`README.md`** - High-level project overview.
- [ ] **`.gitignore`** - Standard git ignore rules.

### Mandatory Structure
- [ ] **`Documents/`** directory - Centralized documentation following the [Documents/ pattern](PROJECT_STRUCTURE_STANDARDS.md#documentation-structure).
  - `Documents/README.md` (Index)
  - `Documents/core/` (Architecture/Operations)
- [ ] **Review History Retention** - `Documents/archives/reviews/`
  - **Why Mandatory**: Facilitates "Black Box Thinking" by analyzing past successes and failures. It ensures institutional memory is preserved so we can learn from patterns rather than repeating mistakes.
- [ ] **`scripts/`** directory - All executable scripts isolated from source code.
- [ ] **`venv/`** or **`node_modules/`** - Virtual environment/dependencies in the project root.

---

## Checklist for New Projects (Quick Start)

## Benefits of This Structure

✅ **Predictable** - Anyone can navigate instantly  
✅ **Maintainable** - Clear separation of concerns  
✅ **Collaborator-friendly** - AI and humans know where things are  
✅ **Scalable** - Structure works for small and large projects  
✅ **Standard** - Follows Python/Node.js community conventions

---

**Version:** 1.0  
**Established:** December 30, 2025  
**Source:** Extracted from image-workflow, Trading Projects, project-tracker

---

*"Convention over configuration - make the right choice the obvious choice"*

