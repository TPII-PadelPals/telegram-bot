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
            response = requests.post(self.url + f'/message/availability/{time};{id_telegram}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            return data['message']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def set_zone(self, zone: str, km: int, id_telegram):
        # se supone que esto no ocurra nunca por las llamadas del bot
        if zone is None and km is None:
            raise ValueError('Zone or km must be provided')
        try:
            if zone is None:
                response = requests.post(self.url + f'/message/zone/km/{km};{id_telegram}')
            elif km is None:
                response = requests.post(self.url + f'/message/zone/location/{zone};{id_telegram}')
            else:
                response = requests.post(self.url + f'/message/zone/{zone};{km};{id_telegram}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            return data['message']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'
