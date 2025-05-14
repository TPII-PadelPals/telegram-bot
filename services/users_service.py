from .base_service import BaseService
from core.config import settings


class User:
    def __init__(self, public_id="", name="", email="", phone="", telegram_id=0):
        self.public_id: str = str(public_id)
        self.name: str = str(name)
        self.email: str = str(email)
        self.phone: str = str(phone)
        self.telegram_id: int = int(telegram_id)


class UsersService(BaseService):
    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.USERS_SERVICE_HOST,
                           settings.USERS_SERVICE_PORT)
        self.base_url += "/api/v1"
        self.x_api_key_header = {"x-api-key": settings.USERS_SERVICE_API_KEY}

    def get_user_info(self, chat_id) -> User | None:
        """Get the information of a user given users's chat ID 
        which corresponds to the telegram ID in the UsersService"""
        content = self.get("/users/", params={"telegram_id": chat_id})
        return [User(**data) for data in content["data"]]

    def get_user_by_id(self, user_public_id):
        """Get the information of a user given users's public ID"""
        data = self.get(f"/users/{user_public_id}/")
        if data is None:
            return None
        return User(**data)

    def generate_google_auth_url(self, chat_id):
        """Generate a URL for Google authentication given user's chat ID 
        which corresponds to the telegram ID in the UsersService"""
        return self.generate_url(f"/google/auth?telegram_id={chat_id}")
