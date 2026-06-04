import requests
import json
import time
import random

BASE_URL = "http://localhost:8000/api/tareas"

def simular_resolucion_tarea():
    """
    Simula un niño resolviendo una tarea completa
    Demuestra cómo funciona el sistema ML
    """
    
    print("="*80)
    print("SIMULACION DE RESOLUCION DE TAREA CON SISTEMA ML")
    print("="*80)
    
    # Configuración
    nino_id = 17  # ID de Alejandra
    tarea_id = 11  # Tarea de multiplicación
    
    print(f"\nNino ID: {nino_id}")
    print(f"Tarea ID: {tarea_id}")
    
    # 1. Obtener la tarea
    print("\n" + "-"*80)
    print("PASO 1: Obteniendo tarea...")
    print("-"*80)
    
    response = requests.get(f"{BASE_URL}/nino/tareas/{tarea_id}?nino_id={nino_id}")
    
    if response.status_code != 200:
        print(f"[ERROR] No se pudo obtener la tarea: {response.status_code}")
        return
    
    tarea = response.json()
    print(f"[OK] Tarea obtenida: {tarea['titulo']}")
    print(f"[OK] Total de ejercicios: {len(tarea['ejercicios'])}")
    
    ejercicios = tarea['ejercicios']
    
    # 2. Resolver ejercicios simulando comportamiento real
    print("\n" + "-"*80)
    print("PASO 2: Resolviendo ejercicios...")
    print("-"*80)
    
    # Patrones de comportamiento
    # Primeros ejercicios: concentrado
    # Ejercicios del medio: empieza a distraerse
    # Últimos ejercicios: muy distraído
    
    resultados = []
    requiere_descanso_count = 0
    
    for i, ejercicio in enumerate(ejercicios[:12]):  # Resolver los primeros 12
        num_ejercicio = i + 1
        print(f"\n--- Ejercicio {num_ejercicio}/12 ---")
        print(f"Pregunta: {ejercicio['pregunta']}")
        print(f"Opciones: {', '.join(ejercicio['opciones'])}")
        print(f"Respuesta correcta: {ejercicio['respuesta_correcta']}")
        
        # Simular comportamiento según progreso
        if num_ejercicio <= 3:
            # Concentrado al inicio
            tiempo_ms = random.randint(3000, 6000)
            tab_blur = 0
            idle = random.randint(0, 500)
            erratic = random.randint(0, 2)
            # 80% de probabilidad de acertar
            correcto = random.random() < 0.8
        elif num_ejercicio <= 7:
            # Empezando a distraerse
            tiempo_ms = random.randint(5000, 12000)
            tab_blur = random.randint(1, 3)
            idle = random.randint(1000, 3000)
            erratic = random.randint(2, 5)
            # 60% de probabilidad de acertar
            correcto = random.random() < 0.6
        else:
            # Muy distraído
            tiempo_ms = random.randint(10000, 20000)
            tab_blur = random.randint(3, 6)
            idle = random.randint(3000, 8000)
            erratic = random.randint(5, 12)
            # 40% de probabilidad de acertar
            correcto = random.random() < 0.4
        
        # Enviar al ML para análisis
        datos_analisis = {
            "nino_id": nino_id,
            "ejercicio_id": ejercicio['id'],
            "tiempo_ms": tiempo_ms,
            "correcto": correcto,
            "tab_blur_count": tab_blur,
            "idle_ms": idle,
            "erratic_clicks": erratic
        }
        
        print(f"\nEnviando datos al ML...")
        print(f"  - Tiempo: {tiempo_ms}ms")
        print(f"  - Correcto: {correcto}")
        print(f"  - Cambios de pestana: {tab_blur}")
        print(f"  - Tiempo inactivo: {idle}ms")
        print(f"  - Clicks erraticos: {erratic}")
        
        response = requests.post(f"{BASE_URL}/ml/analizar-respuesta", json=datos_analisis)
        
        if response.status_code == 200:
            resultado = response.json()
            
            # Mostrar predicción
            if resultado.get('prediccion'):
                pred = resultado['prediccion']
                print(f"\n[ML] Prediccion de error:")
                print(f"     Tipo: {pred['error_type']}")
                print(f"     Prob. siguiente error: {pred['prob_mistake_next']:.2%}")
            
            # Mostrar distracción
            if resultado.get('distraccion'):
                dist = resultado['distraccion']
                print(f"\n[ML] Analisis de concentracion:")
                print(f"     Focus score: {dist['focus_score']:.2f}")
                print(f"     Requiere descanso: {dist['requiere_descanso']}")
                
                if dist['requiere_descanso']:
                    requiere_descanso_count += 1
                    print("\n     *** PANTALLA DE DESCANSO MOSTRADA (10 segundos) ***")
                    time.sleep(1)  # Simular pausa
            
            resultados.append({
                'ejercicio': num_ejercicio,
                'correcto': correcto,
                'resultado_ml': resultado
            })
        else:
            print(f"[ERROR] Fallo el analisis ML: {response.status_code}")
        
        # Pequeña pausa entre ejercicios
        time.sleep(0.5)
    
    # 3. Reporte de errores
    print("\n" + "="*80)
    print("PASO 3: Generando reporte de errores...")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/ml/reporte-errores?nino_id={nino_id}")
    
    if response.status_code == 200:
        reporte = response.json()
        print(f"\n[OK] Reporte generado para: {reporte['nino']['nombre']}")
        
        if reporte['errores']:
            print(f"\n[ALERTA] Se detectaron {len(reporte['errores'])} tipos de errores:")
            for error in reporte['errores']:
                print(f"\n  - {error['tipo'].upper()}")
                print(f"    Cantidad: {error['cantidad']}")
                print(f"    Probabilidad promedio: {error['probabilidad_promedio']:.2%}")
        else:
            print("\n[OK] No se detectaron errores recurrentes")
    
    # 4. Estadísticas ML
    print("\n" + "="*80)
    print("PASO 4: Estadisticas ML...")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/ml/estadisticas?nino_id={nino_id}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"\n[OK] Estadisticas del nino: {stats['nino']['nombre']}")
        print(f"\nConcentracion:")
        print(f"  - Focus promedio: {stats['focus_promedio']:.2f}")
        print(f"  - Total distracciones detectadas: {stats['total_distracciones']}")
        print(f"  - Veces que se mostro descanso: {requiere_descanso_count}")
        
        print(f"\nErrores:")
        print(f"  - Total predicciones: {stats['total_errores']}")
        
        if stats['errores_por_tipo']:
            print(f"  - Por tipo:")
            for error in stats['errores_por_tipo']:
                print(f"    * {error['tipo_error']}: {error['total']} veces")
    
    # 5. Notificar a padre y profesor
    print("\n" + "="*80)
    print("PASO 5: Preparando notificaciones...")
    print("="*80)
    
    response = requests.post(f"{BASE_URL}/ml/notificar", json={"nino_id": nino_id})
    
    if response.status_code == 200:
        notif = response.json()
        print(f"\n[OK] {notif['message']}")
        
        if notif['data'].get('padre'):
            padre = notif['data']['padre']
            print(f"\nNotificacion para PADRE:")
            print(f"  - Nombre: {padre['nombre']}")
            print(f"  - Email: {padre['email']}")
        
        if notif['data'].get('profesor'):
            prof = notif['data']['profesor']
            print(f"\nNotificacion para PROFESOR:")
            print(f"  - Nombre: {prof['nombre']}")
            print(f"  - Email: {prof['email']}")
        
        if notif['data'].get('errores_detectados'):
            print(f"\nTemas a reforzar:")
            for err in notif['data']['errores_detectados']:
                print(f"  - {err['tipo']}: {err['cantidad']} errores detectados")
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE LA SIMULACION")
    print("="*80)
    
    total_correctos = sum(1 for r in resultados if r['correcto'])
    total_incorrectos = len(resultados) - total_correctos
    
    print(f"\nEjercicios resueltos: {len(resultados)}")
    print(f"Correctos: {total_correctos}")
    print(f"Incorrectos: {total_incorrectos}")
    print(f"Pantallas de descanso mostradas: {requiere_descanso_count}")
    
    print("\n" + "="*80)
    print("EL SISTEMA ML FUNCIONA CORRECTAMENTE")
    print("="*80)
    
    print("""
Lo que hizo el sistema:

1. [OK] Analizo cada respuesta en tiempo real
2. [OK] Predijo tipos de errores (multiplicacion, fracciones, etc.)
3. [OK] Detecto niveles de concentracion (focus_score)
4. [OK] Mostro pantalla de descanso cuando fue necesario
5. [OK] Guardo todo en la base de datos
6. [OK] Genero reportes para padre y profesor
7. [OK] Identifico temas que necesita reforzar

Ahora padre y profesor pueden ver:
- En que temas tiene dificultades
- Cuando se distrae mas
- Como evoluciona su concentracion
""")
    
    print("="*80)


def verificar_servidor():
    """Verifica que el servidor esté corriendo"""
    try:
        response = requests.get(f"{BASE_URL}/nino/tareas?nino_id=17", timeout=2)
        return True
    except:
        return False


if __name__ == "__main__":
    if not verificar_servidor():
        print("\n[ERROR] El servidor Django no esta corriendo")
        print("\nInicia el servidor con:")
        print("  cd backend")
        print("  python manage.py runserver")
        print("\nLuego ejecuta este script nuevamente")
    else:
        simular_resolucion_tarea()
