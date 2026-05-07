import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, Tarea, ProgresoTarea
from django.db.models import Sum

print('Poblando datos de progreso de tareas...\n')

ninos = list(Nino.objects.all())
tareas = list(Tarea.objects.all())

if not ninos or not tareas:
    print('ERROR: No hay niños o tareas en la base de datos')
    exit(1)

print(f'Niños: {len(ninos)}, Tareas: {len(tareas)}')

# Crear progresos para los últimos 7 días
hoy = datetime.now()
count = 0

for i in range(7):
    dia = hoy - timedelta(days=6-i)
    
    # Seleccionar algunos niños aleatorios para este día
    ninos_dia = random.sample(ninos, min(len(ninos), random.randint(5, 15)))
    
    for nino in ninos_dia:
        # Seleccionar algunas tareas aleatorias
        tareas_nino = random.sample(tareas, min(len(tareas), random.randint(1, 3)))
        
        for tarea in tareas_nino:
            # Verificar si ya existe
            if ProgresoTarea.objects.filter(nino=nino, tarea=tarea).exists():
                continue
            
            # Generar datos aleatorios
            num_ejercicios = tarea.ejercicios.count() or 5
            aciertos = random.randint(int(num_ejercicios * 0.5), num_ejercicios)
            errores = num_ejercicios - aciertos
            puntos = aciertos * 10
            tiempo = random.randint(60000, 300000)  # 1-5 minutos
            
            ProgresoTarea.objects.create(
                nino=nino,
                tarea=tarea,
                completada=True,
                puntos_obtenidos=puntos,
                cantidad_aciertos=aciertos,
                cantidad_errores=errores,
                tiempo_total_ms=tiempo,
                fecha_completada=dia
            )
            count += 1

print(f'\nOK - {count} registros de progreso creados')

# Mostrar resumen
total_aciertos = ProgresoTarea.objects.filter(completada=True).aggregate(
    total=Sum('cantidad_aciertos')
)['total'] or 0

total_errores = ProgresoTarea.objects.filter(completada=True).aggregate(
    total=Sum('cantidad_errores')
)['total'] or 0

print(f'\nResumen:')
print(f'  Total aciertos: {total_aciertos}')
print(f'  Total errores: {total_errores}')
print(f'  Tasa de éxito: {(total_aciertos / (total_aciertos + total_errores) * 100):.1f}%')
