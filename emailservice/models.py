"""
@author: Silvian Dragan
@Date: 07/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.db import models
from samaritan.models import ChurchRole


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ChurchEmailConfiguration(SingletonModel):
    name = models.CharField(
        max_length=200,
        default='Church Email Configurations',
    )
    church_signature = models.CharField(max_length=500)
    church_email = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class BirthdayEmailGreetingConfiguration(SingletonModel):
    name = models.CharField(
        max_length=200,
        default='Birthdays Email Greeting Configurations',
    )
    threshold = models.IntegerField(default=1900)
    subject = models.CharField(max_length=500)
    greeting = models.TextField()
    send_emails = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BirthdaysListConfiguration(SingletonModel):
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
    name = models.CharField(
        max_length=200,
        default='Password Reset Email Configurations',
    )
    email_subject = models.CharField(max_length=200)
    email_message = models.TextField()
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.name
