import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from django.db import connection
from django.db import reset_queries
from users.models import User
from tareas.models import Nino, ProgresoTarea
from django.db.models import Sum, Avg, Count, Q

# Habilitar logging de queries
from django.conf import settings
settings.DEBUG = True

print('=== TABLAS Y CONSULTAS SQL PARA ESTADÍSTICAS DEL PADRE ===\n')

# Resetear queries
reset_queries()

# Obtener un padre
padre = User.objects.filter(role='padre').first()
print(f'1. OBTENER PADRE')
print(f'   Tabla: users_user')
print(f'   SQL: {connection.queries[-1]["sql"]}\n')

# Obtener hijos del padre
hijos = Nino.objects.filter(padre=padre)
print(f'2. OBTENER HIJOS DEL PADRE')
print(f'   Tabla: tareas_nino')
print(f'   SQL: {connection.queries[-1]["sql"]}\n')

# Para cada hijo, obtener su progreso
for hijo in hijos:
    print(f'3. OBTENER PROGRESO DE {hijo.nombre}')
    progresos = ProgresoTarea.objects.filter(nino=hijo, completada=True)
    print(f'   Tabla: tareas_progresotarea')
    print(f'   SQL: {connection.queries[-1]["sql"]}\n')
    
    # Agregaciones (aciertos, errores, tiempo promedio)
    stats = progresos.aggregate(
        total_aciertos=Sum('cantidad_aciertos'),
        total_errores=Sum('cantidad_errores'),
        promedio_tiempo=Avg('tiempo_total_ms')
    )
    print(f'4. AGREGACIONES (SUM, AVG) PARA {hijo.nombre}')
    print(f'   Tabla: tareas_progresotarea')
    print(f'   SQL: {connection.queries[-1]["sql"]}\n')
    
    # Última actividad
    ultima = progresos.order_by('-fecha_completada').first()
    if ultima:
        print(f'5. ÚLTIMA ACTIVIDAD DE {hijo.nombre}')
        print(f'   Tabla: tareas_progresotarea')
        print(f'   SQL: {connection.queries[-1]["sql"]}\n')

# Estadísticas grupales
print(f'6. TOTAL DE TAREAS COMPLETADAS (GRUPAL)')
total_tareas = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).count()
print(f'   Tabla: tareas_progresotarea')
print(f'   SQL: {connection.queries[-1]["sql"]}\n')

print(f'7. TOTALES GRUPALES (ACIERTOS Y ERRORES)')
totales = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).aggregate(
    total_aciertos=Sum('cantidad_aciertos'),
    total_errores=Sum('cantidad_errores')
)
print(f'   Tabla: tareas_progresotarea')
print(f'   SQL: {connection.queries[-1]["sql"]}\n')

print(f'8. TOTALES DE HIJOS (MONEDAS Y NIVEL PROMEDIO)')
totales_hijos = hijos.aggregate(
    total_monedas=Sum('monedas'),
    promedio_nivel=Avg('nivel')
)
print(f'   Tabla: tareas_nino')
print(f'   SQL: {connection.queries[-1]["sql"]}\n')

print(f'9. HIJO MÁS ACTIVO')
hijo_mas_activo = hijos.annotate(
    num_tareas=Count('progreso_tareas', filter=Q(progreso_tareas__completada=True))
).order_by('-num_tareas').first()
print(f'   Tablas: tareas_nino JOIN tareas_progresotarea')
print(f'   SQL: {connection.queries[-1]["sql"]}\n')

print('\n=== RESUMEN DE TABLAS UTILIZADAS ===')
print('1. users_user - Para obtener información del padre')
print('2. tareas_nino - Para obtener los hijos del padre')
print('3. tareas_progresotarea - Para obtener el progreso de tareas (aciertos, errores, tiempo)')
print('\nTotal de consultas ejecutadas:', len(connection.queries))
