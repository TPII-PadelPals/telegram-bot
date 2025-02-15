from .base_service import BaseService

from core.config import settings


class PlayerService(BaseService):
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


class PlayerServiceBackEnd(BaseService):

    def update_location(self, player_nickname: str, streetname: str):
        """Send location to backend to get coordinates."""
        return self.post(f"/player/{player_nickname}/location", json={'streetname': streetname})


    def update_radius(self, player_nickname: str, location: str, radius: int):
        """Send location radius to backend."""
        return self.post(f"/player/{player_nickname}/location/radius", json={'zone_km': radius})