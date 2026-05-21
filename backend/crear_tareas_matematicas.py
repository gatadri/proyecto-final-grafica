import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Tarea, Ejercicio, Nino

print('=== CREANDO 3 TAREAS DE MATEMÁTICAS ===\n')

# Obtener un profesor para asignar las tareas
profesor = User.objects.filter(role='profesor').first()
if not profesor:
    print('ERROR: No hay profesores en la base de datos')
    exit(1)

print(f'Profesor asignado: {profesor.nombre} {profesor.apellido}\n')

# Obtener todos los estudiantes
estudiantes = Nino.objects.all()
print(f'Total de estudiantes: {estudiantes.count()}\n')

# Tarea 1: Sumas básicas
print('Creando Tarea 1: Sumas Básicas...')
tarea1 = Tarea.objects.create(
    titulo='Sumas Básicas',
    descripcion='Practica sumas con números del 1 al 20',
    tipo_ejercicio='multiple',
    profesor=profesor
)

ejercicios_tarea1 = [
    {
        'pregunta': '¿Cuánto es 5 + 7?',
        'opciones': ['12', '11', '13', '10'],
        'respuesta_correcta': '12',
        'explicacion': '5 + 7 = 12'
    },
    {
        'pregunta': '¿Cuánto es 8 + 9?',
        'opciones': ['17', '16', '18', '15'],
        'respuesta_correcta': '17',
        'explicacion': '8 + 9 = 17'
    },
    {
        'pregunta': '¿Cuánto es 12 + 6?',
        'opciones': ['18', '17', '19', '16'],
        'respuesta_correcta': '18',
        'explicacion': '12 + 6 = 18'
    },
    {
        'pregunta': '¿Cuánto es 15 + 4?',
        'opciones': ['19', '18', '20', '17'],
        'respuesta_correcta': '19',
        'explicacion': '15 + 4 = 19'
    },
    {
        'pregunta': '¿Cuánto es 11 + 8?',
        'opciones': ['19', '18', '20', '17'],
        'respuesta_correcta': '19',
        'explicacion': '11 + 8 = 19'
    }
]

for i, ej in enumerate(ejercicios_tarea1):
    Ejercicio.objects.create(
        tarea=tarea1,
        pregunta=ej['pregunta'],
        opciones=ej['opciones'],
        respuesta_correcta=ej['respuesta_correcta'],
        explicacion=ej['explicacion'],
        orden=i
    )

tarea1.ninos.set(estudiantes)
print(f'OK - Tarea 1 creada con {len(ejercicios_tarea1)} ejercicios')
print(f'  Asignada a {estudiantes.count()} estudiantes\n')

# Tarea 2: Multiplicaciones
print('Creando Tarea 2: Tablas de Multiplicar...')
tarea2 = Tarea.objects.create(
    titulo='Tablas de Multiplicar',
    descripcion='Practica las tablas del 2, 3 y 5',
    tipo_ejercicio='multiple',
    profesor=profesor
)

ejercicios_tarea2 = [
    {
        'pregunta': '¿Cuánto es 2 × 6?',
        'opciones': ['12', '10', '14', '8'],
        'respuesta_correcta': '12',
        'explicacion': '2 × 6 = 12'
    },
    {
        'pregunta': '¿Cuánto es 3 × 7?',
        'opciones': ['21', '20', '22', '18'],
        'respuesta_correcta': '21',
        'explicacion': '3 × 7 = 21'
    },
    {
        'pregunta': '¿Cuánto es 5 × 4?',
        'opciones': ['20', '15', '25', '10'],
        'respuesta_correcta': '20',
        'explicacion': '5 × 4 = 20'
    },
    {
        'pregunta': '¿Cuánto es 2 × 9?',
        'opciones': ['18', '16', '20', '14'],
        'respuesta_correcta': '18',
        'explicacion': '2 × 9 = 18'
    },
    {
        'pregunta': '¿Cuánto es 3 × 8?',
        'opciones': ['24', '21', '27', '18'],
        'respuesta_correcta': '24',
        'explicacion': '3 × 8 = 24'
    },
    {
        'pregunta': '¿Cuánto es 5 × 6?',
        'opciones': ['30', '25', '35', '20'],
        'respuesta_correcta': '30',
        'explicacion': '5 × 6 = 30'
    }
]

for i, ej in enumerate(ejercicios_tarea2):
    Ejercicio.objects.create(
        tarea=tarea2,
        pregunta=ej['pregunta'],
        opciones=ej['opciones'],
        respuesta_correcta=ej['respuesta_correcta'],
        explicacion=ej['explicacion'],
        orden=i
    )

tarea2.ninos.set(estudiantes)
print(f'OK - Tarea 2 creada con {len(ejercicios_tarea2)} ejercicios')
print(f'  Asignada a {estudiantes.count()} estudiantes\n')

# Tarea 3: Restas
print('Creando Tarea 3: Restas con Números Grandes...')
tarea3 = Tarea.objects.create(
    titulo='Restas con Números Grandes',
    descripcion='Practica restas con números del 10 al 50',
    tipo_ejercicio='multiple',
    profesor=profesor
)

ejercicios_tarea3 = [
    {
        'pregunta': '¿Cuánto es 25 - 8?',
        'opciones': ['17', '16', '18', '15'],
        'respuesta_correcta': '17',
        'explicacion': '25 - 8 = 17'
    },
    {
        'pregunta': '¿Cuánto es 30 - 12?',
        'opciones': ['18', '17', '19', '16'],
        'respuesta_correcta': '18',
        'explicacion': '30 - 12 = 18'
    },
    {
        'pregunta': '¿Cuánto es 45 - 19?',
        'opciones': ['26', '25', '27', '24'],
        'respuesta_correcta': '26',
        'explicacion': '45 - 19 = 26'
    },
    {
        'pregunta': '¿Cuánto es 38 - 15?',
        'opciones': ['23', '22', '24', '21'],
        'respuesta_correcta': '23',
        'explicacion': '38 - 15 = 23'
    },
    {
        'pregunta': '¿Cuánto es 50 - 27?',
        'opciones': ['23', '22', '24', '25'],
        'respuesta_correcta': '23',
        'explicacion': '50 - 27 = 23'
    }
]

for i, ej in enumerate(ejercicios_tarea3):
    Ejercicio.objects.create(
        tarea=tarea3,
        pregunta=ej['pregunta'],
        opciones=ej['opciones'],
        respuesta_correcta=ej['respuesta_correcta'],
        explicacion=ej['explicacion'],
        orden=i
    )

tarea3.ninos.set(estudiantes)
print(f'OK - Tarea 3 creada con {len(ejercicios_tarea3)} ejercicios')
print(f'  Asignada a {estudiantes.count()} estudiantes\n')

print('=== RESUMEN ===')
print(f'OK - 3 tareas de matematicas creadas')
print(f'OK - Total de ejercicios: {len(ejercicios_tarea1) + len(ejercicios_tarea2) + len(ejercicios_tarea3)}')
print(f'OK - Asignadas a {estudiantes.count()} estudiantes')
print(f'\nTareas creadas:')
print(f'  1. {tarea1.titulo} - {tarea1.ejercicios.count()} ejercicios')
print(f'  2. {tarea2.titulo} - {tarea2.ejercicios.count()} ejercicios')
print(f'  3. {tarea3.titulo} - {tarea3.ejercicios.count()} ejercicios')
