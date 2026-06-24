import sys
import os

# Configurar la ruta correcta para los modelos ML
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_PATH = os.path.join(PROJECT_ROOT, '..', 'ml')  # Subir un nivel más desde backend/tareas

if os.path.exists(ML_PATH) and ML_PATH not in sys.path:
    sys.path.insert(0, ML_PATH)

import numpy as np

# Intentar cargar modelos ML
ML_LOADED = False
predict_ffn = None
predict_rnn = None
num_features = None

try:
    from predict import predict_ffn, predict_rnn, num_features
    ML_LOADED = True
    print("[OK] Modelos ML cargados exitosamente")
except Exception as e:
    print(f"[AVISO] Modelos ML no disponibles: {e}")
    print(f"[INFO] Ruta ML intentada: {ML_PATH}")
    print("[INFO] La detección básica funcionará sin ML")


def analizar_ejercicio(data):
    """
    Analiza un ejercicio y predice el tipo de error
    data debe contener: difficulty, time_spent_ms, attempts, used_hint, n_hints, 
                       fast_response, correct, tab_blur_count, idle_ms, erratic_clicks
    """
    if not ML_LOADED:
        return None
    
    try:
        resultado = predict_ffn(data)
        return resultado
    except Exception as e:
        print(f"Error en predicción: {e}")
        return None


def detectar_distraccion(historial_estudiante, tiempo_promedio_historico=None):
    """
    Detecta si el estudiante está distraído basado en su historial reciente
    historial_estudiante: lista de diccionarios con las últimas respuestas (mínimo 3)
    tiempo_promedio_historico: tiempo promedio histórico del niño (opcional)
    """
    # IMPORTANTE: Esta función funciona incluso sin modelos ML cargados
    if len(historial_estudiante) < 1:
        return {'requiere_descanso': False, 'focus_score': 1.0, 'motivo': None}
    
    try:
        # Verificar errores consecutivos
        errores_consecutivos = sum(1 for h in historial_estudiante[-5:] if h.get('correct', 1) == 0)
        
        # Verificar tiempo excesivo basado en promedio histórico
        ultimo_tiempo = historial_estudiante[-1].get('time_spent_ms', 0)
        tiempo_excesivo = False
        promedio_usado = tiempo_promedio_historico
        
        if tiempo_promedio_historico and tiempo_promedio_historico > 0:
            # Usar el promedio histórico del niño (más preciso)
            tiempo_excesivo = ultimo_tiempo > (tiempo_promedio_historico * 3)
        elif len(historial_estudiante) >= 3:
            # Fallback: usar promedio de historial reciente
            tiempos = [h.get('time_spent_ms', 0) for h in historial_estudiante if h.get('time_spent_ms', 0) > 0]
            if tiempos:
                promedio_usado = np.mean(tiempos)
                tiempo_excesivo = ultimo_tiempo > (promedio_usado * 3)
        
        # Si hay 3+ errores seguidos o tiempo excesivo, mostrar pantalla de distracción
        if errores_consecutivos >= 3:
            return {
                'requiere_descanso': True,
                'focus_score': 0.3,
                'motivo': 'errores_consecutivos',
                'detalles': f'{errores_consecutivos} errores consecutivos'
            }
        
        if tiempo_excesivo:
            return {
                'requiere_descanso': True,
                'focus_score': 0.3,
                'motivo': 'tiempo_excesivo',
                'detalles': f'Tardó {ultimo_tiempo}ms (promedio: {int(promedio_usado) if promedio_usado else "N/A"}ms)'
            }
        
        # Si los modelos ML están cargados, usar análisis avanzado
        if ML_LOADED and len(historial_estudiante) >= 5:
            # Tomar las últimas 5 entradas (el modelo RNN requiere 5)
            ultimas_5 = historial_estudiante[-5:]
            
            # Convertir a array para el modelo RNN
            secuencia = []
            for entrada in ultimas_5:
                fila = [entrada.get(f, 0) for f in num_features]
                secuencia.append(fila)
            
            # Predecir focus_score
            focus_scores = predict_rnn(secuencia)
            focus_promedio = np.mean(focus_scores)
            
            # Si el focus es bajo (< 0.4), requiere descanso
            requiere_descanso = focus_promedio < 0.4
            
            return {
                'requiere_descanso': requiere_descanso,
                'focus_score': float(focus_promedio),
                'motivo': 'bajo_focus' if requiere_descanso else None,
                'detalles': f'Focus score: {focus_promedio:.2f}' if requiere_descanso else None
            }
        
        # Sin modelos ML, solo retornar que no hay distracción
        return {'requiere_descanso': False, 'focus_score': 1.0, 'motivo': None}
        
    except Exception as e:
        print(f"Error en detección de distracción: {e}")
        return {'requiere_descanso': False, 'focus_score': 1.0, 'motivo': None}


def crear_features_desde_respuesta(respuesta, ejercicio, tiempo_ms, nino, historial_reciente=None):
    """
    Crea el diccionario de features necesario para el ML desde una respuesta
    historial_reciente: lista de respuestas previas del niño para calcular errores consecutivos
    """
    # Calcular errores consecutivos
    consecutive_errors = 0
    if historial_reciente:
        for h in reversed(historial_reciente):
            if h.get('correct', 1) == 0:
                consecutive_errors += 1
            else:
                break
        if not respuesta:
            consecutive_errors += 1
    
    # Calcular si el tiempo es excesivo
    excessive_time = 0
    if historial_reciente and len(historial_reciente) > 0:
        tiempos = [h.get('time_spent_ms', 0) for h in historial_reciente if h.get('time_spent_ms', 0) > 0]
        if tiempos:
            tiempo_promedio = np.mean(tiempos)
            excessive_time = 1 if tiempo_ms > (tiempo_promedio * 3) else 0
    
    return {
        'difficulty': ejercicio.tarea.tipo_ejercicio if hasattr(ejercicio, 'tarea') else 1,
        'time_spent_ms': tiempo_ms,
        'attempts': 1,
        'used_hint': 0,
        'n_hints': 0,
        'fast_response': 1 if tiempo_ms < 2000 else 0,
        'correct': 1 if respuesta else 0,
        'tab_blur_count': 0,
        'idle_ms': 0,
        'erratic_clicks': 0,
        'consecutive_errors': consecutive_errors,
        'excessive_time': excessive_time
    }
