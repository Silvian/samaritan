# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samaritan', '0014_auto_20160628_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='churchgroup',
            name='member',
        ),
        migrations.AddField(
            model_name='churchgroup',
            name='member',
            field=models.ManyToManyField(null=True, to='samaritan.Member'),
        ),
    ]