#!/usr/bin/env python3
"""Patch-Bot Loop - Bounded automated fixes.

The Patch-Bot is triggered by READY_FOR_PATCH status, validates required fields,
and implements deterministic workflow with hard safety boundaries.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add project-tracker to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "project-tracker"))
from scripts.config import DATABASE_PATH, PROJECTS_BASE_DIR
from scripts.db.manager import DatabaseManager

# Import config loader
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config


class PatchBotLoop:
    """Patch-Bot autonomous loop for bounded automated fixes."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.config = load_config()
        self.projects_root = Path(PROJECTS_BASE_DIR)
        self.loop_name = "patch-bot"
        
    def run(self):
        """Execute one iteration of the Patch-Bot loop."""
        execution_id = self._record_start()
        cards_processed = 0
        
        try:
            print(f"🤖 Patch-Bot Loop starting at {datetime.now().isoformat()}")
            
            # Get all tasks in READY_FOR_PATCH status
            tasks = self.db.get_tasks(status="READY_FOR_PATCH")
            
            print(f"  Found {len(tasks)} tasks ready for patching")
            
            for task in tasks:
                task_id = task["id"]
                project_id = task["project_id"]
                
                print(f"  Processing task #{task_id} in {project_id}...")
                
                # Validate required fields
                if not self._validate_task(task):
                    self._reject_task(task_id, "Missing required fields")
                    continue
                
                # Check autonomy level
                project = self.db.get_project(project_id)
                autonomy_level = project.get("autonomy_level", "report")
                
                if autonomy_level == "report":
                    print(f"    Skipping: Project autonomy level is 'report' only")
                    continue
                
                # Process the patch
                try:
                    self._process_patch(task)
                    cards_processed += 1
                except Exception as e:
                    self._reject_task(task_id, f"Patch failed: {e}")
            
            self._record_complete(execution_id, "success", cards_processed)
            print(f"✅ Patch-Bot Loop complete. Processed {cards_processed} cards.")
            
        except Exception as e:
            self._record_complete(execution_id, "failed", cards_processed, str(e))
            print(f"❌ Patch-Bot Loop failed: {e}")
            raise
    
    def _validate_task(self, task: Dict) -> bool:
        """Validate that task has all required fields for patching."""
        required_fields = ["allowed_paths", "definition_of_done"]
        
        for field in required_fields:
            if not task.get(field):
                print(f"    Missing required field: {field}")
                return False
        
        return True
    
    def _process_patch(self, task: Dict):
        """Process a patch for a task."""
        task_id = task["id"]
        project_id = task["project_id"]
        
        # Parse allowed paths
        try:
            allowed_paths = json.loads(task["allowed_paths"])
        except:
            allowed_paths = []
        
        print(f"    Allowed paths: {allowed_paths}")
        
        # For now, just move to In Progress
        # TODO: Implement actual patching workflow:
        # 1. Checkout project
        # 2. Reproduce issue
        # 3. Plan fix
        # 4. Apply patch (only to allowed_paths)
        # 5. Verify against definition_of_done
        # 6. Create PR or commit
        
        self.db.update_task(task_id, status="In Progress")
        print(f"    Moved to In Progress (actual patching not yet implemented)")
    
    def _reject_task(self, task_id: int, reason: str):
        """Reject a task and move it back to TRIAGED with a comment."""
        self.db.update_task(
            task_id,
            status="TRIAGED",
            review_comment=f"[Patch-Bot] Rejected: {reason}"
        )
        print(f"    Rejected: {reason}")
    
    def _record_start(self) -> int:
        """Record loop execution start."""
        with self.db._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO loop_executions (loop_name, started_at, status)
                VALUES (?, ?, 'running')
            """, (self.loop_name, datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def _record_complete(self, execution_id: int, status: str, cards_created: int = 0, error: Optional[str] = None):
        """Record loop execution completion."""
        with self.db._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE loop_executions
                SET completed_at = ?, status = ?, cards_created = ?, error_message = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), status, cards_created, error, execution_id))
            conn.commit()


if __name__ == "__main__":
    patch_bot = PatchBotLoop()
    patch_bot.run()
