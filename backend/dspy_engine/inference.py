import dspy

from backend.dspy_engine.config import configure_student
from backend.dspy_engine.module import DueDiligenceModule


module = DueDiligenceModule()


def synthesize(sql_context, faiss_context, graph_context):

    lm = configure_student()

    with dspy.context(lm=lm):
        prediction = module(
            sql_context=sql_context,
            faiss_context=faiss_context,
            graph_context=graph_context,
        )

    return prediction, "dspy"