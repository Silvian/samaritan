# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-27 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=b'profile_image'),
        ),
    ]