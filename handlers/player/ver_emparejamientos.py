from enum import Enum
from typing import Dict, List
from uuid import UUID
from .responder_al_emparejamiento import handle_player_response_match_callback
from model.telegram_bot import TelegramBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime as dt
from telebot.types import Message, CallbackQuery
from services.users_service import UsersService
from services.matches_service import MatchesService


class ReserveStatus(str, Enum):
    ASSIGNED = "assigned"
    SIMILAR = "similar"
    PROVISIONAL = "Provisional"
    INSIDE = "inside"
    OUTSIDE = "outside"
    REJECTED = "Rejected"


VIEW_PADDLE_MATCHUPS_COMMAND = "ver_emparejamientos"
PLAYER_MATCHES_STATUS = [ReserveStatus.ASSIGNED, ReserveStatus.INSIDE]
INLINE_KEYWORD_ROW_WIDTH = 2

users_service = UsersService()
match_service = MatchesService()


def filter_fn(call: CallbackQuery):
    return call.data.startswith(VIEW_PADDLE_MATCHUPS_COMMAND)


def generate_callback_string(data: str):
    return f"{VIEW_PADDLE_MATCHUPS_COMMAND}:{data}"


def parse_provisional_match(bot: TelegramBot, matchup: dict):
    public_id = matchup['public_id']
    court_id = matchup['court_name']
    # Nota: court_public_id existe, pero actualmente se usa court_name
    # en los endpoints de los micro-servicios
    date = dt.strptime(
        matchup['date'], "%Y-%m-%d").strftime(bot.language_manager.get('DATE_FMT'))
    time = dt.strptime(str(matchup['time']), "%H").strftime(
        bot.language_manager.get('TIME_FMT'))
    status = matchup.get('status', '-')
    match_players = matchup.get('match_players', [])
    return public_id, court_id, date, time, status, match_players


def matchups_keyboard(bot: TelegramBot, matchups: list):
    inline_markup = InlineKeyboardMarkup()
    for matchup in matchups:
        inline_markup.row(matchups_keyboard_line(bot, matchup))
    return inline_markup


def matchups_keyboard_line(bot: TelegramBot, matchup: dict):
    public_id, court_id, date, time, _, _ = parse_provisional_match(
        bot, matchup)

    button_text = f"{public_id} - {court_id} - {time} {date}"
    return InlineKeyboardButton(
        text=button_text,
        callback_data=generate_callback_string(public_id)
    )

def remove_inside_and_outside_buttons(button):
    callback_data = button.get("callback_data")
    inside = ReserveStatus.INSIDE.lower()
    outside = ReserveStatus.OUTSIDE.lower()
    
    if inside in callback_data or outside in callback_data:
        return False
    return True


def filter_buttons_view(buttons: List[Dict[str, str]], user_p_id: UUID, match_p_id: UUID):
    matches_service = MatchesService()
    response = matches_service.get_match_player(user_p_id, match_p_id)
    if not response:
        return buttons

    reserve = response.get('reserve', '')
    if reserve in [ReserveStatus.INSIDE.lower()]:
        return list(filter(remove_inside_and_outside_buttons, buttons))

    return buttons


def matchup_options_keyboard(bot: TelegramBot, user_public_id: UUID,  match_public_id: UUID):
    buttons = [
        {'text': '✅ Confirmar Partido', 'callback_data': generate_callback_string(f"inside:{match_public_id}")},
        {'text': '❌ Rechazar Partido', 'callback_data': generate_callback_string(f"outside:{match_public_id}")},
        {'text': '⬅', 'callback_data': generate_callback_string('back')}
    ]

    buttons = filter_buttons_view(buttons, user_public_id, match_public_id)

    return bot.ui.create_inline_keyboard(buttons=buttons, row_width=INLINE_KEYWORD_ROW_WIDTH)


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
    user_matches = match_service.get_user_matches(user_public_id)
    matches = user_matches.get("data") if user_matches else []
    return filter_matchups_by_players_status(matches, user_public_id)


def handle_matchups(message: Message, bot: TelegramBot):
    chat_id = message.chat.id
    user_public_id = get_user_public_id(chat_id)
    if not user_public_id:
        bot.send_message(chat_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    matches = validate_and_filter_matchups(user_public_id)

    if not matches:
        bot.reply_to(message, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    bot.send_message(message.chat.id, bot.language_manager.get(
        "MESSAGE_SEE_MATCHES"), reply_markup=matchups_keyboard(bot, matches))


def matchups_callback(call: CallbackQuery, bot: TelegramBot):
    is_confirmed = call.data.startswith(generate_callback_string('inside'))
    is_rejected = call.data.startswith(generate_callback_string('outside'))
    if call.data == generate_callback_string('back'):
        matchups_back_callback(call, bot)
    elif is_confirmed or is_rejected:
        handle_player_response_match_callback(call, bot)
    else:
        matchups_main_callback(call, bot)


def matchups_main_callback(call: CallbackQuery, bot: TelegramBot):
    telegram_id = call.from_user.id
    user_public_id = get_user_public_id(telegram_id)
    if not user_public_id:
        bot.send_message(telegram_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    callback_data = call.data
    match_public_id = callback_data.split(':')[-1]
    matches = validate_and_filter_matchups(user_public_id)

    if not matches:
        text_response = bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY")
        bot.reply_to(call.message, text_response)
        return

    selected_match = next(
        (match for match in matches if match["public_id"] == match_public_id), None)

    if not selected_match:
        bot.send_message(call.message.chat.id,
                         bot.language_manager.get("MESSAGE_MATCH_NOT_FOUND"))
        return

    public_id, court_id, date, time, status, match_players = parse_provisional_match(
        bot, selected_match)

    player_info = ""
    for i, player in enumerate(match_players, 1):
        user_data = users_service.get_user_by_id(user_public_id)
        player_info += f"\nJugador {i}: {user_data.get('name')}\n"
        player_info += f"Estado: {player['reserve']}\n"

    text = f"Establecimiento: {public_id}\n" \
           f"Cancha: {court_id}\n" \
           f"Dia: {date}\n" \
           f"Horario: {time}\n" \
           f"Estado: {status}\n" \
           f"\nJugadores:{player_info}"

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=matchup_options_keyboard(bot, user_public_id, public_id))


def matchups_back_callback(call: CallbackQuery, bot: TelegramBot):
    chat_id = call.message.chat.id
    user_public_id = get_user_public_id(chat_id)
    if not user_public_id:
        bot.send_message(chat_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    matches = validate_and_filter_matchups(user_public_id)

    if not matches:
        text_response = bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY")
        bot.reply_to(call.message, text_response)
        return

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=bot.language_manager.get("MESSAGE_SEE_MATCHES"),
        reply_markup=matchups_keyboard(bot, matches)
    )


def get_user_public_id(telegram_id):
    data = users_service.get_user_info(telegram_id)
    return data.get("data")[0].get("public_id") if data.get("data") else None
