import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuración
NUM_STUDENTS = 500  # 500 estudiantes
EXERCISES_PER_STUDENT = 30  # 30 ejercicios por estudiante = 15,000 registros

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

print("Generando dataset masivo...")

data = []
item_id = 1

for student_id in range(1, NUM_STUDENTS + 1):
    # Perfil del estudiante (algunos son más distraídos, otros más enfocados)
    student_focus_base = np.random.beta(5, 2)  # Mayoría con buen focus
    student_speed_factor = np.random.uniform(0.7, 1.4)
    student_error_tendency = np.random.uniform(0.5, 1.5)
    
    # Habilidades del estudiante por skill
    skill_proficiency = {i: np.random.uniform(0.4, 0.95) for i in range(1, 20)}
    
    consecutive_errors = 0
    previous_times = []
    
    for exercise_num in range(EXERCISES_PER_STUDENT):
        # Fatiga: focus baja gradualmente durante la sesión
        fatigue_factor = max(0.6, 1 - (exercise_num / EXERCISES_PER_STUDENT) * 0.3)
        
        # Skill y dificultad
        skill_id = np.random.randint(1, 20)
        difficulty = np.random.choice([1, 2, 3, 4], p=[0.2, 0.35, 0.30, 0.15])
        
        # Tiempo de respuesta
        base_time_range = DIFFICULTY_CONFIGS[difficulty]['time_range']
        time_spent_ms = int(np.random.uniform(*base_time_range) * student_speed_factor)
        
        # Añadir variación por fatiga
        if fatigue_factor < 0.8:
            time_spent_ms = int(time_spent_ms * np.random.uniform(1.0, 1.5))
        
        # Determinar si es correcto
        skill_factor = skill_proficiency[skill_id]
        error_rate = DIFFICULTY_CONFIGS[difficulty]['error_rate'] * student_error_tendency
        error_rate = error_rate / skill_factor  # Mejor skill = menos errores
        error_rate *= (2 - fatigue_factor)  # Fatiga aumenta errores
        
        correct = np.random.random() > min(0.8, error_rate)
        
        # Actualizar errores consecutivos
        if not correct:
            consecutive_errors += 1
        else:
            consecutive_errors = 0
        
        # Tiempo excesivo
        excessive_time = 0
        if len(previous_times) >= 5:
            avg_time = np.mean(previous_times[-5:])
            if time_spent_ms > (avg_time * 3):
                excessive_time = 1
        
        previous_times.append(time_spent_ms)
        
        # Intentos
        attempts = 1
        if not correct:
            attempts = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
        
        # Hints
        hint_prob = DIFFICULTY_CONFIGS[difficulty]['hint_prob']
        if not correct:
            hint_prob *= 1.5
        
        used_hint = 1 if np.random.random() < hint_prob else 0
        n_hints = np.random.choice([0, 1, 2, 3], p=[0.7, 0.2, 0.08, 0.02]) if used_hint else 0
        
        # Respuesta rápida
        fast_response = 1 if time_spent_ms < 2000 else 0
        
        # Comportamientos de distracción
        distraction_level = 1 - (student_focus_base * fatigue_factor)
        
        tab_blur_count = 0
        if distraction_level > 0.4:
            tab_blur_count = np.random.poisson(distraction_level * 3)
        
        idle_ms = 0
        if distraction_level > 0.5:
            idle_ms = int(np.random.exponential(800) * distraction_level)
        
        erratic_clicks = 0
        if distraction_level > 0.6 or consecutive_errors >= 2:
            erratic_clicks = np.random.poisson(distraction_level * 2)
        
        # Tipo de error
        if correct:
            error_type = 'procedimiento'  # Placeholder para correctos
        else:
            # Tipo de error basado en contexto
            if consecutive_errors >= 3:
                error_type = np.random.choice(['inatencion', 'aleatorio'], p=[0.7, 0.3])
            elif excessive_time:
                error_type = np.random.choice(['inatencion', 'consigna'], p=[0.6, 0.4])
            elif fast_response:
                error_type = np.random.choice(['aleatorio', 'inatencion'], p=[0.6, 0.4])
            else:
                error_type = np.random.choice(ERROR_TYPES, p=ERROR_PROBS)
        
        # Predicción de próximo error
        will_mistake_next = 0
        if consecutive_errors >= 2 or distraction_level > 0.5:
            will_mistake_next = 1
        
        # Focus score
        focus_score = max(0.15, min(0.98, student_focus_base * fatigue_factor - (consecutive_errors * 0.1)))
        focus_score = round(focus_score, 2)
        
        # Si hay muchos errores consecutivos o tiempo excesivo, bajar focus
        if consecutive_errors >= 3:
            focus_score = min(focus_score, 0.4)
        if excessive_time:
            focus_score = min(focus_score, 0.45)
        
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
            'tab_blur_count': tab_blur_count,
            'idle_ms': idle_ms,
            'erratic_clicks': erratic_clicks,
            'error_type': error_type,
            'will_mistake_next': will_mistake_next,
            'focus_score': focus_score,
            'consecutive_errors': consecutive_errors,
            'excessive_time': excessive_time
        })
        
        item_id += 1
    
    if student_id % 50 == 0:
        print(f"Generados {student_id}/{NUM_STUDENTS} estudiantes ({len(data)} registros)...")

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar
output_path = os.path.join(BASE_DIR, "tdah_tutor_dataset.csv")
df.to_csv(output_path, index=False)

print(f"\nDataset generado exitosamente!")
print(f"Total de registros: {len(df)}")
print(f"Total de estudiantes: {NUM_STUDENTS}")
print(f"Ejercicios por estudiante: {EXERCISES_PER_STUDENT}")
print(f"\nEstadisticas:")
print(f"   - Tasa de aciertos: {df['correct'].mean():.1%}")
print(f"   - Focus promedio: {df['focus_score'].mean():.2f}")
print(f"   - Errores consecutivos (max): {df['consecutive_errors'].max()}")
print(f"   - Registros con tiempo excesivo: {df['excessive_time'].sum()}")
print(f"\nGuardado en: {output_path}")
