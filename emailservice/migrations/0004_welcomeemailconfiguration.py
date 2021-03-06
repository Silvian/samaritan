# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-29 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailservice', '0003_passwordresetemailconfiguration'),
    ]

    operations = [
        migrations.CreateModel(
            name='WelcomeEmailConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Welcome Email Configurations', max_length=200)),
                ('email_subject', models.CharField(max_length=200)),
                ('email_message', models.TextField()),
                ('send_email', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
