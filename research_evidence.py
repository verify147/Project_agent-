
import json
from pathlib import Path
from datetime import datetime, timezone


class ResearchEvidence:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.project_dir / "research_evidence.json"

        if not self.db_path.exists():
            self._save({
                "sources": [],
                "claims": [],
                "created_at": datetime.now(timezone.utc).isoformat()
            })

    def _load(self):
        return json.loads(self.db_path.read_text(encoding="utf-8"))

    def _save(self, data):
        self.db_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def add_source(self, title, authors, year, publisher, url, notes=""):
        data = self._load()

        source = {
            "source_id": f"S{len(data['sources']) + 1:03d}",
            "title": title,
            "authors": authors,
            "year": year,
            "publisher": publisher,
            "url": url,
            "notes": notes,
            "verification_status": "NOT_VERIFIED"
        }

        data["sources"].append(source)
        self._save(data)
        return source

    def add_claim(self, claim_text, source_ids=None):
        data = self._load()

        claim = {
            "claim_id": f"C{len(data['claims']) + 1:03d}",
            "claim_text": claim_text,
            "source_ids": source_ids or [],
            "verification_status": "NEEDS_REVIEW"
        }

        data["claims"].append(claim)
        self._save(data)
        return claim

    def link_source_to_claim(self, claim_id, source_id):
        """Link a recorded source to a recorded claim."""

        data = self._load()

        claim = next(
            (c for c in data["claims"]
             if c["claim_id"] == claim_id),
            None
        )
        source = next(
            (s for s in data["sources"]
             if s["source_id"] == source_id),
            None
        )

        if claim is None:
            raise ValueError(f"Claim not found: {claim_id}")
        if source is None:
            raise ValueError(f"Source not found: {source_id}")

        if source_id not in claim["source_ids"]:
            claim["source_ids"].append(source_id)

        self._save(data)
        return claim

    def review_source(self, source_id, status, notes):
        allowed = {"VERIFIED", "UNVERIFIED", "INVALID"}

        if status not in allowed:
            raise ValueError(f"Status must be one of {allowed}")

        data = self._load()
        source = next(
            (s for s in data["sources"]
             if s["source_id"] == source_id),
            None
        )

        if source is None:
            raise ValueError(f"Source not found: {source_id}")

        source["verification_status"] = status
        source["verification_notes"] = notes
        source["reviewed_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        self._save(data)
        return source

    def review_claim(self, claim_id, status, notes):
        allowed = {
            "SUPPORTED", "PARTIALLY_SUPPORTED",
            "UNSUPPORTED", "NEEDS_REVIEW"
        }

        if status not in allowed:
            raise ValueError(f"Status must be one of {allowed}")

        data = self._load()
        claim = next(
            (c for c in data["claims"]
             if c["claim_id"] == claim_id),
            None
        )

        if claim is None:
            raise ValueError(f"Claim not found: {claim_id}")

        claim["verification_status"] = status
        claim["review_notes"] = notes
        claim["reviewed_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        self._save(data)
        return claim

    def get_review_report(self):
        data = self._load()

        source_issues = [
            s for s in data["sources"]
            if s.get("verification_status") != "VERIFIED"
        ]

        claim_issues = [
            c for c in data["claims"]
            if (
                c.get("verification_status") != "SUPPORTED"
                or not c.get("source_ids")
            )
        ]

        return {
            "total_sources": len(data["sources"]),
            "total_claims": len(data["claims"]),
            "sources_needing_review": source_issues,
            "claims_needing_review": claim_issues,
            "ready_for_final_review": (
                len(data["sources"]) > 0
                and len(data["claims"]) > 0
                and not source_issues
                and not claim_issues
            ),
        }

    def get_claim_review_details(self):
        """Explain why each claim still needs review."""

        data = self._load()
        sources = {
            s["source_id"]: s
            for s in data["sources"]
        }
        details = []

        for claim in data["claims"]:
            reasons = []
            linked = claim.get("source_ids", [])

            if not linked:
                reasons.append("NO_LINKED_SOURCE")

            for source_id in linked:
                source = sources.get(source_id)

                if source is None:
                    reasons.append(
                        f"SOURCE_NOT_FOUND:{source_id}"
                    )
                elif source.get("verification_status") != "VERIFIED":
                    reasons.append(
                        f"SOURCE_NOT_VERIFIED:{source_id}"
                    )

            if claim.get("verification_status") != "SUPPORTED":
                reasons.append("CLAIM_NOT_MARKED_SUPPORTED")

            details.append({
                "claim_id": claim["claim_id"],
                "claim_text": claim["claim_text"],
                "source_ids": linked,
                "review_reasons": reasons,
            })

        return details

    def list_sources(self):
        return self._load()["sources"]

    def list_claims(self):
        return self._load()["claims"]
