"""Message service models."""

from samaritan.base_models import SingletonModel
from django.db import models


class SMSMessageConfiguration(SingletonModel):
    name = models.CharField(
        max_length=50,
        default='SMS Message'
    )
    sender_name = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    send_message = models.BooleanField(
        default=False,
    )
    counter = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        """Return the string representation"""
        return self.name
