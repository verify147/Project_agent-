from project_classifier import ProjectClassifier


def test_engineering_project_classification():
    classifier = ProjectClassifier()
    result = classifier.classify(
        "Design and Construction of a Solar-Powered Irrigation System"
    )

    assert result["primary_type"] == "engineering_design_construction"
    assert result["needs_review"] is True


def test_experimental_project_classification():
    classifier = ProjectClassifier()
    result = classifier.classify(
        "Experimental Evaluation of Biochar for Water Filtration"
    )

    assert result["primary_type"] == "experimental_or_laboratory"
    assert result["needs_review"] is True


def test_unknown_topic_requires_review():
    classifier = ProjectClassifier()
    result = classifier.classify(
        "The Influence of Digital Learning on Student Motivation"
    )

    assert result["primary_type"] == "other_or_unclassified"
    assert result["needs_review"] is True
