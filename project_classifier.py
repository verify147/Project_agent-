
import re


class ProjectClassifier:
    """Provides an initial, rule-based academic project classification."""

    CATEGORIES = {
        "engineering_design_construction": [
            "design and construction",
            "design and fabrication",
            "fabrication of",
            "construction of",
            "prototype",
            "mechanical design",
        ],
        "software_or_ai": [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "software development",
            "mobile application",
            "web application",
            "computer vision",
            "prediction model",
            "detection system",
        ],
        "agricultural_field_study": [
            "maize yield",
            "crop yield",
            "soil fertility",
            "irrigation scheduling",
            "field trial",
            "growth and yield",
            "fertilizer rates",
            "pest management",
        ],
        "experimental_or_laboratory": [
            "experimental investigation",
            "laboratory analysis",
            "laboratory investigation",
            "experimental study",
        ],
        "survey_or_social_research": [
            "questionnaire",
            "survey of",
            "perception of",
            "attitude towards",
            "consumer behaviour",
            "consumer behavior",
            "social media advertising",
        ],
        "business_or_management": [
            "business performance",
            "marketing strategy",
            "customer satisfaction",
            "financial performance",
            "sales promotion",
        ],
        "literature_review": [
            "literature review",
            "systematic review",
            "review of",
            "state of the art",
        ],
    }

    def classify(self, topic):
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("A project topic is required.")

        text = re.sub(r"\s+", " ", topic.lower()).strip()

        scores = {
            category: sum(
                phrase in text for phrase in phrases
            )
            for category, phrases in self.CATEGORIES.items()
        }

        matched = [
            category for category, score in scores.items()
            if score > 0
        ]

        if not matched:
            return {
                "primary_type": "other_or_unclassified",
                "related_types": [],
                "research_method": "undetermined",
                "confidence": "low",
                "needs_review": True,
                "matched_rules": [],
            }

        matched.sort(
            key=lambda category: scores[category],
            reverse=True,
        )

        highest_score = scores[matched[0]]
        tied = [
            category for category in matched
            if scores[category] == highest_score
        ]

        # Agricultural topics can also be experimental.
        # Keep both classifications when the topic supports them.
        if (
            "agricultural_field_study" in matched
            and "experimental_or_laboratory" in matched
        ):
            primary = "agricultural_field_study"
        else:
            primary = matched[0]

        related = [
            category for category in matched
            if category != primary
        ]

        # A title alone rarely establishes the actual method.
        if "survey_or_social_research" in matched:
            method = "survey_or_social_research_possible"
        elif "experimental_or_laboratory" in matched:
            method = "experimental_possible"
        elif "agricultural_field_study" in matched:
            method = "field_study_possible"
        elif primary == "literature_review":
            method = "literature_review_possible"
        elif primary in (
            "engineering_design_construction",
            "software_or_ai",
        ):
            method = "design_or_development_possible"
        else:
            method = "undetermined"

        confidence = "moderate" if len(tied) == 1 else "low"

        return {
            "primary_type": primary,
            "related_types": related,
            "research_method": method,
            "confidence": confidence,
            "needs_review": True,
            "matched_rules": [
                phrase
                for category in matched
                for phrase in self.CATEGORIES[category]
                if phrase in text
            ],
        }
