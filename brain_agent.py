%cd /content/Project_agent-

code = r'''
from pathlib import Path
from knowledge_retriever import KnowledgeRetriever


class AcademicBrain:
    """Main controller for the Academic Brain project."""

    def __init__(self, root_dir=None):
        self.root_dir = Path(
            root_dir or Path(__file__).resolve().parent
        )
        self.retriever = KnowledgeRetriever(self.root_dir)

    def prepare_project(self, topic, department):
        """Retrieve the knowledge required for a project."""

        if not topic.strip():
            raise ValueError("Project topic cannot be empty.")

        if not department.strip():
            raise ValueError("Department cannot be empty.")

        context = self.retriever.retrieve(topic, department)

        instructions = self.retriever.create_ai_instructions(
            topic, department
        )

        return {
            "project_topic": topic.strip(),
            "department": department.strip(),
            "department_file":
                context["selected_department"]["filename"],
            "institutional_rules":
                context["institutional_rules"],
            "research_rules":
                context["research_rules"],
            "ai_instructions": instructions
        }

    def show_project_report(self, topic, department):
        """Display a project preparation report."""

        project = self.prepare_project(topic, department)

        print("\nACADEMIC BRAIN - PROJECT REPORT")
        print("=" * 40)
        print("Project:", project["project_topic"])
        print("Department:", project["department"])
        print("Department file:", project["department_file"])
        print(
            "Institutional files:",
            len(project["institutional_rules"])
        )
        print(
            "Research policy files:",
            len(project["research_rules"])
        )
        print("\nAI instructions prepared successfully.")
        print("AI model connection: Not configured yet.")
        print("Automated correction: Not implemented yet.")

        return project
'''

file_path = Path("brain_agent.py")
file_path.write_text(code.strip() + "\n", encoding="utf-8")

print("File created:", file_path.exists())
print("Saved to:", file_path.resolve())
