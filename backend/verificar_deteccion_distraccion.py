#!/usr/bin/env python
"""
Script de verificación del sistema de detección de distracciones mejorado
Muestra el tiempo promedio histórico de cada niño y simula detecciones
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, EjercicioProgreso
from django.db.models import Avg, Count, Max, Min
from datetime import datetime, timedelta


def mostrar_linea():
    print("=" * 80)


def mostrar_estadisticas_nino(nino):
    """Muestra estadísticas de tiempo de un niño"""
    print(f"\n👤 {nino.nombre} {nino.apellido} (ID: {nino.id})")
    print(f"   Edad: {nino.edad} años | Grado: {nino.grado}")
    
    # Obtener historial de tiempos (últimos 30)
    historial = EjercicioProgreso.objects.filter(
        student=nino,
        time_spent_ms__gt=0,
        time_spent_ms__lt=180000  # Excluir outliers
    ).order_by('-created_at')[:30]
    
    if not historial.exists():
        print("   ⚠️  Sin historial de ejercicios")
        return None
    
    tiempos = [e.time_spent_ms for e in historial]
    promedio = sum(tiempos) / len(tiempos)
    triple = promedio * 3
    
    estadisticas = historial.aggregate(
        total=Count('id'),
        promedio=Avg('time_spent_ms'),
        maximo=Max('time_spent_ms'),
        minimo=Min('time_spent_ms')
    )
    
    print(f"   📊 Ejercicios analizados: {len(tiempos)}")
    print(f"   ⏱️  Tiempo promedio: {promedio:.0f}ms ({promedio/1000:.1f}s)")
    print(f"   🔺 Máximo: {estadisticas['maximo']}ms ({estadisticas['maximo']/1000:.1f}s)")
    print(f"   🔻 Mínimo: {estadisticas['minimo']}ms ({estadisticas['minimo']/1000:.1f}s)")
    print(f"   ⚡ Triple promedio (umbral): {triple:.0f}ms ({triple/1000:.1f}s)")
    
    # Verificar si tiene ejercicios que exceden el triple
    ejercicios_lentos = [t for t in tiempos if t > triple]
    if ejercicios_lentos:
        print(f"   ⚠️  {len(ejercicios_lentos)} ejercicio(s) excedieron el umbral")
    else:
        print(f"   ✅ Ningún ejercicio excedió el umbral")
    
    return {
        'promedio': promedio,
        'triple': triple,
        'total': len(tiempos),
        'max': estadisticas['maximo'],
        'min': estadisticas['minimo']
    }


def simular_deteccion(nino, tiempo_ms):
    """Simula si un tiempo dado activaría la detección"""
    historial = EjercicioProgreso.objects.filter(
        student=nino,
        time_spent_ms__gt=0,
        time_spent_ms__lt=180000
    ).order_by('-created_at')[:30]
    
    if historial.count() < 5:
        print(f"   ⚠️  Historial insuficiente para {nino.nombre} (< 5 ejercicios)")
        return
    
    tiempos = [e.time_spent_ms for e in historial]
    promedio = sum(tiempos) / len(tiempos)
    triple = promedio * 3
    
    detectado = tiempo_ms > triple
    
    print(f"\n🧪 Simulación para {nino.nombre}:")
    print(f"   Tiempo del ejercicio: {tiempo_ms}ms ({tiempo_ms/1000:.1f}s)")
    print(f"   Promedio histórico: {promedio:.0f}ms ({promedio/1000:.1f}s)")
    print(f"   Umbral (3x): {triple:.0f}ms ({triple/1000:.1f}s)")
    
    if detectado:
        diferencia = tiempo_ms - triple
        print(f"   🛑 DISTRACCIÓN DETECTADA (excedió por {diferencia:.0f}ms / {diferencia/1000:.1f}s)")
    else:
        margen = triple - tiempo_ms
        print(f"   ✅ Normal (margen de {margen:.0f}ms / {margen/1000:.1f}s)")


def main():
    mostrar_linea()
    print("🔍 VERIFICACIÓN DEL SISTEMA DE DETECCIÓN DE DISTRACCIONES")
    print("   Sistema mejorado con tiempo promedio histórico por niño")
    mostrar_linea()
    
    # Obtener todos los niños con progreso
    ninos = Nino.objects.filter(ejercicio_progresos__isnull=False).distinct()
    
    if not ninos.exists():
        print("\n⚠️  No hay niños con ejercicios completados en el sistema")
        print("   Completa algunas tareas primero para ver estadísticas")
        return
    
    print(f"\n📋 Encontrados {ninos.count()} niño(s) con historial")
    
    estadisticas_global = []
    
    for nino in ninos:
        stats = mostrar_estadisticas_nino(nino)
        if stats:
            estadisticas_global.append(stats)
    
    # Resumen global
    if estadisticas_global:
        mostrar_linea()
        print("\n📊 RESUMEN GLOBAL")
        mostrar_linea()
        
        promedio_global = sum(s['promedio'] for s in estadisticas_global) / len(estadisticas_global)
        total_ejercicios = sum(s['total'] for s in estadisticas_global)
        
        print(f"\nTotal de ejercicios analizados: {total_ejercicios}")
        print(f"Promedio global: {promedio_global:.0f}ms ({promedio_global/1000:.1f}s)")
        print(f"Niños con suficiente historial: {len(estadisticas_global)}")
    
    # Simulaciones de ejemplo
    if estadisticas_global:
        mostrar_linea()
        print("\n🧪 SIMULACIONES DE DETECCIÓN")
        mostrar_linea()
        
        nino_ejemplo = ninos.first()
        
        # Simular tiempo normal
        simular_deteccion(nino_ejemplo, 5000)
        
        # Simular tiempo excesivo
        simular_deteccion(nino_ejemplo, 30000)
        
        # Simular tiempo muy excesivo
        simular_deteccion(nino_ejemplo, 60000)
    
    # Recomendaciones
    mostrar_linea()
    print("\n💡 RECOMENDACIONES")
    mostrar_linea()
    print("""
1. ✅ El sistema calcula promedios históricos de los últimos 30 ejercicios
2. ✅ Detecta cuando un niño tarda 3x su propio promedio histórico
3. ✅ Excluye automáticamente outliers (tiempos > 3 minutos)
4. ✅ Tiene fallback para niños con < 5 ejercicios completados
5. ⚡ Para probar: Completa ejercicios tardando intencionalmente más tiempo

📝 Para ver logs detallados:
   - Abre la consola del navegador al completar ejercicios
   - Verás el análisis ML completo con debug info

🔗 Endpoint de prueba:
   POST /api/tareas/ml/analizar-respuesta
   
🗄️  Base de datos: MySQL
   Tabla: tareas_progreso
    """)
    
    mostrar_linea()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
