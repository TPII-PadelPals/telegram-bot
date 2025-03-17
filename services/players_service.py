from .base_service import BaseService

from core.config import settings


class PlayersService(BaseService):
    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.PLAYERS_SERVICE_HOST, settings.PLAYERS_SERVICE_PORT)
        self.set_prefix_url("/api/v1")
        self.x_api_key_header = {"x-api-key": settings.PLAYERS_SERVICE_API_KEY}


    def update_strokes(self, user_public_id_str: str, strokes: dict):
        """Update strokes to player service."""
        return self.put(
            f"/players/{user_public_id_str}/strokes/",
            json=strokes
        )
    

    def update_partial_player(self, user_public_id, partial_player: dict):
        """Partially updates a player."""
        return self.patch(f"/players/?user_public_id={user_public_id}", json=partial_player)
    

    def update_availability(self, user_public_id, availability_days: dict):
        """Update availability day/s from player."""
        return self.patch(f"/players/{user_public_id}/availability/", json=availability_days)
