from .base_service import BaseService


class UsersServiceBackend(BaseService):
    def register_user(self, chat_id):
        """Register a user with the given chat ID."""
        return self.post("/users", json={'chat_id': str(chat_id)})

    def get_user_info(self, chat_id):
        """Get the information of a user with the given chat ID."""
        return self.get(f"/users/{chat_id}")

    def generate_google_auth_url(self, chat_id):
        """Generate a URL for Google authentication."""
        return self.generate_url(f"/google/auth?chat_id={chat_id}")
