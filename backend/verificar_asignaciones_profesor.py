import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino
from users.models import User

print("="*60)
print("VERIFICANDO ASIGNACIONES DE PROFESORES A NIÑOS")
print("="*60)

# Obtener todos los profesores
profesores = User.objects.filter(role='profesor')
print(f"\nTotal de profesores: {profesores.count()}")

for profesor in profesores:
    ninos = Nino.objects.filter(profesor=profesor)
    print(f"\nProfesor: {profesor.first_name} {profesor.last_name} ({profesor.email})")
    print(f"  - Niños asignados: {ninos.count()}")
    
    if ninos.count() > 0:
        for nino in ninos:
            print(f"    * {nino.nombre} {nino.apellido} (Grado {nino.grado})")

# Obtener niños sin profesor
ninos_sin_profesor = Nino.objects.filter(profesor__isnull=True)
print(f"\n{'='*60}")
print(f"Niños SIN profesor asignado: {ninos_sin_profesor.count()}")

if ninos_sin_profesor.count() > 0:
    print("\nAsignando niños sin profesor al primer profesor disponible...")
    
    if profesores.count() > 0:
        primer_profesor = profesores.first()
        
        for nino in ninos_sin_profesor:
            nino.profesor = primer_profesor
            nino.save()
            print(f"  [OK] {nino.nombre} {nino.apellido} -> {primer_profesor.first_name} {primer_profesor.last_name}")
        
        print(f"\n[OK] {ninos_sin_profesor.count()} niños asignados a {primer_profesor.first_name} {primer_profesor.last_name}")
    else:
        print("\n[ERROR] No hay profesores disponibles para asignar")

print(f"\n{'='*60}")
print("VERIFICACIÓN COMPLETADA")
print("="*60)
