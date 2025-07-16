from uuid import UUID
from .base_service import BaseService
from core.config import settings


class PaymentsService(BaseService):

    def __init__(self):
        """Set the base URL for the service."""
        self._set_base_url(settings.PAYMENTS_SERVICE_HOST,
                           settings.PAYMENTS_SERVICE_PORT)
        self.set_prefix_url("/api/v1")
        self.x_api_key_header = {
            "x-api-key": settings.PAYMENTS_SERVICE_API_KEY}

    def create_payment(self, user_public_id: UUID, match_public_id: UUID):
        payload = {
            "user_public_id": user_public_id,
            "match_public_id": match_public_id
        }
        return self.post("/payments", json=payload)
