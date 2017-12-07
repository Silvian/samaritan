#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Silvian Dragan
@Date: 11/11/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Script to send reminders to the group in charge based on a rotation period.
"""

import os
import sys

proj_path = ""
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "samaritan.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from samaritan.models import ChurchGroup
from emailservice.models import GroupRotationConfiguration
from emailservice.mail import send_email
import samaritan.settings as settings


group_rotation = GroupRotationConfiguration.load()
group_name = "{} {}".format(group_rotation.group_name, group_rotation.group_number)

print("GROUP NAME: " + group_name)

group = ChurchGroup.objects.get(name=group_name)

for member in group.members.order_by('last_name').filter(is_active=True):

    if member.email:
        print "Sending group notification to: " + member.last_name + " " + member.first_name
        if not send_email(settings.CHURCH_EMAIL, settings.CHURCH_NAME, member.first_name,
                          member.email, settings.GROUP_EMAIL_TITLE, settings.GROUP_EMAIL_MESSAGE):
            print "Failed to send email to the following recipient: " + member.email




