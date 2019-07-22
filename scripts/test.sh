#!/usr/bin/env bash

docker-compose run --rm web python manage.py test && codecov -t CODECOV_TOKEN
