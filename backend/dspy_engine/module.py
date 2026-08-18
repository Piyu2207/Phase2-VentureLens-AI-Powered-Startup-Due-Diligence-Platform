import dspy
from backend.dspy_engine.signatures import StartupDueDiligence

class DueDiligenceModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.synthesize=dspy.ChainOfThought(StartupDueDiligence)
    def forward(self, sql_context, faiss_context, graph_context):
        return self.synthesize(sql_context=sql_context,faiss_context=faiss_context,graph_context=graph_context)
