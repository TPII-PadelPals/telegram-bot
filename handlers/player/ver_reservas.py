from telebot import TeleBot
from telebot.types import Message

from utils.get_from_env import get_from_env_lang, get_from_env_api

COL_WIDTH = 20

def handle_see_reserves(message: Message, bot: TeleBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    api_conection = get_api()
    language = get_len()
    # obtengo los matches
    id_telegram = message.from_user.username
    reserves = api_conection.get_reserves(id_telegram)
    # caso sin reservas
    if len(reserves) == 0:
        text_response = language["MESSAGE_SEE_RESERVES_EMPTY"]
        bot.reply_to(message, text_response)
        return

    players = [language['PLAYER']]
    courts = [language['COURT']]
    dates = [language['DATE']]
    times = [language['TIME']]
    for reservation in reserves:
        other_player = reservation["player_id_1"]
        if other_player == id_telegram:
            other_player = reservation["player_id_2"]
        players.append(str(other_player))
        courts.append(str(reservation['paddle_court_name']))
        dates.append(str(reservation['begin_date_time']))
        times.append(str(reservation['time_availability']))

    players_col_width = max([len(player) for player in players])
    courts_col_width = max([len(court) for court in courts])
    date_col_width = max([len(date) for date in dates])
    times_col_width = max([len(time) for time in times])

    text_response = "```\n"
    text_response += language["MESSAGE_SEE_RESERVES"]
    for player, court, date, time in zip(players, courts, dates, times):
        text_response += language['SEE_MATCHES_SEPARATOR'].join([
            f"{player.ljust(players_col_width)}",
            f"{court.ljust(courts_col_width)}",
            f"{date.ljust(date_col_width)}",
            f"{time.ljust(times_col_width)}",
        ]) + "\n"
    text_response += "```"
    try:
        bot.reply_to(message, text_response, parse_mode="MarkdownV2")
    except:
        bot.reply_to(message, text_response)
