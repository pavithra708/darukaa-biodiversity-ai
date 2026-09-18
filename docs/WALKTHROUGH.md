# Project Walkthrough (for you)

Use this as your personal study guide before interviews / demos.

## 60-second pitch

“I built a biodiversity intelligence system that behaves like an environmental scientist. It indexes curated soil, climate, land-use, biodiversity, and intervention knowledge into ChromaDB, retrieves evidence with embeddings, then runs a multi-metric reasoner that couples soil carbon, water, and habitat fragmentation. Every recommendation includes what to do, why it works, which metrics move, time horizon, confidence, and a FAO/IPCC/IPBES-style citation. It asks clarifying questions when the critical triad is missing, and supports text + JSON + optional geo.”

## How a request flows

1. **Input** — free text and/or JSON site snapshot (+ optional lat/lon).  
2. **Memory** — session merges new metrics; regex/NLP extracts SOC, rainfall, land use from text.  
3. **Assess** — each metric scored critical/low/moderate/good.  
4. **Link** — explicit couplings (e.g., low rainfall blocks SOC sequestration).  
5. **Retrieve** — query embedding → top-k Chroma hits (shown in response).  
6. **Recommend** — trigger rules + RAG evidence → structured recommendations.  
7. **Clarify** — if SOC / rainfall / land use missing, ask before over-claiming.  
8. **Optional LLM polish** — rewrites draft without inventing new numbers/citations.

## Why this beats a plain LLM chatbot

| Plain LLM | This system |
|-----------|-------------|
| Knowledge only in weights | Explicit retrievable KB |
| Citations often fabricated | Citations attached to indexed chunks / playbook |
| Single-variable advice | Forced multi-metric couplings |
| No memory schema | Cumulative structured site state |
| Opaque | `retrieved_knowledge` + assessments returned |

## Demo script (5 minutes)

1. Incomplete: *“Biodiversity is declining on my land”* → clarifying questions.  
2. Structured JSON example (SOC 0.3%, low rain, wheat monoculture, semi-arid) → agroforestry + cover crops + water harvesting + margins.  
3. Follow-up in same session: *“soil pH is 5.1”* → pH correction recommendation appears (memory).  
4. Open response JSON → show `retrieved_knowledge` scores.  
5. Mention CI + tests for recommender invariants.

## Files to know cold

- `src/conversation/orchestrator.py` — pipeline glue  
- `src/reasoning/multi_metric.py` — couplings  
- `src/reasoning/recommender.py` — evidence-backed actions  
- `src/knowledge/vector_store.py` — embeddings + Chroma  
- `data/knowledge_base/*.py` — scientific content  

## Stretch improvements (if asked “what next?”)

- Swap in real remote-sensing / SoilGrids APIs for geo inputs  
- Add evaluation harness (faithfulness of citations)  
- Persistent session DB (Redis/Postgres)  
- Spatial layer (postgis) for fragmentation metrics  
- Expand KB with full-text PDF ingestion from FAO/IPBES reports  
