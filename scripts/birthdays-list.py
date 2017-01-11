#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Silvian Dragan
@Date: 20/12/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Script to send out the birthdays list to church elder at the start of every month for the previous month.
"""

import os
import sys

from datetime import date

proj_path = "/home/cecilia/PycharmProjects/samaritan"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "samaritan.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from samaritan.models import Member, ChurchRole
from emailservice.mail import send_list_email
import samaritan.settings as settings

# get everyone from members list including guests
everyone = Member.objects.filter(is_active=True)

# get today's date
today = date.today()

# get last month
last_month = today.month - 1

if last_month == 0:
    last_month = 12

birthdays_list = []

if settings.SEND_BIRTHDAYS_LIST and settings.BIRTHDAYS_LIST_SUBJECT != "":
    if today.day <= settings.WEEK_CYCLE and today.weekday() == settings.SENDING_DAY:

        for member in everyone:
            if member.date_of_birth.month == last_month:
                birthdays_list.append(member)


# get church roles from config
church_role_set = ChurchRole.objects.filter(pk__in=settings.RECIPIENT_ROLES)
recipients_list = []

for church_role in church_role_set:
    role_members = Member.objects.filter(church_role=church_role, is_active=True)
    for recipient in role_members:
        recipients_list.append(recipient)


# if the birthday list is not empty send it to all recipients from the recipient_list
if birthdays_list:
    for recipient in recipients_list:
        if not send_list_email(settings.CHURCH_EMAIL, settings.CHURCH_NAME, recipient.first_name,
                          recipient.email, settings.BIRTHDAYS_LIST_SUBJECT, birthdays_list):
            print "Failed to send email to the following recipient: " + recipient.email
