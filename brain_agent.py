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
        """Retrieve knowledge and prepare project instructions."""

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
            "department_file": context["selected_department"]["filename"],
            "institutional_rules": context["institutional_rules"],
            "research_rules": context["research_rules"],
            "ai_instructions": instructions
        }


    def generate_response(self, topic, department, prompt,
                          max_tokens=2000):
        """Generate academic content using Groq."""

        import os
        from groq import Groq

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is missing. Enter your key first."
            )

        project = self.prepare_project(topic, department)
        client = Groq(api_key=api_key)

        system_prompt = (
            "You are Academic Brain, an academic engineering "
            "research assistant. Follow the retrieved academic "
            "guidance. Never invent references, statistics, costs, "
            "measurements, or experimental results. Mark claims "
            "requiring verification with [VERIFIED SOURCE REQUIRED]. "
            "Distinguish proposed designs from actual tested results. "
            "Do not claim that a prototype was built or tested without "
            "evidence. Use clear academic language.\n\n"
            f"PROJECT: {project['project_topic']}\n"
            f"DEPARTMENT: {project['department']}\n"
            f"DEPARTMENT FILE: {project['department_file']}\n"
            f"ACADEMIC INSTRUCTIONS: {project['ai_instructions']}\n"
            f"INSTITUTIONAL RULES: {project['institutional_rules']}\n"
            f"RESEARCH RULES: {project['research_rules']}"
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def show_project_report(self, topic, department):
        """Display a project preparation report."""

        project = self.prepare_project(topic, department)

        print("\nACADEMIC BRAIN - PROJECT REPORT")
        print("=" * 40)
        print("Project:", project["project_topic"])
        print("Department:", project["department"])
        print("Department file:", project["department_file"])
        print("Institutional files:", len(project["institutional_rules"]))
        print("Research policy files:", len(project["research_rules"]))
        print("\nAI instructions prepared successfully.")
        print("Groq connection: Not configured in this module yet.")

        return project
