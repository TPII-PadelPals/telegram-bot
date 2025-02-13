import unittest
from unittest.mock import MagicMock

from handlers.user.start import handle_start, handle_callback_query
from telebot.types import CallbackQuery, Message
from requests.exceptions import ConnectionError


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


    def test_start_with_users_service_disconnected_replies_error(self):
        users_service_mock = MagicMock()
        users_service_mock.get_user_info = MagicMock(
            side_effect=ConnectionError())

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


    def test_start_with_user_not_registered_asks_login(self):
        users = {
            "data": [],
            "count": 0
        }

        users_service_mock = MagicMock()
        users_service_mock.get_user_info = MagicMock(return_value=users)

        handle_start(self.message, self.bot, users_service_mock)

        assert self.bot.reply_to.call_args.args[
            1] == "Bienvenido a PaddlePals! Por favor seleccione un método de registro:"


    def test_handle_callback_query_start_user_pass_replies_error(self):
        self.call.data = "start_user_pass"
        users_service_mock = MagicMock()

        handle_callback_query(self.call, self.bot, users_service_mock)

        self.bot.reply_to.assert_called_once_with(
            self.call.message,
            "Esta opción no esta disponible actualmente. Por favor, intenta de nuevo más tarde."
        )


if __name__ == '__main__':
    unittest.main()
