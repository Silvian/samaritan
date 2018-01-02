#!/bin/bash

sleep 5
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'root@admin.com', 'root')" | python manage.py shell
python manage.py createmembershiptypes
python manage.py createdefaultchurchrole
python manage.py runserver 0.0.0.0:8000
