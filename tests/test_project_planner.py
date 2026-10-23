from pathlib import Path
from project_planner import ProjectPlanner


def test_engineering_topic_selects_engineering_template():
    planner = ProjectPlanner(
        Path("/content/Project_agent-")
    )

    plan = planner.create_plan(
        "Design and Construction of a Solar-Powered Irrigation System",
        "Agricultural and Bio-Environmental Engineering Technology",
    )

    assert plan["project_classification"]["primary_type"] == (
        "engineering_design_construction"
    )
    assert plan["selected_template"] == (
        "engineering_design_construction"
    )
    assert plan["project_classification"]["needs_review"] is True
    assert plan["research_plan"]["chapter_outline"]


def test_unclassified_topic_uses_neutral_fallback():
    planner = ProjectPlanner(
        Path("/content/Project_agent-")
    )

    plan = planner.create_plan(
        "The Influence of Digital Learning on Student Motivation",
        "Agricultural and Bio-Environmental Engineering Technology",
    )

    assert plan["project_classification"]["primary_type"] == (
        "other_or_unclassified"
    )
    assert plan["selected_template"] == "other_or_unclassified"
    assert plan["research_plan"]["chapter_outline"]
    assert plan["research_plan"]["engineering_analysis"]["status"] == (
        "not_assumed_unclassified_topic"
    )



def test_department_requirements_are_preserved():
    planner = ProjectPlanner(
        Path("/content/Project_agent-")
    )

    plan = planner.create_plan(
        "Design and Construction of a Solar-Powered Irrigation System",
        "Agricultural and Bio-Environmental Engineering Technology",
    )

    requirements = plan["department_requirements"]

    assert requirements["knowledge_status"] == "initial_template"
    assert requirements["chapter_requirements"]
    assert requirements["technical_expectations"]
    assert requirements["integrity_rules"]
    assert isinstance(requirements["verified_sources"], list)

    # Provisional rules must not be presented as officially verified.
    assert requirements["knowledge_status"] != "officially_verified"
