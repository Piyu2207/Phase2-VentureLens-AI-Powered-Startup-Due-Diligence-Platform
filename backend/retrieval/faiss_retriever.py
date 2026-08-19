import time

from backend.config import TOP_K
from backend.models.schemas import RetrievalResult
from backend.stores.faiss_store import FAISSStore

def query_faiss(entity, query=None):
    start=time.perf_counter()
    try:
        q= query or f"{entity} financial health customer sentiment market product risks"

        hits= FAISSStore().hybrid_search(q,entity,TOP_K)
        lines= ["[FAISS HYBRID CONTEXT]",f"Entity: {entity}","Retrieval: BM25 + dense FAISS + RRF"]

        for i,h in enumerate(hits,1):
            lines += [f"\nEvidence {i} | source={h['source']} | date={h['date']} | rrf={h['rrf_score']:.5f}",h["text"]]

        return RetrievalResult("FAISS","\n".join(lines),(time.perf_counter()-start)*1000,True,raw=hits)
    
    except Exception as e:
        return RetrievalResult("FAISS",f"[FAISS ERROR] {type(e).__name__}: {e}",(time.perf_counter()-start)*1000,False,str(e))
