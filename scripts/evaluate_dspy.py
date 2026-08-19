"""Measure baseline vs compiled DSPy performance on the same held-out examples.

This script intentionally uses the existing compile_dspy.py example builder and
judge metric. It does not rename or replace any existing script.
"""

import json
import sys
import dspy

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.config import DSPY_COMPILED_PATH
from backend.dspy_engine.config import configure_student
from backend.dspy_engine.metrics import judge_metric
from backend.dspy_engine.module import DueDiligenceModule
from scripts.compile_dspy import examples


def _run(module, dataset, lm):
    scores = []

    with dspy.context(lm=lm):
        for ex in dataset:
            try:
                pred = module(
                    sql_context=ex.sql_context,
                    faiss_context=ex.faiss_context,
                    graph_context=ex.graph_context,
                )
                scores.append(1 if judge_metric(ex, pred) else 0)
            except Exception:
                scores.append(0)
    return sum(scores) / len(scores) if scores else 0.0


def main():
    
    if not DSPY_COMPILED_PATH.exists():
        raise SystemExit(
            f"Compiled DSPy state not found: {DSPY_COMPILED_PATH}\n"
            "Run `python scripts/compile_dspy.py` first."
        )

    lm = configure_student()
    dataset = examples()

    baseline = _run(DueDiligenceModule(), dataset, lm)

    compiled = DueDiligenceModule()
    compiled.load(str(DSPY_COMPILED_PATH))
    optimized = _run(compiled, dataset, lm)

    result = {
        "examples": len(dataset),
        "baseline_metric": baseline,
        "compiled_metric": optimized,
        "improvement": optimized - baseline,
        "compiled_state": str(DSPY_COMPILED_PATH),
        "compiled_state_exists": DSPY_COMPILED_PATH.exists(),
    }

    out = ROOT / "artifacts" / "evaluation" / "dspy_before_after.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
