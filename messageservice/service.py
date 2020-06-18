"""SMS service implementation."""

import requests
from django.conf import settings


class SMSService:
    """SMS Service"""
    service_url = ''
    api_token = ''

    def __init__(
            self,
            service_url=settings.SMS_URL,
            api_token=settings.SMS_TOKEN,
            country_code=settings.COUNTRY_CODE,
    ):
        self.service_url = service_url
        self.api_token = api_token
        self.country_code = country_code

    def send_sms(self, message, phone, sender_id=None):
        """Send SMS"""
        response = requests.post(
            url=self.service_url,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_token,
            },
            json={
                'phone': phone,
                'country_code': self.country_code,
                'sender_id': sender_id,
                'message': message,
            }
        ).json()

        return response
