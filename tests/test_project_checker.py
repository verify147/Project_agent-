from project_checker import ProjectChecker


def test_heading_equivalents():
    checker = ProjectChecker()

    assert checker.normalize_heading(
        "Justification of the Study"
    ) == "significance of the study"

    assert checker.normalize_heading(
        "1. Statement of the Problem"
    ) == "statement of the problem"

    assert checker.normalize_heading(
        "1.1 Aim and Specific Objectives"
    ) == "aim and objectives"


def test_extract_headings_ignores_ordinary_sentences():
    checker = ProjectChecker()

    text = """
# Chapter One
## Background of the Study
1. Statement of the Problem

This section introduces the general context of the project.
"""

    headings = checker.extract_headings(text)

    assert "background of the study" in headings
    assert "statement of the problem" in headings
    assert (
        "this section introduces the general context of the project"
        not in headings
    )



def test_integrity_markers_are_detected(tmp_path):
    checker = ProjectChecker()

    chapter = tmp_path / "chapter.md"
    chapter.write_text(
        """# Chapter One

## Background of the Study

A claim requiring evidence.
[VERIFIED SOURCE REQUIRED]

## Statement of the Problem

A proposed problem.

## Aim and Objectives

Proposed aim.
[STUDENT INPUT REQUIRED]

## Significance of the Study

Potential benefits.

## Scope and Limitations

Proposed scope.
""",
        encoding="utf-8",
    )

    report = checker.check_chapter(
        file_path=chapter,
        chapter_name="Chapter One",
    )

    assert report["source_flags"] == 1
    assert report["student_input_flags"] == 1
    assert "Some claims need verified sources." in report["issues"]
    assert "Some information requires student input." in report["issues"]
