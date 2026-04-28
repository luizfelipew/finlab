from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Sempre `api/.env`, independente do cwd (ex.: worker do uvicorn --reload).
_API_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_API_DIR / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    qdrant_url: str
    qdrant_api_key: str
    collection_name: str = "financial"
    dense_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    sparse_model: str = "Qdrant/bm25"
    colbert_model: str = "colbert-ir/colbertv2.0"
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

settings = Settings()
