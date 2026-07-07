from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
DOCUMENTS_DIR = BASE_DIR / "documents"
METADATA_DIR = BASE_DIR / "metadata"
CHUNKS_DIR = BASE_DIR / "chunks"

FRONTEND_ORIGIN = "http://localhost:5173"

APP_NAME = "Power Electronics Reliability Copilot API"
APP_VERSION = "0.5.2-dev"

CHUNKS_DIR = BASE_DIR / "chunks"

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# OpenAI models
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EXTRACTION_MODEL = os.getenv(
    "OPENAI_EXTRACTION_MODEL",
    "gpt-4.1-mini",
)

