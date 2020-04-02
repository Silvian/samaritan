"""
@author: Silvian Dragan
@Date: 14/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib import admin
from .models import Profile, MFACode


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
    )


@admin.register(MFACode)
class MFACodeAdmin(admin.ModelAdmin):
    """MFACode admin."""

    list_display = (
        'code',
        'user',
        'expiry_date',
        'created_date',
        'expired',
    )
