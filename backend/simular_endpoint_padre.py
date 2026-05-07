import os
import django
import json
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino, ProgresoTarea
from django.db.models import Sum, Avg, Count, Q

# Obtener un padre
padre = User.objects.filter(role='padre').first()
print(f'=== SIMULANDO ENDPOINT: /api/padre/{padre.id}/estadisticas-hijos ===\n')

hijos = Nino.objects.filter(padre=padre)

# Estadísticas individuales
estadisticas_individuales = []

for hijo in hijos:
    progresos = ProgresoTarea.objects.filter(nino=hijo, completada=True)
    
    stats = progresos.aggregate(
        total_aciertos=Sum('cantidad_aciertos'),
        total_errores=Sum('cantidad_errores'),
        promedio_tiempo=Avg('tiempo_total_ms')
    )
    
    total_aciertos = stats['total_aciertos'] or 0
    total_errores = stats['total_errores'] or 0
    total = total_aciertos + total_errores
    tasa_exito = (total_aciertos / total * 100) if total > 0 else 0
    
    ultima_actividad = progresos.order_by('-fecha_completada').first()
    
    estadisticas_individuales.append({
        'id': hijo.id,
        'nombre': hijo.nombre,
        'apellido': hijo.apellido,
        'nivel': hijo.nivel,
        'experiencia': hijo.experiencia,
        'monedas': hijo.monedas,
        'racha_dias': hijo.racha_dias,
        'tareas_completadas': progresos.count(),
        'total_aciertos': total_aciertos,
        'total_errores': total_errores,
        'promedio_tiempo_ms': int(stats['promedio_tiempo'] or 0),
        'tasa_exito': round(tasa_exito, 1),
        'ultima_actividad': ultima_actividad.fecha_completada.strftime('%d/%m/%Y') if ultima_actividad else None
    })

# Estadísticas grupales
total_tareas = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).count()

totales_grupales = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).aggregate(
    total_aciertos=Sum('cantidad_aciertos'),
    total_errores=Sum('cantidad_errores')
)

totales_hijos = hijos.aggregate(
    total_monedas=Sum('monedas'),
    promedio_nivel=Avg('nivel')
)

# Hijo más activo
hijo_mas_activo = hijos.annotate(
    num_tareas=Count('progreso_tareas', filter=Q(progreso_tareas__completada=True))
).order_by('-num_tareas').first()

# Mejor rendimiento
mejor_hijo = None
mejor_tasa = 0
for stats in estadisticas_individuales:
    if stats['tasa_exito'] > mejor_tasa:
        mejor_tasa = stats['tasa_exito']
        mejor_hijo = f"{stats['nombre']} {stats['apellido']}"

# Rendimiento semanal
hoy = datetime.now().date()
rendimiento_semanal = []
dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

for i in range(7):
    dia = hoy - timedelta(days=6-i)
    progresos_dia = ProgresoTarea.objects.filter(
        nino__in=hijos,
        fecha_completada__date=dia,
        completada=True
    ).aggregate(
        aciertos=Sum('cantidad_aciertos'),
        errores=Sum('cantidad_errores')
    )
    
    rendimiento_semanal.append({
        'dia': dias_semana[dia.weekday()],
        'aciertos': progresos_dia['aciertos'] or 0,
        'errores': progresos_dia['errores'] or 0
    })

estadisticas_grupales = {
    'total_hijos': hijos.count(),
    'total_tareas_completadas': total_tareas,
    'total_aciertos': totales_grupales['total_aciertos'] or 0,
    'total_errores': totales_grupales['total_errores'] or 0,
    'promedio_nivel': round(totales_hijos['promedio_nivel'] or 0, 1),
    'total_monedas': totales_hijos['total_monedas'] or 0,
    'hijo_mas_activo': f"{hijo_mas_activo.nombre} {hijo_mas_activo.apellido}" if hijo_mas_activo else 'N/A',
    'mejor_rendimiento': mejor_hijo or 'N/A',
    'rendimiento_semanal': rendimiento_semanal
}

# Respuesta completa
respuesta = {
    'estadisticas_individuales': estadisticas_individuales,
    'estadisticas_grupales': estadisticas_grupales
}

print(json.dumps(respuesta, indent=2, ensure_ascii=False))
