import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

print('Asignando profesores a niños sin profesor...\n')

# Obtener profesores disponibles
profesores = list(User.objects.filter(role='profesor'))
if not profesores:
    print('ERROR: No hay profesores disponibles')
    exit(1)

print(f'Profesores disponibles: {len(profesores)}')
for p in profesores:
    print(f'  - {p.nombre} {p.apellido}')

# Obtener niños sin profesor
ninos_sin_profesor = Nino.objects.filter(profesor__isnull=True)
count = ninos_sin_profesor.count()

if count == 0:
    print('\nTodos los niños ya tienen profesor asignado')
else:
    print(f'\nNiños sin profesor: {count}')
    
    # Asignar profesores de manera balanceada
    for i, nino in enumerate(ninos_sin_profesor):
        profesor = profesores[i % len(profesores)]
        nino.profesor = profesor
        nino.save()
        print(f'  - {nino.nombre} {nino.apellido} -> {profesor.nombre} {profesor.apellido}')
    
    print(f'\nOK - {count} niños asignados a profesores')

# Verificar distribución
print('\n=== DISTRIBUCIÓN DE ESTUDIANTES ===')
for p in profesores:
    estudiantes = Nino.objects.filter(profesor=p)
    print(f'{p.nombre} {p.apellido}: {estudiantes.count()} estudiantes')
