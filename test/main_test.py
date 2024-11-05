import unittest
from unittest.mock import patch, MagicMock
from main import send_welcome, set_availability, KM_STEERING_SEPARATOR, set_zone


class TestTelegramBot(unittest.TestCase):

    @patch('telebot.TeleBot.reply_to')
    def test_start_command(self, mock_reply_to):
        # Crea un mensaje de prueba simulando el mensaje del comando /start
        message = MagicMock()
        message.text = '/start'

        # Llama a la función del manejador de /start
        send_welcome(message)

        # Verifica si se llamó a reply_to con los argumentos correctos
        mock_reply_to.assert_called_once_with(
            message, "Bienvenido a PadelPals")

    @patch('telebot.TeleBot.reply_to')
    def test_send_disponibilidad_horaria_no_number(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_disponibilidad'
        set_availability(message)
        mock_reply_to.assert_called_once_with(
            message,
            'Indicanos los horarios que suelas tener disponibles:\n- Mañana de 8hs hasta 12hs.\n- Tarde de 12hs hasta 18hs.\n- Noche de 18hs hasta 00hs.\n1: Mañana\n2: Tarde\n3: Noche\n4: Mañana y tarde\n5: Mañana y noche\n6: Tarde y noche\n7: Todos\nAsignación: /configurar_disponibilidad <Numero>')

    @patch('telebot.TeleBot.reply_to')
    def test_send_disponibilidad_horaria_no_number_border_case(
            self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_disponibilidad    '
        set_availability(message)
        mock_reply_to.assert_called_once_with(
            message,
            'Indicanos los horarios que suelas tener disponibles:\n- Mañana de 8hs hasta 12hs.\n- Tarde de 12hs hasta 18hs.\n- Noche de 18hs hasta 00hs.\n1: Mañana\n2: Tarde\n3: Noche\n4: Mañana y tarde\n5: Mañana y noche\n6: Tarde y noche\n7: Todos\nAsignación: /configurar_disponibilidad <Numero>')

    @patch('telebot.TeleBot.reply_to')
    def test_send_disponibilidad_horaria_whit_number(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_disponibilidad 4'
        message.author_signature = 'ID'
        set_availability(message)
        mock_reply_to.assert_called_once_with(message, 'OK')

    @patch('telebot.TeleBot.reply_to')
    def test_send_disponibilidad_horaria_whit_invalid_info(
            self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_disponibilidad a'
        set_availability(message)
        mock_reply_to.assert_called_once_with(message, 'No es un valor valido')

    @patch('telebot.TeleBot.reply_to')
    def test_send_ubicacion_help(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_zona'
        set_zone(message)
        mock_reply_to.assert_called_once_with(
            message,
            "Necesitamos saber desde donde querés que realicemos tus matches y a que distancia (en Km), como maximo, estarias dispuesto a recorrer para jugar un partido.\n Ingresar dirección distancia.\n Ej: /configurar_zona <Dirección>;<Numero>")

    @patch('telebot.TeleBot.reply_to')
    def test_send_ubicacion_help_border_case(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_zona   '
        set_zone(message)
        mock_reply_to.assert_called_once_with(
            message,
            "Necesitamos saber desde donde querés que realicemos tus matches y a que distancia (en Km), como maximo, estarias dispuesto a recorrer para jugar un partido.\n Ingresar dirección distancia.\n Ej: /configurar_zona <Dirección>;<Numero>")

    @patch('telebot.TeleBot.reply_to')
    def test_send_ubicacion_only_km(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_zona 54'
        message.author_signature = 'ID'
        set_zone(message)
        mock_reply_to.assert_called_once_with(
            message, "Kilometros actualizados: 54.")

    @patch('telebot.TeleBot.reply_to')
    def test_send_ubicacion_only_zone(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_zona CABA'
        message.author_signature = 'ID'
        set_zone(message)
        mock_reply_to.assert_called_once_with(
            message, "Ubicacion actualizada: CABA.")

    @patch('telebot.TeleBot.reply_to')
    def test_send_ubicacion_all(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + '82'
        message.author_signature = 'ID'
        set_zone(message)
        mock_reply_to.assert_called_once_with(
            message, "Ubicacion actualizada: CABA.\nKilometros actualizados: 82.")

    @patch('telebot.TeleBot.reply_to')
    def test_send_ubicacion_error_in_km(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + 'asd'
        set_zone(message)
        mock_reply_to.assert_called_once_with(message, "No es un valor valido")


if __name__ == '__main__':
    unittest.main()
