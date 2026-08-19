import dspy

from backend.config import DSPY_COMPILED_PATH
from backend.dspy_engine.config import configure_student
from backend.dspy_engine.module import DueDiligenceModule


def _load_module():
    module = DueDiligenceModule()

    if DSPY_COMPILED_PATH.exists():
        try:
            module.load(str(DSPY_COMPILED_PATH))
            print(
                f"[DSPy] Loaded compiled program: "
                f"{DSPY_COMPILED_PATH}"
            )
        except Exception as exc:
            print(
                f"[DSPy] Warning: failed to load compiled program: "
                f"{exc}"
            )
    else:
        print(
            f"[DSPy] Compiled artifact not found: "
            f"{DSPY_COMPILED_PATH}"
        )

    return module


module = _load_module()


def synthesize(sql_context, faiss_context, graph_context):

    lm = configure_student()

    with dspy.context(lm=lm):
        prediction = module(
            sql_context=sql_context,
            faiss_context=faiss_context,
            graph_context=graph_context,
        )

    return prediction, "dspy"