from typing import Any
from uuid import UUID
from .base_service import BaseService
from core.config import settings


# class MatchPlayer:
#     def __init__(
#         self,
#         match_public_id: str = "",
#         user_public_id: str = "",
#         reserve: str = "",
#         pay_url: str | None = None
#     ):
#         self.match_public_id = str(match_public_id)
#         self.user_public_id = str(user_public_id)
#         self.reserve = str(reserve)
#         self.pay_url = pay_url


# class Match:
#     def __init__(
#         self,
#         public_id: str = "",
#         court_public_id: str = "",
#         court_name: str = "",
#         date: str = "",
#         time: int = 0,
#         status: str = "",
#         match_players: list[Any] = []
#     ):
#         self.public_id = str(public_id)
#         self.court_public_id = str(court_public_id)
#         self.court_name = str(court_name)
#         self.date: str = str(date)
#         self.time: int = int(time)
#         self.status: str = str(status)
#         self.players = [MatchPlayer(**player_data)
#                         for player_data in match_players]


# def parse_provisional_match(bot: TelegramBot, matchup: dict):
#     public_id = matchup['public_id']
#     court_id = matchup['court_name']
#     # Nota: court_public_id existe, pero actualmente se usa court_name
#     # en los endpoints de los micro-servicios
#     date = dt.strptime(
#         matchup['date'], "%Y-%m-%d").strftime(bot.language_manager.get('DATE_FMT'))
#     time = dt.strptime(str(matchup['time']), "%H").strftime(
#         bot.language_manager.get('TIME_FMT'))
#     status = matchup.get('status', '-')
#     match_players = matchup.get('match_players', [])
#     return public_id, court_id, date, time, status, match_players


class MatchesService(BaseService):

    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.MATCHES_SERVICE_HOST,
                           settings.MATCHES_SERVICE_PORT)
        self.set_prefix_url("/api/v1")
        self.x_api_key_header = {"x-api-key": settings.MATCHES_SERVICE_API_KEY}

    def get_user_matches(self, user_public_id: UUID):
        """Get provisional_match."""
        # content = self.get(f"/players/{user_public_id}/matches/")
        # matches = [Match(**match_data) for match_data in content["data"]]
        # return matches
        return self.get(f"/players/{user_public_id}/matches/")

    def get_match_player(self, user_public_id: UUID, match_public_id: UUID):
        """Get match player"""
        return self.get(f"/matches/{match_public_id}/players/{user_public_id}")

    def update_match_player_status(self, user_public_id: UUID, match_public_id: UUID, status: str):
        """Patch player status on a match."""
        status_json = {
            "reserve": status,
        }
        return self.patch(f"/matches/{match_public_id}/players/{user_public_id}/", json=status_json)
