#!/bin/bash

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Roda migrations
python manage.py migrate --noinput

# Inicia Gunicorn
exec gunicorn OFF.wsgi:application --bind 127.0.0.1:8000 --workers 3
