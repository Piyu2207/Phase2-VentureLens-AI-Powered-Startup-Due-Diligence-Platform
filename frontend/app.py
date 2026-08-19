import sys
import json

import html
import textwrap

import streamlit as st

from pathlib import Path

# ============================================================
# HTML HELPER
# ============================================================

def render_html(content: str):
    st.html(textwrap.dedent(content))


# ============================================================
# PATH
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ============================================================
# BACKEND
# ============================================================

from backend.config import DATASET_PATH, MOCK_LLM
from backend.retrieval.parallel import parallel_retrieve
from backend.dspy_engine.inference import synthesize


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VentureLens",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

render_html(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
        width: 100%;
        box-sizing: border-box;
    }

    /* ================= HERO ================= */

    .hero {
        width: 100%;
        box-sizing: border-box;
        padding: 2.5rem 1.8rem 1.5rem 1.8rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            rgba(49,51,63,.98),
            rgba(25,27,36,.98)
        );
        border: 1px solid rgba(255,255,255,.08);
        margin-bottom: 1.4rem;
        overflow: visible;
    }

    .hero-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 2rem;
        width: 100%;
        flex-wrap: wrap;
    }

    .hero-row > div:first-child {
        flex: 1 1 auto;
        min-width: 0;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.2;
        white-space: normal;
    }

    .hero-subtitle {
        color: #aeb4c0;
        margin-top: .35rem;
        line-height: 1.4;
        white-space: normal;
    }

    .status-pill {
        flex: 0 0 auto;
        padding: .4rem .85rem;
        border-radius: 999px;
        font-size: .75rem;
        font-weight: 700;
        color: #65e6a0;
        background: rgba(46,204,113,.12);
        border: 1px solid rgba(46,204,113,.25);
        white-space: nowrap;
    }


    /* ================= SECTION ================= */

    .section-title {
        font-size: 1.2rem;
        font-weight: 750;
        margin: 1.3rem 0 .8rem;
    }

    .section-caption {
        color: #8f96a3;
        font-size: .85rem;
        margin-bottom: .8rem;
    }


    /* ================= QUESTION ================= */

    .info-card {
        padding: 1rem 1.2rem;
        border-radius: 15px;
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.08);
        min-height: 88px;
        box-sizing: border-box;
        overflow-wrap: anywhere;
    }

    .label {
        color: #858c99;
        font-size: .7rem;
        font-weight: 750;
        letter-spacing: .08em;
        margin-bottom: .35rem;
    }

    .value {
        font-size: 1.05rem;
        line-height: 1.45;
        overflow-wrap: anywhere;
    }

    .startup-name {
        font-size: 1.25rem;
        font-weight: 750;
        overflow-wrap: anywhere;
    }


    /* ================= VERDICT ================= */

    .verdict-card {
        padding: 1.7rem;
        border-radius: 20px;
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.09);
        margin-bottom: 1rem;
        box-sizing: border-box;
        overflow: hidden;
    }

    .verdict-label {
        color: #9299a6;
        font-size: .75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .12em;
    }

    .verdict {
        font-size: 2.8rem;
        font-weight: 850;
        margin: .2rem 0 1rem;
    }

    .invest {
        color: #4ade80;
    }

    .pass {
        color: #f87171;
    }

    .review {
        color: #fbbf24;
    }

    .reasoning {
        padding: 1rem 1.2rem;
        border-left: 3px solid #7c83fd;
        border-radius: 8px;
        background: rgba(124,131,253,.07);
        line-height: 1.6;
        overflow-wrap: anywhere;
    }


    /* ================= ENGINE ================= */

    .engine-card {
        padding: 1.15rem;
        border-radius: 16px;
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.08);
    }

    .engine-title {
        font-size: 1rem;
        font-weight: 750;
    }

    .engine-description {
        color: #8f96a3;
        font-size: .78rem;
        margin-top: .25rem;
    }

    .ok {
        color: #4ade80;
        font-weight: 700;
    }

    .error {
        color: #f87171;
        font-weight: 700;
    }


    /* ================= EVIDENCE ================= */

    .evidence-card {
        padding: 1rem 1.15rem;
        border-radius: 14px;
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.07);
        margin-bottom: .65rem;
        box-sizing: border-box;
        overflow-wrap: anywhere;
    }

    .evidence-header {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: .5rem;
        flex-wrap: wrap;
    }

    .evidence-title {
        font-weight: 700;
    }

    .evidence-meta {
        color: #8f96a3;
        font-size: .72rem;
        overflow-wrap: anywhere;
    }

    .evidence-text {
        color: #d5d8de;
        line-height: 1.5;
        font-size: .9rem;
        overflow-wrap: anywhere;
    }


    /* ================= SQL ================= */

    .sql-result-card {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.07);
        margin-bottom: .7rem;
        min-height: 78px;
        box-sizing: border-box;
        overflow: hidden;
    }

    .sql-value {
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.35;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    .sql-label {
        color: #8f96a3;
        font-size: .72rem;
        margin-top: .3rem;
        overflow-wrap: anywhere;
    }

    .sql-query {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(0,0,0,.22);
        border: 1px solid rgba(255,255,255,.07);
        font-family: monospace;
        font-size: .82rem;
        line-height: 1.5;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        word-break: break-word;
    }


    /* ================= PIPELINE ================= */

    .pipeline {
        padding: 1.2rem;
        border-radius: 16px;
        background: rgba(255,255,255,.025);
        border: 1px solid rgba(255,255,255,.07);
        overflow-x: auto;
    }

    .pipeline-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-width: 850px;
    }

    .pipeline-step {
        text-align: center;
        flex: 1;
    }

    .pipeline-icon {
        font-size: 1.5rem;
    }

    .pipeline-name {
        font-weight: 700;
        font-size: .82rem;
        margin-top: .25rem;
    }

    .pipeline-sub {
        color: #858c99;
        font-size: .68rem;
    }

    .arrow {
        color: #666d79;
        padding: 0 .25rem;
    }


    /* ================= SIDEBAR ================= */

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255,255,255,.08);
    }

    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 800;
    }

    .sidebar-subtitle {
        color: #9299a6;
        font-size: .78rem;
    }


    /* ================= FOOTER ================= */

    .footer {
        text-align: center;
        color: #777f8c;
        font-size: .75rem;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    </style>
    """
)


# ============================================================
# DATASET
# ============================================================

if not DATASET_PATH.exists():
    st.error(
        "Dataset missing. Run: "
        "`python scripts/generate_dataset.py`"
    )
    st.stop()


data = json.loads(
    DATASET_PATH.read_text(encoding="utf-8")
)

names = [item["name"] for item in data]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            🔎 VentureLens
        </div>
        """
    )

    render_html(
        """
        <div class="sidebar-subtitle">
            AI Startup Due-Diligence Platform
        </div>
        """
    )

    st.divider()

    st.markdown("### 🎯 Analysis Setup")

    entity = st.selectbox(
        "Startup",
        names,
    )

    question = st.text_area(
        "Due-Diligence Question",
        f"Should an investor invest in {entity}?",
        height=120,
    )

    run = st.button(
        "🚀 Run Due Diligence",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.markdown("### 🧠 AI Architecture")

    st.markdown(
        """
        **01 — SQLite**  
        Structured financial retrieval

        **02 — Hybrid Search**  
        BM25 + Dense FAISS + RRF

        **03 — Neo4j**  
        Relationship intelligence

        **04 — DSPy**  
        Multi-source synthesis

        **05 — Gemini**  
        Teacher / Student LLM pipeline
        """
    )

    st.divider()

    st.caption("VentureLens • Phase 2")


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="hero">

        <div class="hero-row">

            <div>
                <div class="hero-title">
                    🔎 VentureLens
                </div>

                <div class="hero-subtitle">
                    AI-Powered Startup Due-Diligence Intelligence
                </div>
            </div>

            <div class="status-pill">
                ● MULTI-ENGINE SYSTEM READY
            </div>

        </div>

    </div>
    """
)


# ============================================================
# QUESTION
# ============================================================

render_html(
    """
    <div class="section-title">
        💬 Analysis Request
    </div>
    """
)

q1, q2 = st.columns([1, 2])

with q1:

    render_html(
        f"""
        <div class="info-card">

            <div class="label">
                TARGET STARTUP
            </div>

            <div class="startup-name">
                {html.escape(entity)}
            </div>

        </div>
        """
    )

with q2:

    render_html(
        f"""
        <div class="info-card">

            <div class="label">
                INVESTOR QUESTION
            </div>

            <div class="value">
                {html.escape(question)}
            </div>

        </div>
        """
    )


# ============================================================
# RUN
# ============================================================

if run:

    # ========================================================
    # RETRIEVAL
    # ========================================================

    with st.spinner(
        "Running SQL, hybrid search and knowledge graph retrieval..."
    ):

        results, total = parallel_retrieve(
            entity,
            question,
        )


    # ========================================================
    # SYNTHESIS
    # ========================================================

    with st.spinner(
        "DSPy + Gemini are synthesizing the analysis..."
    ):

        pred, mode = synthesize(
            results["sql"].context,
            results["faiss"].context,
            results["graph"].context,
        )


    # ========================================================
    # REPORT FIELDS
    # ========================================================

    verdict = str(
        getattr(pred, "verdict", "UNKNOWN")
    ).upper()

    confidence = getattr(
        pred,
        "confidence",
        "N/A",
    )

    financial_risk = getattr(
        pred,
        "financial_risk",
        "N/A",
    )

    market_risk = getattr(
        pred,
        "market_risk",
        "N/A",
    )

    network_strength = getattr(
        pred,
        "network_strength",
        "N/A",
    )

    reasoning = getattr(
        pred,
        "reasoning",
        "No reasoning returned.",
    )


    # ========================================================
    # MAIN ANSWER
    # ========================================================

    render_html(
        """
        <div class="section-title">
            🎯 AI Investment Verdict
        </div>
        """
    )

    if verdict == "INVEST":
        verdict_class = "invest"

    elif verdict == "PASS":
        verdict_class = "pass"

    else:
        verdict_class = "review"


    render_html(
        f"""
        <div class="verdict-card">

            <div class="verdict-label">
                DSPy + Gemini Decision
            </div>

            <div class="verdict {verdict_class}">
                {html.escape(verdict)}
            </div>

            <div class="reasoning">

                <strong>
                    Investment Rationale
                </strong>

                <div style="margin-top:.5rem;">
                    {html.escape(str(reasoning))}
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # METRICS
    # ========================================================

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "🎯 Confidence",
        f"{confidence}%",
    )

    m2.metric(
        "💰 Financial Risk",
        financial_risk,
    )

    m3.metric(
        "📈 Market Risk",
        market_risk,
    )

    m4.metric(
        "🕸️ Network Strength",
        network_strength,
    )


    # ========================================================
    # MULTI-SOURCE EVIDENCE
    # ========================================================

    render_html(
        """
        <div class="section-title">
            🔬 Multi-Source Evidence
        </div>
        """
    )

    render_html(
        """
        <div class="section-caption">
            Evidence retrieved independently from structured data,
            hybrid search and the knowledge graph.
        </div>
        """
    )


    # ========================================================
    # SQL UI
    # ========================================================

    sql_result = results["sql"]

    with st.expander(
        "🗄️ Financial Intelligence — SQLite",
        expanded=True,
    ):

        if sql_result.ok:

            st.success(
                f"SQLite operational • "
                f"{sql_result.latency_ms:.1f} ms"
            )

            raw = sql_result.raw or {}
            rows = raw.get("rows", [])

            if rows:

                st.markdown("#### 📊 Financial Result")

                for row in rows:

                    priority = [
                        "name",
                        "sector",
                        "revenue_musd",
                        "revenue_growth_pct",
                        "total_funding_musd",
                        "valuation_musd",
                        "burn_rate_musd",
                        "runway_months",
                        "employees",
                        "gross_margin_pct",
                        "customer_count",
                        "founded_year",
                        "id",
                    ]

                    ordered_items = []

                    # Preserve the desired order.
                    for key in priority:

                        if key in row:

                            ordered_items.append(
                                (key, row[key])
                            )

                    # Add any unexpected fields.
                    for key, value in row.items():

                        if key not in priority:

                            ordered_items.append(
                                (key, value)
                            )

                    # Render exactly four cards per row.
                    for start in range(
                        0,
                        len(ordered_items),
                        4,
                    ):

                        chunk = ordered_items[
                            start:start + 4
                        ]

                        cols = st.columns(4)

                        for col, (key, value) in zip(
                            cols,
                            chunk,
                        ):

                            with col:

                                render_html(
                                    f"""
                                    <div class="sql-result-card">

                                        <div class="sql-label">
                                            {html.escape(
                                                str(key)
                                            )}
                                        </div>

                                        <div class="sql-value">
                                            {html.escape(
                                                str(value)
                                            )}
                                        </div>

                                    </div>
                                    """
                                )

            else:

                st.info(
                    "SQLite returned no matching records."
                )

            # ------------------------------------------------
            # GENERATED SQL
            # ------------------------------------------------

            st.caption("Generated SQL")

            sql_text = str(
                raw.get(
                    "sql",
                    "Not available",
                )
            )

            render_html(
                f"""
                <div class="sql-query">
                    {html.escape(sql_text)}
                </div>
                """
            )

        else:

            st.error(
                f"SQLite unavailable: "
                f"{sql_result.error or 'Unknown SQL error'}"
            )


    # ========================================================
    # FAISS UI
    # ========================================================

    faiss_result = results["faiss"]

    with st.expander(
        "🔎 Market & Document Intelligence — FAISS + BM25 + RRF",
        expanded=True,
    ):

        if faiss_result.ok:

            st.success(
                f"Hybrid search operational • "
                f"{faiss_result.latency_ms:.1f} ms"
            )

            context = faiss_result.context

            lines = context.splitlines()

            evidence = []

            current = None

            for line in lines:

                if line.startswith("Evidence "):

                    if current:

                        evidence.append(current)

                    current = {
                        "header": line,
                        "text": "",
                    }

                elif current and line.strip():

                    current["text"] += (
                        line + " "
                    )

            if current:

                evidence.append(current)


            if evidence:

                for item in evidence:

                    header = item["header"]

                    header_parts = header.split("|")

                    evidence_title = (
                        header_parts[0].strip()
                    )

                    evidence_meta = " | ".join(
                        x.strip()
                        for x in header_parts[1:]
                    )

                    render_html(
                        f"""
                        <div class="evidence-card">

                            <div class="evidence-header">

                                <div class="evidence-title">
                                    🔎 {
                                        html.escape(
                                            evidence_title
                                        )
                                    }
                                </div>

                                <div class="evidence-meta">
                                    {
                                        html.escape(
                                            evidence_meta
                                        )
                                    }
                                </div>

                            </div>

                            <div class="evidence-text">
                                {
                                    html.escape(
                                        item["text"].strip()
                                    )
                                }
                            </div>

                        </div>
                        """
                    )

            else:

                st.info(
                    "Hybrid retrieval completed, but no structured "
                    "evidence items were returned."
                )

        else:

            st.error(
                f"FAISS unavailable: "
                f"{faiss_result.error or 'Unknown retrieval error'}"
            )


    # ========================================================
    # GRAPH UI
    # ========================================================

    graph_result = results["graph"]

    with st.expander(
        "🕸️ Relationship Intelligence — Neo4j",
        expanded=True,
    ):

        if graph_result.ok:

            st.success(
                f"Knowledge graph operational • "
                f"{graph_result.latency_ms:.1f} ms"
            )

            lines = graph_result.context.splitlines()

            relationships = []

            for line in lines:

                if "--[" in line and "-->" in line:

                    relationships.append(line)


            if relationships:

                st.markdown(
                    "#### 🔗 Discovered Relationships"
                )

                for relationship in relationships:

                    render_html(
                        f"""
                        <div class="evidence-card">

                            <div class="evidence-text">
                                🔗 {
                                    html.escape(
                                        relationship
                                    )
                                }
                            </div>

                        </div>
                        """
                    )

            else:

                st.info(
                    "Knowledge graph returned no structured "
                    "relationship records."
                )

        else:

            st.error(
                f"Neo4j unavailable: "
                f"{graph_result.error or 'Unknown graph error'}"
            )


    # ========================================================
    # PERFORMANCE
    # ========================================================

    render_html(
        """
        <div class="section-title">
            ⚡ System Performance
        </div>
        """
    )

    slowest_engine = max(
        results.items(),
        key=lambda x: x[1].latency_ms,
    )

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Parallel Wall Clock",
        f"{total:.1f} ms",
    )

    p2.metric(
        "Slowest Engine",
        slowest_engine[0].upper(),
    )

    p3.metric(
        "Operational Engines",
        sum(
            1
            for r in results.values()
            if r.ok
        ),
    )


    # ========================================================
    # AI SYNTHESIS
    # ========================================================

    render_html(
        """
        <div class="section-title">
            🧠 AI Synthesis
        </div>
        """
    )

    s1, s2 = st.columns(2)

    with s1:

        st.info(
            f"**DSPy Mode:** {mode}"
        )

    with s2:

        st.info(
            f"**Decision:** {verdict}"
        )


    # ========================================================
    # ARCHITECTURE
    # ========================================================

    render_html(
        """
        <div class="section-title">
            🧩 Execution Architecture
        </div>
        """
    )

    render_html(
        """
        <div class="pipeline">

            <div class="pipeline-row">

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        📝
                    </div>

                    <div class="pipeline-name">
                        Question
                    </div>

                    <div class="pipeline-sub">
                        Investor query
                    </div>

                </div>

                <div class="arrow">
                    →
                </div>

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        ⚡
                    </div>

                    <div class="pipeline-name">
                        Parallel
                    </div>

                    <div class="pipeline-sub">
                        Retrieval
                    </div>

                </div>

                <div class="arrow">
                    →
                </div>

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        🗄️
                    </div>

                    <div class="pipeline-name">
                        SQLite
                    </div>

                    <div class="pipeline-sub">
                        Financial
                    </div>

                </div>

                <div class="arrow">
                    +
                </div>

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        🔎
                    </div>

                    <div class="pipeline-name">
                        FAISS
                    </div>

                    <div class="pipeline-sub">
                        Hybrid
                    </div>

                </div>

                <div class="arrow">
                    +
                </div>

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        🕸️
                    </div>

                    <div class="pipeline-name">
                        Neo4j
                    </div>

                    <div class="pipeline-sub">
                        Graph
                    </div>

                </div>

                <div class="arrow">
                    →
                </div>

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        🧠
                    </div>

                    <div class="pipeline-name">
                        DSPy
                    </div>

                    <div class="pipeline-sub">
                        Synthesis
                    </div>

                </div>

                <div class="arrow">
                    →
                </div>

                <div class="pipeline-step">

                    <div class="pipeline-icon">
                        🎯
                    </div>

                    <div class="pipeline-name">
                        Verdict
                    </div>

                    <div class="pipeline-sub">
                        Decision
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # WARNINGS
    # ========================================================

    for key, r in results.items():

        if not r.ok:

            st.warning(
                f"{r.engine} unavailable; "
                "analysis continued with the remaining engines."
            )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    render_html(
        """
        <div class="verdict-card">

            <div style="
                text-align:center;
                padding:2.5rem;
            ">

                <div style="font-size:3rem;">
                    🔎
                </div>

                <div style="
                    font-size:1.5rem;
                    font-weight:750;
                    margin-top:.5rem;
                ">
                    Ready for Due Diligence
                </div>

                <div style="
                    color:#9299a6;
                    margin-top:.5rem;
                ">
                    Select a startup, enter an investor question,
                    and run the multi-source AI analysis.
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# MOCK MODE
# ============================================================

if MOCK_LLM:

    st.warning(
        "⚠️ MOCK_LLM=true — offline demonstration mode. "
        "Set MOCK_LLM=false to use the real Gemini/DSPy pipeline."
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        VentureLens • Phase 2 • Parallel Multi-Source
        Startup Due-Diligence Engine
    </div>
    """
)