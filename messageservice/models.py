"""Message service models."""

from emailservice.models import SingletonModel
from django.db import models


class SMSMessageConfiguration(SingletonModel):
    name = models.CharField(
        max_length=50,
        default='SMS Message'
    )
    send_message = models.BooleanField(
        default=False,
    )
    counter = models.PositiveIntegerField()

    quota_remaining = models.PositiveIntegerField()

    def __str__(self):
        """Return the string representation"""
        return self.name
