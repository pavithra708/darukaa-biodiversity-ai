from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src import __version__
from src.config import get_settings
from src.conversation.orchestrator import BiodiversityOrchestrator
from src.knowledge.ingest import ingest_knowledge
from src.knowledge.vector_store import get_vector_store
from src.models.schemas import ChatRequest, ChatResponse, IngestStats, StructuredSiteInput

orchestrator = BiodiversityOrchestrator()


@asynccontextmanager
async def lifespan(_: FastAPI):
    store = get_vector_store()
    if store.count() == 0:
        ingest_knowledge(reset=True)
    yield


app = FastAPI(
    title="Darukaa Biodiversity Intelligence API",
    description=(
        "RAG-grounded AI environmental scientist for biodiversity, soil, climate, "
        "and land-use multi-metric reasoning."
    ),
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    settings = get_settings()
    store = get_vector_store()
    return {
        "status": "ok",
        "version": __version__,
        "documents_indexed": store.count(),
        "llm_enabled": settings.llm_enabled,
        "vector_backend": getattr(store, "backend_name", "unknown"),
    }


@app.post("/ingest", response_model=IngestStats)
def ingest(reset: bool = True):
    return ingest_knowledge(reset=reset)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message and not request.site:
        raise HTTPException(
            status_code=400,
            detail="Provide message text and/or structured site JSON.",
        )
    return orchestrator.handle(request)


@app.post("/analyze", response_model=ChatResponse)
def analyze(site: StructuredSiteInput):
    """Structured-input endpoint (JSON site snapshot)."""
    return orchestrator.handle(ChatRequest(site=site, message="Analyze this site for biodiversity risk."))


@app.get("/", response_class=HTMLResponse)
def demo_page():
    html_path = Path(__file__).resolve().parents[1] / "web" / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse(
        "<h1>Darukaa Biodiversity Intelligence</h1>"
        "<p>API is running. Use POST /chat or open /docs.</p>"
    )


def run():
    import uvicorn

    settings = get_settings()
    uvicorn.run("src.main:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    run()
