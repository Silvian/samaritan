# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samaritan', '0016_auto_20160628_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churchgroup',
            name='member',
            field=models.ManyToManyField(blank=True, to='samaritan.Member'),
        ),
    ]
