"""
Power Electronics Reliability Copilot
Application Configuration

Centralised environment-aware configuration for local development and Azure
cloud deployment.

v0.6.0 introduces cloud-ready configuration while preserving backward
compatibility with the existing local development workflow.
"""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    name: str
    version: str
    environment: str
    frontend_origin: str

    @property
    def is_azure(self) -> bool:
        return self.environment.lower().strip() == "azure"


@dataclass(frozen=True)
class OpenAIConfig:
    ai_provider: str
    api_key: str
    model: str
    extraction_model: str
    azure_endpoint: str
    azure_api_key: str
    azure_api_version: str
    azure_chat_deployment: str
    azure_embedding_deployment: str

    @property
    def use_azure_openai(self) -> bool:
        provider = self.ai_provider.lower().strip()

        if provider == "azure_openai":
            return True

        if provider == "openai":
            return False

        return bool(
            self.azure_endpoint
            and self.azure_api_key
            and self.azure_chat_deployment
        )


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str
    username: str
    password: str
    database: str


@dataclass(frozen=True)
class StorageConfig:
    upload_dir: Path
    documents_dir: Path
    metadata_dir: Path
    chunks_dir: Path
    embeddings_dir: Path
    azure_storage_connection_string: str
    azure_storage_account_name: str
    azure_blob_container_name: str

    @property
    def use_azure_blob_storage(self) -> bool:
        return bool(
            self.azure_storage_connection_string
            and self.azure_blob_container_name
        )


@dataclass(frozen=True)
class EmbeddingConfig:
    model_name: str


@dataclass(frozen=True)
class AzureConfig:
    key_vault_name: str
    resource_group: str
    location: str


app_config = AppConfig(
    name=os.getenv("APP_NAME", "Power Electronics Reliability Copilot API"),
    version=os.getenv("APP_VERSION", "0.6.0-dev"),
    environment=os.getenv("APP_ENV", "development"),
    frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
)

openai_config = OpenAIConfig(
    ai_provider=os.getenv("AI_PROVIDER", "openai"),
    api_key=os.getenv("OPENAI_API_KEY", ""),
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    extraction_model=os.getenv("OPENAI_EXTRACTION_MODEL", "gpt-4.1-mini"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
    azure_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    azure_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_chat_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", ""),
    azure_embedding_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", ""),
)

neo4j_config = Neo4jConfig(
    uri=os.getenv("NEO4J_URI", ""),
    username=os.getenv("NEO4J_USERNAME", ""),
    password=os.getenv("NEO4J_PASSWORD", ""),
    database=os.getenv("NEO4J_DATABASE", "neo4j"),
)

storage_config = StorageConfig(
    upload_dir=BASE_DIR / os.getenv("UPLOAD_DIR", "uploads"),
    documents_dir=BASE_DIR / os.getenv("DOCUMENTS_DIR", "documents"),
    metadata_dir=BASE_DIR / os.getenv("METADATA_DIR", "metadata"),
    chunks_dir=BASE_DIR / os.getenv("CHUNKS_DIR", "chunks"),
    embeddings_dir=BASE_DIR / os.getenv("EMBEDDINGS_DIR", "embeddings"),
    azure_storage_connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING", ""),
    azure_storage_account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME", ""),
    azure_blob_container_name=os.getenv(
        "AZURE_BLOB_CONTAINER_NAME",
        "engineering-documents",
    ),
)

embedding_config = EmbeddingConfig(
    model_name=os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5"),
)

azure_config = AzureConfig(
    key_vault_name=os.getenv("AZURE_KEY_VAULT_NAME", ""),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP", "rg-powerelec-copilot-dev"),
    location=os.getenv("AZURE_LOCATION", "uksouth"),
)


# --------------------------------------------------------------------------
# Backward-compatible constants
# --------------------------------------------------------------------------

APP_NAME = app_config.name
APP_VERSION = app_config.version
APP_ENV = app_config.environment
FRONTEND_ORIGIN = app_config.frontend_origin

AI_PROVIDER = openai_config.ai_provider

OPENAI_API_KEY = openai_config.api_key
OPENAI_MODEL = openai_config.model
OPENAI_EXTRACTION_MODEL = openai_config.extraction_model

AZURE_OPENAI_ENDPOINT = openai_config.azure_endpoint
AZURE_OPENAI_API_KEY = openai_config.azure_api_key
AZURE_OPENAI_API_VERSION = openai_config.azure_api_version
AZURE_OPENAI_CHAT_DEPLOYMENT = openai_config.azure_chat_deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = openai_config.azure_embedding_deployment

NEO4J_URI = neo4j_config.uri
NEO4J_USERNAME = neo4j_config.username
NEO4J_PASSWORD = neo4j_config.password
NEO4J_DATABASE = neo4j_config.database

UPLOAD_DIR = storage_config.upload_dir
DOCUMENTS_DIR = storage_config.documents_dir
METADATA_DIR = storage_config.metadata_dir
CHUNKS_DIR = storage_config.chunks_dir
EMBEDDINGS_DIR = storage_config.embeddings_dir

AZURE_STORAGE_CONNECTION_STRING = storage_config.azure_storage_connection_string
AZURE_STORAGE_ACCOUNT_NAME = storage_config.azure_storage_account_name
AZURE_BLOB_CONTAINER_NAME = storage_config.azure_blob_container_name

EMBEDDING_MODEL_NAME = embedding_config.model_name

AZURE_KEY_VAULT_NAME = azure_config.key_vault_name
AZURE_RESOURCE_GROUP = azure_config.resource_group
AZURE_LOCATION = azure_config.location