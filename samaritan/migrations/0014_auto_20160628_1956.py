# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samaritan', '0013_member_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='churchgroup',
            name='member',
        ),
        migrations.AddField(
            model_name='churchgroup',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='samaritan.Member'),
        ),
    ]
