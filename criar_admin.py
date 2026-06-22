import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@scae10.com', 'admin123')
    print("Superuser 'admin' criado com sucesso!")
    print("Login: admin")
    print("Senha: admin123")
else:
    print("Superuser 'admin' ja existe")
