import unittest
from unittest.mock import patch, MagicMock
from telebot.types import CallbackQuery, Message
from handlers.player.ver_emparejamientos import matchups_main_callback, matchups_back_callback, generate_callback_string, DEFAULT_PLAYER, handle_matchups


class TestMatchupsMainCallback(unittest.TestCase):

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

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_handle_matchups_no_matches(self, MockMatchService):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = []

        handle_matchups(self.message, self.bot)

        self.bot.reply_to.assert_called_once_with(self.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.send_message.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_handle_matchups_with_matches(self, MockMatchService):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = [{
            "player_id_1": "test_user",
            "player_id_2": "opponent",
            "court_name": "Court 1",
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "id": 1
        }]

        handle_matchups(self.message, self.bot)

        self.bot.send_message.assert_called_once()
        self.assertIn(self.bot.language_manager.get("MESSAGE_SEE_MATCHES"), self.bot.send_message.call_args[0])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_handle_matchups_default_player(self, MockMatchService):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = [{
            "player_id_1": DEFAULT_PLAYER,
            "player_id_2": "opponent",
            "court_name": "Court 1",
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "id": 1
        }]
        self.message.from_user.username = None

        handle_matchups(self.message, self.bot)

        self.bot.send_message.assert_called_once()
        self.assertIn(self.bot.language_manager.get("MESSAGE_SEE_MATCHES"), self.bot.send_message.call_args[0])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_main_callback_valid(self, MockMatchService):
        self.bot.language_manager.get.side_effect = [
            "%d/%m/%Y",
            "%H:%M",
        ]
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = [{
            "player_id_1": "test_user",
            "player_id_2": "opponent",
            "court_name": "Court 1",
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "id": 1
        }]
        
        self.call.data = generate_callback_string('1')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_called_once()
        self.assertIn("Contrincante: opponent", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Establecimiento: Court 1", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Cancha: 1", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Dia: 10/10/2023", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Horario: 10:00", self.bot.edit_message_text.call_args[1]['text'])

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_main_callback_invalid(self, MockMatchService):
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = []
        
        self.call.data = generate_callback_string('999')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_main_callback_no_matches(self, MockMatchService):
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = []
        
        self.call.data = generate_callback_string('1')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_main_callback_no_username(self, MockMatchService):
        self.bot.language_manager.get.side_effect = [
            "%d/%m/%Y",
            "%H:%M",
        ]
        self.call.message.chat.username = None
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = [{
            "player_id_1": DEFAULT_PLAYER,
            "player_id_2": "opponent",
            "court_name": "Court 1",
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "id": 1
        }]
        
        self.call.data = generate_callback_string('1')
        
        matchups_main_callback(self.call, self.bot)
        
        self.bot.edit_message_text.assert_called_once()
        self.assertIn("Contrincante: opponent", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Establecimiento: Court 1", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Cancha: 1", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Dia: 10/10/2023", self.bot.edit_message_text.call_args[1]['text'])
        self.assertIn("Horario: 10:00", self.bot.edit_message_text.call_args[1]['text'])

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_back_callback_no_matches(self, MockMatchService):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES_EMPTY"
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = []

        matchups_back_callback(self.call, self.bot)

        self.bot.reply_to.assert_called_once_with(self.call.message, self.bot.language_manager.get("MESSAGE_SEE_MATCHES_EMPTY"))
        self.bot.edit_message_text.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_back_callback_with_matches(self, MockMatchService):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = [{
            "player_id_1": "test_user",
            "player_id_2": "opponent",
            "court_name": "Court 1",
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "id": 1
        }]

        matchups_back_callback(self.call, self.bot)

        self.bot.edit_message_text.assert_called_once()
        self.assertIn(self.bot.language_manager.get("MESSAGE_SEE_MATCHES"), self.bot.edit_message_text.call_args[1]['text'])
        self.bot.reply_to.assert_not_called()

    @patch('handlers.player.ver_emparejamientos.MatchService')
    def test_matchups_back_callback_default_player(self, MockMatchService):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_MATCHES"
        mock_service = MockMatchService.return_value
        mock_service.get_provisional_matches.return_value = [{
            "player_id_1": DEFAULT_PLAYER,
            "player_id_2": "opponent",
            "court_name": "Court 1",
            "court_id": "1",
            "date": "2023-10-10",
            "time": "10",
            "id": 1
        }]
        self.call.message.chat.username = None

        matchups_back_callback(self.call, self.bot)

        self.bot.edit_message_text.assert_called_once()
        self.assertIn(self.bot.language_manager.get("MESSAGE_SEE_MATCHES"), self.bot.edit_message_text.call_args[1]['text'])
        self.bot.reply_to.assert_not_called()

if __name__ == '__main__':
    unittest.main()