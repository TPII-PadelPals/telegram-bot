from handlers.player.matchups.utils import MatchupAction, format_price_abbreviated, generate_callback_string, parse_provisional_match, \
    validate_and_filter_matchups, add_court_info
from model.telegram_bot import TelegramBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from services.users_service import UsersService


MAX_BUSINESS_LEN = 20
MAX_COURT_LEN = 10
TRUNCATE_SYMBOL = "..."


def truncate_with_symbol(text: str, max_len: int, symbol: str) -> str:

    return text if len(text) <= max_len else text[:max_len - len(symbol)] + symbol


def matchups_keyboard_line(bot: TelegramBot, matchup: dict):
    matchup = parse_provisional_match(
        bot, matchup)
    button_text_split = [
        truncate_with_symbol(
            matchup['business_name'], MAX_BUSINESS_LEN, TRUNCATE_SYMBOL),
        truncate_with_symbol(matchup['court_name'],
                             MAX_COURT_LEN, TRUNCATE_SYMBOL),
        f"{matchup['date']}",
        f"{matchup['time']} hs",
        format_price_abbreviated(matchup['price_per_hour'])
    ]
    button_text = " | ".join(button_text_split)
    return InlineKeyboardButton(
        text=button_text,
        callback_data=generate_callback_string(
            f"{MatchupAction.ONE}:{matchup['public_id']}")
    )


def matchups_keyboard(bot: TelegramBot, matchups: list):
    inline_markup = InlineKeyboardMarkup()
    add_court_info(matchups)
    for matchup in matchups:
        inline_markup.row(matchups_keyboard_line(bot, matchup))
    return inline_markup


def display_all_matchups(bot: TelegramBot, chat_id: int, message_id: int | None = None):
    users_service = UsersService()

    users = users_service.get_user_info(chat_id)
    if not users:
        bot.send_message(chat_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return
    user = users[0]

    matches = validate_and_filter_matchups(user.public_id)

    if not matches:
        bot.send_message(chat_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=bot.language_manager.get("MESSAGE_SEE_MATCHES"),
            reply_markup=matchups_keyboard(bot, matches)
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=bot.language_manager.get("MESSAGE_SEE_MATCHES"),
            reply_markup=matchups_keyboard(bot, matches),
        )


def handle_display_all_matchups_callback(call: CallbackQuery, bot: TelegramBot):
    display_all_matchups(bot, call.message.chat.id, call.message.message_id)
