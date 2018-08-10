# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from messageservice.models import SMSMessageConfiguration

# Register your models here.


@admin.register(SMSMessageConfiguration)
class SMSMessageAdmin(admin.ModelAdmin):
    """SMSMessage admin."""
    list_display = (
        'name',
        'send_message',
    )