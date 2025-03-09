import unittest
from unittest.mock import MagicMock, patch
from telebot.types import Message, CallbackQuery

from handlers.player.configurar_golpes import (
    handle_configure_strokes,
    strokes_callback,
    skill_level_callback,
    show_strokes_list_callback
)


class TestConfigurarGolpes(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.bot.language_manager = MagicMock()
        self.bot.language_manager.get = MagicMock(side_effect=self._mock_language_get)

        self.bot.ui = MagicMock()
        self.bot.ui.create_inline_keyboard = MagicMock(return_value="mock_markup")

        self.bot.send_message = MagicMock()
        self.bot.edit_message_text = MagicMock()
        self.bot.answer_callback_query = MagicMock()

        self.result_strokes = MagicMock()
        self.result_strokes.get = MagicMock(return_value="123")

        self.player_service = MagicMock()
        self.player_service.update_strokes = MagicMock(
            return_value={"user_public_id": "123"}
        )

        self.get_api = MagicMock(return_value=self.player_service)

        self.user_service_api = MagicMock()
        self.user_service_api.get_user_info = MagicMock(
            return_value={"data": [{"public_id": "123"}]}
        )

        self.user_service = MagicMock(return_value=self.user_service_api)

        self.message = MagicMock()
        self.message.chat = MagicMock()
        self.message.chat.id = 12345

        self.call = MagicMock()
        self.call.id = "call123"
        self.call.message = MagicMock()
        self.call.message.chat = MagicMock()
        self.call.message.chat.id = 12345
        self.call.message.message_id = 67890
        self.call.from_user = MagicMock()
        self.call.from_user.id = 54321
        self.call.data = "configurar_golpes:command:data"

    def _mock_language_get(self, key, *args, **kwargs):
        language_map = {
            "SELECT_STROKE_MESSAGE": "Selecciona un golpe para configurar:",
            "SELECT_SKILL_LEVEL_FOR": "Selecciona tu nivel para: {stroke}",
            "ALL_STROKES": "Todos los golpes",
            "STROKES_NAMES": {
                "1": "Saque",
                "2": "Fondos de derecha",
                "3": "Fondos de revés",
                "4": "Pared de fondo de derecha",
                "5": "Pared de fondo de revés",
                "6": "Pared lateral de derecha",
                "7": "Pared lateral de revés",
                "8": "Dobles paredes de derecha",
                "9": "Dobles paredes de revés",
                "10": "Contrapared de derecha",
                "11": "Contrapared de revés",
                "12": "Volea de derecha",
                "13": "Volea de revés",
                "14": "Globo",
                "15": "Remate",
                "16": "Bandeja"
            },
            "BEGINNER": "Principiante",
            "INTERMEDIATE": "Intermedio",
            "ADVANCED": "Avanzado",
            "BACK": "Volver",
            "STROKE_UPDATED_SUCCESS": "¡Golpe actualizado con éxito!",
            "ERROR_RECEIVE_DATA": "Error al intentar contactar con los servicios.\nPor favor intente de nuevo más tarde.",
        }
        return language_map.get(key, key)

    def test_handle_configure_strokes(self):
        """Test that handle_configure_strokes creates buttons and sends a message"""

        handle_configure_strokes(self.message, self.bot)

        self.bot.ui.create_inline_keyboard.assert_called()

        self.bot.send_message.assert_called_once_with(
            self.message.chat.id,
            "Selecciona un golpe para configurar:",
            reply_markup="mock_markup",
        )

    def test_strokes_callback_single_stroke(self):
        """Test that strokes_callback creates skill level buttons for a single stroke"""

        self.call.data = "configurar_golpes:stroke:1"

        strokes_callback(self.call, self.bot)

        self.bot.ui.create_inline_keyboard.assert_called()

        self.bot.edit_message_text.assert_called_once_with(
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.message_id,
            text="Selecciona tu nivel para: Saque",
            reply_markup="mock_markup",
        )

    def test_strokes_callback_all_strokes(self):
        """Test that strokes_callback creates skill level buttons for all strokes"""

        self.call.data = "configurar_golpes:stroke:all"

        strokes_callback(self.call, self.bot)

        self.bot.ui.create_inline_keyboard.assert_called()

        self.bot.edit_message_text.assert_called_once_with(
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.message_id,
            text="Selecciona tu nivel para: Todos los golpes",
            reply_markup="mock_markup",
        )

    def test_skill_level_callback_single_stroke(self):
        """Test that skill_level_callback updates a single stroke"""

        self.call.data = "configurar_golpes:skill:1:1"

        skill_level_callback(
            self.call, self.bot, get_api=self.get_api, user_service=self.user_service
        )

        self.player_service.update_strokes.assert_called_once()

        args, _ = self.player_service.update_strokes.call_args
        user_id, strokes_body = args
        self.assertEqual(user_id, "123")
        self.assertEqual(len(strokes_body), 1)
        self.assertEqual(strokes_body["serve"], 2.0)

        self.bot.answer_callback_query.assert_called_once_with(
            self.call.id, "¡Golpe actualizado con éxito!"
        )

    def test_skill_level_callback_all_strokes(self):
        """Test that skill_level_callback updates all strokes"""

        self.call.data = "configurar_golpes:skill:all:2"

        skill_level_callback(
            self.call, self.bot, get_api=self.get_api, user_service=self.user_service
        )

        self.player_service.update_strokes.assert_called_once()

        args, _ = self.player_service.update_strokes.call_args
        user_id, strokes_body = args
        self.assertEqual(user_id, "123")
        self.assertEqual(len(strokes_body), 16)

        for stroke_name, skill_level in strokes_body.items():
            self.assertEqual(skill_level, 3.0)

        self.bot.answer_callback_query.assert_called_once_with(
            self.call.id, "¡Golpe actualizado con éxito!"
        )

    def test_show_strokes_list_callback(self):
        """Test that show_strokes_list_callback returns to the strokes list"""

        show_strokes_list_callback(self.call, self.bot)

        self.bot.ui.create_inline_keyboard.assert_called()

        self.bot.edit_message_text.assert_called_once_with(
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.message_id,
            text="Selecciona un golpe para configurar:",
            reply_markup="mock_markup",
        )
