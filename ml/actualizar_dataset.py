import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Leer dataset existente
df = pd.read_csv(os.path.join(BASE_DIR, "tdah_tutor_dataset.csv"))

# Añadir columnas si no existen
if "consecutive_errors" not in df.columns:
    df["consecutive_errors"] = 0

if "excessive_time" not in df.columns:
    df["excessive_time"] = 0

# Calcular valores para cada estudiante
for sid, group in df.groupby("student_id"):
    g = group.sort_values("item_id")
    indices = g.index
    
    # Errores consecutivos
    error_count = 0
    for idx in indices:
        if df.at[idx, "correct"] == 0:
            error_count += 1
        else:
            error_count = 0
        df.at[idx, "consecutive_errors"] = error_count
    
    # Tiempo excesivo (triple del promedio del estudiante)
    avg_time = g["time_spent_ms"].mean()
    for idx in indices:
        if df.at[idx, "time_spent_ms"] > (avg_time * 3):
            df.at[idx, "excessive_time"] = 1

# Guardar dataset actualizado
df.to_csv(os.path.join(BASE_DIR, "tdah_tutor_dataset.csv"), index=False)
print("Dataset actualizado con éxito")
print(f"Total de registros: {len(df)}")
print(f"Nuevas características añadidas: consecutive_errors, excessive_time")
