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


    def get_project_evidence(self, project_dir):
        """Access a project's research evidence tracker."""

        from research_evidence import ResearchEvidence

        folder = Path(project_dir)

        if not folder.is_absolute():
            folder = self.root_dir / folder

        return ResearchEvidence(folder)

    def record_research_source(
        self, project_dir, title, authors, year,
        publisher, url, notes=""
    ):
        """Record a source for later verification."""

        evidence = self.get_project_evidence(project_dir)
        return evidence.add_source(
            title, authors, year, publisher, url, notes
        )

    def record_research_claim(
        self, project_dir, claim_text, source_ids=None
    ):
        """Record a claim for later evidence review."""

        evidence = self.get_project_evidence(project_dir)
        return evidence.add_claim(
            claim_text, source_ids=source_ids
        )

    def show_evidence_report(self, project_dir):
        """Display a project's research evidence status."""

        evidence = self.get_project_evidence(project_dir)
        report = evidence.get_review_report()

        print("\nACADEMIC BRAIN - EVIDENCE REPORT")
        print("=" * 38)
        print("Sources:", report["total_sources"])
        print("Claims:", report["total_claims"])
        print(
            "Sources needing review:",
            len(report["sources_needing_review"])
        )
        print(
            "Claims needing review:",
            len(report["claims_needing_review"])
        )
        print(
            "Ready for final review:",
            report["ready_for_final_review"]
        )

        print("\nCLAIM REVIEW DETAILS")
        for item in evidence.get_claim_review_details():
            print("\nClaim:", item["claim_id"])
            print("Text:", item["claim_text"])
            print("Reasons:", item["review_reasons"])

        report["claim_review_details"] = (
            evidence.get_claim_review_details()
        )

        return report

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
            "You are Academic Brain, a multidisciplinary academic "
            "research assistant. Adapt your terminology, methods, "
            "analysis, and writing to the project's actual discipline "
            "and research type. Follow the retrieved academic "
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
        print("Groq API call: Implemented; API key is checked at generation time.")

        return project
