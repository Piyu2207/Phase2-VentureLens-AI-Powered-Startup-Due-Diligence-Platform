import sys
import dspy

from pathlib import Path

# ============================================================
# PROJECT ROOT
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.config import DSPY_COMPILED_PATH
from backend.dspy_engine.config import configure_student, make_teacher
from backend.dspy_engine.metrics import judge_metric
from backend.dspy_engine.module import DueDiligenceModule

# ============================================================
# TRAINING EXAMPLES
# ============================================================

def examples():

    return [
        dspy.Example(
            sql_context=(
                "[SQL CONTEXT] "
                "Revenue: 100 crore; Growth: 35%"
            ),

            faiss_context=(
                "[FAISS HYBRID CONTEXT] "
                "Market expansion and strong customer adoption reported."
            ),

            graph_context=(
                "[GRAPH CONTEXT] "
                "Founder: Alice; "
                "Investor: ABC Ventures; "
                "Competitor: XYZ Corp"
            ),

            verdict="INVEST",
            confidence=85,
            financial_risk="LOW",
            market_risk="LOW",
            network_strength="HIGH",

            reasoning=(
                "Strong revenue growth, positive market evidence, "
                "and strong investor and founder relationships "
                "support investment."
            ),
        ).with_inputs(
            "sql_context",
            "faiss_context",
            "graph_context",
        ),

        dspy.Example(
            sql_context=(
                "[SQL CONTEXT] "
                "Revenue: 20 crore; Growth: -10%"
            ),

            faiss_context=(
                "[FAISS HYBRID CONTEXT] "
                "Customer growth is slowing and competition is increasing."
            ),

            graph_context=(
                "[GRAPH CONTEXT] "
                "Limited investor relationships; "
                "multiple competitors identified."
            ),

            verdict="PASS",
            confidence=65,
            financial_risk="HIGH",
            market_risk="HIGH",
            network_strength="MEDIUM",

            reasoning=(
                "Declining revenue growth, competitive pressure, "
                "and higher financial risk support a cautious decision."
            ),
        ).with_inputs(
            "sql_context",
            "faiss_context",
            "graph_context",
        ),
    ]


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("VENTURELENS DSPy COMPILATION")
    print("=" * 60)

    print("DSPy version:", dspy.__version__)

    # --------------------------------------------------------
    # Student module
    # --------------------------------------------------------

    student = DueDiligenceModule()

    # --------------------------------------------------------
    # Teacher LM
    # --------------------------------------------------------

    teacher = make_teacher()

    print("Teacher model configured.")

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    optimizer = dspy.BootstrapFewShot(
        metric=judge_metric,
        max_bootstrapped_demos=2,
        max_labeled_demos=2,
    )

    print("BootstrapFewShot optimizer created.")

    # --------------------------------------------------------
    # Compile
    # --------------------------------------------------------
    #
    # IMPORTANT:
    #
    # DSPy 3.3.0 does NOT accept:
    #
    # teacher_settings={"lm": teacher}
    #
    # Therefore we use dspy.context().
    #
    # --------------------------------------------------------

    print("Starting compilation...")

    with dspy.context(lm=teacher):

        compiled = optimizer.compile(
            student=student,
            trainset=examples(),
        )

# --------------------------------------------------------
# Save compiled state
# --------------------------------------------------------

    DSPY_COMPILED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    compiled.save(
        str(DSPY_COMPILED_PATH)
    )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("DSPy COMPILATION SUCCESSFUL")
    print("=" * 60)

    print(
        "Compiled artifact:",
        DSPY_COMPILED_PATH,
    )

    print(
        "Exists:",
        DSPY_COMPILED_PATH.exists(),
    )

    if DSPY_COMPILED_PATH.exists():

        print(
            "Size:",
            DSPY_COMPILED_PATH.stat().st_size,
            "bytes",
        )

    print("=" * 60)


if __name__ == "__main__":
    main()