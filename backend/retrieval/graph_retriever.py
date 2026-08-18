import time
from backend.models.schemas import RetrievalResult
from backend.stores.neo4j_store import Neo4jStore

def query_graph(entity):
    start=time.perf_counter(); store=Neo4jStore()
    try:
        rows=store.query_graph(entity)
        if not rows:
            return RetrievalResult("GRAPH","[GRAPH ERROR] Entity not found or no relationships.",0,False)
        lines=["[GRAPH CONTEXT]",f"Entity: {entity}","Relationship evidence from Neo4j:"]
        for r in rows:
            lines.append(f"- {r['startup']} --[{r['relationship']}]--> {r['connected_entity']} ({r['other_labels']})")
        return RetrievalResult("GRAPH","\n".join(lines),(time.perf_counter()-start)*1000,True,raw=rows)
    except Exception as e:
        return RetrievalResult("GRAPH",f"[GRAPH ERROR] {type(e).__name__}: {e}",(time.perf_counter()-start)*1000,False,str(e))
    finally:
        store.close()
