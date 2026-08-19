import backend.retrieval.parallel as p

from backend.models.schemas import RetrievalResult

def test_parallel_tolerates_failure(monkeypatch):
    monkeypatch.setattr(
        p, "query_sql",
        lambda q: RetrievalResult("SQL", "ok", 1, True),
    )

    monkeypatch.setattr(
        p, "query_faiss",
        lambda e, q=None: RetrievalResult("FAISS", "ok", 2, True),
    )

    monkeypatch.setattr(
        p, "query_graph",
        lambda e: RetrievalResult("GRAPH", "[GRAPH ERROR] down", 3, False, "down"),
    )

    r, _ = p.parallel_retrieve("X", "q")
    assert r["sql"].ok and r["faiss"].ok and not r["graph"].ok


def test_parallel_catches_unexpected_worker_exception(monkeypatch):

    monkeypatch.setattr(
        p, "query_sql",
        lambda q: (_ for _ in ()).throw(RuntimeError("sqlite unexpectedly down")),
    )

    monkeypatch.setattr(
        p, "query_faiss",
        lambda e, q=None: RetrievalResult("FAISS", "ok", 2, True),
    )

    monkeypatch.setattr(
        p, "query_graph",
        lambda e: RetrievalResult("GRAPH", "graph ok", 3, True),
    )

    r, _ = p.parallel_retrieve("X", "q")

    assert not r["sql"].ok
    assert "sqlite unexpectedly down" in r["sql"].error
    assert r["faiss"].ok
    assert r["graph"].ok
