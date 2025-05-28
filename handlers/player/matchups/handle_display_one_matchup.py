import logging
from typing import Dict, List
from uuid import UUID
from handlers.player.matchups.utils import MatchupAction, ReserveStatus, format_time, generate_callback_string, \
    parse_provisional_match, validate_and_filter_matchups, add_business_info
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.matches_service import MatchesService
from services.users_service import UsersService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

INLINE_KEYWORD_ROW_WIDTH = 2


def remove_inside_and_outside_buttons(button):
    callback_data = button.get("callback_data")

    if MatchupAction.PAY in callback_data or MatchupAction.REJECT in callback_data:
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
            f"{MatchupAction.PAY}:{match_public_id}")},
        {'text': '❌ Rechazar Partido', 'callback_data': generate_callback_string(
            f"{MatchupAction.REJECT}:{match_public_id}")},
        {'text': '⬅', 'callback_data': generate_callback_string(
            MatchupAction.ALL)}
    ]

    buttons = filter_buttons_view(buttons, user_public_id, match_public_id)

    return bot.ui.create_inline_keyboard(buttons=buttons, row_width=INLINE_KEYWORD_ROW_WIDTH)


def handle_display_one_matchup_callback(call: CallbackQuery, bot: TelegramBot):
    users_service = UsersService()

    telegram_id = call.from_user.id
    users = users_service.get_user_info(telegram_id)
    if not users:
        bot.send_message(telegram_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return
    user = users[0]

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

    add_business_info([selected_match])
    public_id, business_name, court_id, date, time, status, match_players, business_location = parse_provisional_match(
        bot, selected_match)

    start_time = int(time.split(":")[0])
    end_time = start_time + 1
    start_time = format_time(bot, start_time)
    end_time = format_time(bot, end_time)

    time = f"{start_time} - {end_time} hs"

    reserve_status = bot.language_manager.get("RESERVE_STATUS")
    player_info = ""
    for i, player in enumerate(match_players, 1):
        _user = users_service.get_user_by_id(player["user_public_id"])
        player_info += f"\nJugador {i}: {_user.name}\n"
        player_info += f"Estado: {reserve_status[player['reserve']]}\n"

    text = f"Establecimiento: {business_name}\n" \
           f"Cancha: {court_id}\n" \
           f"Dirección: {business_location}\n" \
           f"Fecha: {date}\n" \
           f"Horario: {time}\n" \
           f"Estado: {status}\n" \
           f"\nJugadores:{player_info}"

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=matchup_options_keyboard(bot, user.public_id, public_id)
    )
