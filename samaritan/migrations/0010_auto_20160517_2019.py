# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-17 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samaritan', '0009_auto_20160517_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='type',
        ),
        migrations.AddField(
            model_name='member',
            name='member_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='samaritan.MembershipType'),
        ),
    ]