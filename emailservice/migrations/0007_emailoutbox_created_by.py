# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-29 17:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emailservice', '0006_emailoutbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailoutbox',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]