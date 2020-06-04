# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from webhook.models import WebhookConfiguration


@admin.register(WebhookConfiguration)
class WebhookConfigurationAdmin(admin.ModelAdmin):
    """WebhookConfiguration admin."""

    list_display = (
        'name',
        'default_role',
        'enabled',
    )
