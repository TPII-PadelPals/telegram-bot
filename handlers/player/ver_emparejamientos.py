from telebot import TeleBot
from telebot.types import Message
from utils.get_from_env import get_from_env_lang, get_from_env_api
import datetime
import pandas as pd


def handle_see_matches(message: Message, bot: TeleBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    api_conection = get_api()
    language = get_len()
    # text = message.text
    # obtengo los matches
    id_telegram = message.from_user.username
    matches = api_conection.get_matches(id_telegram)
    # caso sin emparejamiento
    if len(matches) == 0:
        text_response = language["MESSAGE_SEE_MATCHES_EMPTY"]
        bot.reply_to(message, text_response)
        return

    text_headers = [language['PLAYER'], language['COURT'],
                    language['DATE'], language['TIME']]
    df_matches = pd.DataFrame(columns=text_headers)

    # Cargar matches
    for match in matches:
        other_player = match["player_id_1"]
        if other_player == id_telegram:
            other_player = match["player_id_2"]
        court = str(match['court_name'])
        date = datetime.datetime.strptime(match['date'], "%Y-%m-%d")
        time = datetime.datetime.strptime(str(match['time']), "%H")
        df_matches.loc[len(df_matches)] = [other_player, court, date, time]

    # Ordenar por fecha y horas
    df_matches = df_matches.sort_values(
        by=[language['DATE'], language['TIME']], ignore_index=True)

    # Formatear fecha y hora
    df_matches[language['DATE']] = df_matches[language['DATE']].apply(
        lambda date: date.strftime(language['DATE_FMT']))
    df_matches[language['TIME']] = df_matches[language['TIME']].apply(
        lambda time: time.strftime(language['TIME_FMT']))

    # Ajustar ancho de las columnas
    df_matches.loc[-1] = text_headers
    df_matches.index += 1
    df_matches = df_matches.sort_index()
    for header in text_headers:
        col_width = df_matches[header].str.len().max()
        df_matches[header] = df_matches[header].apply(
            lambda v: v.ljust(col_width))

    # Generar respuesta
    text_response = "```\n"
    text_response += language["MESSAGE_SEE_MATCHES"]
    for _, row in df_matches.iterrows():
        text_response += language['SEE_MATCHES_SEPARATOR'].join(row) + "\n"
    text_response += "```"
    try:
        bot.reply_to(message, text_response, parse_mode="MarkdownV2")
    except:
        bot.reply_to(message, text_response)
