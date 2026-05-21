import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, Logro, LogroNino

print('=== CREANDO LOGROS ===\n')

# Crear logros si no existen
logros_data = [
    {
        'nombre': 'Primera Tarea',
        'descripcion': 'Completa tu primera tarea',
        'icono': 'star',
        'rareza': 'bronce',
        'condicion': 'tareas_completadas',
        'valor_requerido': 1,
        'puntos_bonus': 10
    },
    {
        'nombre': 'Estudiante Dedicado',
        'descripcion': 'Completa 5 tareas',
        'icono': 'book',
        'rareza': 'plata',
        'condicion': 'tareas_completadas',
        'valor_requerido': 5,
        'puntos_bonus': 25
    },
    {
        'nombre': 'Coleccionista de Monedas',
        'descripcion': 'Acumula 50 monedas',
        'icono': 'coins',
        'rareza': 'bronce',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 50,
        'puntos_bonus': 15
    },
    {
        'nombre': 'Rico en Monedas',
        'descripcion': 'Acumula 100 monedas',
        'icono': 'coins',
        'rareza': 'plata',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 100,
        'puntos_bonus': 30
    },
    {
        'nombre': 'Racha Inicial',
        'descripcion': 'Mantén una racha de 3 días',
        'icono': 'fire',
        'rareza': 'bronce',
        'condicion': 'racha_dias',
        'valor_requerido': 3,
        'puntos_bonus': 20
    }
]

logros_creados = []
for logro_data in logros_data:
    logro, created = Logro.objects.get_or_create(
        nombre=logro_data['nombre'],
        defaults=logro_data
    )
    if created:
        print(f'OK - Logro creado: {logro.nombre}')
    else:
        print(f'  - Logro ya existe: {logro.nombre}')
    logros_creados.append(logro)

print(f'\nTotal de logros: {len(logros_creados)}\n')

# Buscar a Jose y Alejandra
jose = Nino.objects.filter(nombre='Jose', pin='7895').first()
alejandra = Nino.objects.filter(nombre='Alejandra', pin='8778').first()

if not jose or not alejandra:
    print('ERROR: No se encontraron Jose o Alejandra')
    exit(1)

print('=== ASIGNANDO LOGROS ===\n')

# Verificar estadísticas de Jose
from tareas.models import ProgresoTarea
tareas_jose = ProgresoTarea.objects.filter(nino=jose, completada=True).count()
print(f'Jose (PIN: 7895):')
print(f'  Tareas completadas: {tareas_jose}')
print(f'  Monedas: {jose.monedas}')
print(f'  Racha: {jose.racha_dias} dias')

# Asignar logros a Jose
logros_jose = []
for logro in logros_creados:
    cumple = False
    
    if logro.condicion == 'tareas_completadas' and tareas_jose >= logro.valor_requerido:
        cumple = True
    elif logro.condicion == 'monedas_acumuladas' and jose.monedas >= logro.valor_requerido:
        cumple = True
    elif logro.condicion == 'racha_dias' and jose.racha_dias >= logro.valor_requerido:
        cumple = True
    
    if cumple:
        logro_nino, created = LogroNino.objects.get_or_create(
            nino=jose,
            logro=logro
        )
        if created:
            jose.monedas += logro.puntos_bonus
            logros_jose.append(logro.nombre)
            print(f'  OK - Logro desbloqueado: {logro.nombre} (+{logro.puntos_bonus} monedas)')

if logros_jose:
    jose.save()
    print(f'  Total logros: {len(logros_jose)}')
    print(f'  Monedas totales: {jose.monedas}\n')
else:
    print('  No cumple requisitos para logros\n')

# Verificar estadísticas de Alejandra
tareas_alejandra = ProgresoTarea.objects.filter(nino=alejandra, completada=True).count()
print(f'Alejandra (PIN: 8778):')
print(f'  Tareas completadas: {tareas_alejandra}')
print(f'  Monedas: {alejandra.monedas}')
print(f'  Racha: {alejandra.racha_dias} dias')

# Asignar logros a Alejandra
logros_alejandra = []
for logro in logros_creados:
    cumple = False
    
    if logro.condicion == 'tareas_completadas' and tareas_alejandra >= logro.valor_requerido:
        cumple = True
    elif logro.condicion == 'monedas_acumuladas' and alejandra.monedas >= logro.valor_requerido:
        cumple = True
    elif logro.condicion == 'racha_dias' and alejandra.racha_dias >= logro.valor_requerido:
        cumple = True
    
    if cumple:
        logro_nino, created = LogroNino.objects.get_or_create(
            nino=alejandra,
            logro=logro
        )
        if created:
            alejandra.monedas += logro.puntos_bonus
            logros_alejandra.append(logro.nombre)
            print(f'  OK - Logro desbloqueado: {logro.nombre} (+{logro.puntos_bonus} monedas)')

if logros_alejandra:
    alejandra.save()
    print(f'  Total logros: {len(logros_alejandra)}')
    print(f'  Monedas totales: {alejandra.monedas}\n')
else:
    print('  No cumple requisitos para logros\n')

print('=== RESUMEN ===')
print(f'Jose: {len(logros_jose)} logros - {jose.monedas} monedas')
print(f'Alejandra: {len(logros_alejandra)} logros - {alejandra.monedas} monedas')
