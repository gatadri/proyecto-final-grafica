import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

print('=== PROFESORES Y SUS ESTUDIANTES ===\n')

profesores = User.objects.filter(role='profesor').order_by('nombre')

for profesor in profesores:
    estudiantes = Nino.objects.filter(profesor=profesor)
    count = estudiantes.count()
    
    print(f'{profesor.nombre} {profesor.apellido} ({profesor.email})')
    print(f'  ID: {profesor.id}')
    print(f'  Total estudiantes: {count}')
    
    if count > 0:
        print(f'  Estudiantes:')
        for estudiante in estudiantes:
            padre_info = f' - Padre: {estudiante.padre.nombre} {estudiante.padre.apellido}' if estudiante.padre else ' - Sin padre'
            print(f'    - {estudiante.nombre} {estudiante.apellido} (PIN: {estudiante.pin}){padre_info}')
    else:
        print(f'  Sin estudiantes asignados')
    
    print()

print('\n=== RESUMEN ===')
total_profesores = profesores.count()
profesores_con_estudiantes = profesores.filter(estudiantes__isnull=False).distinct().count()
profesores_sin_estudiantes = total_profesores - profesores_con_estudiantes

print(f'Total profesores: {total_profesores}')
print(f'Profesores con estudiantes: {profesores_con_estudiantes}')
print(f'Profesores sin estudiantes: {profesores_sin_estudiantes}')
print(f'Total estudiantes: {Nino.objects.count()}')
