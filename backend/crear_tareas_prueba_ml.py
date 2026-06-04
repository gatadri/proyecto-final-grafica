import os
import sys
import django
import random
from fractions import Fraction

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Ejercicio, Nino
from users.models import User


def generar_multiplicacion():
    """Genera ejercicio de multiplicación"""
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    resultado = a * b
    
    # Generar opciones incorrectas
    opciones = [str(resultado)]
    while len(opciones) < 4:
        incorrecto = resultado + random.randint(-10, 10)
        if incorrecto > 0 and str(incorrecto) not in opciones:
            opciones.append(str(incorrecto))
    
    random.shuffle(opciones)
    
    return {
        'pregunta': f'¿Cuánto es {a} × {b}?',
        'opciones': opciones,
        'respuesta_correcta': str(resultado),
        'explicacion': f'{a} × {b} = {resultado}'
    }


def generar_division():
    """Genera ejercicio de división exacta"""
    b = random.randint(2, 10)
    cociente = random.randint(2, 12)
    a = b * cociente
    
    # Generar opciones incorrectas
    opciones = [str(cociente)]
    while len(opciones) < 4:
        incorrecto = cociente + random.randint(-5, 5)
        if incorrecto > 0 and str(incorrecto) not in opciones:
            opciones.append(str(incorrecto))
    
    random.shuffle(opciones)
    
    return {
        'pregunta': f'¿Cuánto es {a} ÷ {b}?',
        'opciones': opciones,
        'respuesta_correcta': str(cociente),
        'explicacion': f'{a} ÷ {b} = {cociente}'
    }


def generar_suma_fracciones():
    """Genera ejercicio de suma de fracciones"""
    # Generar fracciones simples con mismo denominador
    denominador = random.choice([2, 3, 4, 5, 6, 8, 10])
    num1 = random.randint(1, denominador - 1)
    num2 = random.randint(1, denominador - 1)
    
    # Calcular resultado
    resultado = Fraction(num1, denominador) + Fraction(num2, denominador)
    resultado_str = f"{resultado.numerator}/{resultado.denominator}"
    
    # Generar opciones incorrectas
    opciones = [resultado_str]
    while len(opciones) < 4:
        num_inc = random.randint(1, num1 + num2 + 3)
        den_inc = random.choice([denominador, resultado.denominator])
        opcion = f"{num_inc}/{den_inc}"
        if opcion not in opciones and opcion != resultado_str:
            opciones.append(opcion)
    
    random.shuffle(opciones)
    
    return {
        'pregunta': f'¿Cuánto es {num1}/{denominador} + {num2}/{denominador}?',
        'opciones': opciones,
        'respuesta_correcta': resultado_str,
        'explicacion': f'{num1}/{denominador} + {num2}/{denominador} = {resultado_str}'
    }


def crear_tarea_multiplicacion(profesor, ninos):
    """Crea tarea de multiplicación con 12 ejercicios"""
    print("\n[*] Creando tarea de MULTIPLICACION...")
    
    tarea = Tarea.objects.create(
        titulo="Práctica de Multiplicación",
        descripcion="Resuelve las siguientes multiplicaciones. ¡Concéntrate!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    # Asignar a todos los niños
    tarea.ninos.set(ninos)
    
    # Crear 12 ejercicios
    for i in range(12):
        ejercicio_data = generar_multiplicacion()
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=ejercicio_data['pregunta'],
            opciones=ejercicio_data['opciones'],
            respuesta_correcta=ejercicio_data['respuesta_correcta'],
            explicacion=ejercicio_data['explicacion'],
            orden=i + 1
        )
    
    print(f"    [OK] Tarea creada con ID: {tarea.id}")
    print(f"    [OK] 12 ejercicios de multiplicación creados")
    print(f"    [OK] Asignada a {ninos.count()} niños")
    return tarea


def crear_tarea_division(profesor, ninos):
    """Crea tarea de división con 12 ejercicios"""
    print("\n[*] Creando tarea de DIVISION...")
    
    tarea = Tarea.objects.create(
        titulo="Práctica de División",
        descripcion="Resuelve las siguientes divisiones. ¡Tómate tu tiempo!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    # Asignar a todos los niños
    tarea.ninos.set(ninos)
    
    # Crear 12 ejercicios
    for i in range(12):
        ejercicio_data = generar_division()
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=ejercicio_data['pregunta'],
            opciones=ejercicio_data['opciones'],
            respuesta_correcta=ejercicio_data['respuesta_correcta'],
            explicacion=ejercicio_data['explicacion'],
            orden=i + 1
        )
    
    print(f"    [OK] Tarea creada con ID: {tarea.id}")
    print(f"    [OK] 12 ejercicios de división creados")
    print(f"    [OK] Asignada a {ninos.count()} niños")
    return tarea


def crear_tarea_fracciones(profesor, ninos):
    """Crea tarea de suma de fracciones con 12 ejercicios"""
    print("\n[*] Creando tarea de SUMA DE FRACCIONES...")
    
    tarea = Tarea.objects.create(
        titulo="Práctica de Suma de Fracciones",
        descripcion="Resuelve las siguientes sumas de fracciones. ¡Recuerda sumar los numeradores!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    # Asignar a todos los niños
    tarea.ninos.set(ninos)
    
    # Crear 12 ejercicios
    for i in range(12):
        ejercicio_data = generar_suma_fracciones()
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=ejercicio_data['pregunta'],
            opciones=ejercicio_data['opciones'],
            respuesta_correcta=ejercicio_data['respuesta_correcta'],
            explicacion=ejercicio_data['explicacion'],
            orden=i + 1
        )
    
    print(f"    [OK] Tarea creada con ID: {tarea.id}")
    print(f"    [OK] 12 ejercicios de fracciones creados")
    print(f"    [OK] Asignada a {ninos.count()} niños")
    return tarea


def crear_tarea_mixta(profesor, ninos):
    """Crea tarea mixta con 15 ejercicios variados"""
    print("\n[*] Creando tarea MIXTA...")
    
    tarea = Tarea.objects.create(
        titulo="Práctica Mixta de Matemáticas",
        descripcion="Ejercicios variados de multiplicación, división y fracciones. ¡Pon atención!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    # Asignar a todos los niños
    tarea.ninos.set(ninos)
    
    # Crear 15 ejercicios mezclados
    tipos = [generar_multiplicacion, generar_division, generar_suma_fracciones]
    for i in range(15):
        generador = random.choice(tipos)
        ejercicio_data = generador()
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=ejercicio_data['pregunta'],
            opciones=ejercicio_data['opciones'],
            respuesta_correcta=ejercicio_data['respuesta_correcta'],
            explicacion=ejercicio_data['explicacion'],
            orden=i + 1
        )
    
    print(f"    [OK] Tarea creada con ID: {tarea.id}")
    print(f"    [OK] 15 ejercicios mixtos creados")
    print(f"    [OK] Asignada a {ninos.count()} niños")
    return tarea


def main():
    print("="*70)
    print("GENERADOR DE TAREAS PARA PRUEBA DEL SISTEMA ML")
    print("="*70)
    
    # Buscar profesor
    try:
        profesor = User.objects.filter(role='profesor').first()
        if not profesor:
            print("\n[ERROR] No hay profesores en la base de datos")
            return
        
        print(f"\n[OK] Profesor encontrado: {profesor.nombre} {profesor.apellido}")
    except Exception as e:
        print(f"\n[ERROR] Error al buscar profesor: {e}")
        return
    
    # Buscar niños
    ninos = Nino.objects.filter(profesor=profesor)
    if ninos.count() == 0:
        print("\n[ERROR] El profesor no tiene niños asignados")
        return
    
    print(f"[OK] {ninos.count()} niños encontrados")
    for nino in ninos:
        print(f"     - {nino.nombre} {nino.apellido} (ID: {nino.id})")
    
    # Preguntar qué crear
    print("\n" + "="*70)
    print("¿Qué tareas deseas crear?")
    print("="*70)
    print("1. Tarea de Multiplicación (12 ejercicios)")
    print("2. Tarea de División (12 ejercicios)")
    print("3. Tarea de Suma de Fracciones (12 ejercicios)")
    print("4. Tarea Mixta (15 ejercicios)")
    print("5. TODAS las anteriores")
    print("0. Salir")
    
    opcion = input("\nSelecciona una opción: ").strip()
    
    tareas_creadas = []
    
    if opcion == '1':
        tarea = crear_tarea_multiplicacion(profesor, ninos)
        tareas_creadas.append(tarea)
    elif opcion == '2':
        tarea = crear_tarea_division(profesor, ninos)
        tareas_creadas.append(tarea)
    elif opcion == '3':
        tarea = crear_tarea_fracciones(profesor, ninos)
        tareas_creadas.append(tarea)
    elif opcion == '4':
        tarea = crear_tarea_mixta(profesor, ninos)
        tareas_creadas.append(tarea)
    elif opcion == '5':
        tareas_creadas.append(crear_tarea_multiplicacion(profesor, ninos))
        tareas_creadas.append(crear_tarea_division(profesor, ninos))
        tareas_creadas.append(crear_tarea_fracciones(profesor, ninos))
        tareas_creadas.append(crear_tarea_mixta(profesor, ninos))
    elif opcion == '0':
        print("\nSaliendo...")
        return
    else:
        print("\n[ERROR] Opción inválida")
        return
    
    # Resumen
    print("\n" + "="*70)
    print("TAREAS CREADAS EXITOSAMENTE")
    print("="*70)
    for tarea in tareas_creadas:
        print(f"\n[ID: {tarea.id}] {tarea.titulo}")
        print(f"  - Ejercicios: {tarea.ejercicios.count()}")
        print(f"  - Tipo: {tarea.tipo_ejercicio}")
        print(f"  - Asignada a: {tarea.ninos.count()} niños")
        print(f"\n  Para probar en el frontend:")
        print(f"  GET http://localhost:8000/api/tareas/nino/tareas/{tarea.id}?nino_id={ninos.first().id}")
    
    print("\n" + "="*70)
    print("COMO PROBAR EL SISTEMA ML")
    print("="*70)
    print("""
1. Inicia el servidor Django:
   cd backend
   python manage.py runserver

2. Desde el frontend, el niño resuelve los ejercicios:
   - El sistema capturará automáticamente:
     * Tiempo de respuesta
     * Cambios de pestaña (tab_blur_count)
     * Tiempo inactivo (idle_ms)
     * Clicks erráticos (erratic_clicks)

3. Después de 3+ ejercicios, el ML puede detectar distracciones
   - Si focus_score < 0.4 → Muestra pantalla de descanso

4. Los errores se clasifican automáticamente:
   - multiplicacion, division, fracciones, etc.

5. Ver reportes:
   GET http://localhost:8000/api/tareas/ml/reporte-errores?nino_id=X
   GET http://localhost:8000/api/tareas/ml/estadisticas?nino_id=X
""")
    
    print("="*70)
    print("LISTO PARA PROBAR")
    print("="*70)


if __name__ == "__main__":
    main()
