from .base_service import BaseService

from core.config import settings


class PlayerService(BaseService):
    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.PLAYER_SERVICE_HOST, settings.PLAYER_SERVICE_PORT)
        self.base_url += "/api/v1"
        self.x_api_key_header = {"x-api-key": settings.PLAYER_SERVICE_API_KEY}


    def update_strokes(self, player_nickname: str, strokes: dict):
        """Update strokes to player service."""
        # /players/{user_public_id}/strokes/
        # Update Stroke
        return self.put(
            f"/players/{player_nickname}/strokes/",
            headers=self.x_api_key_header,
            # params={"user_public_id": player_nickname},
            json=strokes
        )