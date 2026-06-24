# -*- coding: utf-8 -*-
"""
Script para crear 3 tareas de matematicas con 15 ejercicios cada una
"""
import os
import sys
import django
import random

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Ejercicio, Nino
from users.models import User

def crear_tarea_division():
    """Crea tarea de division con 15 ejercicios"""
    print("\n" + "=" * 70)
    print("CREANDO TAREA: DIVISION")
    print("=" * 70)
    
    # Buscar un profesor para asignar la tarea
    profesor = User.objects.filter(role='profesor').first()
    if not profesor:
        print("[ERROR] No hay profesores en el sistema")
        return None
    
    # Crear la tarea
    tarea = Tarea.objects.create(
        titulo="División Básica",
        descripcion="Practica divisiones básicas con números de 1 a 2 dígitos",
        tipo_ejercicio="multiple",
        profesor=profesor
    )
    
    print(f"Tarea creada: {tarea.titulo} (ID: {tarea.id})")
    print(f"Creando 15 ejercicios...")
    
    # Crear 15 ejercicios
    ejercicios_data = [
        # Divisiones exactas simples
        (12, 3, 4), (15, 5, 3), (20, 4, 5), (18, 6, 3), (24, 8, 3),
        # Divisiones un poco más complejas
        (35, 7, 5), (42, 6, 7), (48, 8, 6), (56, 7, 8), (63, 9, 7),
        # Divisiones con números mayores
        (72, 8, 9), (81, 9, 9), (64, 8, 8), (45, 5, 9), (54, 6, 9)
    ]
    
    for i, (dividendo, divisor, resultado) in enumerate(ejercicios_data, 1):
        # Generar opciones incorrectas
        opciones = [resultado]
        while len(opciones) < 4:
            opcion = resultado + random.randint(-3, 3)
            if opcion > 0 and opcion not in opciones:
                opciones.append(opcion)
        
        random.shuffle(opciones)
        
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=f"¿Cuánto es {dividendo} ÷ {divisor}?",
            opciones=opciones,
            respuesta_correcta=str(resultado),
            explicacion=f"{dividendo} dividido entre {divisor} es {resultado}. Porque {divisor} × {resultado} = {dividendo}",
            orden=i,
            tema=f"division_{dividendo}_{divisor}",
            subtema="division"
        )
    
    print(f"[OK] 15 ejercicios de division creados")
    return tarea

def crear_tarea_multiplicacion():
    """Crea tarea de multiplicacion con 15 ejercicios"""
    print("\n" + "=" * 70)
    print("CREANDO TAREA: MULTIPLICACION")
    print("=" * 70)
    
    profesor = User.objects.filter(role='profesor').first()
    if not profesor:
        print("[ERROR] No hay profesores en el sistema")
        return None
    
    tarea = Tarea.objects.create(
        titulo="Tablas de Multiplicar",
        descripcion="Practica las tablas de multiplicar del 2 al 9",
        tipo_ejercicio="multiple",
        profesor=profesor
    )
    
    print(f"Tarea creada: {tarea.titulo} (ID: {tarea.id})")
    print(f"Creando 15 ejercicios...")
    
    # Crear 15 ejercicios variados
    ejercicios_data = [
        # Tabla del 2 y 3
        (2, 8, 16), (3, 7, 21), (2, 9, 18), (3, 6, 18), (3, 8, 24),
        # Tabla del 4 y 5
        (4, 7, 28), (5, 6, 30), (4, 9, 36), (5, 8, 40), (4, 6, 24),
        # Tablas mayores
        (6, 7, 42), (7, 8, 56), (8, 9, 72), (9, 6, 54), (7, 9, 63)
    ]
    
    for i, (factor1, factor2, resultado) in enumerate(ejercicios_data, 1):
        # Generar opciones incorrectas
        opciones = [resultado]
        while len(opciones) < 4:
            opcion = resultado + random.randint(-10, 10)
            if opcion > 0 and opcion not in opciones:
                opciones.append(opcion)
        
        random.shuffle(opciones)
        
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=f"¿Cuánto es {factor1} × {factor2}?",
            opciones=opciones,
            respuesta_correcta=str(resultado),
            explicacion=f"{factor1} por {factor2} es {resultado}",
            orden=i,
            tema=f"tabla_{factor1}",
            subtema="multiplicacion"
        )
    
    print(f"[OK] 15 ejercicios de multiplicacion creados")
    return tarea

def crear_tarea_fracciones():
    """Crea tarea de suma de fracciones con mismo denominador"""
    print("\n" + "=" * 70)
    print("CREANDO TAREA: SUMA DE FRACCIONES")
    print("=" * 70)
    
    profesor = User.objects.filter(role='profesor').first()
    if not profesor:
        print("[ERROR] No hay profesores en el sistema")
        return None
    
    tarea = Tarea.objects.create(
        titulo="Suma de Fracciones con Mismo Denominador",
        descripcion="Practica sumar fracciones que tienen el mismo denominador",
        tipo_ejercicio="multiple",
        profesor=profesor
    )
    
    print(f"Tarea creada: {tarea.titulo} (ID: {tarea.id})")
    print(f"Creando 15 ejercicios...")
    
    # Crear 15 ejercicios de fracciones
    ejercicios_data = [
        # Denominador 4
        (1, 4, 2, 4, 3, 4), (2, 4, 1, 4, 3, 4), (1, 4, 3, 4, 4, 4),
        # Denominador 5
        (1, 5, 2, 5, 3, 5), (2, 5, 2, 5, 4, 5), (1, 5, 3, 5, 4, 5),
        # Denominador 6
        (1, 6, 2, 6, 3, 6), (2, 6, 3, 6, 5, 6), (1, 6, 4, 6, 5, 6),
        # Denominador 8
        (1, 8, 3, 8, 4, 8), (2, 8, 3, 8, 5, 8), (3, 8, 4, 8, 7, 8),
        # Denominador 10
        (1, 10, 4, 10, 5, 10), (2, 10, 5, 10, 7, 10), (3, 10, 6, 10, 9, 10)
    ]
    
    for i, (num1, den1, num2, den2, num_res, den_res) in enumerate(ejercicios_data, 1):
        # Generar opciones incorrectas
        opciones = [f"{num_res}/{den_res}"]
        
        # Opciones incorrectas comunes
        posibles_incorrectas = [
            f"{num1 + num2}/{den1}",  # Sumar también denominadores (error común)
            f"{num_res + 1}/{den_res}",  # Numerador +1
            f"{num_res - 1}/{den_res}",  # Numerador -1
            f"{num_res}/{den_res * 2}",  # Denominador duplicado
            f"{num1}/{den1}",  # Primera fracción sin sumar
        ]
        
        for opcion in posibles_incorrectas:
            if opcion not in opciones and len(opciones) < 4:
                opciones.append(opcion)
        
        random.shuffle(opciones)
        
        Ejercicio.objects.create(
            tarea=tarea,
            pregunta=f"¿Cuánto es {num1}/{den1} + {num2}/{den2}?",
            opciones=opciones,
            respuesta_correcta=f"{num_res}/{den_res}",
            explicacion=f"Como tienen el mismo denominador ({den1}), solo sumamos los numeradores: {num1} + {num2} = {num_res}. El resultado es {num_res}/{den_res}",
            orden=i,
            tema=f"suma_fracciones_den_{den1}",
            subtema="fracciones"
        )
    
    print(f"[OK] 15 ejercicios de fracciones creados")
    return tarea

def asignar_a_todos_los_ninos(tareas):
    """Asigna las tareas a todos los niños"""
    print("\n" + "=" * 70)
    print("ASIGNANDO TAREAS A TODOS LOS NIÑOS")
    print("=" * 70)
    
    ninos = Nino.objects.all()
    total_ninos = ninos.count()
    
    print(f"\nTotal de niños: {total_ninos}")
    
    for tarea in tareas:
        print(f"\nAsignando: {tarea.titulo}")
        tarea.ninos.set(ninos)
        tarea.save()
        print(f"  [OK] Asignada a {total_ninos} ninos")

def main():
    print("=" * 70)
    print("CREACION DE TAREAS DE MATEMATICAS")
    print("=" * 70)
    print("\nSe crearan 3 tareas:")
    print("  1. Division Basica (15 ejercicios)")
    print("  2. Tablas de Multiplicar (15 ejercicios)")
    print("  3. Suma de Fracciones (15 ejercicios)")
    print("\nTodas las tareas se asignaran a todos los niños")
    
    # Crear las tareas
    tarea_division = crear_tarea_division()
    tarea_multiplicacion = crear_tarea_multiplicacion()
    tarea_fracciones = crear_tarea_fracciones()
    
    tareas = [t for t in [tarea_division, tarea_multiplicacion, tarea_fracciones] if t]
    
    if not tareas:
        print("\n[ERROR] No se pudieron crear las tareas")
        return
    
    # Asignar a todos los niños
    asignar_a_todos_los_ninos(tareas)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    
    for tarea in tareas:
        ejercicios_count = Ejercicio.objects.filter(tarea=tarea).count()
        ninos_count = tarea.ninos.count()
        print(f"\n{tarea.titulo} (ID: {tarea.id})")
        print(f"  Ejercicios: {ejercicios_count}")
        print(f"  Asignada a: {ninos_count} niños")
        print(f"  Tipo: {tarea.tipo_ejercicio}")
    
    print("\n" + "=" * 70)
    print("[OK] TAREAS CREADAS Y ASIGNADAS EXITOSAMENTE")
    print("=" * 70)
    
    print("\nPuedes verlas en:")
    print("  - http://localhost:4200 (login como cualquier niño)")
    print("  - Panel del profesor")

if __name__ == '__main__':
    main()
