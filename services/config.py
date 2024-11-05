import os

class Config:
    """Set the configuration for the service."""
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = os.getenv("API_PORT", "8000")