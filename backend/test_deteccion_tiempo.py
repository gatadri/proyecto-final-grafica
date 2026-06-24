"""
Script para probar la detección de distracción por tiempo excesivo
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, EjercicioProgreso
from tareas.ml_utils import detectar_distraccion

def test_deteccion_tiempo():
    print("=" * 70)
    print("PRUEBA DE DETECCION DE DISTRACCION POR TIEMPO")
    print("=" * 70)
    
    # Obtener un niño con historial
    ninos_con_historial = Nino.objects.filter(
        ejercicio_progresos__time_spent_ms__gt=0
    ).distinct()
    
    if not ninos_con_historial.exists():
        print("[ERROR] No hay ninos con historial de ejercicios")
        return
    
    for nino in ninos_con_historial[:3]:  # Probar con los primeros 3 niños
        print(f"\nNino: {nino.nombre} {nino.apellido} (ID: {nino.id})")
        print("-" * 70)
        
        # Obtener últimos 30 ejercicios
        historial = list(EjercicioProgreso.objects.filter(
            student=nino,
            time_spent_ms__gt=0,
            time_spent_ms__lt=180000  # Menos de 3 minutos
        ).order_by('-created_at')[:30].values_list('time_spent_ms', flat=True))
        
        if len(historial) < 5:
            print(f"[AVISO] Historial insuficiente ({len(historial)} ejercicios)")
            continue
        
        # Calcular promedio
        promedio = sum(historial) / len(historial)
        triple_promedio = promedio * 3
        
        print(f"Ejercicios analizados: {len(historial)}")
        print(f"Tiempo promedio: {promedio:.0f}ms ({promedio/1000:.1f}s)")
        print(f"Umbral 3x: {triple_promedio:.0f}ms ({triple_promedio/1000:.1f}s)")
        
        # Obtener historial para función de detección
        historial_dict = list(EjercicioProgreso.objects.filter(
            student=nino
        ).order_by('-created_at')[:10].values(
            'difficulty', 'time_spent_ms', 'attempts', 'used_hint', 'n_hints',
            'fast_response', 'correct', 'tab_blur_count', 'idle_ms', 'erratic_clicks'
        ))
        historial_dict.reverse()
        
        if not historial_dict:
            print("[AVISO] No hay historial reciente")
            continue
        
        # Verificar que tenemos al menos 3 elementos
        if len(historial_dict) < 3:
            print(f"[AVISO] Historial muy corto ({len(historial_dict)} elementos)")
            continue
        
        # Simular diferentes escenarios
        print("\nSIMULACIONES:")
        
        # Escenario 1: Tiempo normal
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = int(promedio)
        resultado = detectar_distraccion(historial_test, promedio)
        print(f"\n1. Tiempo normal ({int(promedio)}ms):")
        print(f"   Requiere descanso: {resultado['requiere_descanso']}")
        if resultado['motivo']:
            print(f"   Motivo: {resultado['motivo']}")
        
        # Escenario 2: Tiempo 2x (no debería activar)
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = int(promedio * 2)
        resultado = detectar_distraccion(historial_test, promedio)
        print(f"\n2. Tiempo 2x promedio ({int(promedio * 2)}ms):")
        print(f"   Requiere descanso: {resultado['requiere_descanso']}")
        if resultado['motivo']:
            print(f"   Motivo: {resultado['motivo']}")
        
        # Escenario 3: Tiempo 3x (debería activar)
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = int(promedio * 3.5)
        historial_test[-1]['correct'] = 0  # Marcar como incorrecto
        resultado = detectar_distraccion(historial_test, promedio)
        print(f"\n3. Tiempo 3.5x promedio ({int(promedio * 3.5)}ms):")
        print(f"   [OK] Requiere descanso: {resultado['requiere_descanso']}")
        print(f"   Motivo: {resultado['motivo']}")
        print(f"   Detalles: {resultado.get('detalles', 'N/A')}")
        print(f"   Focus score: {resultado.get('focus_score', 'N/A')}")
        
        # Escenario 4: 3 errores consecutivos
        historial_test = historial_dict.copy()
        for i in range(-3, 0):
            historial_test[i]['correct'] = 0
        resultado = detectar_distraccion(historial_test, promedio)
        print(f"\n4. 3 errores consecutivos:")
        print(f"   [OK] Requiere descanso: {resultado['requiere_descanso']}")
        print(f"   Motivo: {resultado['motivo']}")
        print(f"   Detalles: {resultado.get('detalles', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("PRUEBA COMPLETADA")
    print("=" * 70)

if __name__ == '__main__':
    test_deteccion_tiempo()
