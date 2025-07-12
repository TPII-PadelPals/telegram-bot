import requests
from core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.GATEWAY_HOST, settings.GATEWAY_PORT)
        self.x_api_key_header = {"x-api-key": ""}

    def _set_base_url(self, host: str = "localhost", port: int | None = None) -> None:
        """Set the base URL for the service."""
        local_server = ["localhost", "127.0.0.1"]
        private_prod_server = ["172.31.33.238", "172.31.40.104", "172.31.39.179", "172.31.34.23"]
        service_url = f"{host}:{port}" if port is not None else f"{host}"
        self.base_url = (
            f"http://{service_url}"
            if host in local_server or host in private_prod_server
            else f"https://{service_url}"
        )

    def generate_url(self, endpoint):
        """Generate a full URL from an endpoint."""
        if settings.ENV == 'prod':
            return f"{settings.GATEWAY_HOST}/api/v1{endpoint}"
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint, params=None, headers={}):
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        headers.update(self.x_api_key_header)
        logger.info(
            f"GET request to {url}, params: {params}, headers={headers}")
        response = requests.get(url, params=params, headers=headers)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, headers={}):
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url}, json: {json}")
        headers.update(self.x_api_key_header)
        response = requests.post(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def patch(self, endpoint, data=None, json=None, headers={}):
        """Send a PATCH request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH request to {url}, json: {json}")
        headers.update(self.x_api_key_header)
        response = requests.patch(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, headers={}):
        """Send a PUT request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to {url}, json: {json}")
        headers.update(self.x_api_key_header)
        response = requests.put(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def delete(self, endpoint, headers={}):
        """Send a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        headers.update(self.x_api_key_header)
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle the response, raise an exception for bad responses."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.info(f"Request error {e}")
            return None

    def set_prefix_url(self, prefix):
        self.base_url += prefix
        return
