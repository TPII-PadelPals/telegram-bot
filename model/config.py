import os

class Config:
    """Set the configuration for the bot."""
    SERVICE_HOST = os.getenv("SERVICE_HOST", "127.0.0.1")
    SERVICE_PORT = os.getenv("SERVICE_PORT", "8000")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    LANGUAGE = os.getenv("LANGUAGE", "ES")

    @classmethod
    def validate_envs(cls):
        """Validate the required environment variables."""
        missing_envs = []
        if not os.getenv("SERVICE_HOST"):
            missing_envs.append("SERVICE_HOST")
        if not os.getenv("SERVICE_PORT"):
            missing_envs.append("SERVICE_PORT")
        if not os.getenv("TELEGRAM_BOT_TOKEN"):
            missing_envs.append("TELEGRAM_BOT_TOKEN")
        if not os.getenv("LANGUAGE"):
            missing_envs.append("LANGUAGE")
        if missing_envs:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_envs)}")

