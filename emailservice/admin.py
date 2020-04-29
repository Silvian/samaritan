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
    BirthdayEmailGreetingConfiguration,
    BirthdaysListConfiguration,
    GroupRotationConfiguration,
    PasswordResetEmailConfiguration,
    WelcomeEmailConfiguration,
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


@admin.register(WelcomeEmailConfiguration)
class WelcomeEmailConfigurationAdmin(admin.ModelAdmin):
    """WelcomeEmailConfiguration admin."""

    list_display = (
        'name',
        'email_subject',
        'email_message',
        'send_email',
    )
