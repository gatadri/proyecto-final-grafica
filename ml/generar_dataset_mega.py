import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ⚠️ CONFIGURACIÓN MEGA DATASET ⚠️
# Este script genera más de 50,000 registros para entrenamiento robusto
NUM_STUDENTS = 1000  # 1000 estudiantes
EXERCISES_PER_STUDENT = 50  # 50 ejercicios = 50,000 registros

print("⚠️  GENERANDO MEGA DATASET - ESTO PUEDE TARDAR VARIOS MINUTOS...")

# Tipos de error y sus probabilidades
ERROR_TYPES = ['procedimiento', 'inatencion', 'conceptual', 'consigna', 'aleatorio']
ERROR_PROBS = [0.25, 0.30, 0.25, 0.15, 0.05]

# Dificultades y sus características
DIFFICULTY_CONFIGS = {
    1: {'time_range': (1500, 2500), 'error_rate': 0.20, 'hint_prob': 0.15},
    2: {'time_range': (2000, 3500), 'error_rate': 0.30, 'hint_prob': 0.25},
    3: {'time_range': (2500, 4500), 'error_rate': 0.40, 'hint_prob': 0.35},
    4: {'time_range': (3500, 5500), 'error_rate': 0.35, 'hint_prob': 0.30}
}

print("Generando mega dataset...")

data = []
item_id = 1

for student_id in range(1, NUM_STUDENTS + 1):
    # Perfil del estudiante con más variación
    student_type = np.random.choice(['excelente', 'bueno', 'promedio', 'dificultad', 'tdah'], 
                                    p=[0.15, 0.30, 0.35, 0.15, 0.05])
    
    if student_type == 'excelente':
        student_focus_base = np.random.uniform(0.85, 0.98)
        student_error_tendency = np.random.uniform(0.3, 0.6)
    elif student_type == 'bueno':
        student_focus_base = np.random.uniform(0.70, 0.85)
        student_error_tendency = np.random.uniform(0.5, 0.9)
    elif student_type == 'promedio':
        student_focus_base = np.random.uniform(0.55, 0.70)
        student_error_tendency = np.random.uniform(0.8, 1.2)
    elif student_type == 'dificultad':
        student_focus_base = np.random.uniform(0.40, 0.55)
        student_error_tendency = np.random.uniform(1.2, 1.6)
    else:  # TDAH
        student_focus_base = np.random.uniform(0.25, 0.45)
        student_error_tendency = np.random.uniform(1.5, 2.0)
    
    student_speed_factor = np.random.uniform(0.6, 1.5)
    
    # Habilidades del estudiante por skill (más realistas)
    skill_proficiency = {}
    base_ability = np.random.uniform(0.4, 0.9)
    for i in range(1, 25):
        # Algunas skills son mejores/peores que otras
        skill_proficiency[i] = np.clip(base_ability + np.random.uniform(-0.2, 0.2), 0.2, 0.98)
    
    consecutive_errors = 0
    previous_times = []
    session_number = 0
    exercises_in_session = 0
    
    for exercise_num in range(EXERCISES_PER_STUDENT):
        # Simular sesiones de estudio (cada 10-15 ejercicios)
        if exercises_in_session > np.random.randint(10, 16):
            session_number += 1
            exercises_in_session = 0
            consecutive_errors = 0  # Reset en nueva sesión
        
        exercises_in_session += 1
        
        # Fatiga dentro de la sesión
        fatigue_factor = max(0.5, 1 - (exercises_in_session / 15) * 0.4)
        
        # Días de la semana afectan el rendimiento
        day_factor = np.random.choice([0.9, 0.95, 1.0, 1.0, 0.95, 0.85, 0.8], 
                                      p=[0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.1])
        
        # Skill y dificultad
        skill_id = np.random.randint(1, 25)
        
        # Progresión de dificultad a través del tiempo
        if exercise_num < 10:
            difficulty = np.random.choice([1, 2], p=[0.6, 0.4])
        elif exercise_num < 25:
            difficulty = np.random.choice([1, 2, 3], p=[0.2, 0.5, 0.3])
        else:
            difficulty = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])
        
        # Tiempo de respuesta con múltiples factores
        base_time_range = DIFFICULTY_CONFIGS[difficulty]['time_range']
        time_spent_ms = int(
            np.random.uniform(*base_time_range) * 
            student_speed_factor * 
            (2 - fatigue_factor) * 
            day_factor
        )
        
        # Añadir ruido realista
        time_spent_ms = max(1000, int(time_spent_ms + np.random.normal(0, 500)))
        
        # Determinar si es correcto (múltiples factores)
        skill_factor = skill_proficiency[skill_id]
        error_rate = DIFFICULTY_CONFIGS[difficulty]['error_rate'] * student_error_tendency
        error_rate = error_rate / skill_factor
        error_rate *= (2 - fatigue_factor * day_factor)
        
        # Racha de errores aumenta la probabilidad
        if consecutive_errors >= 2:
            error_rate *= (1 + consecutive_errors * 0.2)
        
        correct = np.random.random() > min(0.85, error_rate)
        
        # Actualizar errores consecutivos
        if not correct:
            consecutive_errors += 1
        else:
            consecutive_errors = 0
        
        # Tiempo excesivo
        excessive_time = 0
        if len(previous_times) >= 5:
            avg_time = np.mean(previous_times[-10:])  # Promedio de últimos 10
            if time_spent_ms > (avg_time * 3):
                excessive_time = 1
        
        previous_times.append(time_spent_ms)
        
        # Intentos
        attempts = 1
        if not correct:
            if consecutive_errors >= 3:
                attempts = np.random.choice([2, 3, 4], p=[0.4, 0.4, 0.2])
            else:
                attempts = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        
        # Hints más realistas
        hint_prob = DIFFICULTY_CONFIGS[difficulty]['hint_prob']
        if not correct:
            hint_prob *= 1.8
        if consecutive_errors >= 2:
            hint_prob *= 1.5
        
        used_hint = 1 if np.random.random() < min(0.8, hint_prob) else 0
        n_hints = 0
        if used_hint:
            if difficulty >= 3:
                n_hints = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
            else:
                n_hints = np.random.choice([1, 2], p=[0.7, 0.3])
        
        # Respuesta rápida
        fast_response = 1 if time_spent_ms < 2000 else 0
        
        # Comportamientos de distracción más complejos
        base_distraction = 1 - (student_focus_base * fatigue_factor * day_factor)
        
        # TDAH tiene patrones específicos
        if student_type == 'tdah':
            base_distraction = max(base_distraction, 0.6)
        
        tab_blur_count = 0
        if base_distraction > 0.4:
            tab_blur_count = np.random.poisson(base_distraction * 4)
        
        idle_ms = 0
        if base_distraction > 0.5:
            idle_ms = int(np.random.exponential(1000) * base_distraction)
        
        erratic_clicks = 0
        if base_distraction > 0.6 or consecutive_errors >= 3:
            erratic_clicks = np.random.poisson(base_distraction * 3)
        
        # Tipo de error contextual
        if correct:
            error_type = 'procedimiento'
        else:
            if consecutive_errors >= 4:
                error_type = np.random.choice(['inatencion', 'aleatorio'], p=[0.75, 0.25])
            elif excessive_time:
                error_type = np.random.choice(['inatencion', 'consigna', 'conceptual'], p=[0.5, 0.3, 0.2])
            elif fast_response:
                error_type = np.random.choice(['aleatorio', 'inatencion', 'procedimiento'], p=[0.5, 0.3, 0.2])
            elif student_type == 'tdah':
                error_type = np.random.choice(['inatencion', 'aleatorio', 'procedimiento'], p=[0.5, 0.3, 0.2])
            else:
                error_type = np.random.choice(ERROR_TYPES, p=ERROR_PROBS)
        
        # Predicción más sofisticada
        will_mistake_next = 0
        mistake_prob = 0
        if consecutive_errors >= 2:
            mistake_prob += 0.3 * consecutive_errors
        if base_distraction > 0.6:
            mistake_prob += 0.4
        if excessive_time:
            mistake_prob += 0.2
        
        will_mistake_next = 1 if mistake_prob > 0.5 else 0
        
        # Focus score complejo
        focus_score = student_focus_base * fatigue_factor * day_factor
        focus_score -= (consecutive_errors * 0.12)
        focus_score -= (tab_blur_count * 0.05)
        focus_score = max(0.15, min(0.98, focus_score))
        
        if consecutive_errors >= 3:
            focus_score = min(focus_score, 0.38)
        if excessive_time:
            focus_score = min(focus_score, 0.42)
        
        focus_score = round(focus_score, 2)
        
        # Crear registro
        data.append({
            'student_id': student_id,
            'item_id': item_id,
            'skill_id': skill_id,
            'difficulty': difficulty,
            'time_spent_ms': time_spent_ms,
            'attempts': attempts,
            'used_hint': used_hint,
            'n_hints': n_hints,
            'fast_response': fast_response,
            'correct': 1 if correct else 0,
            'tab_blur_count': min(10, tab_blur_count),
            'idle_ms': min(5000, idle_ms),
            'erratic_clicks': min(15, erratic_clicks),
            'error_type': error_type,
            'will_mistake_next': will_mistake_next,
            'focus_score': focus_score,
            'consecutive_errors': min(10, consecutive_errors),
            'excessive_time': excessive_time
        })
        
        item_id += 1
    
    if student_id % 100 == 0:
        print(f"Generados {student_id}/{NUM_STUDENTS} estudiantes ({len(data):,} registros)...")

# Crear DataFrame
df = pd.DataFrame(data)

# Estadísticas por tipo de estudiante
print("\n📊 Distribución de estudiantes:")
for student_type in ['excelente', 'bueno', 'promedio', 'dificultad', 'tdah']:
    count = len(df[df['student_id'].isin(range(1, NUM_STUDENTS+1))]) // 5
    print(f"   - {student_type.capitalize()}: ~{count} estudiantes")

# Guardar
output_path = os.path.join(BASE_DIR, "tdah_tutor_dataset.csv")
df.to_csv(output_path, index=False)

print(f"\nMEGA DATASET GENERADO EXITOSAMENTE!")
print(f"="*70)
print(f"ESTADISTICAS DEL DATASET:")
print(f"="*70)
print(f"   Total de registros: {len(df):,}")
print(f"   Total de estudiantes: {NUM_STUDENTS:,}")
print(f"   Ejercicios por estudiante: {EXERCISES_PER_STUDENT}")
print(f"\nMETRICAS DE CALIDAD:")
print(f"   Tasa de aciertos: {df['correct'].mean():.1%}")
print(f"   Focus promedio: {df['focus_score'].mean():.2f}")
print(f"   Errores consecutivos (max): {df['consecutive_errors'].max()}")
print(f"   Registros con tiempo excesivo: {df['excessive_time'].sum():,} ({df['excessive_time'].mean():.1%})")
print(f"   Estudiantes con alta distraccion: {len(df[df['focus_score'] < 0.4]):,} registros")
print(f"\nDISTRIBUCION DE ERRORES:")
for error_type in ERROR_TYPES:
    count = len(df[df['error_type'] == error_type])
    pct = count / len(df) * 100
    print(f"   - {error_type.capitalize()}: {count:,} ({pct:.1f}%)")
print(f"\nGuardado en: {output_path}")
print(f"="*70)
print(f"LISTO PARA ENTRENAR MODELOS CON: python train.py")
print(f"="*70)
