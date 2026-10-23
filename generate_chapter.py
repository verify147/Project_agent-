
import json
from pathlib import Path
from brain_agent import AcademicBrain


class ChapterGenerator:
    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir or Path(__file__).resolve().parent)
        self.brain = AcademicBrain()

    def generate_chapter_one(self, plan_path):
        plan_path = Path(plan_path)

        with plan_path.open("r", encoding="utf-8") as f:
            plan = json.load(f)

        research_plan = plan["research_plan"]
        department_requirements = plan.get("department_requirements", {})
        outline = research_plan["chapter_outline"]["Chapter One"]

        sections = "\n".join(
            f"{number}. {section}"
            for number, section in enumerate(outline, start=1)
        )

        prompt = f"""
Write a preliminary academic draft of Chapter One for this project.

Project topic: {plan["topic"]}
Department: {plan["department"]}

Use these headings in this exact order:
{sections}

Planning information:
{json.dumps(research_plan, indent=2, ensure_ascii=False)}
Department requirements (provisional; verify official school rules):
{json.dumps(department_requirements, indent=2, ensure_ascii=False)}


Requirements:
- Use clear, formal academic English.
- Explain the research problem and its context in the relevant discipline.
- Align the aim and objectives with the project topic.
- Keep the scope realistic.
- Do not invent statistics, citations, references, measurements,
  construction activities, or experimental results.
- Mark claims needing evidence with [VERIFIED SOURCE REQUIRED].
- Treat objectives as proposed until the student confirms completion.
- Do not claim the prototype has been built or tested.
- If essential information is unknown, insert [STUDENT INPUT REQUIRED].
- Return only the chapter draft.
"""

        chapter = self.brain.generate_response(
            topic=plan["topic"],
            department=plan["department"],
            prompt=prompt,
            max_tokens=2500
        )

        output_path = plan_path.parent / "Chapter_One.md"
        output_path.write_text(chapter, encoding="utf-8")

        return output_path, chapter
