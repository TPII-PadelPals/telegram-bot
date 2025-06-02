from uuid import UUID
from .base_service import BaseService
from core.config import settings


class BusinessService(BaseService):

    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.BUSINESS_SERVICE_HOST,
                           settings.BUSINESS_SERVICE_PORT)
        self.set_prefix_url("/api/v1")
        self.x_api_key_header = {
            "x-api-key": settings.BUSINESS_SERVICE_API_KEY}

    def get_business(self, business_public_id: UUID):
        """get business"""
        info = self.get(
            "/businesses/", params={"business_public_id": business_public_id, "limit": 1})
        return info['data'][0]

    def get_court(self, court_public_id: UUID):
        """get business"""
        info = self.get(
            "/padel-courts/", params={"court_public_id": court_public_id, "limit": 1})
        return info['data'][0]
