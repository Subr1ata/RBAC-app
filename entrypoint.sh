#!/bin/sh
# cd /app/auth

echo "📦 Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🚀 Starting server..."
exec python manage.py runserver 0.0.0.0:8000
