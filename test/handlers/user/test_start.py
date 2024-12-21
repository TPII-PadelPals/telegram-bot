import unittest
from unittest.mock import MagicMock
from telebot.types import CallbackQuery, Message
from utils.get_from_env import get_from_env_lang
# , ask_login_method, handle_callback_query
from handlers.user.start import handle_start
language = get_from_env_lang()


class TestHandleStart(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()
        self.message = MagicMock(spec=Message)
        self.message.chat = MagicMock()
        self.message.chat.id = 12345
        self.message.from_user = MagicMock()
        self.message.from_user.username = "test_user"
        self.call = MagicMock(spec=CallbackQuery)
        self.call.message = MagicMock(spec=Message)
        self.call.message.chat = MagicMock()
        self.call.message.chat.id = 12345
        self.call.message.message_id = 67890
        self.call.message.chat.username = "test_user"

    def test_start_with_user_service_disconnected_replies_error(self):
        users_service_mock = MagicMock()
        users_service_mock.get_user_info = MagicMock(return_value=None)

        handle_start(self.message, self.bot, users_service_mock)

        self.bot.reply_to.assert_called_once_with(
            self.message, "Ha ocurrido un error. Por favor, intenta de nuevo más tarde.")

    def test_start_with_user_already_registered_replies_welcome(self):
        user = {"name": "Name Surname"}
        users = {
            "data": [user],
            "count": 1
        }

        users_service_mock = MagicMock()
        users_service_mock.get_user_info = MagicMock(return_value=users)

        handle_start(self.message, self.bot, users_service_mock)

        self.bot.reply_to.assert_called_once_with(
            self.message, f"Bienvenido de nuevo, {user['name']}!")


if __name__ == '__main__':
    unittest.main()
