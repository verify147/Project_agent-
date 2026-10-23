import json
from pathlib import Path

from generate_chapter import ChapterGenerator


class MockBrain:
    def __init__(self):
        self.prompt = ""

    def generate_response(self, topic, department, prompt, max_tokens):
        self.prompt = prompt
        return "# Chapter One\\n\\nMock chapter for testing."


def test_generator_includes_department_rules_and_saves_chapter(tmp_path):
    plan = {
        "topic": "Design and Construction of a Solar-Powered Irrigation System",
        "department": "Agricultural and Bio-Environmental Engineering Technology",
        "research_plan": {
            "chapter_outline": {
                "Chapter One": [
                    "Introduction",
                    "Statement of the Problem",
                    "Aim and Objectives"
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

    plan_path = tmp_path / "project_plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    generator = ChapterGenerator.__new__(ChapterGenerator)
    generator.root_dir = tmp_path
    generator.brain = MockBrain()

    output_path, chapter = generator.generate_chapter_one(plan_path)
    prompt = generator.brain.prompt

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == chapter
    assert "chapter_requirements" in prompt
    assert "technical_expectations" in prompt
    assert "integrity_rules" in prompt
    assert "Do not invent statistics" in prompt
