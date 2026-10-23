%cd /content/Project_agent-

from pathlib import Path

brain_code = '''"""
Academic Brain - Main Controller

Connects the knowledge loader, knowledge retriever,
and project planner.
"""

from pathlib import Path
from knowledge_retriever import KnowledgeRetriever


class AcademicBrain:
    """Main controller for the Academic Brain system."""

    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent

        self.root_dir = Path(root_dir)
        self.retriever = KnowledgeRetriever(self.root_dir)

    def prepare_project(self, topic, department):
        """Prepare the knowledge and instructions for a project."""

        topic = topic.strip()
        department = department.strip()

        if not topic:
            raise ValueError("Project topic cannot be empty.")

        if not department:
            raise ValueError("Department cannot be empty.")

        context = self.retriever.retrieve(topic, department)

        instructions = self.retriever.create_ai_instructions(
            topic,
            department
        )

        return {
            "project_topic": topic,
            "department": department,
            "selected_department_file":
                context["selected_department"]["filename"],
            "institutional_rules":
                context["institutional_rules"],
            "research_rules":
                context["research_rules"],
            "ai_instructions": instructions
        }

    def show_project_report(self, topic, department):
        """Display a concise report about project preparation."""

        project = self.prepare_project(topic, department)

        print("\\\\nACADEMIC BRAIN - PROJECT REPORT")
        print("=" * 45)
        print("Topic:", project["project_topic"])
        print("Department:", project["department"])
        print(
            "Department knowledge:",
            project["selected_department_file"]
        )
        print(
            "Institutional rule files:",
            len(project["institutional_rules"])
        )
        print(
            "Research policy files:",
            len(project["research_rules"])
        )

        print("\\\\nAI instructions prepared successfully.")
        print("AI model connection: Not configured yet.")
        print("Automated project correction: Not implemented yet.")

        return project


if __name__ == "__main__":
    brain = AcademicBrain()

    topic = input("Enter your project topic: ").strip()
    department = input("Enter your department: ").strip()

    try:
        brain.show_project_report(topic, department)
    except (ValueError, FileNotFoundError) as error:
        print("Project preparation error:", error)
'''

file_path = Path("brain_agent.py")
file_path.write_text(brain_code, encoding="utf-8")

print("brain_agent.py created successfully!")
print("Location:", file_path.resolve())
'''

exec(brain_code)
