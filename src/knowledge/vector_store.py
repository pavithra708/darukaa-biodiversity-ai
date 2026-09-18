from __future__ import annotations

import hashlib
import json
import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from src.config import get_settings

TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class HashingEmbedder:
    """Deterministic hashing embedder (stdlib + numpy). No native ML DLLs required."""

    def __init__(self, dim: int = 384):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for text in texts:
            vec = np.zeros(self.dim, dtype=np.float64)
            tokens = _tokenize(text)
            if not tokens:
                out.append(vec.tolist())
                continue
            # TF with signed hashing trick
            counts: dict[str, int] = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            for token, tf in counts.items():
                digest = hashlib.md5(token.encode("utf-8")).hexdigest()
                idx = int(digest[:8], 16) % self.dim
                sign = 1.0 if int(digest[8:10], 16) % 2 == 0 else -1.0
                # sublinear TF
                vec[idx] += sign * (1.0 + math.log(tf))
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            out.append(vec.tolist())
        return out


class LocalJsonVectorStore:
    """Persistent cosine-similarity store using JSON + numpy (RAG without Chroma)."""

    COLLECTION = "biodiversity_knowledge"

    def __init__(self, persist_dir: Path | None = None):
        settings = get_settings()
        self.persist_dir = Path(persist_dir or settings.chroma_persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.persist_dir / "local_index.json"
        self.embedder = HashingEmbedder(dim=384)
        self._docs: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            self._docs = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self._docs = []

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._docs, indent=2), encoding="utf-8")

    def reset(self) -> None:
        self._docs = []
        if self.path.exists():
            self.path.unlink()

    def add_documents(self, documents: list[dict[str, Any]]) -> int:
        if not documents:
            return 0
        texts = [
            f"{d.get('title', '')}. {d.get('content', '')} "
            f"Source: {d.get('source', '')}. {d.get('citation', '')}"
            for d in documents
        ]
        embeddings = self.embedder.embed(texts)
        by_id = {d["id"]: i for i, d in enumerate(self._docs)}
        for d, text, emb in zip(documents, texts, embeddings):
            record = {
                "id": d["id"],
                "text": text,
                "embedding": emb,
                "domain": d.get("domain", "general"),
                "title": d.get("title", ""),
                "source": d.get("source", ""),
                "citation": d.get("citation", ""),
                "year": int(d.get("year") or 0),
                "url": d.get("url") or "",
                "metrics": d.get("metrics") or [],
                "time_horizon": d.get("time_horizon") or "",
                "triggers": d.get("triggers") or [],
            }
            if d["id"] in by_id:
                self._docs[by_id[d["id"]]] = record
            else:
                self._docs.append(record)
                by_id[d["id"]] = len(self._docs) - 1
        self._save()
        return len(documents)

    def query(self, text: str, top_k: int = 5, where: dict | None = None) -> list[dict[str, Any]]:
        if not self._docs:
            return []
        q = np.array(self.embedder.embed([text])[0], dtype=np.float64)
        scored: list[tuple[float, dict[str, Any]]] = []
        for doc in self._docs:
            if where and where.get("domain") and doc.get("domain") != where["domain"]:
                continue
            emb = np.array(doc["embedding"], dtype=np.float64)
            score = float(np.dot(q, emb))
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        hits: list[dict[str, Any]] = []
        for score, doc in scored[:top_k]:
            hits.append(
                {
                    "id": doc["id"],
                    "text": doc["text"],
                    "score": score,
                    "domain": doc.get("domain"),
                    "title": doc.get("title"),
                    "source": doc.get("source"),
                    "citation": doc.get("citation"),
                    "year": doc.get("year") or None,
                    "url": doc.get("url") or None,
                    "metrics": doc.get("metrics") or [],
                }
            )
        return hits

    def count(self) -> int:
        return len(self._docs)


class ChromaVectorStore:
    """ChromaDB + sentence-transformers backend when native deps are available."""

    COLLECTION = "biodiversity_knowledge"

    def __init__(self, persist_dir: Path | None = None, model_name: str | None = None):
        import chromadb
        from chromadb.config import Settings as ChromaSettings
        from sentence_transformers import SentenceTransformer

        settings = get_settings()
        self.persist_dir = Path(persist_dir or settings.chroma_persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name or settings.embedding_model
        self._SentenceTransformer = SentenceTransformer
        self._model = None
        self._client = chromadb.PersistentClient(
            path=str(self.persist_dir / "chroma"),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def model(self):
        if self._model is None:
            self._model = self._SentenceTransformer(self.model_name)
        return self._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]

    def reset(self) -> None:
        try:
            self._client.delete_collection(self.COLLECTION)
        except Exception:
            pass
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, documents: list[dict[str, Any]]) -> int:
        if not documents:
            return 0
        ids = [d["id"] for d in documents]
        texts = [
            f"{d.get('title', '')}. {d.get('content', '')} "
            f"Source: {d.get('source', '')}. {d.get('citation', '')}"
            for d in documents
        ]
        embeddings = self.embed(texts)
        metadatas = []
        for d in documents:
            metadatas.append(
                {
                    "domain": d.get("domain", "general"),
                    "title": d.get("title", ""),
                    "source": d.get("source", ""),
                    "citation": d.get("citation", ""),
                    "year": int(d.get("year") or 0),
                    "url": d.get("url") or "",
                    "metrics": json.dumps(d.get("metrics") or []),
                    "time_horizon": d.get("time_horizon") or "",
                    "triggers": json.dumps(d.get("triggers") or []),
                }
            )
        self._collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return len(ids)

    def query(self, text: str, top_k: int = 5, where: dict | None = None) -> list[dict[str, Any]]:
        if self._collection.count() == 0:
            return []
        embedding = self.embed([text])[0]
        kwargs: dict[str, Any] = {
            "query_embeddings": [embedding],
            "n_results": min(top_k, max(1, self._collection.count())),
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where
        result = self._collection.query(**kwargs)
        hits: list[dict[str, Any]] = []
        for i, doc_id in enumerate(result["ids"][0]):
            meta = result["metadatas"][0][i] or {}
            distance = result["distances"][0][i]
            hits.append(
                {
                    "id": doc_id,
                    "text": result["documents"][0][i],
                    "score": 1.0 - float(distance),
                    "domain": meta.get("domain"),
                    "title": meta.get("title"),
                    "source": meta.get("source"),
                    "citation": meta.get("citation"),
                    "year": meta.get("year") or None,
                    "url": meta.get("url") or None,
                    "metrics": json.loads(meta.get("metrics") or "[]"),
                }
            )
        return hits

    def count(self) -> int:
        return self._collection.count()


def _chroma_available() -> bool:
    try:
        settings = get_settings()
        if settings.vector_backend.lower() != "chromadb":
            return False
        import chromadb  # noqa: F401
        from sentence_transformers import SentenceTransformer  # noqa: F401

        return True
    except Exception:
        return False


# Public alias used across the app
class VectorStore:
    """Factory-like wrapper exposing a unified vector store API."""

    COLLECTION = "biodiversity_knowledge"

    def __init__(self, persist_dir: Path | None = None, model_name: str | None = None):
        if _chroma_available():
            self._backend: Any = ChromaVectorStore(persist_dir=persist_dir, model_name=model_name)
            self.backend_name = "chromadb+sentence-transformers"
        else:
            self._backend = LocalJsonVectorStore(persist_dir=persist_dir)
            self.backend_name = "numpy-hashing-rag"

    def reset(self) -> None:
        self._backend.reset()

    def add_documents(self, documents: list[dict[str, Any]]) -> int:
        return self._backend.add_documents(documents)

    def query(self, text: str, top_k: int = 5, where: dict | None = None) -> list[dict[str, Any]]:
        return self._backend.query(text, top_k=top_k, where=where)

    def count(self) -> int:
        return self._backend.count()


@lru_cache
def get_vector_store() -> VectorStore:
    return VectorStore()
