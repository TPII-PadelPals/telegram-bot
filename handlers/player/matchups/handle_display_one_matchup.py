from typing import Dict, List
from uuid import UUID
from handlers.player.matchups.utils import ReserveStatus, generate_callback_string, parse_provisional_match, validate_and_filter_matchups
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.matches_service import MatchesService
from services.users_service import UsersService

users_service = UsersService()
match_service = MatchesService()

INLINE_KEYWORD_ROW_WIDTH = 2


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
        {'text': '✅ Confirmar Partido', 'callback_data': generate_callback_string(
            f"pay:{match_public_id}")},
        {'text': '❌ Rechazar Partido', 'callback_data': generate_callback_string(
            f"outside:{match_public_id}")},
        {'text': '⬅', 'callback_data': generate_callback_string('back')}
    ]

    buttons = filter_buttons_view(buttons, user_public_id, match_public_id)

    return bot.ui.create_inline_keyboard(buttons=buttons, row_width=INLINE_KEYWORD_ROW_WIDTH)


def matchups_main_callback(call: CallbackQuery, bot: TelegramBot):
    telegram_id = call.from_user.id
    user = users_service.get_user_info(telegram_id)
    if not user.public_id:
        bot.send_message(telegram_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    callback_data = call.data
    match_public_id = callback_data.split(':')[-1]
    matches = validate_and_filter_matchups(user.public_id)

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
        user_data = users_service.get_user_by_id(user.public_id)
        player_info += f"\nJugador {i}: {user_data.get('name')}\n"
        player_info += f"Estado: {player['reserve']}\n"

    text = f"Establecimiento: {public_id}\n" \
           f"Cancha: {court_id}\n" \
           f"Dia: {date}\n" \
           f"Horario: {time}\n" \
           f"Estado: {status}\n" \
           f"\nJugadores:{player_info}"

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=matchup_options_keyboard(bot, user.public_id, public_id))
