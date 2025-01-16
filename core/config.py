from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Bot settings
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_LANGUAGE: str

    TELEGRAM_BOT_SERVICE_HOST: str
    TELEGRAM_BOT_SERVICE_PORT: int

    # Gateway settings
    GATEWAY_HOST: str
    GATEWAY_PORT: int

    # Users service settings
    USERS_SERVICE_HOST: str
    USERS_SERVICE_PORT: int
    USERS_SERVICE_API_KEY: str


settings = Settings()
