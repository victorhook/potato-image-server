#!/bin/bash

PY_ENV=/home/victor/coding/web/potato-image-server/env
APP_ENV=/home/victor/coding/web/potato-image-server/potato_image_server

cd $PY_ENV
. bin/activate

cd $APP_ENV
python manage.py livereload & python manage.py runserver