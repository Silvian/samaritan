"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main admin data models import configurations file for the Samaritan CMA app.
"""

from django.contrib import admin
from .models import (
    Address,
    Member,
    ChurchRole,
    ChurchGroup,
    MembershipType,
)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Address admin."""

    list_display = (
        'number',
        'street',
        'locality',
        'city',
        'post_code',
    )

    search_fields = (
        'number',
        'street',
        'locality',
        'city',
        'post_code',
    )

    list_filter = (
        'city',
        'locality',
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Member admin."""

    list_display = (
        'first_name',
        'last_name',
        'date_of_birth',
        'telephone',
        'email',
    )

    search_fields = (
        'first_name',
        'last_name',
        'date_of_birth',
        'telephone',
        'email',
    )

    list_filter = (
        'is_active',
        'is_member',
        'is_baptised',
    )


@admin.register(ChurchRole)
class ChurchRoleAdmin(admin.ModelAdmin):
    """ChurchRole admin."""

    list_display = (
        'name',
        'description',
    )

    search_fields = ('name',)


@admin.register(ChurchGroup)
class ChurchGroupAdmin(admin.ModelAdmin):
    """ChurchGroup admin."""

    list_display = (
        'name',
        'description',
    )

    search_fields = ('name',)


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    """MembershipType admin."""

    list_display = (
        'name',
        'description',
    )

    search_fields = ('name',)
