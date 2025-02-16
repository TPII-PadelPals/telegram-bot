import unittest
from unittest.mock import MagicMock
from telebot.types import Message

from handlers.player import handle_configure_strokes


class TestMatchupsMainCallback(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.bot.language_manager = {
            "ALL": "todos",
            "MESSAGE_STROKES_UPDATED": "messajeInit ",
            "NUMBER_FOR_STROKE": {
                "1": "serve",
                "2": "forehand_ground",
                "3": "background_ground",
                "4": "forehand_back_wall",
                "5": "backhand_back_wall",
                "6": "forehand_side_wall",
                "7": "backhand_side_wall",
                "8": "forehand_double_walls",
                "9": "backhand_double_walls",
                "10": "forehand_counter_wall",
                "11": "backhand_counter_wall",
                "12": "forehand_volley",
                "13": "backhand_volley",
                "14": "lob",
                "15": "smash",
                "16": "bandeja"
            },
            "SENDER_POSITION_STROKE_HABILITY": {
                "principiante": 0,
                "intermedio": 1,
                "avanzado": 2
            },
            "STROKE_HABILITY": ["principiante", "intermedio", "avanzado"],
            "MESSAGE_INVALID_VALUE": "MESSAGE_INVALID_VALUE"
        }
        self.bot.reply_to = MagicMock()

        self.result_strokes = MagicMock()
        self.result_strokes.get = MagicMock(return_value="123")

        self.player_service = MagicMock()
        self.player_service.update_strokes = MagicMock(return_value=self.result_strokes)

        self.get_api = MagicMock(return_value=self.player_service)

        self.user_service_api = MagicMock()
        self.user_service_api.get_user_info = MagicMock(return_value={"public_id": 123})

        self.user_service = MagicMock(return_value=self.user_service_api)

        self.message = MagicMock(spec=Message)
        self.message.from_user = MagicMock()
        self.message.from_user.id = 12345


    def test_handle_configure_strokes_all_advance(self):
        self.message.text = "/configurar_golpes todos avanzado"
        # test
        handle_configure_strokes(self.message, self.bot, get_api=self.get_api, user_service=self.user_service)
        # assert
        self.bot.reply_to.assert_called_once()


    def test_handle_configure_strokes_n_valid_advance(self):
        self.message.text = "/configurar_golpes 1,5,6,16 avanzado"
        expected_respond = "messajeInit avanzado\nserve\nbackhand_back_wall\nforehand_side_wall\nbandeja\n"
        # test
        handle_configure_strokes(self.message, self.bot, get_api=self.get_api, user_service=self.user_service)
        # assert
        self.bot.reply_to.assert_called_once_with(self.message, expected_respond)


    def test_handle_configure_strokes_n_invalid_advance(self):
        self.message.text = "/configurar_golpes 18,20 avanzado"
        expected_respond = "MESSAGE_INVALID_VALUE"
        # test
        handle_configure_strokes(self.message, self.bot, get_api=self.get_api, user_service=self.user_service)
        # assert
        self.bot.reply_to.assert_called_once_with(self.message, expected_respond)