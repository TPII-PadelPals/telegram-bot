from telebot import TeleBot
from telebot.types import Message

from utils.get_from_env import get_from_env_lang, get_from_env_api

COL_WIDTH = 20

DEFAULT_PLAYER = 'francoMartinDiMaria'

def handle_see_matches(message: Message, bot: TeleBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    api_conection = get_api()
    language = get_len()
    # text = message.text
    # obtengo los matches
    id_telegram = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER

    matches = api_conection.get_matches(id_telegram)
    # caso sin emparejamiento
    if len(matches) == 0:
        text_response = language["MESSAGE_SEE_MATCHES_EMPTY"]
        bot.reply_to(message, text_response)
        return

    players = [language['PLAYER']]
    courts = [language['COURT']]
    times = [language['TIME']]
    for match in matches:
        other_player = match["player_id_1"]
        if other_player == id_telegram:
            other_player = match["player_id_2"]
        players.append(str(other_player))
        courts.append(str(match['paddle_court_name']))
        times.append(str(language['TIME_NAMES']
                     [str(match['time_availability'])]))

    players_col_width = max([len(player) for player in players])
    courts_col_width = max([len(court) for court in courts])
    times_col_width = max([len(time) for time in times])

    text_response = "```\n"
    text_response += language["MESSAGE_SEE_MATCHES"]
    for player, court, time in zip(players, courts, times):
        text_response += language['SEE_MATCHES_SEPARATOR'].join([
            f"{player.ljust(players_col_width)}",
            f"{court.ljust(courts_col_width)}",
            f"{time.ljust(times_col_width)}",
        ]) + "\n"
    text_response += "```"

    bot.reply_to(message, text_response, parse_mode="MarkdownV2")
