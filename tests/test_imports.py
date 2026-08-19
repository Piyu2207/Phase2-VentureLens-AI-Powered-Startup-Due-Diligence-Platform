def test_imports():

    from backend.retrieval.parallel import parallel_retrieve

    from backend.dspy_engine.module import DueDiligenceModule

    assert callable(parallel_retrieve) and DueDiligenceModule is not None
