from pathlib import Path

from loguru import logger
from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / ".env"
logger.info(f"Loading '.env' file from: {ENV_FILE}")

assert ENV_FILE.exists(), ".env doesn't exists at the expected location"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding="utf-8")

    # Superlinked
    PROCESSED_DATASET_PATH: Path = Path("data") / "processed_300_sample.jsonl"
    GPU_EMBEDDING_THRESHOLD: int = 32

    # MongoDB
    USE_MONGO_VECTOR_DB: bool = False  # If 'False', we will use an InMemory vector database that requires no credentials.
    MONGO_CLUSTER_URL: str | None = None
    MONGO_DATABASE_NAME: str | None = None
    MONGO_CLUSTER_NAME: str | None = None
    MONGO_PROJECT_ID: str | None = None
    MONGO_API_PUBLIC_KEY: str | None = None
    MONGO_API_PRIVATE_KEY: str | None = None

    # OpenAI
    OPENAI_MODEL_ID: str = "gpt-4o"
    OPENAI_API_KEY: SecretStr

    @model_validator(mode="after")
    def validate_mongo_config(self) -> "Settings":
        """Validates that all MongoDB settings are properly configured when MongoDB is enabled."""

        if self.USE_MONGO_VECTOR_DB:
            required_settings = {
                "MONGO_CLUSTER_URL": self.MONGO_CLUSTER_URL,
                "MONGO_DATABASE_NAME": self.MONGO_DATABASE_NAME,
                "MONGO_CLUSTER_NAME": self.MONGO_CLUSTER_NAME,
                "MONGO_PROJECT_ID": self.MONGO_PROJECT_ID,
                "MONGO_API_PUBLIC_KEY": self.MONGO_API_PUBLIC_KEY,
                "MONGO_API_PRIVATE_KEY": self.MONGO_API_PRIVATE_KEY,
            }

            missing_settings = [
                key for key, value in required_settings.items() if not value
            ]

            if missing_settings:
                raise ValueError(
                    f"MongoDB is enabled but the following required settings are missing: {', '.join(missing_settings)}"
                )

        return self

    def validate_processed_dataset_exists(self):
        if not self.PROCESSED_DATASET_PATH.exists():
            raise ValueError(
                f"Processed dataset not found at '{self.PROCESSED_DATASET_PATH}'. "
                "Please run 'make download-and-process-sample-dataset' first to download and process the Amazon dataset."
            )


settings = Settings()
