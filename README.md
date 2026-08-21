# VentureLens — Parallel Multi-Source Startup Due-Diligence Engine

VentureLens is a **Phase 2 multi-source retrieval system** that evaluates a startup by querying three independent data engines in parallel:

- **SQLite** — structured startup funding and financial data
- **FAISS + BM25** — semantic and hybrid retrieval over startup news/press documents
- **Neo4j** — founder, investor, competitor, and relationship graph
- **DSPy** — synthesizes the three retrieval contexts into a structured due-diligence verdict
- **Streamlit** — transparent UI showing the raw evidence from all three engines and the final verdict

The project follows the Phase 2 requirement to build a parallel structured + semantic + graph retrieval pipeline and use an **optimized DSPy module** for synthesis.

## Architecture

```text
                         ┌─────────────────────┐
                         │   Streamlit UI      │
                         │  Select Startup +   │
                         │  Run Due Diligence  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │ Parallel Retrieval Layer  │
                    │     ThreadPoolExecutor    │
                    └───────┬───────┬───────────┘
                            │       │
              ┌─────────────┘       └─────────────┐
              ▼                                   ▼
       ┌─────────────┐                     ┌─────────────┐
       │   SQLite    │                     │    FAISS    │
       │ Structured  │                     │ + BM25      │
       │ Financials  │                     │ News/Press  │
       └──────┬──────┘                     └──────┬──────┘
              │                                   │
              │              ┌─────────────┐      │
              └─────────────►│   Neo4j     │◄─────┘
                             │ Graph Data  │
                             │ Relations   │
                             └──────┬──────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    DSPy Module      │
                         │ ChainOfThought +    │
                         │ Optimized Synthesis  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Structured Verdict  │
                         │ INVEST / PASS       │
                         │ + Evidence          │
                         └─────────────────────┘
```

## Project Goals

The system demonstrates:

1. Multi-source retrieval from three different database types.
2. Hybrid semantic retrieval using dense search and BM25-style lexical matching.
3. Text-to-SQL querying over structured startup information.
4. GraphRAG-style relationship traversal using Neo4j.
5. True parallel retrieval using `ThreadPoolExecutor`.
6. Graceful degradation when one retrieval engine is unavailable.
7. DSPy declarative prompting with `ChainOfThought`.
8. DSPy optimization using a real optimizer such as `BootstrapFewShot`.
9. Rule-based output validation through a judge metric.
10. A transparent UI that exposes the evidence used to generate the final verdict.

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Structured Store | SQLite |
| Semantic Store | FAISS |
| Keyword Retrieval | BM25 / hybrid retrieval |
| Graph Store | Neo4j |
| Embeddings | Sentence Transformers |
| LLM Orchestration | DSPy |
| DSPy Optimizer | BootstrapFewShot |
| Parallelism | Python ThreadPoolExecutor |
| Validation | Rule-based DSPy judge metric |
| Graph Deployment | Docker |
| Language | Python |

## Data Flow

For a selected startup, VentureLens performs the following:

### 1. Structured Retrieval — SQLite
Retrieves structured information such as:

- Funding
- Financial metrics
- Valuation
- Revenue and related startup statistics

### 2. Semantic Retrieval — FAISS + BM25
Searches startup news, press releases, and other textual evidence using hybrid retrieval.

The retrieval layer combines lexical/exact matching with dense semantic similarity so that relevant evidence can be found even when the wording of the question differs from the stored document.

### 3. Graph Retrieval — Neo4j
Traverses relationships such as:

- Founder → Startup
- Investor → Startup
- Startup → Competitor
- Other relevant startup relationships

### 4. Parallel Retrieval
The three engines are executed concurrently instead of sequentially.

This reduces overall latency because the retrieval time approaches the slowest individual engine rather than the sum of all three.

If one engine is unavailable, the system returns a tagged error for that engine while preserving the results from the other engines.

### 5. DSPy Synthesis
The three contexts are passed to a DSPy module.

The module produces a structured due-diligence result using the retrieved evidence rather than relying on a manually written prompt alone.

### 6. Judge Metric
A rule-based metric validates the generated output by checking:

- Output structure
- Required fields
- Valid value ranges
- Hard content constraints

Invalid outputs are rejected by the judge.

## Repository Structure

```text
VentureLens/
│
├── backend/
│   ├── models/
│   ├── retrieval/
│   │   ├── sql_retriever.py
│   │   ├── faiss_retriever.py
│   │   └── graph_retriever.py
│   ├── dspy/
│   └── ...
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── sqlite/
│   ├── faiss/
│   └── ...
│
├── tests/
│
├── scripts/
│   └── generate_sandbox.py
│
├── requirements.txt
├── README.md
└── ...
```

> Folder names may vary slightly depending on the final repository structure.

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the required LLM credentials used by the project.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit API keys or other secrets to GitHub.

### 5. Start Neo4j

Neo4j is required for graph retrieval.

If the project uses Docker Compose:

```bash
docker compose up -d
```

Verify that Neo4j is running before testing graph retrieval.

### 6. Generate the synthetic dataset

Run the project's data-generation script:

```bash
python scripts/generate_sandbox.py
```

The generator should populate:

- SQLite tables
- FAISS index and metadata
- Neo4j nodes and relationships

### 7. Test the three retrieval engines

Each retrieval engine should be independently testable before running the synthesis layer.

```text
SQL Retrieval       → structured startup information
FAISS/BM25          → textual evidence
Neo4j               → relationship information
```

### 8. Run the Streamlit application

```bash
streamlit run frontend/app.py
```

Open the URL displayed by Streamlit in your browser.

## Example Questions

VentureLens can answer questions such as:

- Which startup has the highest revenue?
- Which startup has the highest valuation?
- What is the funding history of a startup?
- What evidence exists about a startup from news or press documents?
- Who are the founders or investors connected to a startup?
- Which competitors are connected to a startup?
- What relationships exist in the startup's network?
- Should the startup be considered for investment based on the available evidence?

The exact questions depend on the fields and relationships included in the generated dataset.

## Transparency UI

The UI is designed to make the retrieval process visible rather than hiding everything behind a chatbot.

For a selected startup, it can display:

- Generated SQL and SQL results
- FAISS/BM25 evidence
- Neo4j graph relationships
- Parallel retrieval timing
- Final DSPy-generated verdict
- Retrieval-engine status/errors

This makes it possible to inspect **what each engine contributed to the final decision**.

## Fault Tolerance

The three retrieval engines are independent.

If Neo4j is unavailable, for example, the system should still return:

```text
SQL      → Available
FAISS    → Available
Neo4j    → [GRAPH ERROR]
DSPy     → Synthesizes using available context
```

The goal is to prevent a single unavailable engine from crashing the entire request.

## DSPy Optimization

The synthesis module is optimized using a real DSPy optimizer such as `BootstrapFewShot`.

The workflow is:

```text
Training Examples
       │
       ▼
Parallel Retrieval
       │
       ▼
DSPy Examples
       │
       ▼
Judge Metric
       │
       ▼
BootstrapFewShot
       │
       ▼
Compiled DSPy Module
       │
       ▼
Saved Optimized State
```

The compiled state can be saved and loaded for later runs instead of recompiling every time.

## Evaluation

The project is designed around the Phase 2 evaluation criteria:

- Do all three engines return genuinely different information?
- Does the system continue working when one engine is unavailable?
- Is there evidence that the DSPy module was actually optimized?
- Does the judge metric reject deliberately invalid outputs?
- Is the final UI transparent about the retrieved evidence?

## Testing

Run the project's tests with:

```bash
pytest
```

Individual retrieval functions should also be tested independently before testing the complete pipeline.

## Scope

This project focuses on **Phase 2 — Multi-Source Retrieval**.

The following are intentionally outside the Phase 2 scope:

- LangGraph agent orchestration
- Tool-calling loops
- Multi-agent supervisors
- Production observability
- Caching
- Fallback cascades

The DSPy synthesis stage is intended to remain a **single compiled module call**, rather than a multi-step agent.

## Deployment

The application can be deployed using Streamlit.

For a deployed version, make sure the deployment environment has:

1. Python dependencies installed.
2. Required API secrets configured.
3. Generated SQLite/FAISS data available.
4. A reachable Neo4j instance if graph retrieval is required.
5. The optimized DSPy state file available.

If Neo4j is running only on a local machine, a cloud deployment will not be able to access it directly. A hosted/reachable Neo4j database is required for full graph functionality in that case.

## Phase 2 Requirements Checklist

- [x] Synthetic data across SQL, FAISS and Neo4j
- [x] Three independent retrieval functions
- [x] Parallel multi-engine retrieval
- [x] Graceful handling of individual engine failures
- [x] Hybrid semantic retrieval
- [x] DSPy signature and synthesis module
- [x] DSPy optimization
- [x] Teacher/student model setup
- [x] Rule-based judge metric
- [x] Transparent UI
- [x] Architecture documentation
- [x] Setup instructions
- [x] Testing support
