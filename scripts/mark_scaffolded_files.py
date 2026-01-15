import os
from pathlib import Path

# Configuration
SCAFFOLDING_ROOT = Path(__file__).parent.parent
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", SCAFFOLDING_ROOT.parent)).resolve()
TEMPLATES_ROOT = SCAFFOLDING_ROOT / "templates"

PROJECTS = [
    "project-tracker", "flo-fi", "national-cattle-brands", "trading-copilot",
    "3d-pose-factory", "ai-journal", "ai-usage-billing-tracker", "analyze-youtube-videos",
    "cortana-personal-ai", "holoscape", "image-workflow", "muffinpanrecipes",
    "portfolio-ai", "sherlock-holmes", "smart-invoice-workflow", "subscription-tracker",
    "synth-insight-labs", "tax-organizer", "van-build", "writing"
]

FILE_MAP = {
    "AGENTS.md": "Source of Truth for AI Agents",
    "CLAUDE.md": "AI Collaboration Instructions",
    "TODO.md": "Pending Tasks",
    "README.md": "Quick Start",
    ".cursorrules": "Context Window Management",
    ".cursorignore": "Dependencies & Packages",
    ".gitignore": "Virtual environments"
}

MARKER = "\n<!-- project-scaffolding template appended -->\n"

results = {
    "added": [],
    "no_match": [],
    "skipped": []
}

for project in PROJECTS:
    project_path = PROJECTS_ROOT / project
    if not project_path.exists():
        results["skipped"].append(f"{project} (Project dir not found)")
        continue
        
    for filename, match_str in FILE_MAP.items():
        file_path = project_path / filename
        if not file_path.exists():
            results["skipped"].append(f"{project}/{filename} (File not found)")
            continue
            
        try:
            content = file_path.read_text()
            if "project-scaffolding template appended" in content:
                results["skipped"].append(f"{project}/{filename} (Marker already present)")
                continue
                
            if match_str in content:
                # Use plain file write - tool will handle it
                with open(file_path, "a") as f:
                    f.write(MARKER)
                results["added"].append(f"{project}/{filename}")
            else:
                results["no_match"].append(f"{project}/{filename}")
        except Exception as e:
            results["skipped"].append(f"{project}/{filename} (Error: {str(e)})")

print("--- MARKER ADDED ---")
for item in results["added"]:
    print(f"✅ {item}")

print("\n--- NO MATCH FOUND ---")
for item in results["no_match"]:
    print(f"❌ {item}")

print("\n--- SKIPPED ---")
for item in results["skipped"]:
    print(f"⏩ {item}")
