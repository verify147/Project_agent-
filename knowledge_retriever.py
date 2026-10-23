import json
import re
from pathlib import Path

from knowledge_loader import KnowledgeBaseLoader


class KnowledgeRetriever:
    """
    Selects relevant institutional, departmental,
    and research knowledge for an academic project.
    """

    def __init__(self, root_dir=None):
        self.loader = KnowledgeBaseLoader(root_dir)
        self.knowledge = self.loader.load_all()

    def normalize(self, text):
        """Normalize text for simple keyword matching."""

        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return " ".join(text.split())

    def get_department(self, department_name):
        """Find a department by name or filename."""

        query = self.normalize(department_name)

        departments = self.knowledge["departments"]

        # First, try matching the department name in the file.
        for filename, data in departments.items():
            stored_name = self.normalize(
                data.get("department", "")
            )

            if query == stored_name or query == self.normalize(filename):
                return filename, data

        # Next, allow partial matching.
        for filename, data in departments.items():
            stored_name = self.normalize(
                data.get("department", "")
            )

            if query in stored_name or stored_name in query:
                return filename, data

            if query in self.normalize(filename):
                return filename, data

        return None, None

    def retrieve(self, topic, department_name):
        """
        Assemble the knowledge relevant to a project.
        """

        filename, department = self.get_department(
            department_name
        )

        if department is None:
            available = list(
                self.knowledge["departments"].keys()
            )

            raise ValueError(
                f"Department not found: {department_name}. "
                f"Available department files: {available}"
            )

        return {
            "project_topic": topic,
            "selected_department": {
                "filename": filename,
                "knowledge": department
            },
            "institutional_rules":
                self.knowledge["institution"],
            "research_rules":
                self.knowledge["research"]
        }

    def create_ai_instructions(self, topic, department_name):
        """
        Turn retrieved knowledge into a structured
        instruction package for an AI model.
        """

        context = self.retrieve(topic, department_name)

        instructions = {
            "role": (
                "You are an academic engineering research assistant. "
                "Use the supplied knowledge as guidance, distinguish "
                "verified rules from provisional rules, and never "
                "invent sources, measurements, or experimental results."
            ),
            "project_topic": context["project_topic"],
            "department": context["selected_department"],
            "institutional_rules": context["institutional_rules"],
            "research_rules": context["research_rules"],
            "requirements": [
                "Follow applicable verified institutional rules.",
                "Use the selected department's relevant guidance.",
                "Identify missing project information.",
                "State assumptions explicitly.",
                "Verify references before presenting them as verified.",
                "Do not invent experimental findings."
            ]
        }

        return json.dumps(instructions, indent=2)

    def show_summary(self, topic, department_name):
        """Display the knowledge selected for a project."""

        context = self.retrieve(topic, department_name)

        print("\nACADEMIC BRAIN: RETRIEVAL REPORT")
        print("=" * 45)
        print(f"Project: {topic}")
        print(f"Department: {department_name}")
        print(
            "Department file:",
            context["selected_department"]["filename"]
        )
        print(
            "Institutional files:",
            len(context["institutional_rules"])
        )
        print(
            "Research policy files:",
            len(context["research_rules"])
        )

        print("\nKnowledge selection completed.")


if __name__ == "__main__":
    retriever = KnowledgeRetriever()

    topic = input("Enter your project topic: ").strip()
    department = input("Enter your department: ").strip()

    try:
        retriever.show_summary(topic, department)

        print("\n--- AI INSTRUCTION PREVIEW ---\n")

        print(
            retriever.create_ai_instructions(
                topic,
                department
            )
        )

    except ValueError as error:
        print(f"\nError: {error}")
