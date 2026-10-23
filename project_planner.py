import json
import re
from pathlib import Path
from datetime import datetime, timezone

from knowledge_retriever import KnowledgeRetriever


class ProjectPlanner:
    """
    Creates and saves structured research plans
    for engineering projects.
    """

    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent

        self.root_dir = Path(root_dir)
        self.projects_dir = self.root_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        self.retriever = KnowledgeRetriever(self.root_dir)

    @staticmethod
    def make_project_id(topic):
        """Create a readable identifier from a project topic."""

        slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
        return slug[:80] or "engineering-project"

    def create_plan(self, topic, department_name):
        """Create an initial research plan."""

        context = self.retriever.retrieve(topic, department_name)

        department = context["selected_department"]["knowledge"]

        plan = {
            "project_id": self.make_project_id(topic),
            "topic": topic,
            "department": department.get(
                "department", department_name
            ),
            "institution": department.get(
                "institution", "Not specified"
            ),
            "status": "planning",
            "created_at": datetime.now(timezone.utc).isoformat(),

            "knowledge_status": {
                "department_rules": department.get(
                    "knowledge_status", "Not specified"
                ),
                "institutional_rules": "Check individual files",
                "research_policies_loaded": len(
                    context["research_rules"]
                )
            },

            "research_plan": {
                "problem_statement": {
                    "status": "needs_research",
                    "guidance": (
                        "Investigate the real problem, its evidence, "
                        "who is affected, and why the proposed project "
                        "could help."
                    )
                },

                "aim": {
                    "status": "draft_required",
                    "guidance": (
                        "Define one clear overall aim that matches "
                        "the project topic."
                    )
                },

                "objectives": [
                    {
                        "objective": (
                            "Investigate the existing problem "
                            "and relevant engineering solutions."
                        ),
                        "status": "proposed"
                    },
                    {
                        "objective": (
                            "Develop a suitable design based on "
                            "documented requirements."
                        ),
                        "status": "proposed"
                    },
                    {
                        "objective": (
                            "Construct or implement the system, "
                            "if construction is within the project scope."
                        ),
                        "status": "proposed"
                    },
                    {
                        "objective": (
                            "Test and evaluate the system using "
                            "defined performance criteria."
                        ),
                        "status": "proposed"
                    }
                ],

                "research_questions": [
                    "What problem must the project solve?",
                    "What existing solutions are available?",
                    "Which design is appropriate for the requirements?",
                    "How can the system be tested objectively?"
                ],

                "methodology": {
                    "status": "requires_project_specific_design",
                    "steps": [
                        "Review relevant literature and existing designs.",
                        "Define system requirements and constraints.",
                        "Develop and justify the proposed design.",
                        "Identify required materials and components.",
                        "Perform applicable engineering calculations.",
                        "Construct or implement the system if required.",
                        "Develop a repeatable testing procedure.",
                        "Collect actual measurements where testing occurs.",
                        "Analyse results against predefined criteria."
                    ]
                },

                "engineering_analysis": {
                    "status": "identify_after_design",
                    "required_items": [
                        "Design assumptions",
                        "Relevant equations",
                        "Input parameters and units",
                        "Material and component selection",
                        "Safety considerations",
                        "Cost estimate",
                        "Testing and performance criteria"
                    ]
                },

                "evidence_requirements": [
                    "Verified technical sources",
                    "Documented design requirements",
                    "Traceable calculations",
                    "Material and component specifications",
                    "Actual test data when testing is performed",
                    "Documented limitations"
                ],

                "chapter_outline": {
                    "Chapter One": [
                        "Background of the Study",
                        "Statement of the Problem",
                        "Aim and Objectives",
                        "Significance of the Study",
                        "Scope and Limitations"
                    ],
                    "Chapter Two": [
                        "Review of Relevant Literature",
                        "Review of Existing Systems",
                        "Relevant Engineering Principles",
                        "Research Gap"
                    ],
                    "Chapter Three": [
                        "Materials and Equipment",
                        "Design Methodology",
                        "Engineering Calculations",
                        "Construction or Implementation",
                        "Testing Procedure"
                    ],
                    "Chapter Four": [
                        "Results and Observations",
                        "Analysis and Discussion",
                        "Performance Evaluation"
                    ],
                    "Chapter Five": [
                        "Summary",
                        "Conclusion",
                        "Recommendations"
                    ]
                },

                "open_questions": [
                    "What exact problem is the project intended to solve?",
                    "Is this a design-only project or will a prototype be built?",
                    "What budget and equipment are available?",
                    "Which testing facilities are available?",
                    "What project structure does the department require?"
                ]
            }
        }

        return plan

    def save_plan(self, plan):
        """Save a project plan as JSON."""

        filename = f"{plan['project_id']}_plan.json"
        path = self.projects_dir / filename

        with path.open("w", encoding="utf-8") as file:
            json.dump(plan, file, indent=2, ensure_ascii=False)

        return path

    def run(self):
        """Interactively create and save a plan."""

        topic = input("Enter your project topic: ").strip()
        department = input("Enter your department: ").strip()

        if not topic or not department:
            print("Topic and department are required.")
            return

        try:
            plan = self.create_plan(topic, department)
            path = self.save_plan(plan)

            print("\nPROJECT PLAN CREATED")
            print("=" * 40)
            print(f"Topic: {plan['topic']}")
            print(f"Department: {plan['department']}")
            print(f"Status: {plan['status']}")
            print(f"Objectives: {len(plan['research_plan']['objectives'])}")
            print(f"Saved to: {path}")

            print("\nIMPORTANT:")
            print(
                "This is an initial planning template. "
                "Its objectives, methodology, and chapter structure "
                "must be reviewed against the actual project and "
                "verified departmental requirements."
            )

        except (ValueError, FileNotFoundError) as error:
            print(f"\nCould not create the plan: {error}")


if __name__ == "__main__":
    ProjectPlanner().run()
