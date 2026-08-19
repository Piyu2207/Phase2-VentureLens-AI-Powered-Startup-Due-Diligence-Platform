from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env", override=True)

SQLITE_PATH = ROOT / os.getenv("SQLITE_PATH", "data/sqlite/venturelens.db")
FAISS_DIR = ROOT / os.getenv("FAISS_DIR", "artifacts/faiss")

DATASET_PATH = ROOT / os.getenv("DATASET_PATH", "data/startups.json")
DSPY_COMPILED_PATH = ROOT / os.getenv("DSPY_COMPILED_PATH", "artifacts/dspy/compiled_startup_diligence.json")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "5"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "venturelens")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

TEACHER_MODEL = os.getenv("TEACHER_MODEL", "gemini/gemini-3.1-pro-preview")
STUDENT_MODEL = os.getenv("STUDENT_MODEL", "gemini/gemini-3.6-flash")

MOCK_LLM = os.getenv("MOCK_LLM", "false").lower() == "true"

for path in [SQLITE_PATH.parent, FAISS_DIR, DSPY_COMPILED_PATH.parent]:
    path.mkdir(parents=True, exist_ok=True)