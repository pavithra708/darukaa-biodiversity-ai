# Interview Questions & Model Answers

Prepared for Darukaa.Earth / AI biodiversity system interviews.

---

## A. Product & problem understanding

### 1. What problem does this system solve that ChatGPT alone does not?
**Answer:** Generative models can sound plausible but lack a guaranteed retrieval trail, structured multi-metric state, and constrained recommendation schemas. We separate **knowledge retrieval**, **ecological assessment**, and **language generation**, so claims are grounded in indexed evidence and cross-variable logic (soil × water × land use).

### 2. Why did the brief forbid “generic sustainable practices”?
**Answer:** Vague advice is not decision-support. Land managers need **actionable interventions**, **mechanisms**, **metric deltas**, and **credible sources**—otherwise the system is not scientifically useful.

### 3. What is the “critical triad” of inputs?
**Answer:** Soil organic carbon %, rainfall pattern, and land-use type. With those three, we can already couple soil degradation, water stress, and habitat homogenization—the minimum for multi-metric reasoning.

---

## B. System design & RAG

### 4. Explain your RAG pipeline.
**Answer:** Curated documents (soil, biodiversity, climate, land use, human impact, interventions) are embedded with `sentence-transformers/all-MiniLM-L6-v2`, stored in ChromaDB with cosine similarity. At query time we build a composite query from user text + structured fields + degraded-metric signals, retrieve top-k chunks, and expose them in the API response.

### 5. Why ChromaDB + local embeddings instead of only an LLM context window?
**Answer:** Persistent, inspectable retrieval; cheaper/repeatable; works without API keys; supports growth of the knowledge base; and makes grounding **auditable** for evaluators.

### 6. How do you prevent hallucinated citations?
**Answer:** Citations are attached to knowledge chunks and recommendation templates. Optional LLM polish is instructed **not to invent numbers or sources**; the structured recommender is source-of-truth.

### 7. What is in each vector metadata record?
**Answer:** domain, title, source, citation, year, url, metrics JSON, optional triggers/time horizon for interventions.

### 8. How would you ingest real research PDFs at scale?
**Answer:** Parse PDF → chunk by section → LLM/heuristic metadata extraction (metrics, geography) → embed → deduplicate → human review queue for high-stakes claims. Add citation graph filters (FAO/IPCC/IPBES whitelist).

---

## C. Multi-metric reasoning

### 9. Give an example of multi-metric reasoning from your system.
**Answer:** SOC 0.3% + low rainfall + wheat monoculture in semi-arid land → not “add fertilizer.” We link: monoculture suppresses SOC; low rainfall gates sequestration and species survival; monoculture fragments habitat. Recommendations jointly apply water harvesting, legume covers, agroforestry, and habitat margins.

### 10. Why water harvesting before expecting large SOC gains in drylands?
**Answer:** Organic matter decomposition and root growth need moisture. Without infiltration/mulching, cover-crop carbon inputs fail—soil and hydrology are coupled.

### 11. How do you score confidence?
**Answer:** Base confidence from trigger strength (how many reinforcing signals fired) plus a small bump when retrieved RAG text supports the same metrics. It is heuristic, not Bayesian—honest about uncertainty.

### 12. What if metrics conflict (e.g., high habitat diversity but toxic pollution)?
**Answer:** Pollution is treated as a blocking constraint: habitat strips alone are insufficient; IPM/toxicity reduction is prioritized because chemical stress can erase biodiversity gains.

---

## D. Conversational intelligence

### 13. How does memory work?
**Answer:** Session object stores turns and a cumulative `StructuredSiteInput`. Later messages merge newly extracted fields (e.g., user later says pH 5.1).

### 14. How do you extract structure from free text?
**Answer:** Lightweight pattern extraction for SOC, pH, rainfall keywords, land-use terms, crops, pollution, and lat/lon—enough for hackathon robustness without a heavy NER dependency.

### 15. When do you ask clarifying questions vs answer?
**Answer:** If critical triad missing and we lack ≥3 assessed metrics, we emphasize clarifying questions. If enough context exists, we answer and may still ask one optional follow-up (e.g., geo).

---

## E. APIs, engineering, CI

### 16. Key endpoints?
**Answer:** `POST /chat` (text+JSON), `POST /analyze` (structured only), `POST /ingest`, `GET /health`, `GET /` demo UI, OpenAPI at `/docs`.

### 17. What does CI verify?
**Answer:** Recommender invariants on the challenge example (multi-metric links, evidence present, agroforestry/intercrop themes), clarifying-question behavior, and import sanity.

### 18. How would you productionize sessions?
**Answer:** Move memory to Redis/Postgres, add auth, rate limits, observability on retrieval scores, and evaluation dashboards for citation faithfulness.

---

## F. Domain / science depth (they will probe this)

### 19. Why is SOC a “master variable”?
**Answer:** It proxies soil structure, water holding, nutrient cycling, and microbial habitat. Raising SOC tends to improve multiple biodiversity-relevant functions—but climate and land use determine whether gains stick.

### 20. What does IPBES emphasize about land use?
**Answer:** Land-use change and homogenization are top drivers of biodiversity loss; plot-level agronomy without habitat structure/connectivity underperforms.

### 21. Difference between species richness and habitat diversity?
**Answer:** Richness counts taxa; habitat diversity captures structural/niche variety that *enables* richness. We intervene on habitat to move richness sustainably.

### 22. Name credible sources you rely on.
**Answer:** FAO (soils, cover crops, dryland agroforestry, pollinators), IPCC (climate–ecosystem), IPBES (biodiversity drivers), CGIAR/ICRISAT (dryland water), UNEP (pollution), USDA NRCS (pH/soil biology).

---

## G. Behavioral / design trade-off questions

### 23. Why keep a rule-guided recommender instead of pure LLM tool-calling?
**Answer:** Controllability and evaluability. Rules encode scientific guardrails; RAG supplies evidence; LLM is optional narration. For high-stakes environmental advice, constrained generation is safer.

### 24. What’s the biggest limitation today?
**Answer:** Knowledge base is curated summaries—not full corpus scale; geo is optional context only (no live SoilGrids yet); confidence is heuristic; sessions are in-memory.

### 25. If you had one more week, what would you ship?
**Answer:** PDF ingestion pipeline + faithfulness eval set + geo enrichment API + persistent sessions—deepening grounding and measurability rather than UI chrome.

---

## H. Rapid-fire definitions

| Term | One-liner |
|------|-----------|
| RAG | Retrieve evidence chunks, then generate/decide with them |
| Embedding | Vector representation of meaning for similarity search |
| SOC | Soil organic carbon — key soil health indicator |
| Habitat fragmentation | Breakup of continuous habitat reducing connectivity |
| Agroforestry | Integrating trees with crops/livestock for multi-strata benefits |
| IPM | Integrated Pest Management — ecology-based pest control |
| Multi-metric reasoning | Explaining outcomes via interactions of several variables |

---

## I. Questions *you* can ask them

1. Which biodiversity indicators matter most for Darukaa’s customers (farm, forest, wetland)?  
2. Do you prioritize remote-sensing inputs or farmer-reported ground truth?  
3. How do you validate scientific claims in production—expert review, literature graphs?  
4. What’s the deployment constraint—edge offline vs cloud LLM?

---

## J. Practice prompt (mock interview)

Interviewer: “User says biodiversity is falling; SOC unknown.”  
You: Ask for SOC %, rainfall, land use; explain why those three unlock soil↔water↔habitat reasoning; offer to proceed with scenarios if they only know land use.

Interviewer: “Give one non-obvious recommendation for semi-arid wheat monoculture with SOC 0.3%.”  
You: Lead with **water harvesting + agroforestry/intercropping sequence**, cite FAO dryland guidance + IPCC AFOLU framing, list metrics (SOC, habitat diversity, microclimate), give medium/long horizons, confidence ~0.85.
