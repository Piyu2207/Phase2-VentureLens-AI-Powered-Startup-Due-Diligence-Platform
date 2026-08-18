import dspy

from backend.config import GEMINI_API_KEY, STUDENT_MODEL


DATABASE_SCHEMA = """
SQLite database: startups

Table: startups

Columns:
- id TEXT
- name TEXT
- sector TEXT
- founded_year INTEGER
- revenue_musd REAL
- revenue_growth_pct REAL
- total_funding_musd REAL
- valuation_musd REAL
- burn_rate_musd REAL
- runway_months INTEGER
- employees INTEGER
- gross_margin_pct REAL
- customer_count INTEGER

Important mappings:
- revenue -> revenue_musd
- revenue growth -> revenue_growth_pct
- funding -> total_funding_musd
- valuation -> valuation_musd
- burn rate -> burn_rate_musd
- runway -> runway_months
"""


class TextToSQLSignature(dspy.Signature):
    """
    Convert a natural-language startup due-diligence question
    into exactly one safe SQLite SELECT query.

    The generated SQL must answer the user's question directly.
    Never invent a startup name or filter by a startup name unless
    the user explicitly asks about that specific startup.
    """

    question = dspy.InputField(
        desc=(
            "Natural-language question about startup data. "
            "Interpret the user's intent carefully. "
            "Questions asking for highest, lowest, maximum, minimum, "
            "most, or least require ranking/aggregation."
        )
    )

    db_schema = dspy.InputField(
        desc=(
            "SQLite database schema. "
            "Use only the startups table and only the columns "
            "defined in this schema."
        )
    )

    sql = dspy.OutputField(
        desc=(
            "Return ONLY one valid SQLite SELECT statement. "
            "Do not return explanations, reasoning, markdown, or code fences. "

            "Rules: "
            "1. Use ONLY the startups table. "
            "2. Use ONLY columns defined in the schema. "
            "3. Map revenue to revenue_musd. "
            "4. Map revenue growth to revenue_growth_pct. "
            "5. Map funding to total_funding_musd. "
            "6. Map valuation to valuation_musd. "
            "7. Map burn rate to burn_rate_musd. "
            "8. Map runway to runway_months. "
            "9. For 'highest', 'maximum', 'most', or similar questions, "
            "ORDER BY the relevant numeric column DESC and use LIMIT 1 "
            "when the question asks for one startup. "
            "10. For 'lowest', 'minimum', 'least', or similar questions, "
            "ORDER BY the relevant numeric column ASC and use LIMIT 1 "
            "when the question asks for one startup. "
            "11. Do not invent or guess a startup name. "
            "12. If the question asks which startup has the highest "
            "valuation, return the startup name and optionally the "
            "valuation using valuation_musd. "
            "13. If the question asks which startup has the highest "
            "revenue, use revenue_musd. "
            "14. Use IS NOT NULL when ranking a numeric column so "
            "NULL values are excluded. "
            "15. The result must directly answer the user's question."
        )
    )


class TextToSQLModule(dspy.Module):

    def __init__(self):
        super().__init__()

        self.generate_sql = dspy.ChainOfThought(
            TextToSQLSignature
        )

    def forward(self, question, db_schema):

        return self.generate_sql(
            question=question,
            db_schema=db_schema,
        )


def generate_sql(question: str) -> str:

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing from .env"
        )

    lm = dspy.LM(
        STUDENT_MODEL,
        api_key=GEMINI_API_KEY,
        max_tokens=500,
        cache=True,
    )

    module = TextToSQLModule()

    with dspy.context(lm=lm):

        prediction = module(
            question=question,
            db_schema=DATABASE_SCHEMA,
        )

    sql = prediction.sql.strip()

    sql = (
        sql
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    return sql