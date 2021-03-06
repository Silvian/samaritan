# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('samaritan', '0018_auto_20160628_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthdayEmailGreetingConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Birthdays Email Greeting Configurations', max_length=200)),
                ('threshold', models.IntegerField(default=1900)),
                ('subject', models.CharField(max_length=500)),
                ('greeting', models.TextField()),
                ('send_greeting', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BirthdaysListConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Birthday List Configurations', max_length=200)),
                ('subject', models.CharField(max_length=500)),
                ('sending_day', models.IntegerField(default=5)),
                ('week_cycle', models.IntegerField(default=7)),
                ('send_list', models.BooleanField(default=False)),
                ('recipient_roles', models.ManyToManyField(to='samaritan.ChurchRole')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChurchEmailConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Church Email Configurations', max_length=200)),
                ('church_signature', models.CharField(max_length=500)),
                ('church_email', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupRotationConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Church Group Rotation Configurations', max_length=200)),
                ('group_name', models.CharField(max_length=200)),
                ('group_number', models.IntegerField()),
                ('email_subject', models.CharField(max_length=500)),
                ('email_message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
