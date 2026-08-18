import time

from backend.models.schemas import RetrievalResult
from backend.stores.sqlite_store import execute_query
from backend.stores.sql_generator import generate_sql
from backend.stores.sql_validator import validate_sql


def query_sql(question):
    """
    Text-to-SQL retrieval engine.

    Natural-language question
        -> Gemini
        -> SQL validation
        -> SQLite
        -> structured RetrievalResult
    """

    start = time.perf_counter()

    try:

        # --------------------------------------------------
        # 1. Generate SQL
        # --------------------------------------------------

        sql = generate_sql(question)

        # --------------------------------------------------
        # 2. Validate generated SQL
        # --------------------------------------------------

        valid, error = validate_sql(sql)

        if not valid:

            return RetrievalResult(
                "SQL",
                f"[SQL ERROR] Invalid generated SQL: {error}",
                (time.perf_counter() - start) * 1000,
                False,
                error,
                raw={
                    "question": question,
                    "sql": sql,
                },
            )

        # --------------------------------------------------
        # 3. Execute SQL
        # --------------------------------------------------

        result = execute_query(sql)

        rows = result["rows"]

        if not rows:

            context = (
                "[SQL CONTEXT]\n"
                "No matching startup records were found."
            )

        else:

            context_lines = [
                "[SQL CONTEXT]",
                f"Question: {question}",
                f"Generated SQL: {sql}",
                "",
                "Results:",
            ]

            for index, row in enumerate(rows, start=1):

                context_lines.append(
                    f"Row {index}: {row}"
                )

            context = "\n".join(context_lines)

        return RetrievalResult(
            "SQL",
            context,
            (time.perf_counter() - start) * 1000,
            True,
            raw={
                "question": question,
                "sql": sql,
                "columns": result["columns"],
                "rows": rows,
            },
        )

    except Exception as e:

        return RetrievalResult(
            "SQL",
            f"[SQL ERROR] {type(e).__name__}: {e}",
            (time.perf_counter() - start) * 1000,
            False,
            str(e),
            raw={
                "question": question,
            },
        )