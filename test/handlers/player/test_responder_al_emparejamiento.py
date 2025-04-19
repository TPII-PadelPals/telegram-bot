import unittest
from unittest.mock import patch, MagicMock
from telebot.types import CallbackQuery, Message
from handlers.player.responder_al_emparejamiento import handle_player_response_match_callback
from handlers.player.ver_emparejamientos import generate_callback_string


class TestMatchupResponseMatchPlayerCallback(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()

        self.language_manager = {
            "MESSAGE_MATCH_PLAYER_CONFIRMATION": "Gracias por su confirmación. Ha ingresado al partido.",
            "ERROR_SET_MATCH_PLAYER_STATUS": "No se pudo actualizar el estado del match. Por favor inténtelo nuevamente.",
            "ERROR_USER_NOT_FOUND": "Usted no se encuentra registrado.\nPor favor intente registrarse con el comando /start y vuelva a intentarlo.",
        }

        self.bot.language_manager.get = MagicMock(
            side_effect=self._mock_language_manager_get
        )

        self.message = MagicMock(spec=Message)
        self.message.chat = MagicMock()
        self.message.chat.id = 12345
        self.message.from_user = MagicMock()
        self.message.from_user.id = 12345
        self.call = MagicMock(spec=CallbackQuery)
        self.call.from_user = MagicMock()
        self.call.from_user.id = 12345
        self.call.message = MagicMock(spec=Message)
        self.call.message.chat = MagicMock()
        self.call.message.chat.id = 12345
        self.call.message.message_id = 67890
        
        self.user_public_id = "c8a2204a-08a0-4ea6-889d-b51d6a7c6851"
        self.match_public_id = "0e40744f-79f2-4e31-b149-266f5e260300"

    def _mock_language_manager_get(self, key, *_args, **_kwargs):
        return self.language_manager.get(key, None)

    @patch('handlers.player.responder_al_emparejamiento.UsersService')
    @patch('handlers.player.responder_al_emparejamiento.MatchesService')
    def test_match_player_response_confirm_match_callback(self, MockMatchesService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_matches_service = MockMatchesService.return_value

        mock_users_service.get_user_info.return_value = {
            "data": [{"public_id": self.user_public_id}]
        }
        
        mock_matches_service.update_match_player_status.return_value = {
            'user_public_id': self.user_public_id,
            'match_public_id': self.match_public_id,
            'reserve': 'inside'
        }
        
        self.call.data = generate_callback_string(f'inside:{self.match_public_id}')

        handle_player_response_match_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_called_once_with(
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.message_id,
            text=self.language_manager.get("MESSAGE_MATCH_PLAYER_CONFIRMATION"),
        )

    @patch('handlers.player.responder_al_emparejamiento.UsersService')
    @patch('handlers.player.responder_al_emparejamiento.MatchesService')
    def test_match_player_response_confirm_match_callback_with_service_error(self, MockMatchesService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_matches_service = MockMatchesService.return_value

        mock_users_service.get_user_info.return_value = {
            "data": [{"public_id": self.user_public_id}]
        }
        
        mock_matches_service.update_match_player_status.return_value = None
        
        self.call.data = generate_callback_string(f'inside:{self.match_public_id}')

        handle_player_response_match_callback(self.call, self.bot)
        
        self.bot.reply_to.assert_called_once_with(
            self.call.message,
            self.language_manager.get("ERROR_SET_MATCH_PLAYER_STATUS")
        )

    @patch('handlers.player.responder_al_emparejamiento.UsersService')
    @patch('handlers.player.responder_al_emparejamiento.MatchesService')
    def test_match_player_response_confirm_match_callback_without_user_public_id_returns_error(self, MockMatchesService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_matches_service = MockMatchesService.return_value

        mock_users_service.get_user_info.return_value = {"data": []}
        
        mock_matches_service.update_match_player_status.return_value = {
            'user_public_id': self.user_public_id,
            'match_public_id': self.match_public_id,
            'reserve': 'inside'
        }
        
        self.call.data = generate_callback_string(f'inside:{self.match_public_id}')

        handle_player_response_match_callback(self.call, self.bot)
        
        self.bot.send_message.assert_called_once_with(
            self.message.chat.id,
            self.language_manager.get("ERROR_USER_NOT_FOUND"),
        )