# -*- coding: utf-8 -*-
"""
Script simple de demostracion de deteccion por tiempo
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, EjercicioProgreso

def main():
    print("=" * 70)
    print("VERIFICACION DE DATOS PARA DETECCION POR TIEMPO")
    print("=" * 70)
    
    # Obtener ninos con historial
    ninos = Nino.objects.filter(ejercicio_progresos__time_spent_ms__gt=0).distinct()[:5]
    
    if not ninos.exists():
        print("\n[ERROR] No hay ninos con historial de ejercicios")
        print("Por favor, completa algunos ejercicios primero en la interfaz web.")
        return
    
    print(f"\nSe encontraron {ninos.count()} ninos con historial")
    print("\n" + "=" * 70)
    
    for nino in ninos:
        print(f"\nNino: {nino.nombre} {nino.apellido} (ID: {nino.id})")
        print("-" * 70)
        
        # Obtener ultimos 30 ejercicios
        ejercicios = EjercicioProgreso.objects.filter(
            student=nino,
            time_spent_ms__gt=0,
            time_spent_ms__lt=180000
        ).order_by('-created_at')[:30]
        
        total = ejercicios.count()
        
        if total == 0:
            print("  Sin ejercicios validos")
            continue
        
        tiempos = [e.time_spent_ms for e in ejercicios]
        promedio = sum(tiempos) / len(tiempos)
        triple = promedio * 3
        
        print(f"  Total ejercicios: {total}")
        print(f"  Tiempo promedio: {promedio:.0f}ms ({promedio/1000:.1f}s)")
        print(f"  Umbral 3x: {triple:.0f}ms ({triple/1000:.1f}s)")
        print(f"  Tiempo minimo: {min(tiempos)}ms")
        print(f"  Tiempo maximo: {max(tiempos)}ms")
        
        # Mostrar que pasaria en diferentes escenarios
        print(f"\n  Escenarios de deteccion:")
        print(f"    - Si tarda {int(promedio)}ms -> NO SE ACTIVA (normal)")
        print(f"    - Si tarda {int(promedio*2)}ms -> NO SE ACTIVA (2x)")
        print(f"    - Si tarda {int(triple + 1000)}ms -> SE ACTIVA (>3x)")
        
    print("\n" + "=" * 70)
    print("COMO FUNCIONA LA DETECCION:")
    print("=" * 70)
    print("""
1. El sistema calcula el promedio de los ultimos 30 ejercicios del nino
2. Si el nino tarda 3 veces o mas ese promedio, se activa pantalla de descanso
3. La deteccion es personalizada para cada nino

PARA PROBAR:
1. Inicia el servidor: python manage.py runserver
2. Abre http://localhost:4200 y haz login como nino
3. Abre la consola del navegador (F12)
4. Completa ejercicios y veras los logs de deteccion
5. Tarda intencionalmente mas de lo normal y veras la pantalla de descanso
    """)
    print("=" * 70)

if __name__ == '__main__':
    main()
