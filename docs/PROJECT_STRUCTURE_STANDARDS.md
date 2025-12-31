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
├── docs/                      # Documentation
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
- ✅ **Documentation clear:** `docs/` for detailed docs

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
├── docs/                     # Documentation
├── package.json              # Node dependencies
├── README.md
├── TODO.md
└── .gitignore
```

**Key rules:**
- ✅ **Standard React structure:** Follow Create React App / Next.js conventions
- ✅ **Scripts separate:** Build scripts in `scripts/`, source in `src/`
- ✅ **Documentation clear:** `docs/` for detailed docs

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
├── docs/                     # Documentation
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
- ❌ Documentation (goes in `docs/`)
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
docs/
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
- Document data structure in `docs/core/DATA_MODEL.md`
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

## Checklist for New Projects

- [ ] Virtual environment in root (`venv/` or `node_modules/`)
- [ ] Scripts in `scripts/` directory
- [ ] Data files in `data/` directory
- [ ] Documentation in `docs/` directory
- [ ] Configuration files in root
- [ ] `.gitignore` includes venv, data, secrets
- [ ] `README.md` in root with quick start
- [ ] `TODO.md` in root for task tracking
- [ ] `requirements.txt` or `package.json` in root

---

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

