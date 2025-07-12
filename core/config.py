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

    # Players service settings
    PLAYERS_SERVICE_HOST: str
    PLAYERS_SERVICE_PORT: int
    PLAYERS_SERVICE_API_KEY: str

    # Business service settings
    BUSINESS_SERVICE_HOST: str
    BUSINESS_SERVICE_PORT: int
    BUSINESS_SERVICE_API_KEY: str

    # Matches service settings
    MATCHES_SERVICE_HOST: str
    MATCHES_SERVICE_PORT: int
    MATCHES_SERVICE_API_KEY: str

    # Payments service settings
    PAYMENTS_SERVICE_HOST: str
    PAYMENTS_SERVICE_PORT: int
    PAYMENTS_SERVICE_API_KEY: str


settings = Settings()
