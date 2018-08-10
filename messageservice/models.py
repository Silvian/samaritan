# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from emailservice.models import SingletonModel
from django.db import models


# Create your models here.

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
