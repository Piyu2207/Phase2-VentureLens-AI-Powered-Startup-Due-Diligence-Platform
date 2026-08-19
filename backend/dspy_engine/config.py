import dspy

from backend.config import (
    GEMINI_API_KEY,
    TEACHER_MODEL,
    STUDENT_MODEL,
)

def configure_student():
    """
    Create the student LM.

    We intentionally do NOT call dspy.configure() here.
    Streamlit can execute this function from different
    ScriptRunner threads.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to .env."
        )

    return dspy.LM(
        STUDENT_MODEL,
        api_key=GEMINI_API_KEY,
        max_tokens=1800,
        cache=True,
    )


def make_teacher():
    """
    Create the teacher LM used by DSPy optimization.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to .env."
        )

    return dspy.LM(
        TEACHER_MODEL,
        api_key=GEMINI_API_KEY,
        max_tokens=1800,
        cache=True,
    )