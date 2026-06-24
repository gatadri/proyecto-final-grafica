# -*- coding: utf-8 -*-
"""
Script para llenar datos de prueba en la base de datos
Especificamente para Alejandra y Elena
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, Ejercicio, EjercicioProgreso

def llenar_datos():
    print("=" * 70)
    print("LLENANDO DATOS DE PRUEBA PARA DETECCION")
    print("=" * 70)
    
    # Buscar a Alejandra y Elena
    try:
        alejandra = Nino.objects.get(nombre__icontains='alejandra')
        print(f"\nEncontrada: {alejandra.nombre} {alejandra.apellido} (ID: {alejandra.id})")
    except Nino.DoesNotExist:
        print("\n[ERROR] No se encontro a Alejandra")
        alejandra = None
    except Nino.MultipleObjectsReturned:
        alejandra = Nino.objects.filter(nombre__icontains='alejandra').first()
        print(f"\nEncontrada: {alejandra.nombre} {alejandra.apellido} (ID: {alejandra.id})")
    
    try:
        elena = Nino.objects.get(nombre__icontains='elena')
        print(f"Encontrada: {elena.nombre} {elena.apellido} (ID: {elena.id})")
    except Nino.DoesNotExist:
        print("[ERROR] No se encontro a Elena")
        elena = None
    except Nino.MultipleObjectsReturned:
        elena = Nino.objects.filter(nombre__icontains='elena').first()
        print(f"Encontrada: {elena.nombre} {elena.apellido} (ID: {elena.id})")
    
    # Buscar ejercicios disponibles
    ejercicios = list(Ejercicio.objects.all()[:20])
    
    if not ejercicios:
        print("\n[ERROR] No hay ejercicios en la base de datos")
        print("Por favor, crea algunas tareas con ejercicios primero")
        return
    
    print(f"\nEjercicios disponibles: {len(ejercicios)}")
    
    # Llenar datos para cada niña
    for nino in [alejandra, elena]:
        if not nino:
            continue
        
        print(f"\n{'-' * 70}")
        print(f"Llenando datos para: {nino.nombre}")
        print(f"{'-' * 70}")
        
        # Verificar si ya tiene datos
        datos_existentes = EjercicioProgreso.objects.filter(student=nino).count()
        print(f"Datos existentes: {datos_existentes}")
        
        if datos_existentes >= 30:
            print("[OK] Ya tiene suficientes datos (>= 30)")
            continue
        
        # Calcular cuantos datos crear
        datos_a_crear = 35 - datos_existentes
        print(f"Creando {datos_a_crear} registros nuevos...")
        
        # Definir tiempo promedio base para esta niña
        if 'alejandra' in nino.nombre.lower():
            tiempo_base = 5000  # 5 segundos promedio
        else:
            tiempo_base = 7000  # 7 segundos promedio
        
        # Crear registros
        creados = 0
        fecha_base = datetime.now() - timedelta(days=10)
        
        for i in range(datos_a_crear):
            # Seleccionar ejercicio aleatorio
            ejercicio = random.choice(ejercicios)
            
            # Generar tiempo con variacion natural (±40%)
            variacion = random.uniform(0.6, 1.4)
            tiempo = int(tiempo_base * variacion)
            
            # Decidir si es correcto (80% correcto, 20% incorrecto)
            correcto = random.random() < 0.8
            
            # Crear progreso
            try:
                EjercicioProgreso.objects.create(
                    student=nino,
                    item=ejercicio,
                    difficulty=1,
                    time_spent_ms=tiempo,
                    attempts=1,
                    used_hint=False,
                    n_hints=0,
                    fast_response=tiempo < 3000,
                    correct=correcto,
                    tab_blur_count=0,
                    idle_ms=0,
                    erratic_clicks=0,
                    error_type='' if correcto else 'wrong_answer',
                    created_at=fecha_base + timedelta(minutes=i*5)
                )
                creados += 1
            except Exception as e:
                print(f"  [ERROR] No se pudo crear registro: {e}")
        
        print(f"[OK] Se crearon {creados} registros")
        
        # Verificar total
        total_ahora = EjercicioProgreso.objects.filter(student=nino).count()
        tiempos = list(EjercicioProgreso.objects.filter(
            student=nino,
            time_spent_ms__gt=0
        ).order_by('-created_at')[:30].values_list('time_spent_ms', flat=True))
        
        if tiempos:
            promedio = sum(tiempos) / len(tiempos)
            triple = promedio * 3
            
            print(f"\nEstadisticas finales:")
            print(f"  Total registros: {total_ahora}")
            print(f"  Tiempo promedio: {promedio:.0f}ms ({promedio/1000:.1f}s)")
            print(f"  Umbral 3x: {triple:.0f}ms ({triple/1000:.1f}s)")
            print(f"  [INFO] Si tarda mas de {triple/1000:.1f}s se activara la pantalla")
    
    print("\n" + "=" * 70)
    print("DATOS CREADOS EXITOSAMENTE")
    print("=" * 70)
    print("\nAhora puedes probar:")
    print("1. python manage.py runserver")
    print("2. ng serve")
    print("3. Login como Alejandra o Elena")
    print("4. Completa un ejercicio tardando MAS del umbral 3x")
    print("5. Veras la pantalla de descanso")
    print("\nALTERNATIVA: Si tardas mas de 1 minuto en cualquier ejercicio")
    print("             tambien se activara la pantalla de descanso")
    print("=" * 70)

if __name__ == '__main__':
    llenar_datos()
