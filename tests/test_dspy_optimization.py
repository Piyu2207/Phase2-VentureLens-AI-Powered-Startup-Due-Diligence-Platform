from pathlib import Path

from backend.config import DSPY_COMPILED_PATH

def test_compiled_dspy_artifact_is_present():

    """Evidence test: run scripts/compile_dspy.py before this test in a real evaluation."""

    if not DSPY_COMPILED_PATH.exists():
        # Do not fabricate a pass. The evaluator should see exactly what is missing.
        raise AssertionError(
            f"DSPy compiled state not found at {DSPY_COMPILED_PATH}. "
            "Run: python scripts/compile_dspy.py"
        )

    assert Path(DSPY_COMPILED_PATH).stat().st_size > 0
