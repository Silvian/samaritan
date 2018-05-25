"""
@author: Silvian Dragan
@Date: 07/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib import admin
from .models import (
    ChurchEmailConfiguration,
    BirthdayEmailGreetingConfiguration,
    BirthdaysListConfiguration,
    GroupRotationConfiguration,
    PasswordResetEmailConfiguration,
)


@admin.register(ChurchEmailConfiguration)
class ChurchEmailConfigurationAdmin(admin.ModelAdmin):
    """ChurchEmailConfiguration admin."""

    list_display = (
        'name',
        'church_signature',
        'church_email',
    )


@admin.register(BirthdayEmailGreetingConfiguration)
class BirthdayEmailGreetingConfigurationAdmin(admin.ModelAdmin):
    """BirthdayEmailGreetingConfiguration admin."""

    list_display = (
        'name',
        'threshold',
        'subject',
        'greeting',
        'send_emails',
    )


@admin.register(BirthdaysListConfiguration)
class BirthdaysListConfigurationAdmin(admin.ModelAdmin):
    """BirthdaysListConfiguration admin."""

    list_display = (
        'name',
        'subject',
        'sending_day',
        'week_cycle',
        'send_emails',
    )


@admin.register(GroupRotationConfiguration)
class GroupRotationConfigurationAdmin(admin.ModelAdmin):
    """GroupRotationConfiguration admin."""

    list_display = (
        'name',
        'group_name',
        'group_number',
        'email_subject',
        'email_message',
        'send_emails',
    )


@admin.register(PasswordResetEmailConfiguration)
class PasswordResetEmailConfigurationAdmin(admin.ModelAdmin):
    """PasswordResetEmailConfiguration admin."""

    list_display = (
        'name',
        'email_subject',
        'email_message',
        'send_email',
    )
