# Darukaa.Earth Submission Document

**Project:** AI Biodiversity Intelligence Chatbot  
**Hackathon:** Darukaa.Earth — AI Biodiversity Intelligence Challenge  
**Document purpose:** Paste/convert this content into the required `.docx` submission.

---

## 1. GitHub repository link

> **TODO before submit:** Create a GitHub repo, push this project, then replace the line below.

**Repository:** `https://github.com/<your-username>/darukaa-biodiversity-ai`

### If the repository is private — grant access to:

- ankita.dasgupta@darukaa.com  
- harsh.kumar@darukaa.com  
- utkarsh.gauniyal@darukaa.com  
- guneet.mutreja@darukaa.com  

If public, only the link is required.

---

## 2. Live demo URL

> **TODO before submit:** Deploy (Railway / Render / Hugging Face Spaces / your VPS) and replace below.

**Live demo:** `https://<your-deployed-host>/`  

**Local demo (reviewers):**

```bash
pip install -r requirements.txt
python scripts/ingest_knowledge.py
python -m src.main
```

Open `http://127.0.0.1:8000` (UI) or `http://127.0.0.1:8000/docs` (API).

**No special credentials required** unless you enable optional OpenAI polish (`OPENAI_API_KEY`).

---

## 3. README overview (architecture, schema, setup, CI/CD)

### What we built

An AI environmental scientist that:

1. Maintains a **retrievable knowledge base** (not prompt-only) covering soil, land use, biodiversity, climate, and human impact.  
2. Handles **multi-turn conversation** with memory and clarifying questions.  
3. Emits **evidence-backed recommendations** (what / why / metrics / citation / time horizon / confidence).  
4. Performs **multi-metric reasoning** (soil ↔ biodiversity ↔ water ↔ land-use fragmentation).  
5. Accepts **text**, **structured JSON**, and optional **geo coordinates**.

### Architecture (short)

`User → Conversation Memory → Multi-metric Assessor → ChromaDB RAG Retriever → Intervention Recommender → Structured Answer (+ optional LLM polish)`

**Stack:** Python, FastAPI, ChromaDB, sentence-transformers (`all-MiniLM-L6-v2`), Pydantic, GitHub Actions CI.

### Database / schema

- **Vector DB:** ChromaDB collection `biodiversity_knowledge`  
- **Chunk fields:** id, title, content, domain, metrics, source, citation, year, url, triggers  
- **Session:** `session_id` + cumulative site metrics  

Critical triad for reasoning: **SOC %**, **rainfall pattern**, **land-use type**.

### Local setup

See repository `README.md`. Summary:

1. `python -m venv .venv` && activate  
2. `pip install -r requirements.txt`  
3. `python scripts/ingest_knowledge.py`  
4. `python -m src.main` or `python scripts/demo_cli.py`

### CI/CD

GitHub Actions workflow runs unit tests on the reasoning layer and import checks on every push/PR to `main`.

---

## 4. Other links / notes for reviewers

| Item | Value |
|------|--------|
| API health | `GET /health` |
| Chat | `POST /chat` |
| Structured analyze | `POST /analyze` |
| Re-ingest KB | `POST /ingest` |
| Example fixture | SOC 0.3%, low rainfall, monoculture wheat, semi-arid |
| Optional LLM | Set `OPENAI_API_KEY` — not required |
| Tests | `pytest tests/test_reasoning.py` |
| Docs in repo | `docs/WALKTHROUGH.md`, `docs/INTERVIEW_PREP.md` |

### Design choices (for evaluators)

- **Knowledge grounding first:** recommendations are generated from metric triggers + retrieved evidence, not free-form hallucination.  
- **Works offline of LLM APIs:** embeddings + rules produce complete, citable answers.  
- **Shows retrieval:** each `/chat` response includes `retrieved_knowledge` with scores and sources.  
- **Dual vector backend:** ChromaDB + sentence-transformers when available; automatic NumPy hashing RAG fallback on locked-down environments (same API, still true retrieval).  
- **Non-obvious sequencing:** e.g., water harvesting unlocked before expecting SOC gains in drylands; pH correction before biodiversity plantings.

### Sample expected behavior (challenge use case)

**Input:** SOC 0.3%, low rainfall, monoculture wheat, semi-arid  

**Output themes:**

- Drought-tolerant agroforestry + intercropping  
- Legume cover crops (~15–25% SOC over 2–3 years, FAO)  
- Micro-catchments / mulching for water–biodiversity coupling  
- Native field margins for habitat diversity  
- Explicit links: SOC↔land use, rainfall↔species survival, land use↔fragmentation  
- Citations: FAO, IPCC, IPBES, ICRISAT  

---

## 5. Submission checklist

- [ ] Push code to GitHub  
- [ ] Add repo URL in this document  
- [ ] Make repo public **or** invite the four Darukaa emails  
- [ ] (Optional) Deploy live demo and paste URL  
- [ ] Convert this file to `.docx` and upload via My Jobs / Applied Job page  
- [ ] Confirm README renders on GitHub  

---

*End of submission document.*
