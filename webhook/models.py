# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from samaritan.base_models import SingletonModel
from samaritan.models import ChurchRole, MembershipType


class WebhookConfiguration(SingletonModel):
    name = models.CharField(
        max_length=50,
        default='Webhook configuration'
    )
    default_role = models.ForeignKey(
        ChurchRole,
        on_delete=models.PROTECT,
    )
    default_membership_type = models.ForeignKey(
        MembershipType,
        on_delete=models.PROTECT,
    )
    enabled = models.BooleanField(
        default=False,
    )

    def __str__(self):
        """Return the string representation"""
        return self.name
