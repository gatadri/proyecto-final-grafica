import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino, ProgresoTarea
from django.db.models import Sum, Avg

print('=== VERIFICANDO DATOS DE LA BASE DE DATOS ===\n')

# Obtener un padre
padre = User.objects.filter(role='padre').first()
if not padre:
    print('No hay padres en la base de datos')
    exit(1)

print(f'Padre: {padre.nombre} {padre.apellido} (ID: {padre.id})')
print(f'Email: {padre.email}\n')

# Obtener hijos del padre
hijos = Nino.objects.filter(padre=padre)
print(f'Total de hijos: {hijos.count()}\n')

# Estadísticas de cada hijo
for hijo in hijos:
    print(f'--- {hijo.nombre} {hijo.apellido} ---')
    
    # Obtener progresos del hijo
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
    
    print(f'  Nivel: {hijo.nivel}')
    print(f'  Experiencia: {hijo.experiencia} XP')
    print(f'  Monedas: {hijo.monedas}')
    print(f'  Racha: {hijo.racha_dias} días')
    print(f'  Tareas completadas: {progresos.count()}')
    print(f'  Total aciertos: {total_aciertos}')
    print(f'  Total errores: {total_errores}')
    print(f'  Tasa de éxito: {tasa_exito:.1f}%')
    print(f'  Tiempo promedio: {int(stats["promedio_tiempo"] or 0)} ms')
    print()

# Estadísticas grupales
print('=== ESTADÍSTICAS GRUPALES ===')
total_tareas = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).count()
totales = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).aggregate(
    total_aciertos=Sum('cantidad_aciertos'),
    total_errores=Sum('cantidad_errores')
)

print(f'Total tareas completadas: {total_tareas}')
print(f'Total aciertos: {totales["total_aciertos"] or 0}')
print(f'Total errores: {totales["total_errores"] or 0}')
print(f'Total monedas: {sum(h.monedas for h in hijos)}')
print(f'Nivel promedio: {sum(h.nivel for h in hijos) / hijos.count():.1f}')
