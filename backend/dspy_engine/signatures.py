import dspy

class StartupDueDiligence(dspy.Signature):
    """Synthesize an investment verdict ONLY from the supplied SQL, text and graph evidence.
    Do not invent facts. Return exactly the allowed categorical values."""
    sql_context: str = dspy.InputField(desc="Structured financial/funding facts from SQLite.")
    faiss_context: str = dspy.InputField(desc="News/press/customer evidence from BM25+dense+RRF.")
    graph_context: str = dspy.InputField(desc="Founder/investor/competitor/partner relationships from Neo4j.")
    verdict: str = dspy.OutputField(desc="Exactly INVEST or PASS.")
    confidence: int = dspy.OutputField(desc="Integer 0 to 100.")
    financial_risk: str = dspy.OutputField(desc="Exactly LOW, MEDIUM or HIGH.")
    market_risk: str = dspy.OutputField(desc="Exactly LOW, MEDIUM or HIGH.")
    network_strength: str = dspy.OutputField(desc="Exactly LOW, MEDIUM or HIGH.")
    reasoning: str = dspy.OutputField(desc="Concise evidence-based reasoning.")
