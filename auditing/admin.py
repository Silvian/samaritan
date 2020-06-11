# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """Activity admin."""

    list_display = (
        'id',
        'user',
        'member',
        'action',
        'date',
    )

    list_filter = (
        'action',
    )

    search_fields = (
        'user__username',
        'member__first_name',
        'member__last_name',
    )
