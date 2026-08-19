import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from backend.retrieval.sql_retriever import query_sql
from backend.retrieval.faiss_retriever import query_faiss
from backend.retrieval.graph_retriever import query_graph

for fn in [query_sql,query_faiss,query_graph]:
    r=fn("NovaHealth AI");print("\n"+"="*80);print(r.engine,r.ok,f"{r.latency_ms:.2f}ms");print(r.context)
