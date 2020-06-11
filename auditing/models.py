# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from enum import Enum
from django.utils import timezone
from django.db import models
from django_common.auth_backends import User
from samaritan.models import Member


class ActionsTypes(Enum):
    CREATE_MEMBER = "CREATE MEMBER"
    DELETE_MEMBER = "DELETE MEMBER"
    UPDATE_MEMBER = "UPDATE MEMBER"
    ARCHIVE_MEMBER = "ARCHIVE MEMBER"
    UNARCHIVE_MEMBER = "UNARCHIVE MEMBER"

    @classmethod
    def choices(cls):
        return tuple((key.name, key.value) for key in cls)


class ActivityLog(models.Model):
    """Activity log for user actions"""

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=100,
        choices=ActionsTypes.choices(),
    )

    date = models.DateTimeField(
        default=timezone.now,
    )

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.id)
