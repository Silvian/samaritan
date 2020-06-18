"""Message service admin."""

from django.contrib import admin
from messageservice.models import SMSMessageConfiguration


@admin.register(SMSMessageConfiguration)
class SMSMessageAdmin(admin.ModelAdmin):
    """SMSMessage admin."""
    list_display = (
        'name',
        'sender_name',
        'counter',
        'send_message',
    )
