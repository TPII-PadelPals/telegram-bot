from enum import Enum
from model.telegram_bot import TelegramBot
from datetime import datetime as dt

from services.business_service import BusinessService
from services.matches_service import MatchesService

VIEW_PADDLE_MATCHUPS_COMMAND = "ver_emparejamientos"


class MatchupAction(str):
    # It has to be limited to one Byte and so one character
    ALL = "A"
    ONE = "O"
    PAY = "P"
    CONFIRM = "C"
    REJECT = "R"


class ReserveStatus(str, Enum):
    ASSIGNED = "assigned"
    SIMILAR = "similar"
    INSIDE = "inside"
    OUTSIDE = "outside"
    # The following states might be deprecated in the future
    PROVISIONAL = "Provisional"
    REJECTED = "Rejected"


PLAYER_MATCHES_STATUS = [ReserveStatus.ASSIGNED, ReserveStatus.INSIDE]


def generate_callback_string(data: str):
    return f"{VIEW_PADDLE_MATCHUPS_COMMAND}:{data}"


def check_players_has_required_status(matchup: dict, user_public_id: str | None):
    """ Check if any player in the match has a status in PLAYER_MATCHES_STATUS and if the user is in the match """
    match_players = matchup.get('match_players', [])

    return_players = []
    includes_user = False

    for player in match_players:
        status = player.get('reserve')
        if status in PLAYER_MATCHES_STATUS:
            return_players.append(player)

            if player.get('user_public_id') == user_public_id:
                includes_user = True

    return includes_user, return_players


def filter_matchups_by_players_status(matchups: list, user_public_id: str | None):
    """ Filter matchups by player status using check_players_has_required_status"""
    matches_selected = []
    for match in matchups:
        has_user, players = check_players_has_required_status(
            match, user_public_id)
        if has_user and players:
            match['match_players'] = players
            matches_selected.append(match)
    return matches_selected


def validate_and_filter_matchups(user_public_id: str | None):
    match_service = MatchesService()
    user_matches = match_service.get_user_matches(user_public_id)
    matches = user_matches.get("data") if user_matches else []
    return filter_matchups_by_players_status(matches, user_public_id)


def format_time(bot: TelegramBot, time: int):
    return dt.strptime(str(time), "%H").strftime(
        bot.language_manager.get('TIME_FMT'))


def parse_provisional_match(bot: TelegramBot, matchup: dict):
    public_id = matchup['public_id']
    business_name = matchup['business_name']
    business_location = matchup['business_location']
    court_id = matchup['court_name']
    # Nota: court_public_id existe, pero actualmente se usa court_name
    # en los endpoints de los micro-servicios
    date = dt.strptime(
        matchup['date'], "%Y-%m-%d").strftime(bot.language_manager.get('DATE_FMT'))
    time = format_time(bot, matchup["time"])
    status = matchup.get('status', '-')
    match_players = matchup.get('match_players', [])
    return public_id, business_name, court_id, date, time, status, match_players, business_location


def add_business_info(matches: list[dict[str, str]]):
    business_service = BusinessService()
    business_matches = {}
    for match in matches:
        business_public_id = match["business_public_id"]
        matches_for_business = business_matches.get(business_public_id)
        if matches_for_business is not None:
            matches_for_business.append(match)
        else:
            business_matches[business_public_id] = [match]
    for business_public_id, matches in business_matches.items():
        business = business_service.get_business(business_public_id)
        for match in matches:
            match["business_name"] = business["name"]
            match["business_location"] = business["location"]
