"""
@author: Silvian Dragan
@Date: 07/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib import admin
from .models import (
    EmailOutbox,
    ChurchEmailConfiguration,
    EmailConfiguration,
)


@admin.register(EmailOutbox)
class EmailOutbox(admin.ModelAdmin):
    """EmailOutbox admin."""

    list_display = (
        'subject',
        'message',
        'attachment',
        'created_by',
        'created_date',
    )


@admin.register(ChurchEmailConfiguration)
class ChurchEmailConfigurationAdmin(admin.ModelAdmin):
    """ChurchEmailConfiguration admin."""

    list_display = (
        'name',
        'church_signature',
        'church_email',
    )


@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(admin.ModelAdmin):
    """EmailConfiguration admin."""

    list_display = (
        'type',
        'description',
        'subject',
        'message',
        'send_email',
    )
