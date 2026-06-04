import os
import sys
import django
import re

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Ejercicio, Tarea

def detectar_tema_subtema(pregunta):
    """Detecta el tema y subtema basándose en el contenido de la pregunta."""
    pregunta_lower = pregunta.lower()
    
    # Detectar multiplicación y tabla específica
    match_mult = re.search(r'(\d+)\s*×\s*(\d+)|(\d+)\s*x\s*(\d+)', pregunta)
    if match_mult or '×' in pregunta or 'multiplica' in pregunta_lower:
        # Extraer los números
        numeros = re.findall(r'\d+', pregunta)
        if numeros:
            numeros = [int(n) for n in numeros if int(n) >= 2 and int(n) <= 12]
            if numeros:
                tabla = max(numeros)  # Usar el número más grande como tabla
                return f'tabla_{tabla}', 'multiplicacion'
        return 'multiplicacion_general', 'multiplicacion'
    
    # Detectar división
    if '÷' in pregunta or '/' in pregunta or 'divide' in pregunta_lower or 'division' in pregunta_lower:
        numeros = re.findall(r'\d+', pregunta)
        if numeros and len(numeros) >= 2:
            divisor = int(numeros[1]) if len(numeros) > 1 else int(numeros[0])
            if divisor >= 2 and divisor <= 12:
                return f'division_entre_{divisor}', 'division'
        return 'division_general', 'division'
    
    # Detectar fracciones
    if '/' in pregunta and any(c.isdigit() for c in pregunta):
        if '+' in pregunta:
            return 'suma_fracciones', 'fracciones'
        elif '-' in pregunta:
            return 'resta_fracciones', 'fracciones'
        elif '×' in pregunta or 'multiplica' in pregunta_lower:
            return 'multiplicacion_fracciones', 'fracciones'
        elif '÷' in pregunta or 'divide' in pregunta_lower:
            return 'division_fracciones', 'fracciones'
        return 'fracciones_general', 'fracciones'
    
    # Detectar suma
    if '+' in pregunta:
        return 'suma', 'aritmetica'
    
    # Detectar resta
    if '-' in pregunta and not re.search(r'\d+\s*-\s*\d+\s*=', pregunta):
        return 'resta', 'aritmetica'
    
    # Detectar álgebra
    if 'x' in pregunta_lower and '=' in pregunta and not '×' in pregunta:
        return 'ecuaciones', 'algebra'
    
    # Detectar geometría
    if any(word in pregunta_lower for word in ['área', 'perímetro', 'volumen', 'triángulo', 'cuadrado', 'círculo']):
        return 'geometria_figuras', 'geometria'
    
    # Por defecto
    return 'general', 'matematicas'

def etiquetar_ejercicios():
    """Etiqueta todos los ejercicios existentes con tema y subtema."""
    ejercicios = Ejercicio.objects.all()
    total = ejercicios.count()
    actualizados = 0
    
    print(f"Encontrados {total} ejercicios para etiquetar")
    print("-" * 60)
    
    for ej in ejercicios:
        tema, subtema = detectar_tema_subtema(ej.pregunta)
        ej.tema = tema
        ej.subtema = subtema
        ej.save()
        actualizados += 1
        
        # Mostrar algunos ejemplos
        if actualizados <= 10:
            print(f"#{ej.id}: {ej.pregunta[:50]}...")
            print(f"   -> Tema: {tema}, Subtema: {subtema}")
            print()
    
    print("-" * 60)
    print(f"Total actualizado: {actualizados} ejercicios")
    
    # Mostrar resumen por tema
    print("\nResumen por tema:")
    temas = {}
    for ej in Ejercicio.objects.all():
        key = f"{ej.subtema} - {ej.tema}"
        temas[key] = temas.get(key, 0) + 1
    
    for tema, cantidad in sorted(temas.items(), key=lambda x: x[1], reverse=True):
        print(f"   {tema}: {cantidad} ejercicios")

if __name__ == '__main__':
    etiquetar_ejercicios()
