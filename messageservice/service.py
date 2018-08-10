"""SMS service implementation."""

import requests
from django.conf import settings


class SMSService:
    """SMS Service"""
    service_url = ''
    api_token = ''

    def __init__(self, service_url=settings.SMS_URL, api_token=settings.SMS_TOKEN):
        self.service_url = service_url
        self.api_token = api_token

    def send_sms(self, message, phone):
        """Send SMS"""
        response = requests.post(
            self.service_url,
            {
                'phone': phone,
                'message': message,
                'key': self.api_token
            }).json()

        return response
