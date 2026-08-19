VALID_VERDICTS = {"INVEST", "PASS"}
VALID_RISK = {"LOW", "MEDIUM", "HIGH"}

BANNED = {
    "maybe",
    "as an ai",
    "i cannot determine",
}


def _get(prediction, key, default=None):
    return getattr(prediction, key, default)


def _valid_evidence_context(context):
    if not context:
        return False

    text = str(context).strip()

    if not text:
        return False

    error_prefixes = (
        "[SQL ERROR]",
        "[FAISS ERROR]",
        "[GRAPH ERROR]",
    )

    return not text.startswith(error_prefixes)


def judge_metric(example, prediction, trace=None, **kwargs):

    try:
        confidence = int(
            _get(prediction, "confidence", -1)
        )
    except (TypeError, ValueError):
        return False

    # --------------------------------------------------
    # Verdict
    # --------------------------------------------------

    verdict = str(
        _get(prediction, "verdict", "")
    ).strip().upper()

    if verdict not in VALID_VERDICTS:
        return False

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    if not 0 <= confidence <= 100:
        return False

    # --------------------------------------------------
    # Risk fields
    # --------------------------------------------------

    for field in (
        "financial_risk",
        "market_risk",
        "network_strength",
    ):

        value = str(
            _get(prediction, field, "")
        ).strip().upper()

        if value not in VALID_RISK:
            return False

    # --------------------------------------------------
    # Reasoning
    # --------------------------------------------------

    reasoning = str(
        _get(prediction, "reasoning", "")
    ).strip()

    if not reasoning:
        return False

    reasoning_lower = reasoning.lower()

    if any(
        banned in reasoning_lower
        for banned in BANNED
    ):
        return False

    # --------------------------------------------------
    # Evidence availability
    # --------------------------------------------------

    contexts = []

    if example is not None:

        for field in (
            "sql_context",
            "faiss_context",
            "graph_context",
        ):

            context = getattr(
                example,
                field,
                None,
            )

            if context:
                contexts.append(str(context))

    # If evaluation provides contexts, require at least
    # one usable evidence source.
    
    if contexts and not any(
        _valid_evidence_context(context)
        for context in contexts
    ):
        return False

    return True


def bad_output_example():

    return {
        "verdict": "MAYBE",
        "confidence": 137,
        "financial_risk": "UNKNOWN",
        "market_risk": "LOW",
        "network_strength": "HIGH",
        "reasoning": "",
    }


def validate_dict(d):

    class O:
        pass

    o = O()

    for key, value in d.items():
        setattr(o, key, value)

    return judge_metric(None, o)