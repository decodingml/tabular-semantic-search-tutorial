from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Superlinked
    APP_MODULE_PATH: str = "product_search"
    USE_MONGODB: bool = True
    GPU_EMBEDDING_THRESHOLD: int = 32

    # MongoDB
    MONGO_CLUSTER_URL: str
    MONGO_DATABASE_NAME: str
    MONGO_CLUSTER_NAME: str
    MONGO_PROJECT_ID: str
    MONGO_API_PUBLIC_KEY: str
    MONGO_API_PRIVATE_KEY: str

    # OpenAI
    OPENAI_MODEL_ID: str = "gpt-4o"
    OPENAI_API_KEY: SecretStr


settings = Settings()
