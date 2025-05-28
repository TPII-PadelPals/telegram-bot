import locale
from enum import Enum
from model.telegram_bot import TelegramBot
from datetime import datetime as dt

from services.business_service import BusinessService
from services.matches_service import MatchesService

locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')

VIEW_PADDLE_MATCHUPS_COMMAND = "ver_emparejamientos"
MAX_PLAYERS = 4


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


def format_price_abbreviated(amount):
    amount = float(amount)
    abs_amount = abs(amount)
    sign = "-" if amount < 0 else ""

    if abs_amount >= 1_000_000:
        formatted = f"{abs_amount / 1_000_000:.1f}M"
    elif abs_amount >= 1_000:
        formatted = f"{abs_amount / 1_000:.1f}K"
    else:
        formatted = f"{abs_amount:.2f}".replace(".", ",")

    return f"{sign}~${formatted}"


def format_price_complete(amount):
    amount = float(amount)
    return locale.currency(float(amount), grouping=True)


def parse_provisional_match(bot: TelegramBot, matchup: dict):
    matchup['date'] = dt.strptime(
        matchup['date'], "%Y-%m-%d").strftime(bot.language_manager.get('DATE_FMT'))
    matchup['time'] = format_time(bot, matchup["time"])
    matchup['price_per_hour'] = str(
        float(matchup['price_per_hour']) / MAX_PLAYERS)

    return matchup


def add_court_info(matches: list[dict[str, str]]):
    business_service = BusinessService()
    court_matches = {}
    for match in matches:
        court_public_id = match["court_public_id"]
        if court_public_id in court_matches:
            court_matches[court_public_id].append(match)
        else:
            court_matches[court_public_id] = [match]
    for court_public_id, matches in court_matches.items():
        court = business_service.get_court(court_public_id)
        for match in matches:
            match["business_name"] = court["business_name"]
            match["business_location"] = court["business_location"]
            match["court_name"] = court["name"]
            match["price_per_hour"] = court["price_per_hour"]
