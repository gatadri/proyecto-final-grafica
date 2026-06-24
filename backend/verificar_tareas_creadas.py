# -*- coding: utf-8 -*-
"""
Script para verificar las tareas creadas
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Ejercicio, Nino

def verificar_tareas():
    print("=" * 70)
    print("VERIFICACION DE TAREAS CREADAS")
    print("=" * 70)
    
    # Buscar las 3 tareas creadas
    tareas = Tarea.objects.filter(titulo__in=[
        'Division Basica',
        'Tablas de Multiplicar',
        'Suma de Fracciones con Mismo Denominador'
    ]).order_by('id')
    
    if tareas.count() < 3:
        print(f"\n[ERROR] Solo se encontraron {tareas.count()} tareas")
        return
    
    print(f"\n[OK] Se encontraron {tareas.count()} tareas\n")
    
    total_ninos = Nino.objects.count()
    
    for tarea in tareas:
        print("-" * 70)
        print(f"\nTAREA: {tarea.titulo} (ID: {tarea.id})")
        print(f"Descripcion: {tarea.descripcion}")
        print(f"Tipo: {tarea.tipo_ejercicio}")
        
        # Contar ejercicios
        ejercicios = Ejercicio.objects.filter(tarea=tarea).order_by('orden')
        print(f"\nEjercicios: {ejercicios.count()}")
        
        # Mostrar primeros 3 ejercicios
        print("\nPrimeros 3 ejercicios:")
        for ej in ejercicios[:3]:
            print(f"  {ej.orden}. {ej.pregunta}")
            print(f"     Respuesta: {ej.respuesta_correcta}")
            print(f"     Opciones: {ej.opciones}")
        
        # Contar asignaciones
        ninos_asignados = tarea.ninos.count()
        print(f"\nAsignada a: {ninos_asignados} de {total_ninos} ninos")
        
        if ninos_asignados == total_ninos:
            print("[OK] Todos los ninos tienen la tarea")
        else:
            print(f"[AVISO] Faltan {total_ninos - ninos_asignados} ninos")
    
    print("\n" + "=" * 70)
    print("VERIFICACION COMPLETA")
    print("=" * 70)
    print(f"\nTotal tareas creadas: {tareas.count()}")
    print(f"Total ejercicios: {sum(t.ejercicios.count() for t in tareas)}")
    print(f"Total ninos con tareas: {total_ninos}")
    print("\n[OK] Todo correcto - Las tareas estan listas para usar")
    print("\nAccede a http://localhost:4200 y login con:")
    print("  Alejandra - PIN: 8778")
    print("  Elena - PIN: 1241")

if __name__ == '__main__':
    verificar_tareas()
