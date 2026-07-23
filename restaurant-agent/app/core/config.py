from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app settings. Every module should import `settings` from here
    instead of reading os.environ directly.
    """

    # --- LLM (Gemini) ---
    gemini_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    gemini_model: str = Field("gemini-2.0-flash", alias="GEMINI_MODEL")
    gemini_temperature: float = Field(0.3, alias="GEMINI_TEMPERATURE")
    gemini_embed_model: str = Field("models/gemini-embedding-001", alias="GEMINI_EMBED_MODEL")
    embedding_dimension: int = Field(768, alias="EMBEDDING_DIMENSION")

    # --- Pinecone ---
    pinecone_api_key: str = Field(..., alias="PINECONE_API_KEY")
    pinecone_index_name: str = Field(..., alias="PINECONE_INDEX_NAME")
    pinecone_environment: str = Field("us-east-1", alias="PINECONE_ENVIRONMENT")

    # --- Database ---
    database_url: str = Field("sqlite:///./app.db", alias="DATABASE_URL")

    # --- App ---
    app_name: str = Field("Restaurant Reservation Assistant", alias="APP_NAME")
    debug: bool = Field(False, alias="DEBUG")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — reads .env only once per process."""
    return Settings()


# Import this directly wherever you need config: `from app.core.config import settings`
settings = get_settings()