from uuid import UUID
from .base_service import BaseService
from core.config import settings

class MatchesService(BaseService):

    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.MATCHES_SERVICE_HOST, settings.MATCHES_SERVICE_PORT)
        self.set_prefix_url("/api/v1")
        self.x_api_key_header = {"x-api-key": settings.MATCHES_SERVICE_API_KEY}

    def get_user_matches(self, user_public_id: UUID):
        """Get provisional_match."""
        return self.get(f"/players/{user_public_id}/matches/")
    
    def get_match_player(self, user_public_id: UUID, match_public_id: UUID):
        """Get match player"""
        return self.get(f"/matches/{match_public_id}/players/{user_public_id}")
    
    def update_match_player_status(self, user_public_id: UUID, match_public_id: UUID, status:str):
        """Patch player status on a match."""
        status_json = {
            "reserve": status,
        }
        return self.patch(f"/matches/{match_public_id}/players/{user_public_id}/", json=status_json)
