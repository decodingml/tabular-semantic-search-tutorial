from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # OpenAI
    OPENAI_MODEL_ID: str = "gpt-4o"
    OPENAI_API_KEY: SecretStr | None = None


settings = Settings()
