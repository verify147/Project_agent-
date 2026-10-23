from pathlib import Path
import json

from project_planner import ProjectPlanner
from brain_agent import AcademicBrain


class ProjectWriter:
    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent

        self.root_dir = Path(root_dir)
        self.projects_dir = self.root_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        self.planner = ProjectPlanner(self.root_dir)
        self.brain = AcademicBrain(self.root_dir)

    def create_project(self, topic, department):
        plan = self.planner.create_plan(topic, department)

        project_dir = self.projects_dir / plan["project_id"]
        project_dir.mkdir(parents=True, exist_ok=True)

        plan_path = project_dir / "project_plan.json"
        with plan_path.open("w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)

        return plan, project_dir

    def run_full_workflow(self, topic, department):
        """Create a project, generate Chapter One, and check it."""

        from generate_chapter import ChapterGenerator
        from project_checker import ProjectChecker

        plan, project_dir = self.create_project(topic, department)
        plan_path = project_dir / "project_plan.json"

        generator = ChapterGenerator(self.root_dir)
        chapter_path, chapter_text = generator.generate_chapter_one(
            plan_path
        )

        checker = ProjectChecker()
        chapter_report = checker.check_chapter(
            chapter_path,
            "Chapter One",
            plan=plan
        )

        evidence_report = checker.check_research_evidence(
            project_dir
        )

        return {
            "project_id": plan["project_id"],
            "topic": plan["topic"],
            "department": plan["department"],
            "project_dir": str(project_dir),
            "plan_path": str(plan_path),
            "chapter_path": str(chapter_path),
            "chapter_report": chapter_report,
            "evidence_report": evidence_report,
        }
