"""Run the Phase 2 evaluator-facing checks.

This script does not require the LLM for the judge/degradation checks. The
engine-diversity check is integration-dependent and is reported honestly.
"""

import json
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.config import DATASET_PATH, DSPY_COMPILED_PATH
from backend.dspy_engine.metrics import bad_output_example, validate_dict
from backend.retrieval.parallel import parallel_retrieve


def main():
    data = json.loads(Path(DATASET_PATH).read_text(encoding="utf-8"))
    entity = data[0]["name"]

    retrieval, latency = parallel_retrieve(
        entity,
        f"What are the financial, market, and relationship risks for {entity}?",
    )

    judge_failed_bad_output = not validate_dict(bad_output_example())

    result = {
        "entity": entity,
        "parallel_latency_ms": round(latency, 2),
        "engines": {
            name: {
                "ok": value.ok,
                "context_prefix": value.context[:180],
                "error": value.error,
            }
            for name, value in retrieval.items()
        },
        "engine_contexts_are_nonempty": all(
            bool(v.context.strip()) for v in retrieval.values()
        ),
        "judge_rejects_bad_output": judge_failed_bad_output,
        "compiled_state_exists": DSPY_COMPILED_PATH.exists(),
        "compiled_state_path": str(DSPY_COMPILED_PATH),
    }

    out = ROOT / "artifacts" / "evaluation" / "rubric_evidence.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
