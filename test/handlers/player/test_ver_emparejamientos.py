import unittest
from unittest.mock import patch, MagicMock
from telebot.types import CallbackQuery, Message
from handlers.player.ver_emparejamientos import matchups_main_callback, matchups_back_callback, generate_callback_string, handle_matchups

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
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "status": "pending",
            "match_players": [
                {"reserve": "confirmed", "user_id": "user1"},
                {"reserve": "pending", "user_id": "user2"}
            ]
        }

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    def test_handle_matchups_no_matches(self, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        mock_match_service.get_user_matches.return_value = {"data": []}

        handle_matchups(self.message, self.bot)

        self.bot.reply_to.assert_called_once_with(self.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.send_message.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    def test_handle_matchups_with_matches(self, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_match_service.get_user_matches.return_value = {"data": [self.sample_match]}

        handle_matchups(self.message, self.bot)

        self.bot.send_message.assert_called_once()
        self.assertIn(self.bot.language_manager.get("MESSAGE_SEE_MATCHES"), self.bot.send_message.call_args[0])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    def test_handle_matchups_no_user_id(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        handle_matchups(self.message, self.bot)

        self.bot.send_message.assert_called_once_with(self.message.chat.id, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    @patch('handlers.player.ver_emparejamientos.users_service')
    def test_matchups_main_callback_valid(self, mock_users_service, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.side_effect = [
            "%d/%m/%Y",
            "%H:%M",
        ]
        mock_match_service.get_user_matches.return_value = {"data": [self.sample_match]}
        mock_users_service.get_user_by_id.return_value = {"name": "Player Name"}
        
        self.call.data = generate_callback_string('1')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_called_once()
        args = self.bot.edit_message_text.call_args[1]
        self.assertIn("Establecimiento: 1", args['text'])
        self.assertIn("Cancha: 1", args['text'])
        self.assertIn("Dia: 10/10/2023", args['text'])
        self.assertIn("Horario: 10:00", args['text'])
        self.assertIn("Estado: pending", args['text'])
        self.assertIn("Jugador 1: Player Name", args['text'])
        self.assertIn("Estado: confirmed", args['text'])

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    def test_matchups_main_callback_invalid(self, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        mock_match_service.get_user_matches.return_value = {"data": []}
        
        self.call.data = generate_callback_string('999')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    def test_matchups_main_callback_no_matches(self, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        mock_match_service.get_user_matches.return_value = {"data": []}
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        
        self.call.data = generate_callback_string('1')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.reply_to.assert_called_once_with(self.call.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    def test_matchups_main_callback_no_user_id(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        
        self.call.data = generate_callback_string('1')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.send_message.assert_called_once_with(self.call.from_user.id, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    def test_matchups_back_callback_no_matches(self, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        mock_match_service.get_user_matches.return_value = {"data": []}

        matchups_back_callback(self.call, self.bot)

        self.bot.reply_to.assert_called_once_with(self.call.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    @patch('handlers.player.ver_emparejamientos.match_service')
    def test_matchups_back_callback_with_matches(self, mock_match_service, mock_get_user_id):
        mock_get_user_id.return_value = "test_user_id"
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_match_service.get_user_matches.return_value = {"data": [self.sample_match]}

        matchups_back_callback(self.call, self.bot)

        self.bot.edit_message_text.assert_called_once()
        self.assertIn(self.bot.language_manager.get("MESSAGE_SEE_MATCHES"), self.bot.edit_message_text.call_args[1]['text'])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.get_user_public_id')
    def test_matchups_back_callback_no_user_id(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"

        matchups_back_callback(self.call, self.bot)

        self.bot.send_message.assert_called_once_with(self.call.message.chat.id, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

if __name__ == '__main__':
    unittest.main()