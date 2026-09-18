from __future__ import annotations

from data.knowledge_base import ALL_DOCUMENTS
from src.config import get_settings
from src.knowledge.vector_store import VectorStore, get_vector_store
from src.models.schemas import IngestStats


def ingest_knowledge(reset: bool = True) -> IngestStats:
    """Index curated biodiversity / environmental documents into ChromaDB."""
    settings = get_settings()
    store = get_vector_store()
    if reset:
        # Drop cached singleton state by rebuilding collection
        store.reset()
    count = store.add_documents(list(ALL_DOCUMENTS))
    return IngestStats(
        documents_indexed=count,
        collection=VectorStore.COLLECTION,
        persist_dir=str(settings.chroma_persist_dir),
    )


if __name__ == "__main__":
    stats = ingest_knowledge(reset=True)
    print(stats.model_dump_json(indent=2))
