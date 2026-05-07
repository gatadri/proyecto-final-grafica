import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import EjercicioPractica

ejercicios = [
    # Matemáticas
    {'pregunta': '¿Cuánto es 5 + 3?', 'opciones': ['8', '7', '9', '6'], 'respuesta_correcta': '8', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 1},
    {'pregunta': '¿Cuánto es 12 - 4?', 'opciones': ['8', '7', '9', '6'], 'respuesta_correcta': '8', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 1},
    {'pregunta': '¿Cuánto es 6 × 2?', 'opciones': ['12', '10', '14', '8'], 'respuesta_correcta': '12', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 1},
    {'pregunta': '¿Cuánto es 15 ÷ 3?', 'opciones': ['5', '4', '6', '3'], 'respuesta_correcta': '5', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 1},
    {'pregunta': '¿Cuánto es 7 + 8?', 'opciones': ['15', '14', '16', '13'], 'respuesta_correcta': '15', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 1},
    {'pregunta': '¿Cuánto es 20 - 7?', 'opciones': ['13', '12', '14', '11'], 'respuesta_correcta': '13', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 1},
    {'pregunta': '¿Cuánto es 9 × 3?', 'opciones': ['27', '24', '30', '21'], 'respuesta_correcta': '27', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 2},
    {'pregunta': '¿Cuánto es 24 ÷ 4?', 'opciones': ['6', '5', '7', '8'], 'respuesta_correcta': '6', 'tipo_ejercicio': 'multiple', 'categoria': 'matematicas', 'dificultad': 2},
    
    # Lengua
    {'pregunta': '¿Cuál es el plural de "casa"?', 'opciones': ['casas', 'casaes', 'casis', 'casases'], 'respuesta_correcta': 'casas', 'tipo_ejercicio': 'multiple', 'categoria': 'lengua', 'dificultad': 1},
    {'pregunta': '¿Qué palabra es un verbo?', 'opciones': ['correr', 'mesa', 'azul', 'rápido'], 'respuesta_correcta': 'correr', 'tipo_ejercicio': 'multiple', 'categoria': 'lengua', 'dificultad': 1},
    {'pregunta': '¿Cuál es el sinónimo de "feliz"?', 'opciones': ['alegre', 'triste', 'enojado', 'cansado'], 'respuesta_correcta': 'alegre', 'tipo_ejercicio': 'multiple', 'categoria': 'lengua', 'dificultad': 1},
    {'pregunta': '¿Cuál es el antónimo de "grande"?', 'opciones': ['pequeño', 'enorme', 'alto', 'largo'], 'respuesta_correcta': 'pequeño', 'tipo_ejercicio': 'multiple', 'categoria': 'lengua', 'dificultad': 1},
    
    # Ciencias
    {'pregunta': '¿Cuántos planetas hay en el sistema solar?', 'opciones': ['8', '7', '9', '10'], 'respuesta_correcta': '8', 'tipo_ejercicio': 'multiple', 'categoria': 'ciencias', 'dificultad': 1},
    {'pregunta': '¿Qué animal es un mamífero?', 'opciones': ['perro', 'pez', 'serpiente', 'águila'], 'respuesta_correcta': 'perro', 'tipo_ejercicio': 'multiple', 'categoria': 'ciencias', 'dificultad': 1},
    {'pregunta': '¿Qué necesitan las plantas para crecer?', 'opciones': ['agua y luz', 'solo agua', 'solo luz', 'nada'], 'respuesta_correcta': 'agua y luz', 'tipo_ejercicio': 'multiple', 'categoria': 'ciencias', 'dificultad': 1},
    {'pregunta': '¿Cuál es el planeta más cercano al Sol?', 'opciones': ['Mercurio', 'Venus', 'Tierra', 'Marte'], 'respuesta_correcta': 'Mercurio', 'tipo_ejercicio': 'multiple', 'categoria': 'ciencias', 'dificultad': 2},
    
    # Inglés
    {'pregunta': '¿Cómo se dice "perro" en inglés?', 'opciones': ['dog', 'cat', 'bird', 'fish'], 'respuesta_correcta': 'dog', 'tipo_ejercicio': 'multiple', 'categoria': 'ingles', 'dificultad': 1},
    {'pregunta': '¿Cómo se dice "casa" en inglés?', 'opciones': ['house', 'home', 'building', 'room'], 'respuesta_correcta': 'house', 'tipo_ejercicio': 'multiple', 'categoria': 'ingles', 'dificultad': 1},
    {'pregunta': '¿Qué significa "hello"?', 'opciones': ['hola', 'adiós', 'gracias', 'por favor'], 'respuesta_correcta': 'hola', 'tipo_ejercicio': 'multiple', 'categoria': 'ingles', 'dificultad': 1},
    {'pregunta': '¿Qué significa "thank you"?', 'opciones': ['gracias', 'hola', 'adiós', 'perdón'], 'respuesta_correcta': 'gracias', 'tipo_ejercicio': 'multiple', 'categoria': 'ingles', 'dificultad': 1},
]

print('Creando ejercicios de práctica...')
for ej in ejercicios:
    EjercicioPractica.objects.get_or_create(
        pregunta=ej['pregunta'],
        defaults=ej
    )

print(f'OK - {len(ejercicios)} ejercicios de practica creados')
