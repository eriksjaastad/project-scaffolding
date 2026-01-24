"""
Centralized constants for the project scaffolding system.
"""

# Projects that should NEVER be modified by scaffolding or automated cleanup
PROTECTED_PROJECTS = {
    "ai-journal",
    "writing",
    "plugin-duplicate-detection",
    "plugin-find-names-chrome",
    "Name Highlighter",
    "project-scaffolding",  # Scaffolding should not scaffold itself
    "_tools",               # Infrastructure tools
    "__Knowledge",          # Obsidian knowledge base
}
