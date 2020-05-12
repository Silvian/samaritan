"""
@author: Silvian Dragan
@Date: 07/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from enum import Enum

from django.db import models
from django.utils import timezone
from django_common.auth_backends import User

from samaritan.base_models import SingletonModel
from samaritan.models import ChurchRole


class EmailOutbox(models.Model):
    """Email outbox model."""

    subject = models.CharField(
        max_length=255,
    )
    message = models.TextField()

    attachment = models.FileField(
        blank=True,
        null=True,
        upload_to='attachments',
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    created_date = models.DateTimeField(
        default=timezone.now,
    )

    def __str__(self):
        return self.message


class ChurchEmailConfiguration(SingletonModel):
    """ChurchEmailConfiguration data model."""

    name = models.CharField(
        max_length=200,
        default='Church Email Configurations',
    )
    church_signature = models.CharField(max_length=500)
    church_email = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class EmailTypes(Enum):
    WELCOME_EMAIL = "WELCOME EMAIL"
    PASSWORD_RESET = "PASSWORD RESET"
    BIRTHDAY_LIST = "BIRTHDAY LIST"
    BIRTHDAY_GREETING = "BIRTHDAY GREETING"

    @classmethod
    def choices(cls):
        return tuple((key.name, key.value) for key in cls)


class EmailConfiguration(models.Model):
    """Email configuration data model."""

    type = models.CharField(
        choices=EmailTypes.choices(),
        primary_key=True,
        max_length=100,
        unique=True,
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    subject = models.CharField(
        max_length=200,
    )
    message = models.TextField()
    scheduled_day = models.IntegerField(
        null=True,
        blank=True,
    )
    recipient_roles = models.ManyToManyField(
        ChurchRole,
        related_name="recipient",
        blank=True,
    )
    excluded_roles = models.ManyToManyField(
        ChurchRole,
        related_name="excluded",
        blank=True,
    )
    send_email = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.type)
