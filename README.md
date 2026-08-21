# Phase2-VentureLens-AI-Powered-Startup-Due-Diligence-Platform
VentureLens is an agentic AI-powered startup due-diligence platform that evaluates investment opportunities by combining structured financial analysis, hybrid semantic retrieval, knowledge-graph reasoning, and LLM-based synthesis.

The project is designed as the continuation of the Phase 1 RAG project and demonstrates how an AI system can intelligently route user questions to the appropriate retrieval mechanism instead of relying on a single search strategy.

---

## 🚀 Project Overview

Traditional RAG systems work well when information is stored as unstructured text, but they are not ideal for questions involving:

* Aggregations
* Sorting
* Filtering
* Comparisons
* Numerical values
* Rankings
* Database records

For example:

> **"Which startup has the highest revenue?"**

This type of question is better answered by querying a structured SQL database rather than performing semantic vector search.

The Phase 2 assistant therefore combines **LLM reasoning with SQL-based retrieval** to answer structured-data questions.

---

## 🎯 Problem Statement

Build an AI-powered research assistant capable of answering questions about startup/company information.

The system should:

1. Accept a natural-language question from the user.
2. Understand what information the user is requesting.
3. Generate an appropriate SQL query when structured database information is required.
4. Execute the generated SQL query safely.
5. Return the database result to the LLM.
6. Generate a natural-language answer based on the retrieved data.
7. Handle SQL-generation or database errors gracefully.
8. Provide a user-friendly Streamlit interface.

The application should avoid blindly generating SQL against unknown database columns or tables and should provide meaningful error handling when a query cannot be executed.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         │ Natural Language    │
                         │      Question       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Agent / Router    │
                         │                     │
                         │ Understand Question │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                ┌─────────────────┐   ┌─────────────────┐
                │ SQL Retrieval   │   │ Other Retrieval │
                │     Path        │   │     Path        │
                └────────┬────────┘   └─────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ SQL Generation  │
                │      LLM        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ SQLite Database │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Query Result    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Answer          │
                │ Generation      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Streamlit UI    │
                └─────────────────┘
```

---

# 📁 Project Structure

```text
phase2-startup-research-assistant/
│
├── backend/
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── retrieval/
│   │   └── sql_retriever.py
│   │
│   ├── services/
│   │   └── ...
│   │
│   └── app.py
│
├── data/
│   └── startups.db
│
├── frontend/
│   └── ...
│
├── tests/
│   └── ...
│
├── scripts/
│   └── ...
│
├── app.py
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

> The exact file structure may vary slightly depending on the implementation, but the major responsibilities should remain separated into UI, retrieval, models, data, and application logic.

---

# 🧠 Key Components

## 1. Streamlit Application

The Streamlit application provides the user interface.

Users can enter questions such as:

```text
Which startup has the highest revenue?
```

or:

```text
Show me startups founded after 2020.
```

The UI sends the question to the backend retrieval/agent pipeline and displays the resulting answer.

---

## 2. SQL Retriever

The SQL retriever is responsible for converting natural-language questions into executable SQL queries.

Example:

```text
User:
Which startup has the highest revenue?
```

The LLM should generate something conceptually similar to:

```sql
SELECT name, revenue
FROM startups
ORDER BY revenue DESC
LIMIT 1;
```

The SQL query is then executed against the SQLite database.

---

## 3. Database

The project uses a structured SQL database containing startup/company information.

Typical fields may include:

```text
id
name
industry
location
founded_year
employees
funding
valuation
revenue
```

The **actual database schema must always be treated as the source of truth**.

The LLM should not assume that a column exists merely because the user mentioned that concept.

For example, if the database does not contain:

```text
revenue
```

then the system must not blindly execute:

```sql
SELECT revenue FROM startups;
```

Instead, the application should detect the schema mismatch and return a useful error or fallback response.

---

# 🔄 SQL Query Generation Flow

The SQL retrieval pipeline follows this process:

```text
Natural Language Question
          │
          ▼
   Schema Information
          │
          ▼
      LLM Prompt
          │
          ▼
     SQL Generation
          │
          ▼
 SQL Validation / Cleaning
          │
          ▼
    SQLite Execution
          │
          ▼
     Query Result
          │
          ▼
   Natural Language Answer
```

---

# 🧩 Schema-Aware SQL Generation

One of the important lessons from this project is that **SQL generation must be schema-aware**.

A prompt such as:

```text
Generate SQL for the user's question.
```

is insufficient.

The model should receive information about the available database tables and columns.

For example:

```text
Database schema:

Table: startups

Columns:
- id
- name
- industry
- founded_year
- funding
- valuation
```

Then the model can determine whether a question can actually be answered using the available data.

---

# 🛡️ Error Handling

The application should gracefully handle failures such as:

### Invalid column

```text
OperationalError:
no such column: revenue
```

### Invalid table

```text
OperationalError:
no such table: startups
```

### Invalid SQL

```text
SQL syntax error
```

### LLM failure

```text
Model/API error
```

### Rate limiting

```text
429 / rate limit error
```

Instead of crashing the application, these errors should be converted into meaningful application-level responses.

---

# 🤖 DSPy / LLM Integration

The project can use DSPy to structure the LLM-based reasoning process.

A simplified conceptual flow is:

```text
Question
   │
   ▼
DSPy Module
   │
   ├── Understand Question
   │
   ├── Generate SQL
   │
   └── Interpret Result
   │
   ▼
Final Answer
```

DSPy helps separate the **reasoning/program structure** from hard-coded prompt logic.

---

# 🔐 Security Considerations

Generated SQL should not be treated as trusted input.

Recommended protections include:

* Restricting execution to read-only SQL.
* Blocking destructive operations.
* Preventing `DROP`.
* Preventing `DELETE`.
* Preventing `UPDATE`.
* Preventing `INSERT`.
* Validating table names and columns.
* Using parameterized queries where user-provided values are inserted.
* Limiting query execution time/complexity where appropriate.

For example, the system should reject queries such as:

```sql
DROP TABLE startups;
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it using PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation, you can alternatively use:

```cmd
.venv\Scripts\activate.bat
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If the project uses `uv`:

```bash
uv sync
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_api_key_here
```

Use `.env.example` as the template.

**Never commit your real API key to GitHub.**

Make sure `.env` is included in `.gitignore`.

---

# ▶️ Running the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🧪 Testing SQL Retrieval

The SQL retriever can be tested independently from the Streamlit UI.

Example:

```bash
python -c "from backend.retrieval.sql_retriever import query_sql; r=query_sql('Which startup has the highest revenue?'); print(r.context); print(r.ok)"
```

The returned object should indicate whether the SQL operation succeeded.

For example:

```text
True
```

means the query completed successfully.

---

# 🧪 Running Tests

If tests are included:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

---

# 💡 Example Questions

The assistant should be able to handle questions such as:

### Ranking

```text
Which startup has the highest valuation?
```

### Filtering

```text
Which startups were founded after 2020?
```

### Aggregation

```text
How many startups are in the fintech industry?
```

### Comparison

```text
Which startup has received the most funding?
```

### Sorting

```text
List the top 5 startups by valuation.
```

### Conditional query

```text
Show startups founded after 2019 with funding greater than 10 million.
```

---

# ❌ Example of an Unanswerable Question

If the database contains:

```text
name
industry
funding
valuation
founded_year
```

but does not contain:

```text
revenue
```

then asking:

```text
Which startup has the highest revenue?
```

cannot be answered from the database.

The system should **not hallucinate a revenue value**.

Instead, it should explain that the required field is unavailable in the database.

---

# 📊 Example End-to-End Execution

### User Question

```text
Which startup has the highest valuation?
```

### Step 1 — Understand Question

The system determines that this is a structured-data question.

### Step 2 — Inspect Schema

```text
startups:
- name
- valuation
- funding
- industry
```

### Step 3 — Generate SQL

```sql
SELECT name, valuation
FROM startups
ORDER BY valuation DESC
LIMIT 1;
```

### Step 4 — Execute SQL

SQLite returns:

```text
Startup A | 500000000
```

### Step 5 — Generate Answer

```text
Startup A has the highest valuation at $500 million.
```

---

# 🧱 Design Principles

The project follows several important AI engineering principles.

### Separation of concerns

UI, retrieval, database access, schemas, and LLM logic should remain separated.

### Schema awareness

The model should generate SQL based on the real database schema.

### Explicit failure handling

Database and LLM errors should be returned as controlled application responses.

### No hallucination

The assistant should not invent information that is unavailable in the database.

### Testability

The SQL retrieval component should be testable independently from the UI.

### Observability

Important steps such as SQL generation, execution, and errors should be logged during development.

---

# 🛠️ Technology Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core programming language       |
| Streamlit     | User interface                  |
| SQLite        | Structured data storage         |
| DSPy          | LLM program/reasoning framework |
| Google Gemini | LLM                             |
| Pydantic      | Structured data validation      |
| Pytest        | Testing                         |
| python-dotenv | Environment configuration       |

---

# 🧪 Troubleshooting

## `streamlit` is not recognized

Make sure the virtual environment is activated and Streamlit is installed:

```bash
pip install streamlit
```

Then:

```bash
streamlit run app.py
```

---

## `no such column`

Example:

```text
OperationalError: no such column: revenue
```

This means the generated SQL references a column that does not exist in the database.

Check the database schema before changing the SQL-generation prompt.

---

## API rate limit

If the LLM provider returns a rate-limit error:

```text
429
```

check:

* API quota
* API key
* model availability
* request frequency
* provider limits

Avoid repeatedly retrying requests without backoff.

---

## `.env` not loading

Ensure the file is named:

```text
.env
```

and not:

```text
.env.txt
```

Example:

```env
GOOGLE_API_KEY=your_key
```

Restart the application after modifying environment variables.

---

# 📌 Development Workflow

A recommended workflow is:

```text
1. Check database schema
        ↓
2. Test SQL retriever independently
        ↓
3. Test LLM SQL generation
        ↓
4. Test SQL execution
        ↓
5. Test error handling
        ↓
6. Connect retriever to agent
        ↓
7. Connect agent to Streamlit
        ↓
8. Run pytest
        ↓
9. Test complete application
```

---
