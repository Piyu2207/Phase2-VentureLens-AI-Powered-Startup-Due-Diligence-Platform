import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.config import DATASET_PATH, DSPY_COMPILED_PATH
from backend.dspy_engine.inference import synthesize
from backend.dspy_engine.metrics import bad_output_example, validate_dict
from backend.retrieval.parallel import parallel_retrieve

def main():

    # --------------------------------------------------
    # Output path
    # --------------------------------------------------

    out = ROOT / "artifacts" / "evaluation" / "baseline_vs_compiled.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Load dataset
    # --------------------------------------------------

    data = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    entity = data[-1]["name"]

    question = (
        f"Should an investor invest in {entity}?"
    )

    result = {
        "held_out_entity": entity,
        "question": question,
        "compiled_state_exists": DSPY_COMPILED_PATH.exists(),
        "compiled_state_path": str(DSPY_COMPILED_PATH),
    }

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    try:

        retrieval_start = time.perf_counter()

        retrieval, parallel_latency = parallel_retrieve(
            entity,
            question,
        )

        retrieval_elapsed = (
            time.perf_counter() - retrieval_start
        ) * 1000

        result["parallel_latency_ms"] = round(
            parallel_latency,
            2,
        )

        result["retrieval_elapsed_ms"] = round(
            retrieval_elapsed,
            2,
        )

        result["retrieval_ok"] = {
            name: value.ok
            for name, value in retrieval.items()
        }

        result["retrieval_context_nonempty"] = {
            name: bool(value.context.strip())
            for name, value in retrieval.items()
        }

    except Exception as exc:

        result["retrieval_error"] = (
            f"{type(exc).__name__}: {exc}"
        )

        retrieval = None

    # --------------------------------------------------
    # DSPy synthesis
    # --------------------------------------------------

    if retrieval is not None:

        try:

            synthesis_start = time.perf_counter()

            pred, mode = synthesize(
                retrieval["sql"].context,
                retrieval["faiss"].context,
                retrieval["graph"].context,
            )

            synthesis_latency = (
                time.perf_counter() - synthesis_start
            ) * 1000

            result["mode"] = mode

            result["synthesis_latency_ms"] = round(
                synthesis_latency,
                2,
            )

            result["prediction"] = {
                key: getattr(pred, key, None)
                for key in [
                    "verdict",
                    "confidence",
                    "financial_risk",
                    "market_risk",
                    "network_strength",
                    "reasoning",
                ]
            }

            result["prediction_valid"] = validate_dict(
                result["prediction"]
            )

        except Exception as exc:

            result["synthesis_error"] = (
                f"{type(exc).__name__}: {exc}"
            )

    # --------------------------------------------------
    # Evaluator robustness
    # --------------------------------------------------

    result["judge_bad_output_rejected"] = (
        not validate_dict(
            bad_output_example()
        )
    )

    # --------------------------------------------------
    # Save evidence
    # --------------------------------------------------

    out.write_text(
        json.dumps(
            result,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )

    print()
    print(
        f"Evaluation evidence written to: {out}"
    )


if __name__ == "__main__":
    main()