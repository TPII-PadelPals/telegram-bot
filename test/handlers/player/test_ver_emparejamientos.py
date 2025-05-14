import unittest
from unittest.mock import patch, MagicMock
from telebot.types import CallbackQuery, Message

from handlers.player.matchups.handle_display_all_matchups import handle_display_all_matchups_callback
from handlers.player.matchups.handle_display_one_matchup import handle_display_one_matchup_callback
from handlers.player.matchups.utils import generate_callback_string
from handlers.player.matchups.ver_emparejamientos import handle_matchups


class TestMatchupsMainCallback(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()
        self.message = MagicMock(spec=Message)
        self.message.chat = MagicMock()
        self.message.chat.id = 12345
        self.message.from_user = MagicMock()
        self.message.from_user.id = 12345
        self.message.from_user.username = "test_user"
        self.call = MagicMock(spec=CallbackQuery)
        self.call.from_user = MagicMock()
        self.call.from_user.id = 12345
        self.call.message = MagicMock(spec=Message)
        self.call.message.chat = MagicMock()
        self.call.message.chat.id = 12345
        self.call.message.message_id = 67890
        self.call.message.chat.username = "test_user"

        self.sample_match = {
            "public_id": "1",
            "court_name": "1",
            "date": "2023-10-10",
            "time": "10",
            "status": "pending",
            "match_players": [
                {"reserve": "assigned", "user_id": "user1"},
                {"reserve": "inside", "user_id": "user2"}
            ]
        }

        self.player_outside_matches = {
            "data": [
                {
                    "public_id": "a5f94e1a-e03c-49be-a8fe-9d6fcb912e19",
                    "court_name": "Cancha1",
                    "court_public_id": "55fac2f7-1989-46b1-b2c0-4b662c5ecb87",
                    "time": 9,
                    "date": "2025-05-02",
                    "status": "Provisional",
                    "match_players": [
                        {
                            "match_public_id": "a5f94e1a-e03c-49be-a8fe-9d6fcb912e19",
                            "user_public_id": "3a7ebc3c-0300-4f50-ae18-3ee0a79aa1e1",
                            "distance": 0,
                            "reserve": "outside"
                        },
                        {
                            "match_public_id": "a5f94e1a-e03c-49be-a8fe-9d6fcb912e19",
                            "user_public_id": "ba1cb889-f70f-45ef-9cbd-222f6a587651",
                            "distance": 3,
                            "reserve": "assigned"
                        },
                        {
                            "match_public_id": "a5f94e1a-e03c-49be-a8fe-9d6fcb912e19",
                            "user_public_id": "ccd5ceca-e2f2-4a2a-a784-5d3bc2803d78",
                            "distance": 2,
                            "reserve": "assigned"
                        },
                        {
                            "match_public_id": "a5f94e1a-e03c-49be-a8fe-9d6fcb912e19",
                            "user_public_id": "0ba9065b-b3dd-492e-bcef-54b72fd5109e",
                            "distance": 1,
                            "reserve": "assigned"
                        }
                    ]
                },
            ],
            "count": 1
        }

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    def test_handle_matchups_no_matches(self, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        mock_validate_and_filter_matchups.return_value = []

        handle_matchups(self.message, self.bot)

        self.bot.reply_to.assert_called_once_with(
            self.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.send_message.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.match_service')
    def test_handle_matchups_no_matches_when_i_rejected_match(self, mock_match_service, mock_get_user_id):
        mock_match_service.get_user_matches.return_value = self.player_outside_matches
        mock_get_user_id.return_value = "3a7ebc3c-0300-4f50-ae18-3ee0a79aa1e1"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        handle_matchups(self.message, self.bot)

        self.bot.reply_to.assert_called_once_with(
            self.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.send_message.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    def test_handle_matchups_with_matches(self, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_validate_and_filter_matchups.return_value = [self.sample_match]

        handle_matchups(self.message, self.bot)

        self.bot.send_message.assert_called_once()
        self.assertIn(self.bot.language_manager.get(
            "MESSAGE_SEE_MATCHES"), self.bot.send_message.call_args[0])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    def test_handle_matchups_no_user_id(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        handle_matchups(self.message, self.bot)

        self.bot.send_message.assert_called_once_with(
            self.message.chat.id, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    @patch('handlers.player.matchups.ver_emparejamientos.users_service')
    def test_handle_display_one_matchup_callback_valid(self, mock_users_service, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.side_effect = [
            "%d/%m/%Y",
            "%H:%M",
        ]
        mock_validate_and_filter_matchups.return_value = [self.sample_match]
        mock_users_service.get_user_by_id.return_value = {
            "name": "Player Name"}

        self.call.data = generate_callback_string('1')

        handle_display_one_matchup_callback(self.call, self.bot)

        self.bot.edit_message_text.assert_called_once()
        args = self.bot.edit_message_text.call_args[1]
        self.assertIn("Establecimiento: 1", args['text'])
        self.assertIn("Cancha: 1", args['text'])
        self.assertIn("Dia: 10/10/2023", args['text'])
        self.assertIn("Horario: 10:00", args['text'])
        self.assertIn("Estado: pending", args['text'])
        self.assertIn("Jugador 1: Player Name", args['text'])
        self.assertIn("Estado: assigned", args['text'])

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    def test_handle_display_one_matchup_callback_invalid(self, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        mock_validate_and_filter_matchups.return_value = []

        self.call.data = generate_callback_string('999')

        handle_display_one_matchup_callback(self.call, self.bot)

        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    def test_handle_display_one_matchup_callback_no_matches(self, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        mock_validate_and_filter_matchups.return_value = []
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        self.call.data = generate_callback_string('1')

        handle_display_one_matchup_callback(self.call, self.bot)

        self.bot.reply_to.assert_called_once_with(
            self.call.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    def test_handle_display_one_matchup_callback_no_user_id(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        self.call.data = generate_callback_string('1')

        handle_display_one_matchup_callback(self.call, self.bot)

        self.bot.send_message.assert_called_once_with(
            self.call.from_user.id, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    def test_handle_display_all_matchups_callback_no_matches(self, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        mock_validate_and_filter_matchups.return_value = []

        handle_display_all_matchups_callback(self.call, self.bot)

        self.bot.reply_to.assert_called_once_with(
            self.call.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.matchups.ver_emparejamientos.validate_and_filter_matchups')
    def test_handle_display_all_matchups_callback_with_matches(self, mock_validate_and_filter_matchups, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_validate_and_filter_matchups.return_value = [self.sample_match]

        handle_display_all_matchups_callback(self.call, self.bot)

        self.bot.edit_message_text.assert_called_once()
        self.assertIn(self.bot.language_manager.get(
            "MESSAGE_SEE_MATCHES"), self.bot.edit_message_text.call_args[1]['text'])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.matchups.ver_emparejamientos.get_user_public_id')
    def test_handle_display_all_matchups_callback_no_user_id(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        handle_display_all_matchups_callback(self.call, self.bot)

        self.bot.send_message.assert_called_once_with(
            self.call.message.chat.id, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()


if __name__ == '__main__':
    unittest.main()
