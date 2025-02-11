from .base_service import BaseService


class PlayerServiceBackEnd(BaseService):

    def update_location(self, player_nickname: str, streetname: str):
        """Send location to backend to get coordinates."""
        return self.post(f"/player/{player_nickname}/location", json={'streetname': streetname})


    def update_radius(self, player_nickname: str, location: str, radius: int):
        """Send location radius to backend."""
        return self.post(f"/player/{player_nickname}/location/radius", json={'zone_km': radius})