import time

from backend.models.schemas import RetrievalResult
from backend.retrieval.sql_retriever import query_sql
from backend.retrieval.faiss_retriever import query_faiss
from backend.retrieval.graph_retriever import query_graph
from concurrent.futures import ThreadPoolExecutor

def _safe_result(name, future):

    """Convert an unexpected worker exception into a failed RetrievalResult."""
    
    try:
        return future.result()
    except Exception as exc:
        return RetrievalResult(
            engine=name.upper(),
            context=f"[{name.upper()} ERROR] {type(exc).__name__}: {exc}",
            latency_ms=0.0,
            ok=False,
            error=str(exc),
        )


def parallel_retrieve(entity, question=None):

    """Run SQL, hybrid FAISS/BM25, and Neo4j retrieval in parallel.

    A failure in one worker is isolated and represented as RetrievalResult(ok=False);
    the other engines can still be consumed by the synthesis layer.
    """

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=3) as ex:
        fs = {
            "sql": ex.submit(query_sql, question),
            "faiss": ex.submit(query_faiss, entity, question),
            "graph": ex.submit(query_graph, entity),
        }
        results = {name: _safe_result(name, future) for name, future in fs.items()}

    return results, (time.perf_counter() - start) * 1000
