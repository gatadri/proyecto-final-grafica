import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from django.contrib.auth.hashers import make_password

print('=== VERIFICANDO USUARIOS Y CONTRASEÑAS ===\n')

usuarios = User.objects.all().values('id', 'email', 'role', 'activo', 'password')

for u in usuarios:
    tiene_hash = u['password'].startswith('pbkdf2_sha256$') if u['password'] else False
    print(f"ID: {u['id']}")
    print(f"Email: {u['email']}")
    print(f"Role: {u['role']}")
    print(f"Activo: {u['activo']}")
    print(f"Tiene hash válido: {tiene_hash}")
    print(f"Password (primeros 50 chars): {u['password'][:50] if u['password'] else 'None'}")
    print('-' * 60)
