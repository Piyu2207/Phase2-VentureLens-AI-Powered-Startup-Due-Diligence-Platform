import sqlite3

from backend.config import SQLITE_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS startups (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    sector TEXT NOT NULL,
    founded_year INTEGER NOT NULL,
    revenue_musd REAL NOT NULL,
    revenue_growth_pct REAL NOT NULL,
    total_funding_musd REAL NOT NULL,
    valuation_musd REAL NOT NULL,
    burn_rate_musd REAL NOT NULL,
    runway_months INTEGER NOT NULL,
    employees INTEGER NOT NULL,
    gross_margin_pct REAL NOT NULL,
    customer_count INTEGER NOT NULL
);
"""


def connect():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize():
    with connect() as conn:
        conn.executescript(SCHEMA)


def insert_startups(rows):
    initialize()

    with connect() as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO startups
            (
                id,
                name,
                sector,
                founded_year,
                revenue_musd,
                revenue_growth_pct,
                total_funding_musd,
                valuation_musd,
                burn_rate_musd,
                runway_months,
                employees,
                gross_margin_pct,
                customer_count
            )
            VALUES (
                :id,
                :name,
                :sector,
                :founded_year,
                :revenue_musd,
                :revenue_growth_pct,
                :total_funding_musd,
                :valuation_musd,
                :burn_rate_musd,
                :runway_months,
                :employees,
                :gross_margin_pct,
                :customer_count
            )
            """,
            rows,
        )


def get_startup(name):
    initialize()

    with connect() as conn:
        return conn.execute(
            """
            SELECT *
            FROM startups
            WHERE lower(name) = lower(?)
            """,
            (name,),
        ).fetchone()


def execute_query(sql, params=()):
    """
    Execute a validated read-only SQL query.
    """

    initialize()

    with connect() as conn:
        cursor = conn.execute(sql, params)

        columns = [
            description[0]
            for description in cursor.description
        ]

        rows = [
            dict(row)
            for row in cursor.fetchall()
        ]

    return {
        "columns": columns,
        "rows": rows,
    }


def count_rows():
    initialize()

    with connect() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM startups"
        ).fetchone()[0]