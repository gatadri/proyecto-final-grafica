# -*- coding: utf-8 -*-
"""
Script para probar la deteccion de distraccion con datos reales
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

def probar_deteccion():
    print("=" * 70)
    print("PROBANDO DETECCION CON DATOS REALES")
    print("=" * 70)
    
    # Buscar a Alejandra y Elena
    ninos = Nino.objects.filter(nombre__in=['Alejandra', 'Elena']).order_by('nombre')
    
    for nino in ninos:
        print(f"\n{'=' * 70}")
        print(f"NINO: {nino.nombre} {nino.apellido} (ID: {nino.id})")
        print(f"{'=' * 70}")
        
        # Obtener historial
        historial = list(EjercicioProgreso.objects.filter(
            student=nino,
            time_spent_ms__gt=0,
            time_spent_ms__lt=180000
        ).order_by('-created_at')[:30].values_list('time_spent_ms', flat=True))
        
        if not historial:
            print("[ERROR] Sin historial")
            continue
        
        promedio = sum(historial) / len(historial)
        triple = promedio * 3
        
        print(f"\nEstadisticas:")
        print(f"  Registros: {len(historial)}")
        print(f"  Promedio: {promedio:.0f}ms ({promedio/1000:.1f}s)")
        print(f"  Umbral 3x: {triple:.0f}ms ({triple/1000:.1f}s)")
        
        # Obtener historial para deteccion
        historial_dict = list(EjercicioProgreso.objects.filter(
            student=nino
        ).order_by('-created_at')[:10].values(
            'difficulty', 'time_spent_ms', 'attempts', 'used_hint', 'n_hints',
            'fast_response', 'correct', 'tab_blur_count', 'idle_ms', 'erratic_clicks'
        ))
        historial_dict.reverse()
        
        print(f"\n{'*' * 70}")
        print("SIMULACIONES DE DETECCION:")
        print(f"{'*' * 70}")
        
        # Escenario 1: Tiempo normal
        print(f"\n1. TIEMPO NORMAL ({int(promedio)}ms):")
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = int(promedio)
        resultado = detectar_distraccion(historial_test, promedio)
        print(f"   Requiere descanso: {resultado['requiere_descanso']}")
        if resultado['motivo']:
            print(f"   Motivo: {resultado['motivo']}")
            print(f"   Detalles: {resultado.get('detalles', 'N/A')}")
        else:
            print(f"   [OK] No se detecta distraccion")
        
        # Escenario 2: Justo en el limite (3x)
        print(f"\n2. JUSTO EN EL LIMITE ({int(triple)}ms):")
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = int(triple)
        resultado = detectar_distraccion(historial_test, promedio)
        print(f"   Requiere descanso: {resultado['requiere_descanso']}")
        if resultado['motivo']:
            print(f"   Motivo: {resultado['motivo']}")
            print(f"   Detalles: {resultado.get('detalles', 'N/A')}")
        
        # Escenario 3: EXCEDE el limite (3.5x) - DEBE ACTIVAR
        tiempo_excesivo = int(promedio * 3.5)
        print(f"\n3. EXCEDE EL LIMITE ({tiempo_excesivo}ms = 3.5x):")
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = tiempo_excesivo
        resultado = detectar_distraccion(historial_test, promedio)
        
        if resultado['requiere_descanso']:
            print(f"   [OK] DETECTADO! Requiere descanso: True")
            print(f"   [OK] Motivo: {resultado['motivo']}")
            print(f"   [OK] Detalles: {resultado.get('detalles', 'N/A')}")
        else:
            print(f"   [ERROR] NO SE DETECTO! Requiere descanso: False")
            print(f"   [ERROR] Esto es un problema - deberia activarse")
        
        # Escenario 4: 60 segundos (para probar limite de 1 minuto)
        print(f"\n4. 60 SEGUNDOS (60000ms):")
        historial_test = historial_dict.copy()
        historial_test[-1]['time_spent_ms'] = 60000
        resultado = detectar_distraccion(historial_test, promedio)
        
        if 60000 > triple:
            print(f"   [INFO] 60s excede el umbral de {triple/1000:.1f}s")
            if resultado['requiere_descanso']:
                print(f"   [OK] DETECTADO! Requiere descanso: True")
                print(f"   [OK] Motivo: {resultado['motivo']}")
            else:
                print(f"   [ERROR] NO SE DETECTO!")
        else:
            print(f"   [INFO] 60s NO excede el umbral de {triple/1000:.1f}s")
            print(f"   [INFO] Se usara el timer de 1 minuto del frontend")
        
        # Escenario 5: 3 errores consecutivos
        print(f"\n5. 3 ERRORES CONSECUTIVOS:")
        historial_test = historial_dict.copy()
        for i in range(-3, 0):
            if i < len(historial_test):
                historial_test[i]['correct'] = 0
        resultado = detectar_distraccion(historial_test, promedio)
        
        if resultado['requiere_descanso']:
            print(f"   [OK] DETECTADO! Requiere descanso: True")
            print(f"   [OK] Motivo: {resultado['motivo']}")
            print(f"   [OK] Detalles: {resultado.get('detalles', 'N/A')}")
        else:
            print(f"   [ERROR] NO SE DETECTO!")
    
    print("\n" + "=" * 70)
    print("COMO PROBAR EN LA INTERFAZ:")
    print("=" * 70)
    print("""
1. Inicia el servidor:
   Terminal 1: python manage.py runserver
   Terminal 2: ng serve

2. Abre http://localhost:4200 y login como Alejandra o Elena

3. IMPORTANTE: Abre la consola del navegador (F12)

4. Completa un ejercicio y observa los logs

5. Para activar la pantalla de descanso:
   OPCION A: Tarda mas del umbral 3x (ver arriba)
   OPCION B: Tarda mas de 60 segundos (timer de 1 minuto)
   OPCION C: Comete 3 errores consecutivos

6. Veras en consola:
   ═══════════════════════════════════
   🛑 PANTALLA DE DESCANSO ACTIVADA
   📋 Razón: tiempo_excesivo
   ═══════════════════════════════════
    """)
    print("=" * 70)

if __name__ == '__main__':
    probar_deteccion()
