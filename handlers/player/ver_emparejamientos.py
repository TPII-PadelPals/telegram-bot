from services.match_service import MatchService
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.get_from_env import get_from_env_lang
from datetime import datetime as dt
from telebot.types import Message, CallbackQuery
from telebot import types, TeleBot


DEFAULT_PLAYER = 'francoMartinDiMaria'
VIEW_PADDLE_MATCHUPS_COMMAND = "ver_emparejamientos"

language = get_from_env_lang()

def filter_fn(call: CallbackQuery):
    return call.data.startswith(VIEW_PADDLE_MATCHUPS_COMMAND)

def generate_callback_string(data: str):
    return f"{VIEW_PADDLE_MATCHUPS_COMMAND}:{data}"

def parse_provisional_match(player_nickname, matchup: dict):
    other_player = matchup["player_id_1"] if matchup["player_id_1"] != player_nickname else matchup["player_id_2"]
    court_name = matchup['court_name']
    court_id = matchup['court_id']
    date = dt.strptime(matchup['date'], "%Y-%m-%d").strftime(language['DATE_FMT'])
    time = dt.strptime(str(matchup['time']), "%H").strftime(language['TIME_FMT'])
    return other_player, court_id, court_name, date, time

def matchups_keyboard(player_nickname, matchups: list):
    inline_markup = InlineKeyboardMarkup()
    for matchup in matchups:
        inline_markup.row(matchups_keyboard_line(player_nickname, matchup))
    return inline_markup

def matchups_keyboard_line(player_nickname, matchup: dict):
    other_player, _, court_name, date, time = parse_provisional_match(player_nickname, matchup)

    button_text = f"{other_player} - {court_name} - {time} {date}"
    return InlineKeyboardButton(
        text=button_text,
        callback_data=generate_callback_string(matchup["id"])
    )

def matchups_back_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text='⬅',
                    callback_data=generate_callback_string('back')
                )
            ]
        ]
    )

def handle_matchups(message: Message, bot: TeleBot):

    id_telegram = message.from_user.username if message.from_user.username else DEFAULT_PLAYER

    match_service = MatchService()
    matches = match_service.get_provisional_matches({'player_id_1': id_telegram})

    if not matches:
        text_response = language["MESSAGE_SEE_MATCHES_EMPTY"]
        bot.reply_to(message, text_response)
        return

    bot.send_message(message.chat.id, language["MESSAGE_SEE_MATCHES"], reply_markup=matchups_keyboard(id_telegram, matches))


def matchups_callback(call: types.CallbackQuery, bot: TeleBot):
    if call.data == generate_callback_string('back'):
        matchups_back_callback(call, bot)
    else:
        matchups_main_callback(call, bot)


def matchups_main_callback(call: types.CallbackQuery, bot: TeleBot):
    callback_data: dict = call.data
    id_telegram = call.message.chat.username if call.message.chat.username else DEFAULT_PLAYER
    matchup_id = int(callback_data.split(':')[-1])
    match_service = MatchService()
    get_provisional_matches = match_service.get_provisional_matches({'id': matchup_id})
    provisional_match = get_provisional_matches[0]

    other_player, court_id, court_name, date, time = parse_provisional_match(id_telegram, provisional_match)

    text = f"Contrincante: {other_player}\n" \
           f"Establecimiento: {court_name}\n" \
           f"Cancha: {court_id}\n" \
           f"Horario: {time}\n" \
           f"Dia: {date}\n"

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=matchups_back_keyboard())
    

def matchups_back_callback(call: types.CallbackQuery, bot: TeleBot):
    id_telegram = call.message.chat.username if call.message.chat.username else DEFAULT_PLAYER

    match_service = MatchService()
    matches = match_service.get_provisional_matches({'player_id_1': id_telegram})

    if not matches:
        text_response = language["MESSAGE_SEE_MATCHES_EMPTY"]
        bot.reply_to(call.message, text_response)
        return
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=language["MESSAGE_SEE_MATCHES"], reply_markup=matchups_keyboard(id_telegram, matches))
                        
