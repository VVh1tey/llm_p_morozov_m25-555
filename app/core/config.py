from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "llm-p"
    ENV: str = "local"

    JWT_SECRET: str
    JWT_ALG: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SQLITE_PATH: str

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_SITE_URL: str
    OPENROUTER_APP_NAME: str


settings = Settings()
