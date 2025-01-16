from .base_service import BaseService
from core.config import settings


class UsersService(BaseService):
    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.USERS_SERVICE_HOST,
                           settings.USERS_SERVICE_PORT)
        self.base_url += "/api/v1"
        self.x_api_key_header = {"x-api-key": settings.USERS_SERVICE_API_KEY}

    def get_user_info(self, chat_id):
        """Get the information of a user given users's chat ID 
        which corresponds to the telegram ID in the UsersService"""
        return self.get("/users/", params={"telegram_id": chat_id})

    def generate_google_auth_url(self, chat_id):
        """Generate a URL for Google authentication given user's chat ID 
        which corresponds to the telegram ID in the UsersService"""
        return self.generate_url(f"/google/auth?telegram_id={chat_id}")
