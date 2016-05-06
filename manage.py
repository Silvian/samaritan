#!/usr/bin/env python
"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "samaritan.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
