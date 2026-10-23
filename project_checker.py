
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

    @staticmethod
    def normalize_heading(heading):
        """Normalize heading text and approved equivalent headings."""
        import re

        value = heading.strip().lower()
        value = re.sub(r"^#+\s*", "", value)
        value = re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", value)
        value = re.sub(r"[^a-z0-9 ]", " ", value)
        value = " ".join(value.split())

        aliases = {
            "justification of the study": "significance of the study",
            "justification or significance of the study": "significance of the study",
            "scope of the study": "scope and limitations",
            "aim and specific objectives": "aim and objectives",
            "research objectives": "aim and objectives",
        }

        return aliases.get(value, value)

    @classmethod
    def extract_headings(cls, text):
        """Extract Markdown and numbered headings only."""
        import re

        headings = []

        for line in text.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("#"):
                headings.append(cls.normalize_heading(stripped))
            elif re.match(r"^\d+(?:\.\d+)*[.)]?\s+\S", stripped):
                headings.append(cls.normalize_heading(stripped))

        return set(headings)

    def check_department_requirements(self, text, chapter_name, plan):
        """Check chapter text against saved department requirements."""

        department = plan.get("department_requirements", {})
        chapter_requirements = department.get(
            "chapter_requirements", {}
        )

        chapter_key = {
            "Chapter One": "chapter_one",
            "Chapter Two": "chapter_two",
            "Chapter Three": "chapter_three",
            "Chapter Four": "chapter_four",
            "Chapter Five": "chapter_five",
        }.get(chapter_name)

        if not chapter_key:
            return {
                "status": "NOT CHECKED",
                "reason": "Unknown chapter name.",
                "missing_requirements": [],
            }

        required = chapter_requirements.get(chapter_key, [])

        if not required:
            return {
                "status": "NOT CHECKED",
                "reason": "No department requirements recorded for this chapter.",
                "missing_requirements": [],
            }

        found_headings = self.extract_headings(text)
        missing = [
            item for item in required
            if self.normalize_heading(item) not in found_headings
        ]

        return {
            "status": "NEEDS REVIEW" if missing else "PASSED TEXT MATCH CHECK",
            "knowledge_status": department.get(
                "knowledge_status", "unknown"
            ),
            "missing_requirements": missing,
            "note": (
                "Text matching checks wording only; it does not prove "
                "that a section is complete or academically correct."
            ),
        }

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

        found_headings = self.extract_headings(text)
        missing = [
            heading for heading in required
            if self.normalize_heading(heading) not in found_headings
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

        department_report = None

        if plan is not None:
            department_report = self.check_department_requirements(
                text=text,
                chapter_name=chapter_name,
                plan=plan
            )

        issues = []

        if missing:
            issues.append("Required headings are missing.")

        if (
            department_report
            and department_report["status"] == "NEEDS REVIEW"
            and department_report.get("missing_requirements")
        ):
            issues.append("Department chapter requirements are missing.")

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
            "department_requirements": department_report,
            "source_flags": source_flags,
            "source_lines": source_lines,
            "student_input_flags": input_flags,
            "student_input_lines": student_input_lines,
            "issues": issues,
        }
