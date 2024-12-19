from model.telegram_bot import TelegramBot
from telebot.types import Message

from utils.get_from_env import get_from_env_lang, get_from_env_api

COL_WIDTH = 30

def handle_see_reserves(message: Message, bot: TelegramBot, get_api=get_from_env_api, get_len=get_from_env_lang):
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
    accepts_1 = [language['I_ACCEPT']]
    accepts_2 = [language['ACCEPT']]
    for reservation in reserves:
        # reservation = reservation["Reserves"]
        other_player = reservation["player_id_1"]
        if other_player == id_telegram:
            other_player = reservation["player_id_2"]
            other_accept = reservation["player_id_2_response_accept"]
            i_accept = reservation["player_id_1_response_accept"]
        else:
            other_accept = reservation["player_id_1_response_accept"]
            i_accept = reservation["player_id_2_response_accept"]
        players.append(str(other_player))
        courts.append(str(reservation['paddle_court_name']))
        dates.append(str(reservation['begin_date_time']))
        times.append(str(reservation['time_availability']))
        accepts_1.append(str(i_accept))
        accepts_2.append(str(other_accept))

    players_col_width = max([len(player) for player in players])
    courts_col_width = max([len(court) for court in courts])
    date_col_width = max([len(date) for date in dates])
    times_col_width = max([len(time) for time in times])
    accepts_1_col_width = max([len(time) for time in times])
    accepts_2_col_width = max([len(time) for time in times])

    text_response = "```\n"
    text_response += language["MESSAGE_SEE_RESERVES"]
    for player, court, date, time, accept_1, accept_2 in zip(players, courts, dates, times, accepts_1, accepts_2):
        text_response += language['SEE_MATCHES_SEPARATOR'].join([
            f"{player.ljust(players_col_width)}",
            f"{court.ljust(courts_col_width)}",
            f"{date.ljust(date_col_width)}",
            f"{time.ljust(times_col_width)}",
            f"{accept_1.ljust(accepts_1_col_width)}",
            f"{accept_2.ljust(accepts_2_col_width)}",
        ]) + "\n"
    text_response += "```"
    try:
        bot.reply_to(message, text_response, parse_mode="MarkdownV2")
    except:
        bot.reply_to(message, text_response)
