import unittest
from unittest.mock import patch, Mock
# Cambia `my_module` al nombre real del archivo donde está la clase
from model.api_conection import ApiConection


class TestApiConection(unittest.TestCase):

    def setUp(self):
        self.api = ApiConection("https://api.example.com")

    @patch('requests.get')
    def test_get_hi_name_success(self, mock_get):
        # Simulamos una respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Hola, Carlos!'}
        mock_get.return_value = mock_response

        result = self.api.get_hi_name("Carlos")
        self.assertEqual(result, 'Hola, Carlos!')

    @patch('requests.get')
    def test_get_hi_name_other_error(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")

        result = self.api.get_hi_name("Carlos")
        self.assertIn('An error occurred', result)

    @patch('requests.put')
    def test_set_availability_success(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'time_availability': 10}
        mock_put.return_value = mock_response

        result = self.api.set_availability(10, 'ID')
        self.assertEqual(result, 10)

    @patch('requests.put')
    def test_set_zone_success(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'zone_km': 1, 'zone_location': 'CABA'}
        mock_put.return_value = mock_response

        result = self.api.set_zone("CABA", 15, 'ID')
        self.assertEqual(result, (1, 'CABA'))

    @patch('requests.put')
    def test_set_zone_only_zone_success(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'zone_km': 0, 'zone_location': 'CABA'}
        mock_put.return_value = mock_response

        result = self.api.set_zone("CABA", None, 'ID')
        self.assertEqual(result, (0, 'CABA'))

    @patch('requests.put')
    def test_set_zone_only_km_success(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'zone_km': 15, 'zone_location': 'SA'}
        mock_put.return_value = mock_response

        result = self.api.set_zone(None, 15, 'ID')
        self.assertEqual(result, (15, 'SA'))

    # @patch('requests.post')
    # def test_set_zone_no_values_error(self):
    #     # Prueba para el caso donde no se proporciona `zone` ni `km`
    #     try:
    #         ApiConection("https://api.example.com").set_zone(zone=None, km=None)
    #         print("NO lanza excepcion")
    #         assert False
    #     except ValueError:
    #         print("OK")
    #         assert True
    #     except:
    #         print("lanza otra excepcion")
    #         assert False

    @patch('requests.put')
    def test_set_available_day_success(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = 4
        mock_put.return_value = mock_response

        result = self.api.set_available_day(4, 'ID')
        self.assertEqual(result, 4)

    @patch('requests.get')
    def test_get_matches_success_empty(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_put.return_value = mock_response

        result = self.api.get_matches('ID')
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_get_matches_success_no_empty(self, mock_put):
        result_base = [
            {
                "player_id_1": "test_40",
                "player_id_2": "test_48",
                "paddle_court_id": 1,
                "time_availability": 4,
                "begin_date_time": "2024-11-11T19:59:49.808321"
            },
            {
                "player_id_1": "test_40",
                "player_id_2": "test_48",
                "paddle_court_id": 4,
                "time_availability": 4,
                "begin_date_time": "2024-11-11T19:59:49.808409"
            }
        ]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = result_base
        mock_put.return_value = mock_response

        result = self.api.get_matches('ID')
        self.assertEqual(result, result_base)

    @patch('requests.put')
    def test_put_strokes(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "OK"
        mock_put.return_value = mock_response

        result = self.api.put_strokes(4, {"a": "2"})
        self.assertEqual(result, "OK")

    @patch('requests.get')
    def test_get_reserves(self, mock_put):
        result_base = [
            {
                "player_id_1": "test_40",
                "player_id_2": "test_48",
                "paddle_court_id": 1,
                "time_availability": 4,
                "begin_date_time": "2024-11-11",
                "player_id_1_response_accept": False,
                "player_id_2_response_accept": True
            },
            {
                "player_id_1": "test_40",
                "player_id_2": "test_48",
                "paddle_court_id": 4,
                "time_availability": 4,
                "begin_date_time": "2024-11-12",
                "player_id_1_response_accept": False,
                "player_id_2_response_accept": True
            }
        ]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = result_base
        mock_put.return_value = mock_response

        result = self.api.get_reserves(4)
        self.assertEqual(result, result_base)

    @patch('requests.put')
    def test_respond_to_matchmaking_accept(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "OK"
        mock_put.return_value = mock_response

        info = {
            "player_id_1": "test_40",
            "player_id_2": "test_48",
            "paddle_court_id": 1,
            "time_availability": 4,
            #"begin_date_time": "2024-11-11"
        }

        result = self.api.respond_to_matchmaking(4, info, True)
        self.assertEqual(result, "OK")

    @patch('requests.put')
    def test_respond_to_matchmaking_reject(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "OK"
        mock_put.return_value = mock_response

        info = {
            "player_id_1": "test_40",
            "player_id_2": "test_48",
            "paddle_court_id": 1,
            "time_availability": 4,
            #"begin_date_time": "2024-11-11"
        }

        result = self.api.respond_to_matchmaking(4, info, False)
        self.assertEqual(result, "OK")


if __name__ == "__main__":
    unittest.main()
