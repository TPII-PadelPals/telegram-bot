import unittest
from unittest.mock import MagicMock

from handlers.player.configurar_disponibilidad import handle_configure_availability, process_time_step


class TestConfigurarDisponibilidad(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()
        
        self.language_manager = {
            "AVAILABLE_TIME_MESSAGE": "Indícanos los horarios que suelas tener disponibles:",
            "AVAILABILITY_TIME_BUTTONS": [
                {"text": "Mañana", "callback_data": "1"},
                {"text": "Tarde", "callback_data": "2"},
                {"text": "Noche", "callback_data": "3"},
                {"text": "Mañana y tarde", "callback_data": "4"},
                {"text": "Mañana y noche", "callback_data": "5"},
                {"text": "Tarde y noche", "callback_data": "6"},
                {"text": "Todos", "callback_data": "7"},
            ],
            "AVAILABLE_DAYS_MESSAGE": "Selecciona el día disponible:",
            "AVAILABILITY_DAY_BUTTONS": [
                {
                "text": "Lunes",
                "callback_data": "1"
                },
                {
                "text": "Martes",
                "callback_data": "2"
                },
                {
                "text": "Miércoles",
                "callback_data": "3"
                },
                {
                "text": "Jueves",
                "callback_data": "4"
                },
                {
                "text": "Viernes",
                "callback_data": "5"
                },
                {
                "text": "Sábado",
                "callback_data": "6"
                },
                {
                "text": "Domingo",
                "callback_data": "7"
                }
            ],
            "ERROR_SET_AVAILABILITY": "No se pudo configurar la disponibilidad. Por favor inténtelo nuevamente.",
            "ERROR_RECEIVE_DATA": "Error al intentar contactar con los servicios.\nPor favor intente de nuevo más tarde.",
            "ERROR_USER_NOT_FOUND": "Usted no se encuentra registrado.\nPor favor intente registrarse con el comando /start y vuelva a intentarlo.",
        }

        self.bot.language_manager.get = MagicMock(side_effect=self._mock_language_manager_get)

        self.bot.ui = MagicMock()
        self.bot.ui.create_inline_keyboard = MagicMock(return_value="mock_markup")

        self.bot.send_message = MagicMock()
        self.bot.edit_message_text = MagicMock()
        self.bot.answer_callback_query = MagicMock()

        self.players_service = MagicMock()
        self.players_service.update_partial_player = MagicMock(
            return_value={
                'user_public_id': 'c9270134-7e5e-4e77-b6a8-b7998598c8a1',
                'telegram_id': 12345, 
                'search_range_km': None, 
                'address': None, 
                'latitude': None, 
                'longitude': None, 
                'time_availability': 5
            }
        )

        self.get_api = MagicMock(return_value=self.players_service)

        self.users_service_api = MagicMock()
        self.users_service_api.get_user_info = MagicMock(
            return_value={"data": [{"public_id": "c9270134-7e5e-4e77-b6a8-b7998598c8a1"}]}
        )

        self.users_service = MagicMock(return_value=self.users_service_api)

        self.message = MagicMock()
        self.message.chat = MagicMock()
        self.message.chat.id = 12345

        self.call = MagicMock()
        self.call.id = "call123"

        self.call.message = MagicMock()
        self.call.message.chat = MagicMock()
        self.call.message.chat.id = 12345

    def _mock_language_manager_get(self, key, *_args, **_kwargs):
        return self.language_manager.get(key, None)

    def test_handle_configure_availability(self):
        """Test that handle_configure_availability creates buttons and sends a message"""

        handle_configure_availability(self.message, self.bot)

        self.bot.ui.create_inline_keyboard.assert_called()

        self.bot.send_message.assert_called_once_with(
            self.message.chat.id,
            self.language_manager["AVAILABLE_TIME_MESSAGE"],
            reply_markup="mock_markup",
        )

    def test_process_time_step_update_one_time(self):
        """Test that process_time_step updates a single time availability"""

        self.call.data = "configurar_disponibilidad:time:7"

        process_time_step(
            self.call, self.bot, players_service=self.get_api, users_service=self.users_service
        )

        self.players_service.update_partial_player.assert_called_once()

        args, _ = self.players_service.update_partial_player.call_args

        user_id, time_availability_body = args
        self.assertEqual(user_id, "c9270134-7e5e-4e77-b6a8-b7998598c8a1")
        self.assertEqual(len(time_availability_body), 1)
        self.assertEqual(time_availability_body["time_availability"], 7)

        self.bot.edit_message_text.assert_called_once()
    
    def test_process_time_step_user_not_found(self):
        """Test that process_time_step sends an error when user is not found"""

        self.call.data = "configurar_disponibilidad:time:7"

        self.users_service_api.get_user_info.return_value = {"data": []}

        process_time_step(
            self.call, self.bot, players_service=self.get_api, users_service=self.users_service
        )

        self.players_service.update_partial_player.assert_not_called()

        self.bot.answer_callback_query.assert_called_once_with(
            self.call.id, self.language_manager["ERROR_USER_NOT_FOUND"]
        )
