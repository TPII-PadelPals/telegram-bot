import os


class Config:
    """Set the configuration for the bot."""
    GATEWAY_HOST = os.getenv("GATEWAY_HOST", "127.0.0.1")
    GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_LANGUAGE = os.getenv("TELEGRAM_BOT_LANGUAGE", "ES")

    @classmethod
    def validate_envs(cls):
        """Validate the required environment variables."""
        missing_envs = []
        if not os.getenv("GATEWAY_HOST"):
            missing_envs.append("GATEWAY_HOST")
        if not os.getenv("GATEWAY_PORT"):
            missing_envs.append("GATEWAY_PORT")
        if not os.getenv("TELEGRAM_BOT_TOKEN"):
            missing_envs.append("TELEGRAM_BOT_TOKEN")
        if not os.getenv("TELEGRAM_BOT_LANGUAGE"):
            missing_envs.append("TELEGRAM_BOT_LANGUAGE")
        if missing_envs:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_envs)}")
