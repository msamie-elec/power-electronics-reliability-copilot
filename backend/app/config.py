from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
DOCUMENTS_DIR = BASE_DIR / "documents"
METADATA_DIR = BASE_DIR / "metadata"
CHUNKS_DIR = BASE_DIR / "chunks"

FRONTEND_ORIGIN = "http://localhost:5173"

APP_NAME = "Power Electronics Reliability Copilot API"
APP_VERSION = "0.3.0"

CHUNKS_DIR = BASE_DIR / "chunks"

EMBEDDINGS_DIR = BASE_DIR / "embeddings"