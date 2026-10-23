
from pathlib import Path


class ProjectChecker:

    REQUIRED_SECTIONS = {
        "Chapter One": [
            "Background of the Study",
            "Statement of the Problem",
            "Aim and Objectives",
            "Significance of the Study",
            "Scope and Limitations",
        ],
        "Chapter Two": [
            "Review of Relevant Literature",
            "Review of Existing Systems",
            "Relevant Engineering Principles",
            "Research Gap",
        ],
        "Chapter Three": [
            "Materials and Equipment",
            "Design Methodology",
            "Engineering Calculations",
            "Construction or Implementation",
            "Testing Procedure",
        ],
        "Chapter Four": [
            "Results and Observations",
            "Analysis and Discussion",
            "Performance Evaluation",
        ],
        "Chapter Five": [
            "Summary",
            "Conclusion",
            "Recommendations",
        ],
    }

    def load_institutional_rules(self):
        import json

        root = Path("knowledge_base/institution")

        files = {
            "institutional_rules": root / "institutional_rules.json",
            "formatting_rules": root / "formatting_rules.json",
        }

        result = {}

        for name, file_path in files.items():
            if not file_path.exists():
                result[name] = {
                    "status": "FILE NOT FOUND",
                    "data": None,
                }
                continue

            try:
                data = json.loads(
                    file_path.read_text(encoding="utf-8")
                )
                result[name] = {
                    "status": "LOADED",
                    "data": data,
                }
            except (json.JSONDecodeError, OSError) as error:
                result[name] = {
                    "status": "ERROR",
                    "message": str(error),
                    "data": None,
                }

        return result

    def check_research_evidence(self, project_dir):
        from research_evidence import ResearchEvidence

        evidence = ResearchEvidence(project_dir)
        return evidence.get_review_report()

    def check_chapter(self, file_path, chapter_name, plan=None):
        path = Path(file_path)

        if not path.exists():
            return {
                "status": "ERROR",
                "message": f"File not found: {path}",
            }

        text = path.read_text(encoding="utf-8")
        lower_text = text.lower()

        required = self.REQUIRED_SECTIONS.get(chapter_name, [])

        if plan is not None:
            research_plan = plan.get("research_plan", {})
            outline = research_plan.get("chapter_outline", {})
            template_headings = outline.get(chapter_name)

            if template_headings is not None:
                required = template_headings

        missing = [
            heading for heading in required
            if heading.lower() not in lower_text
        ]

        word_count = len(text.split())

        source_flags = text.count("[VERIFIED SOURCE REQUIRED]")
        input_flags = text.count("[STUDENT INPUT REQUIRED]")

        source_lines = [
            line.strip()
            for line in text.splitlines()
            if "[VERIFIED SOURCE REQUIRED]" in line
        ]

        student_input_lines = [
            line.strip()
            for line in text.splitlines()
            if "[STUDENT INPUT REQUIRED]" in line
        ]

        issues = []

        if missing:
            issues.append("Required headings are missing.")

        if word_count < 300:
            issues.append("Chapter may be too short.")

        if source_flags:
            issues.append("Some claims need verified sources.")

        if input_flags:
            issues.append("Some information requires student input.")

        if text.rstrip().endswith(("select", "and", "or", "the")):
            issues.append("The chapter may end mid-sentence.")

        institutional = self.load_institutional_rules()
        institutional_data = institutional.get(
            "institutional_rules", {}
        ).get("data") or {}

        institution_info = institutional_data.get(
            "institution", {}
        )

        return {
            "status": "NEEDS REVIEW" if issues else "PASSED BASIC CHECKS",
            "institution": institution_info.get("name", "Unknown"),
            "institutional_rules_status": institution_info.get(
                "rules_status", "unknown"
            ),
            "template_validation": (
                "CHECKED AGAINST PROJECT OUTLINE"
                if plan is not None
                else "CHECKED AGAINST DEFAULT SECTIONS"
            ),
            "institutional_compliance": (
                "NOT VERIFIED: OFFICIAL REQUIREMENTS NOT CHECKED"
            ),
            "chapter": chapter_name,
            "word_count": word_count,
            "missing_headings": missing,
            "source_flags": source_flags,
            "source_lines": source_lines,
            "student_input_flags": input_flags,
            "student_input_lines": student_input_lines,
            "issues": issues,
        }
