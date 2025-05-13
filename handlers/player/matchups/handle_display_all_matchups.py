from handlers.player.matchups.utils import generate_callback_string, get_user_public_id, parse_provisional_match, validate_and_filter_matchups
from model.telegram_bot import TelegramBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


def matchups_keyboard_line(bot: TelegramBot, matchup: dict):
    public_id, court_id, date, time, _, _ = parse_provisional_match(
        bot, matchup)

    button_text = f"{public_id} - {court_id} - {time} {date}"
    return InlineKeyboardButton(
        text=button_text,
        callback_data=generate_callback_string(public_id)
    )


def matchups_keyboard(bot: TelegramBot, matchups: list):
    inline_markup = InlineKeyboardMarkup()
    for matchup in matchups:
        inline_markup.row(matchups_keyboard_line(bot, matchup))
    return inline_markup


def display_all_matchups(bot: TelegramBot, chat_id: int, message_id: int | None = None):
    user_public_id = get_user_public_id(chat_id)
    if not user_public_id:
        bot.send_message(chat_id, bot.language_manager.get(
            "MESSAGE_SEE_MATCHES_EMPTY"))
        return

    matches = validate_and_filter_matchups(user_public_id)

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
            chat_id,
            bot.language_manager.get("MESSAGE_SEE_MATCHES"),
            reply_markup=matchups_keyboard(bot, matches)
        )


def matchups_back_callback(call: CallbackQuery, bot: TelegramBot):
    display_all_matchups(bot, call.message.chat.id, call.message.message_id)
