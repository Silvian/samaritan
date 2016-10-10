#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Silvian Dragan
@Date: 10/10/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Script to send out a greetings email if any active member has a birthday on the current date.
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

from samaritan.models import Member
from emailservice.mail import send_email
import samaritan.settings as settings

# get everyone from members list including guests
everyone = Member.objects.filter(is_active=True)

# get today's date
today = date.today()

if settings.SEND_GREETINGS and settings.BIRTHDAY_SUBJECT != "" and settings.BIRTHDAY_GREETING != "":

    for member in everyone:

        # check each member's date of birth matches current day and month
        if member.date_of_birth.month == today.month and member.date_of_birth.day == today.day:
            print "Sending greeting: " + member.last_name + " " + member.first_name
            if member.email is not None and member.email != "":
                if not send_email(settings.CHURCH_EMAIL, settings.CHURCH_NAME, member.first_name,
                                  member.email, settings.BIRTHDAY_SUBJECT, settings.BIRTHDAY_GREETING):
                    print "Failed to send email to the following recipient: "+member.email
