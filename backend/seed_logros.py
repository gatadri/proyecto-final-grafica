import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Logro

print('=== POBLANDO LOGROS EN LA BASE DE DATOS ===\n')

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
        'rareza': 'bronce',
        'condicion': 'tareas_completadas',
        'valor_requerido': 5,
        'puntos_bonus': 25
    },
    {
        'nombre': 'Maestro del Aprendizaje',
        'descripcion': 'Completa 10 tareas',
        'icono': 'graduation-cap',
        'rareza': 'plata',
        'condicion': 'tareas_completadas',
        'valor_requerido': 10,
        'puntos_bonus': 50
    },
    {
        'nombre': 'Experto Académico',
        'descripcion': 'Completa 25 tareas',
        'icono': 'trophy',
        'rareza': 'oro',
        'condicion': 'tareas_completadas',
        'valor_requerido': 25,
        'puntos_bonus': 100
    },
    {
        'nombre': 'Leyenda del Conocimiento',
        'descripcion': 'Completa 50 tareas',
        'icono': 'crown',
        'rareza': 'legendario',
        'condicion': 'tareas_completadas',
        'valor_requerido': 50,
        'puntos_bonus': 250
    },
    {
        'nombre': 'Perfeccionista',
        'descripcion': 'Completa una tarea sin errores',
        'icono': 'check-circle',
        'rareza': 'plata',
        'condicion': 'tareas_perfectas',
        'valor_requerido': 1,
        'puntos_bonus': 30
    },
    {
        'nombre': 'Racha de Fuego',
        'descripcion': 'Mantén una racha de 3 días',
        'icono': 'fire',
        'rareza': 'bronce',
        'condicion': 'racha_dias',
        'valor_requerido': 3,
        'puntos_bonus': 20
    },
    {
        'nombre': 'Constancia Imparable',
        'descripcion': 'Mantén una racha de 7 días',
        'icono': 'fire',
        'rareza': 'plata',
        'condicion': 'racha_dias',
        'valor_requerido': 7,
        'puntos_bonus': 50
    },
    {
        'nombre': 'Dedicación Absoluta',
        'descripcion': 'Mantén una racha de 30 días',
        'icono': 'fire',
        'rareza': 'oro',
        'condicion': 'racha_dias',
        'valor_requerido': 30,
        'puntos_bonus': 200
    },
    {
        'nombre': 'Velocista del Saber',
        'descripcion': 'Responde 10 preguntas rápidamente',
        'icono': 'bolt',
        'rareza': 'plata',
        'condicion': 'respuestas_rapidas',
        'valor_requerido': 10,
        'puntos_bonus': 40
    },
    {
        'nombre': 'Nivel 5',
        'descripcion': 'Alcanza el nivel 5',
        'icono': 'level-up-alt',
        'rareza': 'bronce',
        'condicion': 'nivel_alcanzado',
        'valor_requerido': 5,
        'puntos_bonus': 30
    },
    {
        'nombre': 'Nivel 10',
        'descripcion': 'Alcanza el nivel 10',
        'icono': 'level-up-alt',
        'rareza': 'plata',
        'condicion': 'nivel_alcanzado',
        'valor_requerido': 10,
        'puntos_bonus': 75
    },
    {
        'nombre': 'Nivel 20',
        'descripcion': 'Alcanza el nivel 20',
        'icono': 'level-up-alt',
        'rareza': 'oro',
        'condicion': 'nivel_alcanzado',
        'valor_requerido': 20,
        'puntos_bonus': 150
    },
    {
        'nombre': 'Coleccionista de Monedas',
        'descripcion': 'Acumula 100 monedas',
        'icono': 'coins',
        'rareza': 'bronce',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 100,
        'puntos_bonus': 20
    },
    {
        'nombre': 'Millonario del Saber',
        'descripcion': 'Acumula 500 monedas',
        'icono': 'coins',
        'rareza': 'plata',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 500,
        'puntos_bonus': 50
    },
    {
        'nombre': 'Magnate Académico',
        'descripcion': 'Acumula 1000 monedas',
        'icono': 'coins',
        'rareza': 'oro',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 1000,
        'puntos_bonus': 100
    },
]

print('Creando Logros...')
for logro_data in logros_data:
    logro, created = Logro.objects.get_or_create(
        nombre=logro_data['nombre'],
        defaults=logro_data
    )
    if created:
        print(f'  OK Creado: {logro.nombre} ({logro.rareza}) - {logro.puntos_bonus} puntos bonus')
    else:
        print(f'  - Ya existe: {logro.nombre}')

print(f'\n=== LOGROS POBLADOS EXITOSAMENTE ===')
print(f'Total Logros: {Logro.objects.count()}')

# Mostrar resumen por rareza
print('\nResumen por rareza:')
for rareza in ['bronce', 'plata', 'oro', 'legendario']:
    count = Logro.objects.filter(rareza=rareza).count()
    print(f'  {rareza.capitalize()}: {count}')
