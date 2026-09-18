from __future__ import annotations

from typing import Any

from src.config import get_settings
from src.knowledge.vector_store import get_vector_store
from src.models.schemas import StructuredSiteInput


def build_retrieval_query(
    message: str | None,
    site: StructuredSiteInput | None,
    assessments: list[dict[str, Any]] | None = None,
) -> str:
    """Compose a retrieval query from free text + structured site context."""
    parts: list[str] = []
    if message:
        parts.append(message)
    if site:
        for field, value in site.model_dump(exclude_none=True).items():
            parts.append(f"{field}: {value}")
    if assessments:
        for a in assessments:
            if a.get("status") in {"critical", "low"}:
                parts.append(f"degraded {a.get('metric')}: {a.get('value')}")
    parts.append(
        "biodiversity soil carbon rainfall land use habitat climate intervention evidence"
    )
    return " | ".join(parts)


class KnowledgeRetriever:
    def __init__(self, top_k: int | None = None):
        self.top_k = top_k or get_settings().top_k
        self.store = get_vector_store()

    def retrieve(
        self,
        message: str | None = None,
        site: StructuredSiteInput | None = None,
        assessments: list[dict[str, Any]] | None = None,
        top_k: int | None = None,
    ) -> list[dict[str, Any]]:
        query = build_retrieval_query(message, site, assessments)
        hits = self.store.query(query, top_k=top_k or self.top_k)
        # Also pull intervention-focused hits when degradation signals exist
        if assessments and any(a.get("status") in {"critical", "low"} for a in assessments):
            intervention_hits = self.store.query(
                query + " | recommended intervention agroforestry cover crop habitat",
                top_k=3,
            )
            seen = {h["id"] for h in hits}
            for h in intervention_hits:
                if h["id"] not in seen:
                    hits.append(h)
                    seen.add(h["id"])
        return hits[: (top_k or self.top_k) + 2]
