# VentureLens Architecture

SQL stores structured financial facts. FAISS stores local embeddings for press/customer/founder text. BM25 supplies sparse lexical retrieval and RRF fuses sparse and dense rankings. Neo4j stores typed founder/investor/competitor/partner relationships.

`parallel_retrieve()` runs all three query functions using `ThreadPoolExecutor(max_workers=3)`. Each engine returns a `RetrievalResult`; failures become tagged context strings.

A single DSPy `ChainOfThought` module consumes the three contexts. `BootstrapFewShot` compiles the student using a stronger teacher LM and a rule-based metric. The compiled state is persisted and loaded by the Streamlit application.

Phase 2 intentionally avoids LangGraph, agents, multi-agent supervisors and tool-calling loops.
