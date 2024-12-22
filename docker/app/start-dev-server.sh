#!/bin/sh
echo "Running migrations.."
python manage.py migrate

echo "Create admin user..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
import os
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
EOF

echo "Starting server.."
python manage.py runserver 0.0.0.0:8000
