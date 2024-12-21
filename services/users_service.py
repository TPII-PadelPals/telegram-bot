from .base_service import BaseService
from core.config import settings


class UsersService(BaseService):
    def __init__(self):
        """Set the base URL for the service."""
        local_server = ["localhost", "127.0.0.1"]
        host = f"{settings.USERS_SERVICE_HOST}:{settings.USERS_SERVICE_PORT}/api/v1"
        self.base_url = f"http://{host}" if settings.USERS_SERVICE_HOST in local_server else f"https://{host}"
        self.x_api_key_header = {"x-api-key": settings.USERS_SERVICE_API_KEY}

    def get_user_info(self, chat_id):
        """Get the information of a user with the given chat ID."""
        return self.get("/users/", params={"telegram_id": chat_id})

    def generate_google_auth_url(self, chat_id):
        """Generate a URL for Google authentication."""
        return self.generate_url(f"/google/auth?chat_id={chat_id}")
