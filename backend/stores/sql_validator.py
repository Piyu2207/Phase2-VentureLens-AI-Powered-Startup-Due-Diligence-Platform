import re
import sqlite3

from backend.config import SQLITE_PATH


ALLOWED_TABLE = "startups"


ALLOWED_COLUMNS = {
    "id",
    "name",
    "sector",
    "founded_year",
    "revenue_musd",
    "revenue_growth_pct",
    "total_funding_musd",
    "valuation_musd",
    "burn_rate_musd",
    "runway_months",
    "employees",
    "gross_margin_pct",
    "customer_count",
}


FORBIDDEN_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "replace",
    "attach",
    "detach",
    "pragma",
    "vacuum",
}


SQL_KEYWORDS = {
    "select",
    "from",
    "where",
    "join",
    "inner",
    "left",
    "right",
    "full",
    "outer",
    "on",
    "order",
    "by",
    "group",
    "having",
    "limit",
    "offset",
    "asc",
    "desc",
    "and",
    "or",
    "not",
    "is",
    "in",
    "like",
    "between",
    "as",
    "distinct",
    "count",
    "avg",
    "sum",
    "min",
    "max",
    "case",
    "when",
    "then",
    "else",
    "end",
    "union",
    "all",
    "null",
    "true",
    "false",
}


SQL_FUNCTIONS = {
    "lower",
    "upper",
    "round",
    "cast",
    "coalesce",
    "abs",
    "length",
}


def validate_sql(sql: str) -> tuple[bool, str]:

    if not sql:
        return False, "Empty SQL query."

    normalized = sql.strip().lower()

    # --------------------------------------------------
    # Only SELECT statements
    # --------------------------------------------------

    if not normalized.startswith("select"):
        return False, "Only SELECT queries are allowed."

    # --------------------------------------------------
    # Prevent multiple statements
    # --------------------------------------------------

    cleaned = normalized.rstrip(";")

    if ";" in cleaned:
        return False, "Multiple SQL statements are not allowed."

    # --------------------------------------------------
    # Block dangerous operations
    # --------------------------------------------------

    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(rf"\b{keyword}\b", normalized):
            return False, f"Forbidden SQL keyword: {keyword}"

    # --------------------------------------------------
    # Require startups table
    # --------------------------------------------------

    if not re.search(r"\bstartups\b", normalized):
        return False, "Query must use the startups table."

    # --------------------------------------------------
    # Check FROM / JOIN tables
    # --------------------------------------------------

    tables = re.findall(
        r"\b(?:from|join)\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)",
        normalized,
    )

    for table in tables:

        if table != ALLOWED_TABLE:
            return False, (
                f"Table '{table}' is not allowed."
            )

    # --------------------------------------------------
    # Check column references
    # --------------------------------------------------

    # First remove quoted string literals.
    #
    # Example:
    # 'NovaHealth AI'
    #
    # must NOT be interpreted as a column name.
    sql_for_column_check = re.sub(
        r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"",
        " ",
        normalized,
    )

    # Remove SQL keywords.
    sql_for_column_check = re.sub(
        r"\b(?:"
        + "|".join(SQL_KEYWORDS)
        + r")\b",
        " ",
        sql_for_column_check,
    )

    # Detect identifiers.
    identifiers = re.findall(
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
        sql_for_column_check,
    )

    for identifier in identifiers:

        if identifier == ALLOWED_TABLE:
            continue

        if identifier in SQL_FUNCTIONS:
            continue

        if identifier not in ALLOWED_COLUMNS:
            return False, (
                f"Unknown column or identifier: "
                f"{identifier}"
            )

    # --------------------------------------------------
    # Validate against the actual SQLite schema
    # --------------------------------------------------

    try:
        conn = sqlite3.connect(SQLITE_PATH)

        try:
            conn.execute(f"EXPLAIN QUERY PLAN {cleaned}")
        finally:
            conn.close()

    except sqlite3.Error as exc:
        return False, f"SQLite validation failed: {exc}"

    return True, ""
