import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from tareas.models import Nino, Tarea, ProgresoTarea, ProgresoPractica

# ── Limpiar registros previos de progreso ──────────────────────────────────
ProgresoTarea.objects.all().delete()
ProgresoPractica.objects.all().delete()

ninos  = list(Nino.objects.all())
tareas = list(Tarea.objects.all())

if not ninos:
    print("No hay niños en la BD. Ejecuta seed.py primero.")
    exit()

if not tareas:
    print("No hay tareas en la BD. Ejecuta seed.py primero.")
    exit()

# ── Datos de progreso de tareas ────────────────────────────────────────────
# Cada niño tiene al menos 2 registros en tarea_progresotarea
progreso_tareas_data = [
    # (nino_idx, tarea_idx, completada, aciertos, errores, puntos, dias_atras, ms)
    (0, 0, True,  4, 1, 40, 3, 185000),
    (0, 1, True,  3, 2, 30, 1, 210000),
    (1, 0, True,  5, 0, 50, 4, 160000),
    (1, 1, False, 2, 3, 20, 2, 230000),
    (2, 0, True,  4, 1, 40, 5, 195000),
    (2, 1, True,  5, 0, 50, 2, 170000),
    (3, 0, True,  3, 2, 30, 6, 220000),
    (3, 1, True,  4, 1, 40, 3, 200000),
    (4, 0, True,  5, 0, 50, 2, 155000),
    (4, 1, False, 1, 4, 10, 1, 260000),
    (5, 0, True,  4, 1, 40, 4, 180000),
    (5, 1, True,  3, 2, 30, 2, 215000),
]

for nino_idx, tarea_idx, completada, aciertos, errores, puntos, dias, ms in progreso_tareas_data:
    if nino_idx >= len(ninos) or tarea_idx >= len(tareas):
        continue
    nino  = ninos[nino_idx]
    tarea = tareas[tarea_idx]
    # Solo crear si el niño tiene esa tarea asignada
    if not tarea.ninos.filter(id=nino.id).exists():
        tarea.ninos.add(nino)
    fecha = timezone.now() - timedelta(days=dias)
    ProgresoTarea.objects.update_or_create(
        nino=nino, tarea=tarea,
        defaults={
            'completada':        completada,
            'puntos_obtenidos':  puntos,
            'fecha_completada':  fecha if completada else None,
            'cantidad_aciertos': aciertos,
            'cantidad_errores':  errores,
            'tiempo_total_ms':   ms,
        }
    )

print(f"✓ ProgresoTarea: {ProgresoTarea.objects.count()} registros creados")

# ── Datos de progreso de prácticas ─────────────────────────────────────────
# Cada niño tiene al menos 2 sesiones de práctica en tarea_progresopractica
practicas_data = [
    # (nino_idx, aciertos, errores, puntos, dificultad, tipo, dias_atras, ms)
    (0, 5, 1, 5, 3, 'multiple',        2, 120000),
    (0, 3, 3, 3, 2, 'completar',       1, 145000),
    (1, 6, 0, 6, 4, 'multiple',        3, 110000),
    (1, 4, 2, 4, 3, 'verdadero_falso', 1, 130000),
    (2, 5, 1, 5, 3, 'multiple',        4, 125000),
    (2, 2, 4, 2, 1, 'completar',       2, 160000),
    (3, 4, 2, 4, 2, 'multiple',        5, 135000),
    (3, 6, 0, 6, 4, 'verdadero_falso', 1, 108000),
    (4, 3, 3, 3, 2, 'multiple',        3, 150000),
    (4, 5, 1, 5, 3, 'completar',       1, 118000),
    (5, 6, 0, 6, 4, 'multiple',        2, 105000),
    (5, 4, 2, 4, 3, 'verdadero_falso', 1, 140000),
]

for nino_idx, aciertos, errores, puntos, dificultad, tipo, dias, ms in practicas_data:
    if nino_idx >= len(ninos):
        continue
    nino  = ninos[nino_idx]
    fecha = timezone.now() - timedelta(days=dias)
    ProgresoPractica.objects.create(
        nino              = nino,
        completada        = True,
        puntos_obtenidos  = puntos,
        cantidad_aciertos = aciertos,
        cantidad_errores  = errores,
        tiempo_total_ms   = ms,
        dificultad        = dificultad,
        tipo_ejercicio    = tipo,
        fecha_practica    = fecha,
    )

print(f"✓ ProgresoPractica: {ProgresoPractica.objects.count()} registros creados")
print("\nResumen por niño:")
for nino in ninos:
    pt = ProgresoTarea.objects.filter(nino=nino).count()
    pp = ProgresoPractica.objects.filter(nino=nino).count()
    print(f"  {nino.nombre}: {pt} tareas, {pp} prácticas")
