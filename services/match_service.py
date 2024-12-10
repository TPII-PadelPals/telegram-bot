from .base_service import BaseService


class MatchService(BaseService):

    def get_provisional_matches(self, match_data: dict):
        """Get provisional_match."""
        return self.get("/provisional_match", params=match_data)
