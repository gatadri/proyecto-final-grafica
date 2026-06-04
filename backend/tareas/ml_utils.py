import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml'))

import numpy as np
try:
    from ml.predict import predict_ffn, predict_rnn, num_features
    ML_LOADED = True
except Exception as e:
    print(f"Error cargando modelos ML: {e}")
    ML_LOADED = False


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


def detectar_distraccion(historial_estudiante):
    """
    Detecta si el estudiante está distraído basado en su historial reciente
    historial_estudiante: lista de diccionarios con las últimas respuestas (mínimo 3)
    """
    if not ML_LOADED or len(historial_estudiante) < 3:
        return {'requiere_descanso': False, 'focus_score': 1.0, 'motivo': None}
    
    try:
        # Verificar errores consecutivos
        errores_consecutivos = sum(1 for h in historial_estudiante[-5:] if h.get('correct', 1) == 0)
        
        # Verificar tiempo excesivo
        tiempos = [h.get('time_spent_ms', 0) for h in historial_estudiante if h.get('time_spent_ms', 0) > 0]
        tiempo_promedio = np.mean(tiempos) if tiempos else 5000
        ultimo_tiempo = historial_estudiante[-1].get('time_spent_ms', 0)
        tiempo_excesivo = ultimo_tiempo > (tiempo_promedio * 3)
        
        # Si hay 3+ errores seguidos o tiempo excesivo, mostrar pantalla de distracción
        if errores_consecutivos >= 3:
            return {
                'requiere_descanso': True,
                'focus_score': 0.3,
                'motivo': 'errores_consecutivos'
            }
        
        if tiempo_excesivo:
            return {
                'requiere_descanso': True,
                'focus_score': 0.3,
                'motivo': 'tiempo_excesivo'
            }
        
        # Tomar las últimas 3 entradas
        ultimas_3 = historial_estudiante[-3:]
        
        # Convertir a array para el modelo RNN
        secuencia = []
        for entrada in ultimas_3:
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
            'motivo': 'bajo_focus' if requiere_descanso else None
        }
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
