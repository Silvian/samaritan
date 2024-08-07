"""
@author: Silvian Dragan
@Date: 14/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib import admin
from .models import (
    Profile,
    LoginToken,
    MFACode,
    MFACookie,
    MFAConfiguration,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'user',
        'mobile_number',
        'password_strength',
        'password_breached',
        'password_reset',
        'password_last_updated',
        'mfa_enabled',
    )


@admin.register(LoginToken)
class LoginTokenAdmin(admin.ModelAdmin):
    """LoginToken admin."""

    list_display = (
        'token',
        'user',
        'expiry_date',
        'created_date',
        'expired',
    )


@admin.register(MFACode)
class MFACodeAdmin(admin.ModelAdmin):
    """MFACode admin."""

    list_display = (
        'token',
        'code',
        'user',
        'expiry_date',
        'created_date',
        'expired',
    )


@admin.register(MFACookie)
class MFACookieAdmin(admin.ModelAdmin):
    """MFACookie admin."""

    list_display = (
        'id',
        'user',
        'expiry_date',
        'created_date',
        'expired',
    )


@admin.register(MFAConfiguration)
class MFAConfigurationAdmin(admin.ModelAdmin):
    """MFAConfiguration admin."""

    list_display = (
        'name',
        'enabled',
        'active',
    )
