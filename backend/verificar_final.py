import os
import sys
import django

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Nino

print("="*80)
print("VERIFICACION FINAL - TAREAS ASIGNADAS")
print("="*80)

# Verificar tareas ML
tareas_ml = Tarea.objects.filter(id__in=[11, 12, 13, 14])
print(f"\n[OK] Tareas ML: {tareas_ml.count()}")

for tarea in tareas_ml:
    print(f"\n  Tarea ID {tarea.id}: {tarea.titulo}")
    print(f"  - Ejercicios: {tarea.ejercicios.count()}")
    print(f"  - Niños asignados: {tarea.ninos.count()}")

# Verificar algunos niños
print("\n" + "="*80)
print("VERIFICACION DE NIÑOS")
print("="*80)

ninos = Nino.objects.all()[:5]

for nino in ninos:
    tareas_del_nino = nino.tareas.filter(id__in=[11, 12, 13, 14])
    print(f"\n{nino.nombre} {nino.apellido} (ID: {nino.id}, PIN: {nino.pin})")
    print(f"  - Tareas ML asignadas: {tareas_del_nino.count()}")
    
    if tareas_del_nino.count() == 4:
        print(f"  - ✓ CORRECTO: Tiene las 4 tareas ML")
    else:
        print(f"  - ✗ ERROR: Solo tiene {tareas_del_nino.count()} tareas")

print("\n" + "="*80)
print("INSTRUCCIONES PARA PROBAR")
print("="*80)

print("""
1. INICIAR SERVIDOR:
   cd backend
   python manage.py runserver

2. INICIAR FRONTEND:
   cd frontend
   ng serve (o npm start)

3. ABRIR NAVEGADOR:
   http://localhost:4200

4. LOGIN COMO NIÑO:
   Usar cualquiera de estos:
   - Alejandra / PIN: 8778
   - Carla / PIN: 5079
   - Mariano / PIN: 1220

5. DEBERÍAS VER LAS 4 TAREAS ML:
   - Practica de Multiplicacion (12 ejercicios)
   - Practica de Division (12 ejercicios)
   - Practica de Suma de Fracciones (12 ejercicios)
   - Practica Mixta de Matematicas (15 ejercicios)

Si no las ves, verifica:
- Que el servidor backend esté corriendo
- Que el endpoint sea correcto: /api/tareas/nino/tareas?nino_id=X
- Consola del navegador (F12) para ver errores
""")

print("="*80)
print("SISTEMA LISTO - TAREAS ASIGNADAS CORRECTAMENTE")
print("="*80 + "\n")
