import os


class Config:
    """Set the configuration for the bot."""
    SERVICE_HOST = os.getenv("SERVICE_HOST", "127.0.0.1")
    SERVICE_PORT = os.getenv("SERVICE_PORT", "8000")
    USERS_SERVICE_HOST = os.getenv("USERS_SERVICE_HOST", "127.0.0.1")
    USERS_SERVICE_PORT = os.getenv("USERS_SERVICE_PORT", "8000")
    USERS_SERVICE_API_KEY = os.getenv("USERS_SERVICE_API_KEY", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    LANGUAGE = os.getenv("LANGUAGE", "ES")

    ENV_VARS = [
        "SERVICE_HOST",
        "SERVICE_PORT",
        "USERS_SERVICE_HOST",
        "USERS_SERVICE_PORT",
        "USERS_SERVICE_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "LANGUAGE"
    ]

    @classmethod
    def validate_envs(cls):
        """Validate the required environment variables."""
        missing_envs = []
        for env_var in cls.ENV_VARS:
            if not os.getenv(env_var):
                missing_envs.append(env_var)
        # if not os.getenv("SERVICE_HOST"):
        #     missing_envs.append("SERVICE_HOST")
        # if not os.getenv("SERVICE_PORT"):
        #     missing_envs.append("SERVICE_PORT")
        # if not os.getenv("TELEGRAM_BOT_TOKEN"):
        #     missing_envs.append("TELEGRAM_BOT_TOKEN")
        # if not os.getenv("LANGUAGE"):
        #     missing_envs.append("LANGUAGE")
        if missing_envs:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_envs)}")
