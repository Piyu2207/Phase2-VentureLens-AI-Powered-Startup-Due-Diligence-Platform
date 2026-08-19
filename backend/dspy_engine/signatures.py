import dspy

class StartupDueDiligence(dspy.Signature):
    """
    Perform startup due diligence using ONLY the evidence supplied in
    sql_context, faiss_context, and graph_context.

    Evidence-grounding rules:
    - Do not use outside knowledge or unstated assumptions.
    - Do not invent financial, market, customer, founder, investor,
      competitor, or relationship facts.
    - Every factual statement in the reasoning must be supported by
      one or more supplied evidence contexts.
    - Retrieval errors or missing evidence must be treated as UNKNOWN,
      not as negative evidence.
    - If evidence sources conflict, acknowledge the conflict and make
      the most conservative decision supported by the evidence.
    - Confidence must reflect the strength and completeness of the
      supplied evidence, not certainty from the language model.
    - Use all three evidence sources when they contain relevant evidence.
    """

    sql_context: str = dspy.InputField(
        desc=(
            "Financial and quantitative startup evidence retrieved from "
            "SQLite. Use this source for revenue, growth, funding, "
            "valuation, burn rate, runway, employees, margins, and "
            "customer counts. Do not invent missing values."
        )
    )

    faiss_context: str = dspy.InputField(
        desc=(
            "Textual evidence retrieved using BM25 + dense FAISS + RRF. "
            "Use this source for market, customer, product, competitive, "
            "and business-development evidence. Only use facts explicitly "
            "present in the supplied context."
        )
    )

    graph_context: str = dspy.InputField(
        desc=(
            "Relationship evidence retrieved from Neo4j. Use this source "
            "for founders, investors, competitors, partners, and other "
            "relationships. Do not infer relationships that are not "
            "explicitly present."
        )
    )

    verdict: str = dspy.OutputField(
        desc=(
            "Exactly one of: INVEST or PASS. "
            "Choose the decision supported by the supplied evidence only. "
            "Do not use outside knowledge."
        )
    )

    confidence: int = dspy.OutputField(
        desc=(
            "Integer from 0 to 100 representing confidence in the verdict "
            "based only on the quality, consistency, and completeness of "
            "the supplied evidence. Do not report false certainty."
        )
    )

    financial_risk: str = dspy.OutputField(
        desc=(
            "Exactly one of: LOW, MEDIUM, HIGH. "
            "Assess only from financial evidence supplied in sql_context. "
            "If important financial evidence is missing, use the most "
            "conservative supported assessment rather than inventing facts."
        )
    )

    market_risk: str = dspy.OutputField(
        desc=(
            "Exactly one of: LOW, MEDIUM, HIGH. "
            "Assess only from market, customer, product, and competitive "
            "evidence supplied in faiss_context."
        )
    )

    network_strength: str = dspy.OutputField(
        desc=(
            "Exactly one of: LOW, MEDIUM, HIGH. "
            "Assess only from founder, investor, partner, and competitor "
            "relationships explicitly supplied in graph_context."
        )
    )

    reasoning: str = dspy.OutputField(
        desc=(
            "Concise evidence-grounded reasoning. "
            "Reference the strongest relevant evidence from SQL, FAISS, "
            "and/or Graph. Do not introduce facts that are absent from "
            "the supplied contexts. If a source contains an error or "
            "insufficient evidence, explicitly acknowledge that limitation."
        )
    )