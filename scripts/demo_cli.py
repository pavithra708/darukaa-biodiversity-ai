#!/usr/bin/env python
"""Interactive CLI demo for the Darukaa biodiversity intelligence system."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.conversation.orchestrator import BiodiversityOrchestrator
from src.knowledge.ingest import ingest_knowledge
from src.knowledge.vector_store import get_vector_store
from src.models.schemas import ChatRequest, StructuredSiteInput

console = Console()


EXAMPLE_JSON = {
    "soil_organic_carbon_pct": 0.3,
    "rainfall": "low",
    "land_use": "monoculture",
    "crop": "wheat",
    "region": "semi-arid",
}


def ensure_index() -> None:
    store = get_vector_store()
    if store.count() == 0:
        console.print("[yellow]Indexing knowledge base (first run)...[/yellow]")
        stats = ingest_knowledge(reset=True)
        console.print(f"[green]Indexed {stats.documents_indexed} documents[/green]")


def main() -> None:
    ensure_index()
    orch = BiodiversityOrchestrator()
    session_id = None

    console.print(
        Panel.fit(
            "[bold green]Darukaa.Earth Biodiversity Intelligence[/bold green]\n"
            "Type a question, paste JSON site data, or 'example' / 'quit'.",
            border_style="green",
        )
    )

    while True:
        try:
            user = console.input("\n[bold cyan]You>[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye.")
            break

        if not user:
            continue
        if user.lower() in {"quit", "exit", "q"}:
            break
        if user.lower() == "example":
            user = json.dumps(EXAMPLE_JSON)

        request: ChatRequest
        if user.startswith("{"):
            data = json.loads(user)
            request = ChatRequest(
                session_id=session_id,
                site=StructuredSiteInput(**data),
                message="Analyze this land parcel and recommend biodiversity interventions.",
            )
        else:
            request = ChatRequest(session_id=session_id, message=user)

        response = orch.handle(request)
        session_id = response.session_id
        console.print(Markdown(response.answer))

        if os.environ.get("DARUKAA_DEBUG") == "1":
            console.print(
                f"\n[dim]session={session_id} | needs_more_info={response.needs_more_info} "
                f"| recs={len(response.recommendations)} | rag_hits={len(response.retrieved_knowledge)}[/dim]"
            )


if __name__ == "__main__":
    main()
