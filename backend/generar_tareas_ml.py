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
        'pregunta': f'Cuanto es {a} x {b}?',
        'opciones': opciones,
        'respuesta_correcta': str(resultado),
        'explicacion': f'{a} x {b} = {resultado}'
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
        'pregunta': f'Cuanto es {a} dividido {b}?',
        'opciones': opciones,
        'respuesta_correcta': str(cociente),
        'explicacion': f'{a} dividido {b} = {cociente}'
    }


def generar_suma_fracciones():
    """Genera ejercicio de suma de fracciones"""
    # Generar fracciones simples con mismo denominador
    denominador = random.choice([2, 3, 4, 5, 6, 8])
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
        'pregunta': f'Cuanto es {num1}/{denominador} + {num2}/{denominador}?',
        'opciones': opciones,
        'respuesta_correcta': resultado_str,
        'explicacion': f'{num1}/{denominador} + {num2}/{denominador} = {resultado_str}'
    }


def crear_tarea_multiplicacion(profesor, ninos):
    """Crea tarea de multiplicación con 12 ejercicios"""
    print("\n[*] Creando tarea de MULTIPLICACION...")
    
    tarea = Tarea.objects.create(
        titulo="Practica de Multiplicacion",
        descripcion="Resuelve las siguientes multiplicaciones. Concentrate!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    tarea.ninos.set(ninos)
    
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
    print(f"    [OK] 12 ejercicios de multiplicacion creados")
    print(f"    [OK] Asignada a {ninos.count()} ninos")
    return tarea


def crear_tarea_division(profesor, ninos):
    """Crea tarea de división con 12 ejercicios"""
    print("\n[*] Creando tarea de DIVISION...")
    
    tarea = Tarea.objects.create(
        titulo="Practica de Division",
        descripcion="Resuelve las siguientes divisiones. Tomate tu tiempo!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    tarea.ninos.set(ninos)
    
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
    print(f"    [OK] 12 ejercicios de division creados")
    print(f"    [OK] Asignada a {ninos.count()} ninos")
    return tarea


def crear_tarea_fracciones(profesor, ninos):
    """Crea tarea de suma de fracciones con 12 ejercicios"""
    print("\n[*] Creando tarea de SUMA DE FRACCIONES...")
    
    tarea = Tarea.objects.create(
        titulo="Practica de Suma de Fracciones",
        descripcion="Resuelve las siguientes sumas de fracciones. Recuerda sumar los numeradores!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    tarea.ninos.set(ninos)
    
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
    print(f"    [OK] Asignada a {ninos.count()} ninos")
    return tarea


def crear_tarea_mixta(profesor, ninos):
    """Crea tarea mixta con 15 ejercicios variados"""
    print("\n[*] Creando tarea MIXTA...")
    
    tarea = Tarea.objects.create(
        titulo="Practica Mixta de Matematicas",
        descripcion="Ejercicios variados de multiplicacion, division y fracciones. Pon atencion!",
        tipo_ejercicio='multiple',
        profesor=profesor
    )
    
    tarea.ninos.set(ninos)
    
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
    print(f"    [OK] Asignada a {ninos.count()} ninos")
    return tarea


def main():
    print("="*70)
    print("GENERADOR AUTOMATICO DE TAREAS PARA PRUEBA DEL SISTEMA ML")
    print("="*70)
    
    # Buscar profesor
    profesor = User.objects.filter(role='profesor').first()
    if not profesor:
        print("\n[ERROR] No hay profesores en la base de datos")
        return
    
    print(f"\n[OK] Profesor: {profesor.nombre} {profesor.apellido}")
    
    # Buscar niños
    ninos = Nino.objects.filter(profesor=profesor)
    if ninos.count() == 0:
        print("[ERROR] El profesor no tiene ninos asignados")
        return
    
    print(f"[OK] {ninos.count()} ninos encontrados")
    for nino in ninos:
        print(f"     - {nino.nombre} {nino.apellido} (ID: {nino.id})")
    
    # Crear todas las tareas
    tareas_creadas = []
    tareas_creadas.append(crear_tarea_multiplicacion(profesor, ninos))
    tareas_creadas.append(crear_tarea_division(profesor, ninos))
    tareas_creadas.append(crear_tarea_fracciones(profesor, ninos))
    tareas_creadas.append(crear_tarea_mixta(profesor, ninos))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TAREAS CREADAS")
    print("="*70)
    
    for tarea in tareas_creadas:
        print(f"\n[ID: {tarea.id}] {tarea.titulo}")
        print(f"  - Ejercicios: {tarea.ejercicios.count()}")
        print(f"  - Asignada a: {tarea.ninos.count()} ninos")
        
        # Mostrar algunos ejercicios de ejemplo
        ejemplos = tarea.ejercicios.all()[:3]
        print(f"  - Ejemplos:")
        for ej in ejemplos:
            print(f"    * {ej.pregunta}")
            print(f"      Respuesta: {ej.respuesta_correcta}")
    
    # Información para API
    print("\n" + "="*70)
    print("ENDPOINTS PARA PROBAR")
    print("="*70)
    
    primer_nino = ninos.first()
    print(f"\nUsando nino: {primer_nino.nombre} (ID: {primer_nino.id})")
    
    print("\n1. Ver todas las tareas del nino:")
    print(f"   GET http://localhost:8000/api/tareas/nino/tareas?nino_id={primer_nino.id}")
    
    for tarea in tareas_creadas:
        print(f"\n2. Ver tarea '{tarea.titulo}':")
        print(f"   GET http://localhost:8000/api/tareas/nino/tareas/{tarea.id}?nino_id={primer_nino.id}")
    
    print("\n3. Analizar respuesta con ML:")
    print(f"""   POST http://localhost:8000/api/tareas/ml/analizar-respuesta
   Body:
   {{
     "nino_id": {primer_nino.id},
     "ejercicio_id": 1,
     "tiempo_ms": 15000,
     "correcto": false,
     "tab_blur_count": 3,
     "idle_ms": 5000,
     "erratic_clicks": 8
   }}""")
    
    print("\n4. Ver reporte de errores:")
    print(f"   GET http://localhost:8000/api/tareas/ml/reporte-errores?nino_id={primer_nino.id}")
    
    print("\n5. Ver estadisticas ML:")
    print(f"   GET http://localhost:8000/api/tareas/ml/estadisticas?nino_id={primer_nino.id}")
    
    print("\n" + "="*70)
    print("COMO FUNCIONA EL SISTEMA ML")
    print("="*70)
    print("""
Cuando el nino resuelve ejercicios:

1. Por cada respuesta, el frontend envia datos al endpoint:
   /api/tareas/ml/analizar-respuesta

2. El ML analiza:
   - Tipo de error (multiplicacion, division, fracciones)
   - Nivel de concentracion (focus_score)

3. Si focus_score < 0.4:
   - El frontend muestra pantalla de descanso (10 segundos)
   - Se guarda en EventoDistraccion

4. Los errores se guardan en PrediccionError para:
   - Reportes a padres
   - Reportes a profesores
   - Identificar temas que necesita reforzar

5. Minimo 3 ejercicios resueltos para detectar distracciones
   (el RNN necesita secuencia de datos)
""")
    
    print("\n" + "="*70)
    print("TAREAS LISTAS PARA PROBAR")
    print("="*70)
    print("\nInicia el servidor:")
    print("  cd backend")
    print("  python manage.py runserver")
    print("\nLuego prueba desde el frontend o con Postman/curl")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
