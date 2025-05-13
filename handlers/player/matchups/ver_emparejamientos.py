
from handlers.player.matchups.handle_display_all_matchups import display_all_matchups, matchups_back_callback
from handlers.player.matchups.handle_display_one_matchup import matchups_main_callback
from handlers.player.matchups.handle_reply_one_matchup import handle_player_response_match_callback
from handlers.player.matchups.utils import VIEW_PADDLE_MATCHUPS_COMMAND, generate_callback_string
from handlers.player.ver_emparejamientos import handle_match_confirmation_step
from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery


def filter_fn(call: CallbackQuery):
    return call.data.startswith(VIEW_PADDLE_MATCHUPS_COMMAND)


def handle_matchups(message: Message, bot: TelegramBot):
    display_all_matchups(bot, message.chat.id)  # message.message_id


# Switch callbacks
def matchups_callback(call: CallbackQuery, bot: TelegramBot):
    data = call.data

    if data == generate_callback_string('back'):
        matchups_back_callback(call, bot)

    elif data.startswith(generate_callback_string('pay')):
        handle_match_confirmation_step(call, bot)

    elif (data.startswith(generate_callback_string('inside')) or
          data.startswith(generate_callback_string('outside'))):
        handle_player_response_match_callback(call, bot)

    else:
        matchups_main_callback(call, bot)
