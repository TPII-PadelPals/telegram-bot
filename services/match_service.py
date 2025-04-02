from uuid import UUID
from .base_service import BaseService
from core.config import settings

class MatchService(BaseService):

    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.MATCHES_SERVICE_HOST, settings.MATCHES_SERVICE_PORT)
        self.set_prefix_url("/api/v1")
        self.x_api_key_header = {"x-api-key": settings.MATCHES_SERVICE_API_KEY}

    def get_user_matches(self, user_public_id: UUID):
        """Get provisional_match."""
        return self.get(f"/players/{user_public_id}/matches/")
