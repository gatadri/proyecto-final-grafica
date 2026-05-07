import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User

print('Corrigiendo roles mal escritos...\n')

# Corregir "pofesor" a "profesor"
usuarios_incorrectos = User.objects.filter(role='pofesor')
count = usuarios_incorrectos.count()

if count > 0:
    print(f'Encontrados {count} usuarios con rol "pofesor":')
    for u in usuarios_incorrectos:
        print(f'  - {u.nombre} {u.apellido} ({u.email})')
        u.role = 'profesor'
        u.save()
    print(f'\nOK - {count} usuarios corregidos a "profesor"')
else:
    print('No se encontraron usuarios con rol incorrecto')

# Verificar
print('\n=== PROFESORES ACTUALES ===')
profesores = User.objects.filter(role='profesor')
for p in profesores:
    print(f'  - {p.nombre} {p.apellido} ({p.email})')
