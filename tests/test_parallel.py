from backend.models.schemas import RetrievalResult
import backend.retrieval.parallel as p

def test_parallel_tolerates_failure(monkeypatch):
    monkeypatch.setattr(p,"query_sql",lambda e:RetrievalResult("SQL","ok",1,True))
    monkeypatch.setattr(p,"query_faiss",lambda e,q=None:RetrievalResult("FAISS","ok",2,True))
    monkeypatch.setattr(p,"query_graph",lambda e:RetrievalResult("GRAPH","[GRAPH ERROR] down",3,False,"down"))
    r,_=p.parallel_retrieve("X","q")
    assert r["sql"].ok and r["faiss"].ok and not r["graph"].ok
