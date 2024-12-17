import requests
from model.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self):
        """Set the base URL for the service."""
        local_server = ["localhost", "127.0.0.1"]
        host = f"{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}"
        self.base_url = f"http://{host}" if settings.GATEWAY_HOST in local_server else f"https://{host}"

    def generate_url(self, endpoint):
        """Generate a full URL from an endpoint."""
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint, params=None, headers=None):
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to {url}, params: {params}")
        response = requests.get(url, params=params, headers=headers)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, headers=None):
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url}, json: {json}")
        response = requests.post(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, headers=None):
        """Send a PUT request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to {url}, json: {json}")
        response = requests.put(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def delete(self, endpoint, headers=None):
        """Send a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle the response, raise an exception for bad responses."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return None
