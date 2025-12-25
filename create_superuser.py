# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'beto')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'betower24@gmail.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'beto12345678')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Superusuario {username} creado exitosamente')
else:
    print(f'⚠️ El superusuario {username} ya existe')
