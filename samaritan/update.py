"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""


import os
import shutil
import settings
settings_sample = __import__('settings-sample')
STATUS = "Release"

if settings_sample.STATUS == STATUS:
    replacements = {settings.VERSION: settings_sample.VERSION, settings.STATUS: settings_sample.STATUS}

    with open('settings.py') as infile, open('settings-new.py', 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)

    # cleanup temp file
    shutil.copyfile("settings-new.py", "settings.py")
    os.remove("settings-new.py")
    print("Release performed to version: " + settings_sample.VERSION)
    exit(1)
