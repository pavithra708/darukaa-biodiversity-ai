# Darukaa.Earth — AI Biodiversity Intelligence

RAG-grounded conversational system that reasons like an environmental scientist across **soil × water × land-use × biodiversity × climate × human impact**.

Not a prompt-only chatbot: curated knowledge is embedded into a **retrievable vector index**, retrieved per query, and combined with a **multi-metric reasoning engine** that produces evidence-backed recommendations (FAO, IPCC, IPBES, CGIAR/ICRISAT, UNEP, USDA NRCS).

## Architecture

```
User (text | JSON | geo)
        │
        ▼
┌───────────────────┐
│ Conversation      │  session memory + NLP metric extraction
│ Memory            │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Multi-metric      │  assess SOC, pH, rainfall, land use, habitat…
│ Assessor          │  build soil↔biodiversity↔water couplings
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ RAG Retriever     │  embeddings + vector search
│ (knowledge layer) │  ChromaDB if available, else NumPy hashing RAG
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Recommender       │  multi-trigger interventions + citations
│ + Clarifier       │  ask for missing critical variables
└─────────┬─────────┘
          ▼
   Structured response
   (optional OpenAI polish)
```

### Knowledge domains indexed

| Domain | Examples |
|--------|----------|
| Soil health | SOC thresholds, pH window, moisture–fauna, legume cover crops |
| Biodiversity | species richness, pollinators, microbiome, fragmentation |
| Climate | rainfall–survival, temperature/phenology, dryland agroforestry |
| Land use | monoculture risks, intercropping, riparian buffers |
| Human impact | deforestation cascades, pollution, overgrazing |
| Interventions | actionable playbook with metrics, horizons, triggers |

## Database / schema

**Vector store:** collection `biodiversity_knowledge`

- **Preferred:** ChromaDB + sentence-transformers  
- **Fallback:** NumPy hashing embeddings + cosine search (`data/chroma/local_index.json`) — used automatically when native ML DLLs are blocked

Each chunk metadata:

- `domain`, `title`, `source`, `citation`, `year`, `url`
- `metrics` (JSON list)
- `time_horizon`, `triggers` (for intervention docs)

**Session memory:** in-process store keyed by `session_id` with cumulative `StructuredSiteInput`.

### Structured site schema (JSON)

```json
{
  "soil_organic_carbon_pct": 0.3,
  "soil_ph": 6.2,
  "soil_moisture": "dry",
  "rainfall": "low",
  "temperature_c": 34,
  "land_use": "monoculture",
  "crop": "wheat",
  "region": "semi-arid",
  "species_richness": 8,
  "habitat_diversity_index": 0.2,
  "deforestation_pressure": "moderate",
  "pollution_level": "low",
  "latitude": 26.9,
  "longitude": 75.8
}
```

## Local setup

```bash
cd darukaa-biodiversity-ai
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # or: cp .env.example .env

# Index knowledge (downloads embedding model on first run)
python scripts/ingest_knowledge.py

# API + minimal demo UI
python -m src.main
# → http://127.0.0.1:8000      (UI)
# → http://127.0.0.1:8000/docs (OpenAPI)

# CLI
python scripts/demo_cli.py
```

Optional: set `OPENAI_API_KEY` in `.env` for natural-language polish. **The system is fully functional without it** (deterministic RAG + reasoning).

### Example API call

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Analyze biodiversity risk\",\"site\":{\"soil_organic_carbon_pct\":0.3,\"rainfall\":\"low\",\"land_use\":\"monoculture\",\"crop\":\"wheat\",\"region\":\"semi-arid\"}}"
```

### Clarifying-question demo

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Biodiversity is declining on my land\"}"
```

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`):

1. Install Python 3.11 + dependencies  
2. Run `pytest tests/test_reasoning.py`  
3. Import/syntax sanity check  

## Project layout

```
darukaa-biodiversity-ai/
├── data/knowledge_base/     # curated scientific chunks
├── src/
│   ├── knowledge/           # ingest, ChromaDB, retriever
│   ├── reasoning/           # multi-metric + recommender + clarifier
│   ├── conversation/        # memory + orchestrator
│   ├── llm/                 # optional OpenAI polish
│   ├── models/schemas.py
│   └── main.py              # FastAPI
├── scripts/                 # ingest + CLI
├── web/index.html           # lightweight demo UI
├── tests/
├── docs/                    # submission + interview prep
└── .github/workflows/ci.yml
```

## Evaluation mapping

| Criterion | How this project addresses it |
|-----------|-------------------------------|
| Depth of reasoning | Cross-links SOC↔land use↔rainfall↔habitat; non-obvious sequences (water harvesting before SOC build in drylands) |
| Scientific grounding | Every recommendation carries citation + measurable impact estimate |
| Knowledge system | Real embeddings + ChromaDB RAG; retrieval shown in API response |
| Conversational intelligence | Session memory, metric extraction from text, clarifying questions |
| Output clarity | Action, why, metrics, horizon, confidence, evidence |

## License

Built for the Darukaa.Earth Hackathon challenge.
