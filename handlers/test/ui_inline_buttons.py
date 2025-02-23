from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery

import logging

logging.basicConfig(level=logging.INFO)
loger = logging.getLogger(__name__)

COMMAND = "ui_inline_buttons"

def filter_fn(call: CallbackQuery):
    return call.data.startswith(COMMAND)

def generate_callback_string(data: str):
    return f"{COMMAND}:{data}"

def handle_configure_ui_inline_buttons(message: Message, bot: TelegramBot):

    buttons = [
        {'text': '🍕 Pizza - $10', 'callback_data': generate_callback_string('order_pizza')},
        {'text': '🍔 Burger - $8', 'callback_data': generate_callback_string('order_burger')},
        {'text': '🥗 Salad - $6', 'callback_data': generate_callback_string('order_salad')}
    ]
    
    menu = bot.ui.create_inline_keyboard(buttons, row_width=2)

    bot.reply_to(message, "Welcome to our Restaurant Bot! How can I help you today?", reply_markup=menu)
    loger.info("Se ha configurado ui_inline_buttons")


def ui_inline_buttons_callback(call: CallbackQuery, bot: TelegramBot):
    if call.data.startswith(generate_callback_string('order_')):
        handle_order(call, bot)
    else:
        handle_confirm(call, bot)


def handle_order(call: CallbackQuery, bot: TelegramBot):
    action = call.data.split(':')[1]
    item =action.split('_')[1]
    
    confirm_buttons = [
        {'text': '✅ Add to Cart', 'callback_data': generate_callback_string(f'confirm_{item}')}
    ]
    
    confirm_keyboard = bot.ui.create_inline_keyboard(confirm_buttons)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Add {item.capitalize()} to your cart?", reply_markup=confirm_keyboard)

def handle_confirm(call: CallbackQuery, bot: TelegramBot):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Pedido confirmado")