import requests


class ApiConection:
    def __init__(self, url):
        self.url = url

    def get_hi_name(self, name):
        try:
            response = requests.get(self.url + f'/message/{name}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            return data['message']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def set_availability(self, time: int, id_telegram):
        try:
            # response = requests.put(self.url + f'/message/availability/{time};{id_telegram}')
            # cambio a endpoint en lugar de main
            response = requests.put(
                self.url + f'/player/change_time/{id_telegram}:{time}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            # return data['message']
            return data['time_availability']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def set_available_day(self, day, id_telegram):
        try:
            # /player/change_days/{item_id}:{day}
            response = requests.put(
                self.url + f'/player/change_days/{id_telegram}:{day}')
            # Lanza un error si la respuesta no es 201
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def set_zone(self, zone: str, km: int, id_telegram):
        # se supone que esto no ocurra nunca por las llamadas del bot
        if zone is None and km is None:
            raise ValueError('Zone or km must be provided')
        try:
            # if zone is None:
            #     response = requests.put(self.url + f'/message/zone/km/{km};{id_telegram}')
            # elif km is None:
            #     response = requests.put(self.url + f'/message/zone/location/{zone};{id_telegram}')
            # else:
            #     response = requests.put(self.url + f'/message/zone/{zone};{km};{id_telegram}')
            # cambio a endpoint en lugar de main
            if zone is None:
                response = requests.put(
                    self.url + f'/player/change_zone/only_km/{id_telegram}:{km}')
            elif km is None:
                response = requests.put(
                    self.url + f'/player/change_zone/only_location/{id_telegram}:{zone}')
            else:
                response = requests.put(
                    self.url + f'/player/change_zone/{id_telegram}:{zone}:{km}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            # return data['message']
            return data['zone_km'], data['zone_location']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def get_matches(self, id_telegram):
        try:
            matches = []
            for key_player_id in ["player_id_1", "player_id_2"]:
                response = requests.get(
                    self.url + f"/provisional_match?{key_player_id}={id_telegram}")
                matches += response.json()
            return matches
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def put_strokes(self, id_telegram, body):
        try:
            # /provisional_match/create/{day}/{time}
            response = requests.put(
                self.url + f'/player/{id_telegram}/strokes',
                json=body
            )
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def get_reserves(self, id_telegram):
        try:
            response = requests.get(
                self.url + f'/reserves/get/{id_telegram}')
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def respond_to_matchmaking(self, id_telegram, information_of_match, accept: bool):
        try:
            # caso aceptar
            if accept:
                url = f'{self.url}{f'/player/match/{id_telegram}/accept'}'
                # response = requests.put(
                #     self.url + f'/player/match/{id_telegram}/accept',
                #     json=information_of_match
                # )
            # caso rechazar
            else:
                url = f'{self.url}{f'/player/match/{id_telegram}/reject'}'
                # response = requests.put(
                #     self.url + f'/player/match/{id_telegram}/reject',
                #     json=information_of_match
                # )
                # data = response.json()
            response = requests.put(
                url,
                json=information_of_match
            )
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'
