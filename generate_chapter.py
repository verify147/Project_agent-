import json
from pathlib import Path
from brain_agent import AcademicBrain


class ChapterGenerator:
    def __init__(self, root_dir=None):
        self.root_dir = Path(
            root_dir or Path(__file__).resolve().parent
        )
        self.brain = AcademicBrain(self.root_dir)

    @staticmethod
    def _load_approved_plan(plan_path):
        plan_path = Path(plan_path)

        with plan_path.open("r", encoding="utf-8") as f:
            plan = json.load(f)

        if plan.get("status") != "approved":
            raise ValueError(
                "Chapter generation blocked: the saved plan must be "
                "explicitly approved first."
            )

        research_plan = plan.get("research_plan")
        if not isinstance(research_plan, dict):
            raise ValueError("The saved plan has no valid research_plan.")

        outline = research_plan.get("chapter_outline")
        if not isinstance(outline, dict):
            raise ValueError("The saved plan has no chapter outline.")

        if not plan.get("topic") or not plan.get("department"):
            raise ValueError("The saved plan needs a topic and department.")

        return plan_path, plan

    @staticmethod
    def _format_outline(outline):
        if not isinstance(outline, list) or not outline:
            raise ValueError(
                "The approved plan must contain a non-empty chapter outline."
            )

        return "\\n".join(
            f"{number}. {section}"
            for number, section in enumerate(outline, start=1)
        )

    def _generate_chapter(
        self,
        plan_path,
        chapter_name,
        output_filename,
        source_notes_path=None,
    ):
        plan_path, plan = self._load_approved_plan(plan_path)

        research_plan = plan["research_plan"]
        outline = research_plan["chapter_outline"].get(chapter_name)
        sections = self._format_outline(outline)

        department_requirements = plan.get(
            "department_requirements", {}
        )

        source_notes = ""
        source_note_status = (
            "No source notes were supplied. Do not invent references."
        )

        if source_notes_path is not None:
            notes_path = Path(source_notes_path)
            if not notes_path.is_absolute():
                notes_path = plan_path.parent / notes_path

            if notes_path.exists() and notes_path.is_file():
                source_notes = notes_path.read_text(
                    encoding="utf-8"
                ).strip()
                if source_notes:
                    source_note_status = (
                        "Source notes were supplied. Their accuracy "
                        "and bibliographic details still require verification."
                    )
                else:
                    source_note_status = (
                        "The source-notes file is empty. Do not invent references."
                    )
            else:
                source_note_status = (
                    "The specified source-notes file was not found. "
                    "Do not invent references."
                )

        if chapter_name == "Chapter One":
            chapter_specific_requirements = """
- Explain the research problem and its context in the relevant discipline.
- Align the aim and objectives with the project topic.
- Keep the scope realistic.
- Treat objectives as proposed until the student confirms completion.
- Do not claim a prototype has been built or tested.
- Do not invent statistics, citations, measurements, construction activities,
  or experimental results.
"""
            max_tokens = 2500
        else:
            chapter_specific_requirements = """
- Review relevant concepts, engineering principles, and related systems.
- Compare prior studies only where the supplied evidence supports comparison.
- Identify a research gap only when the reviewed material supports it.
- Do not invent authors, publication titles, publication dates, DOIs,
  URLs, quotations, page numbers, or bibliographic references.
- If source details are missing, use [VERIFIED SOURCE REQUIRED].
- Distinguish established information from proposed design choices.
- Do not claim that the project has been built or tested.
"""
            max_tokens = 4000

        prompt = f"""
Write a preliminary academic draft of {chapter_name}.

Project topic: {plan["topic"]}
Department: {plan["department"]}

Use these headings in this exact order:
{sections}

Saved research plan:
{json.dumps(research_plan, indent=2, ensure_ascii=False)}

Department requirements (provisional; verify official school rules):
{json.dumps(department_requirements, indent=2, ensure_ascii=False)}

Source-note status: {source_note_status}

Supplied source notes:
{source_notes if source_notes else "[NO SOURCE NOTES SUPPLIED]"}

Requirements:
- Use clear, formal academic English.
- Follow the approved outline exactly and do not add or reorder headings.
- Do not invent sources, statistics, measurements, costs, or results.
- Mark claims needing evidence with [VERIFIED SOURCE REQUIRED].
- Mark missing project-specific information with [STUDENT INPUT REQUIRED].
- Treat departmental requirements as provisional unless independently verified.
{chapter_specific_requirements}
Return only the chapter draft.
"""

        chapter = self.brain.generate_response(
            topic=plan["topic"],
            department=plan["department"],
            prompt=prompt,
            max_tokens=max_tokens,
        )

        if not isinstance(chapter, str) or not chapter.strip():
            raise RuntimeError(
                f"{chapter_name} generation returned empty output."
            )

        output_path = plan_path.parent / output_filename
        output_path.write_text(chapter, encoding="utf-8")

        return output_path, chapter

    def generate_chapter_one(self, plan_path):
        return self._generate_chapter(
            plan_path,
            "Chapter One",
            "Chapter_One.md",
        )

    def generate_chapter_two(
        self,
        plan_path,
        source_notes_path=None,
    ):
        return self._generate_chapter(
            plan_path,
            "Chapter Two",
            "Chapter_Two.md",
            source_notes_path=source_notes_path,
        )
