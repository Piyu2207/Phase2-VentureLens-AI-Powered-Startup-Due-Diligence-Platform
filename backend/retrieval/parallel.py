from concurrent.futures import ThreadPoolExecutor
import time
from backend.retrieval.sql_retriever import query_sql
from backend.retrieval.faiss_retriever import query_faiss
from backend.retrieval.graph_retriever import query_graph

def parallel_retrieve(entity, question=None):
    start=time.perf_counter()
    with ThreadPoolExecutor(max_workers=3) as ex:
        fs={"sql": ex.submit(query_sql, question),
            "faiss":ex.submit(query_faiss,entity,question),
            "graph":ex.submit(query_graph,entity)}
        results={k:f.result() for k,f in fs.items()}
    return results,(time.perf_counter()-start)*1000
