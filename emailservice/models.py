"""
@author: Silvian Dragan
@Date: 07/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

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


class BirthdayEmailGreetingConfiguration(SingletonModel):
    """BirthdayEmailGreetingConfiguration data model."""

    name = models.CharField(
        max_length=200,
        default='Birthdays Email Greeting Configurations',
    )
    threshold = models.IntegerField(default=1900)
    subject = models.CharField(max_length=500)
    greeting = models.TextField()
    excluded_roles = models.ManyToManyField(ChurchRole)
    send_emails = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BirthdaysListConfiguration(SingletonModel):
    """BirthdaysListConfiguration data model."""

    name = models.CharField(
        max_length=200,
        default='Birthday List Configurations',
    )
    subject = models.CharField(max_length=500)
    sending_day = models.IntegerField(default=5)
    week_cycle = models.IntegerField(default=7)
    recipient_roles = models.ManyToManyField(ChurchRole)
    send_emails = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GroupRotationConfiguration(SingletonModel):
    """GroupRotationConfiguration data model."""

    name = models.CharField(
        max_length=200,
        default='Church Group Rotation Configurations',
    )
    group_name = models.CharField(max_length=200)
    group_number = models.IntegerField()
    email_subject = models.CharField(max_length=500)
    email_message = models.TextField()
    send_emails = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PasswordResetEmailConfiguration(SingletonModel):
    """PasswordResetEmailConfiguration data model."""

    name = models.CharField(
        max_length=200,
        default='Password Reset Email Configurations',
    )
    email_subject = models.CharField(max_length=200)
    email_message = models.TextField()
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WelcomeEmailConfiguration(SingletonModel):
    """WelcomeEmailConfiguration data model."""

    name = models.CharField(
        max_length=200,
        default='Welcome Email Configurations',
    )
    email_subject = models.CharField(max_length=200)
    email_message = models.TextField()
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.name
