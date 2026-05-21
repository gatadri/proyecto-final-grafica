import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

print('=== ASIGNANDO PROFESORES A NIÑOS ===\n')

# Obtener todos los profesores
profesores = User.objects.filter(role='profesor', activo=True)

if not profesores.exists():
    print('No hay profesores disponibles en el sistema.')
    exit()

print(f'Profesores disponibles: {profesores.count()}\n')

# Obtener niños sin profesor
ninos_sin_profesor = Nino.objects.filter(profesor__isnull=True)

if not ninos_sin_profesor.exists():
    print('Todos los niños ya tienen profesor asignado.')
    exit()

print(f'Niños sin profesor: {ninos_sin_profesor.count()}\n')

# Asignar profesores de forma equitativa
profesor_index = 0
for nino in ninos_sin_profesor:
    profesor = profesores[profesor_index % profesores.count()]
    nino.profesor = profesor
    nino.save()
    print(f'Asignado: {nino.nombre} {nino.apellido} -> Profesor: {profesor.nombre} {profesor.apellido}')
    profesor_index += 1

print(f'\n=== ASIGNACIÓN COMPLETADA ===')
print(f'Total de niños asignados: {ninos_sin_profesor.count()}')

# Mostrar resumen por profesor
print('\n=== RESUMEN POR PROFESOR ===\n')
for profesor in profesores:
    estudiantes = Nino.objects.filter(profesor=profesor)
    print(f'{profesor.nombre} {profesor.apellido}: {estudiantes.count()} estudiantes')
    for est in estudiantes:
        print(f'  - {est.nombre} {est.apellido}')
