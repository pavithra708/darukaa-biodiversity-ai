#!/usr/bin/env python
"""Ingest curated knowledge into ChromaDB."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.knowledge.ingest import ingest_knowledge


if __name__ == "__main__":
    reset = "--no-reset" not in sys.argv
    stats = ingest_knowledge(reset=reset)
    print(stats.model_dump_json(indent=2))
