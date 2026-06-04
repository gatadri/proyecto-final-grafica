import requests
import json

BASE_URL = "http://localhost:8000/api/tareas"

def probar_sistema_ml():
    """
    Prueba el sistema de ML
    """
    
    print("="*50)
    print("PRUEBA DEL SISTEMA DE ML")
    print("="*50)
    
    # Datos de ejemplo
    nino_id = 1  # Cambia esto por un ID real de tu base de datos
    
    # 1. Analizar una respuesta con error
    print("\n1. Analizando respuesta con error...")
    respuesta_error = {
        "nino_id": nino_id,
        "ejercicio_id": 1,
        "tiempo_ms": 15000,  # 15 segundos (tiempo alto)
        "correcto": False,
        "tab_blur_count": 3,  # Cambio de pestaña 3 veces
        "idle_ms": 5000,      # 5 segundos inactivo
        "erratic_clicks": 8   # 8 clicks erráticos
    }
    
    response = requests.post(f"{BASE_URL}/ml/analizar-respuesta", json=respuesta_error)
    if response.status_code == 200:
        data = response.json()
        print(f"   Predicción: {data.get('prediccion')}")
        print(f"   Distracción: {data.get('distraccion')}")
    else:
        print(f"   Error: {response.status_code} - {response.text}")
    
    # 2. Analizar varias respuestas para detectar distracción
    print("\n2. Simulando varias respuestas para detectar distracción...")
    for i in range(5):
        respuesta = {
            "nino_id": nino_id,
            "ejercicio_id": i,
            "tiempo_ms": 8000 + (i * 2000),  # Tiempo incrementando
            "correcto": i % 2 == 0,  # Alternando correcto/incorrecto
            "tab_blur_count": i,
            "idle_ms": 3000 + (i * 1000),
            "erratic_clicks": 5 + i
        }
        
        response = requests.post(f"{BASE_URL}/ml/analizar-respuesta", json=respuesta)
        if response.status_code == 200:
            data = response.json()
            if data.get('distraccion', {}).get('requiere_descanso'):
                print(f"   ⚠️ Respuesta {i+1}: REQUIERE DESCANSO - Focus: {data['distraccion']['focus_score']:.2f}")
            else:
                print(f"   ✓ Respuesta {i+1}: OK - Focus: {data['distraccion']['focus_score']:.2f}")
    
    # 3. Obtener reporte de errores
    print("\n3. Obteniendo reporte de errores...")
    response = requests.get(f"{BASE_URL}/ml/reporte-errores?nino_id={nino_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Niño: {data['nino']['nombre']} {data['nino']['apellido']}")
        print(f"   Errores detectados: {len(data['errores'])}")
        for error in data['errores']:
            print(f"      - {error['tipo']}: {error['cantidad']} veces (prob: {error['probabilidad_promedio']:.2f})")
    else:
        print(f"   Error: {response.status_code}")
    
    # 4. Notificar a padre y profesor
    print("\n4. Preparando notificaciones...")
    response = requests.post(f"{BASE_URL}/ml/notificar", json={"nino_id": nino_id})
    if response.status_code == 200:
        data = response.json()
        print(f"   {data['message']}")
        if data['data'].get('padre'):
            print(f"   Padre: {data['data']['padre']['nombre']} ({data['data']['padre']['email']})")
        if data['data'].get('profesor'):
            print(f"   Profesor: {data['data']['profesor']['nombre']} ({data['data']['profesor']['email']})")
    
    # 5. Ver estadísticas
    print("\n5. Estadísticas de ML...")
    response = requests.get(f"{BASE_URL}/ml/estadisticas?nino_id={nino_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total errores: {data['total_errores']}")
        print(f"   Focus promedio: {data['focus_promedio']:.2f}")
        print(f"   Total distracciones: {data['total_distracciones']}")
        print(f"   Errores por tipo:")
        for error in data['errores_por_tipo']:
            print(f"      - {error['tipo_error']}: {error['total']} (prob: {error['prob_promedio']:.2f})")
    
    print("\n" + "="*50)
    print("PRUEBA COMPLETADA")
    print("="*50)


if __name__ == "__main__":
    try:
        probar_sistema_ml()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el backend esté corriendo.")
    except Exception as e:
        print(f"Error: {e}")
