#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
python manage.py migrate --settings=apis.settings.dev
gunicorn apis.wsgi