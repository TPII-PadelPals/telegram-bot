import unittest
from unittest.mock import patch, MagicMock
from telebot.types import CallbackQuery, Message

from handlers.player.matchups.handle_reply_one_matchup import handle_reply_one_matchup_callback
from handlers.player.matchups.utils import MatchupAction, generate_callback_string
from services.users_service import User


class TestMatchupResponseMatchPlayerCallback(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()

        self.language_manager = {
            "MESSAGE_MATCH_PLAYER_CONFIRMATION": "Para confirmar el partido, realice el pago de la reserva utilizando uno de los siguientes metodos de pago.\nUna vez realizado el pago, verá el estado de su reserva actualizado en el emparejamiento: /ver_emparejamientos",
            "MESSAGE_MATCH_PLAYER_REJECT": "Ha rechazado el partido correctamente. Si desea participar de un partido puede buscar sus matches disponibles con el comando /ver_emparejamientos.",
            "ERROR_SET_MATCH_PLAYER_STATUS": "No se pudo confirmar la reserva. Por favor inténtelo nuevamente.",
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

    @patch('handlers.player.matchups.handle_reply_one_matchup.UsersService')
    @patch('handlers.player.matchups.handle_reply_one_matchup_confirm.PaymentsService')
    def test_match_player_response_confirm_match_callback(self, MockPaymentsService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_payments_service = MockPaymentsService.return_value
        pay_url = 'http://a-payment-method.com'

        mock_users_service.get_user_info.return_value = [User(
            public_id=self.user_public_id)]

        mock_payments_service.update_match_player_status.return_value = {
            'user_public_id': self.user_public_id,
            'match_public_id': self.match_public_id,
            'reserve': 'inside',
            'pay_url': pay_url
        }

        self.call.data = generate_callback_string(
            f'{MatchupAction.CONFIRM}:{self.match_public_id}')

        handle_reply_one_matchup_callback(self.call, self.bot)

        _args, kwargs = self.bot.edit_message_text.call_args
        assert kwargs['chat_id'] == self.call.message.chat.id
        assert kwargs['message_id'] == self.call.message.message_id
        assert kwargs['text'] == self.language_manager.get(
            "MESSAGE_MATCH_PLAYER_CONFIRMATION")

    @patch('handlers.player.matchups.handle_reply_one_matchup.UsersService')
    @patch('handlers.player.matchups.handle_reply_one_matchup_confirm.PaymentsService')
    def test_match_player_response_confirm_match_callback_with_service_error(self, MockPaymentsService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_payments_service = MockPaymentsService.return_value

        mock_users_service.get_user_info.return_value = [User(
            public_id=self.user_public_id)]

        mock_payments_service.update_match_player_status.return_value = None

        self.call.data = generate_callback_string(
            f'inside:{self.match_public_id}')

        handle_reply_one_matchup_callback(self.call, self.bot)

        self.bot.reply_to.assert_called_once_with(
            self.call.message,
            self.language_manager.get("ERROR_SET_MATCH_PLAYER_STATUS")
        )

    @patch('handlers.player.matchups.handle_reply_one_matchup.UsersService')
    @patch('handlers.player.matchups.handle_reply_one_matchup_confirm.PaymentsService')
    def test_match_player_response_confirm_match_callback_without_user_public_id_returns_error(self, MockPaymentsService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_payments_service = MockPaymentsService.return_value

        mock_users_service.get_user_info.return_value = None

        mock_payments_service.update_match_player_status.return_value = {
            'user_public_id': self.user_public_id,
            'match_public_id': self.match_public_id,
            'reserve': 'inside'
        }

        self.call.data = generate_callback_string(
            f'f{MatchupAction.CONFIRM}:{self.match_public_id}')

        handle_reply_one_matchup_callback(self.call, self.bot)

        self.bot.send_message.assert_called_once_with(
            self.message.chat.id,
            self.language_manager.get("ERROR_USER_NOT_FOUND"),
        )

    @patch('handlers.player.matchups.handle_reply_one_matchup.UsersService')
    @patch('handlers.player.matchups.handle_reply_one_matchup_reject.MatchesService')
    def test_match_player_response_reject_match_callback(self, MockMatchesService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_matches_service = MockMatchesService.return_value

        mock_users_service.get_user_info.return_value = [User(
            public_id=self.user_public_id)]

        mock_matches_service.update_match_player_status.return_value = {
            'user_public_id': self.user_public_id,
            'match_public_id': self.match_public_id,
            'reserve': 'outside',
            'pay_url': 'http://a-payment-method.com'
        }

        self.call.data = generate_callback_string(
            f'{MatchupAction.REJECT}:{self.match_public_id}')

        handle_reply_one_matchup_callback(self.call, self.bot)

        _args, kwargs = self.bot.edit_message_text.call_args
        assert kwargs['chat_id'] == self.call.message.chat.id
        assert kwargs['message_id'] == self.call.message.message_id
        assert kwargs['text'] == self.language_manager.get(
            "MESSAGE_MATCH_PLAYER_REJECT")

    @patch('handlers.player.matchups.handle_reply_one_matchup.UsersService')
    @patch('handlers.player.matchups.handle_reply_one_matchup_reject.MatchesService')
    def test_match_player_response_reject_match_callback_with_service_error(self, MockMatchesService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_matches_service = MockMatchesService.return_value

        mock_users_service.get_user_info.return_value = [User(
            public_id=self.user_public_id)]

        mock_matches_service.update_match_player_status.return_value = None

        self.call.data = generate_callback_string(
            f'{MatchupAction.REJECT}:{self.match_public_id}')

        handle_reply_one_matchup_callback(self.call, self.bot)

        self.bot.reply_to.assert_called_once_with(
            self.call.message,
            self.language_manager.get("ERROR_SET_MATCH_PLAYER_STATUS")
        )

    @patch('handlers.player.matchups.handle_reply_one_matchup.UsersService')
    @patch('handlers.player.matchups.handle_reply_one_matchup_reject.MatchesService')
    def test_match_player_response_reject_match_callback_without_user_public_id_returns_error(self, MockMatchesService, MockUsersService):
        mock_users_service = MockUsersService.return_value
        mock_matches_service = MockMatchesService.return_value

        mock_users_service.get_user_info.return_value = []

        mock_matches_service.update_match_player_status.return_value = {
            'user_public_id': self.user_public_id,
            'match_public_id': self.match_public_id,
            'reserve': 'outside'
        }

        self.call.data = generate_callback_string(
            f'{MatchupAction.REJECT}:{self.match_public_id}')

        handle_reply_one_matchup_callback(self.call, self.bot)

        self.bot.send_message.assert_called_once_with(
            self.message.chat.id,
            self.language_manager.get("ERROR_USER_NOT_FOUND"),
        )
