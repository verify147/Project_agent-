import json
from pathlib import Path
import pytest

from generate_chapter import ChapterGenerator


class MockBrain:
    def __init__(self):
        self.prompt = ""
        self.calls = []

    def generate_response(self, topic, department, prompt, max_tokens):
        self.prompt = prompt
        self.calls.append({
            "topic": topic,
            "department": department,
            "prompt": prompt,
            "max_tokens": max_tokens,
        })
        if "Chapter Two" in prompt:
            return "# Chapter Two\\n\\nMock literature review."
        return "# Chapter One\\n\\nMock chapter for testing."


def make_plan(status="approved"):
    return {
        "status": status,
        "topic": "Design and Construction of a Solar-Powered Irrigation System",
        "department": "Agricultural and Bio-Environmental Engineering Technology",
        "research_plan": {
            "chapter_outline": {
                "Chapter One": [
                    "Introduction",
                    "Statement of the Problem",
                    "Aim and Objectives"
                ],
                "Chapter Two": [
                    "Review of Relevant Literature",
                    "Review of Existing Systems",
                    "Research Gap"
                ]
            },
            "methodology": {
                "status": "requires_project_specific_design"
            }
        },
        "department_requirements": {
            "knowledge_status": "initial_template",
            "chapter_requirements": {"chapter_one": ["Introduction"]},
            "technical_expectations": {
                "calculations": "required where applicable"
            },
            "integrity_rules": {"no_fabricated_results": True}
        }
    }


def make_generator(tmp_path, plan):
    plan_path = tmp_path / "project_plan.json"
    plan_path.write_text(
        json.dumps(plan), encoding="utf-8"
    )

    generator = ChapterGenerator.__new__(ChapterGenerator)
    generator.root_dir = tmp_path
    generator.brain = MockBrain()

    return generator, plan_path


def test_generator_includes_department_rules_and_saves_chapter(tmp_path):
    generator, plan_path = make_generator(tmp_path, make_plan())

    output_path, chapter = generator.generate_chapter_one(plan_path)
    prompt = generator.brain.prompt

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == chapter
    assert "chapter_requirements" in prompt
    assert "technical_expectations" in prompt
    assert "integrity_rules" in prompt
    assert "Do not invent sources" in prompt
    assert "Introduction" in prompt


def test_unapproved_plan_cannot_generate_chapter_one(tmp_path):
    generator, plan_path = make_generator(
        tmp_path, make_plan(status="awaiting_student_review")
    )

    with pytest.raises(ValueError, match="explicitly approved"):
        generator.generate_chapter_one(plan_path)

    assert generator.brain.calls == []


def test_chapter_two_uses_saved_outline_and_source_notes(tmp_path):
    generator, plan_path = make_generator(tmp_path, make_plan())

    notes_path = tmp_path / "source_notes.txt"
    notes_path.write_text(
        "Example source supplied by student; details require verification.",
        encoding="utf-8",
    )

    output_path, chapter = generator.generate_chapter_two(
        plan_path, source_notes_path=notes_path
    )

    assert output_path.name == "Chapter_Two.md"
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == chapter
    assert "Review of Existing Systems" in generator.brain.prompt
    assert "Do not invent authors" in generator.brain.prompt
    assert "Example source supplied by student" in generator.brain.prompt


def test_chapter_two_without_notes_flags_missing_evidence(tmp_path):
    generator, plan_path = make_generator(tmp_path, make_plan())

    generator.generate_chapter_two(plan_path)

    assert "[NO SOURCE NOTES SUPPLIED]" in generator.brain.prompt
    assert "[VERIFIED SOURCE REQUIRED]" in generator.brain.prompt


def test_chapter_two_requires_approval(tmp_path):
    generator, plan_path = make_generator(
        tmp_path, make_plan(status="awaiting_student_review")
    )

    with pytest.raises(ValueError, match="explicitly approved"):
        generator.generate_chapter_two(plan_path)

    assert generator.brain.calls == []
