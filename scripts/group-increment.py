#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Silvian Dragan
@Date: 11/11/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Script to increment the group number that will be emailed with a reminder.
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

from samaritan.models import GroupRotation


group_rotation = GroupRotation.load()

if group_rotation.group_number:
    if group_rotation.group_number == 4:
        group_rotation.group_number = 1
    else:
        group_rotation.group_number += 1

    print("Group Rotation: " + str(group_rotation.group_number))

    group_rotation.save()
