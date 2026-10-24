from pathlib import Path
import json
from datetime import datetime, timezone

from project_planner import ProjectPlanner


class ProjectWriter:
    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent

        self.root_dir = Path(root_dir)
        self.projects_dir = self.root_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        self.planner = ProjectPlanner(self.root_dir)

    def create_project(self, topic, department):
        """Create and save a plan without generating any chapters."""

        plan = self.planner.create_plan(topic, department)

        project_dir = self.projects_dir / plan["project_id"]
        project_dir.mkdir(parents=True, exist_ok=True)

        plan_path = project_dir / "project_plan.json"
        with plan_path.open("w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)

        return plan, project_dir

    def approve_plan(self, plan_path, confirmation):
        """Approve a saved plan only after an explicit APPROVE command."""

        if confirmation != "APPROVE":
            raise ValueError(
                "Plan approval requires the exact confirmation APPROVE."
            )

        plan_path = Path(plan_path)
        with plan_path.open("r", encoding="utf-8") as f:
            plan = json.load(f)

        if plan.get("status") != "awaiting_student_review":
            raise ValueError(
                "Only a plan awaiting student review can be approved."
            )

        plan["status"] = "approved"
        plan["approval"] = {
            "approved_at": datetime.now(timezone.utc).isoformat(),
            "method": "explicit_student_confirmation",
        }

        with plan_path.open("w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)

        return plan

    def run_full_workflow(self, topic, department):
        """Create a project and stop for student review."""

        plan, project_dir = self.create_project(topic, department)
        plan_path = project_dir / "project_plan.json"

        return {
            "project_id": plan["project_id"],
            "topic": plan["topic"],
            "department": plan["department"],
            "project_dir": str(project_dir),
            "plan_path": str(plan_path),
            "status": plan["status"],
            "message": (
                "Review the saved plan. Approve it explicitly before "
                "generating chapters."
            ),
        }

    def generate_approved_chapters(
        self,
        plan_path,
        source_notes_path=None,
    ):
        """Generate Chapters One and Two from an approved saved plan."""

        from generate_chapter import ChapterGenerator

        plan_path = Path(plan_path)
        generator = ChapterGenerator(self.root_dir)

        chapter_one_path, chapter_one = (
            generator.generate_chapter_one(plan_path)
        )
        chapter_two_path, chapter_two = (
            generator.generate_chapter_two(
                plan_path,
                source_notes_path=source_notes_path,
            )
        )

        return {
            "chapter_one_path": str(chapter_one_path),
            "chapter_two_path": str(chapter_two_path),
            "chapter_one_characters": len(chapter_one),
            "chapter_two_characters": len(chapter_two),
        }
