#!/bin/sh
cd /code && \
python manage.py migrate --noinput && \
python manage.py runserver 0.0.0.0:8000 && \
manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
