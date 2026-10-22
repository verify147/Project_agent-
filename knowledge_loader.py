import json
from pathlib import Path


class KnowledgeBaseLoader:
    """
    Loads and validates JSON knowledge files
    for the Academic Brain system.
    """

    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent

        self.root_dir = Path(root_dir)
        self.knowledge_dir = self.root_dir / "knowledge_base"

    def load_json(self, file_path):
        """Load a JSON file and report useful errors."""

        path = Path(file_path)

        if not path.is_absolute():
            path = self.root_dir / path

        if not path.exists():
            raise FileNotFoundError(
                f"Knowledge file not found: {path}"
            )

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON in {path}: "
                f"line {error.lineno}, column {error.colno}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                f"Knowledge file must contain a JSON object: {path}"
            )

        return data

    def load_directory(self, directory):
        """Load all JSON files from a directory."""

        directory = Path(directory)

        if not directory.is_absolute():
            directory = self.root_dir / directory

        if not directory.exists():
            return {}

        knowledge = {}

        for path in sorted(directory.glob("*.json")):
            knowledge[path.stem] = self.load_json(path)

        return knowledge

    def load_institution_rules(self):
        """Load institutional rules and formatting rules."""

        directory = self.knowledge_dir / "institution"

        return self.load_directory(directory)

    def load_department_rules(self):
        """Load all available departmental knowledge."""

        directory = self.knowledge_dir / "departments"

        return self.load_directory(directory)

    def load_research_rules(self):
        """Load research policies."""

        directory = self.knowledge_dir / "research_rules"

        return self.load_directory(directory)

    def load_all(self):
        """Load the complete available knowledge base."""

        return {
            "institution": self.load_institution_rules(),
            "departments": self.load_department_rules(),
            "research": self.load_research_rules()
        }

    def report(self):
        """Print a summary of the knowledge currently available."""

        knowledge = self.load_all()

        print("\nACADEMIC BRAIN: KNOWLEDGE BASE REPORT")
        print("=" * 45)

        for category, files in knowledge.items():
            print(f"\n{category.upper()}")

            if not files:
                print("  No knowledge files found.")
                continue

            for name, data in files.items():
                status = data.get(
                    "knowledge_status",
                    data.get("status", "status not specified")
                )

                print(f"  - {name}: {status}")

        print("\nKnowledge loading completed.")
        return knowledge


if __name__ == "__main__":
    loader = KnowledgeBaseLoader()
    loader.report()
