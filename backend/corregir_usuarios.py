import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User

print('=== CORRIGIENDO USUARIOS ===\n')

# Obtener usuarios con problemas
usuarios_problema = User.objects.filter(id__gte=24)

for usuario in usuarios_problema:
    print(f'Corrigiendo: {usuario.email}')
    
    # Corregir rol a minúsculas
    if usuario.role.isupper():
        usuario.role = usuario.role.lower()
        print(f'  - Role cambiado a: {usuario.role}')
    
    # Verificar si la contraseña no está hasheada
    if not usuario.password.startswith('pbkdf2_sha256$'):
        password_plano = usuario.password
        usuario.set_password(password_plano)
        print(f'  - Contraseña hasheada correctamente')
    
    usuario.save()
    print(f'  OK Usuario guardado\n')

print('=== CORRECCIÓN COMPLETADA ===')
print('\nVerificando usuarios corregidos:\n')

usuarios_corregidos = User.objects.filter(id__gte=24).values('id', 'email', 'role', 'password')
for u in usuarios_corregidos:
    tiene_hash = u['password'].startswith('pbkdf2_sha256$')
    print(f"{u['email']} | Role: {u['role']} | Hash válido: {tiene_hash}")
