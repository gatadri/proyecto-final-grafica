import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

import tensorflow as tf
from tensorflow.keras import layers, Model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)


def train_models():
    print("Iniciando entrenamiento...")

    # =========================
    # 1. CARGA DATOS
    # =========================
    df = pd.read_csv(os.path.join(BASE_DIR, "tdah_tutor_dataset.csv"))
    print(f"Datos cargados: {len(df)} registros")
    print(f"Estudiantes únicos: {df['student_id'].nunique()}")
    print(f"Tasa de aciertos: {df['correct'].mean():.1%}")

    # =========================
    # 2. PREPROCESAMIENTO
    # =========================
    le = LabelEncoder()
    df["error_type_enc"] = le.fit_transform(df["error_type"])

    # Calcular errores consecutivos y tiempo excesivo si no existen
    if "consecutive_errors" not in df.columns:
        df["consecutive_errors"] = 0
        df["excessive_time"] = 0
        
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

    num_features = [
        "difficulty", "time_spent_ms", "attempts", "used_hint",
        "n_hints", "fast_response", "correct", "tab_blur_count",
        "idle_ms", "erratic_clicks", "consecutive_errors", "excessive_time"
    ]

    X = df[num_features].values
    y_error = df["error_type_enc"].values
    y_next = df["will_mistake_next"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_error_train, y_error_test, y_next_train, y_next_test = train_test_split(
        X_scaled, y_error, y_next, test_size=0.2, random_state=42
    )
    print(f"Datos de entrenamiento: {len(X_train)}")
    print(f"Datos de prueba: {len(X_test)}")

    # =========================
    # 3. MODELO FFN MEJORADO
    # =========================
    print("\nEntrenando modelo FFN...")
    input_num = layers.Input(shape=(len(num_features),))
    x = layers.Dense(128, activation="relu")(input_num)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(32, activation="relu")(x)

    out_error = layers.Dense(len(le.classes_), activation="softmax", name="error_type")(x)
    out_next = layers.Dense(1, activation="sigmoid", name="will_mistake_next")(x)

    model_ffn = Model(inputs=input_num, outputs=[out_error, out_next])

    model_ffn.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss={
            "error_type": "sparse_categorical_crossentropy",
            "will_mistake_next": "binary_crossentropy"
        },
        metrics={
            "error_type": "accuracy",
            "will_mistake_next": "accuracy"
        }
    )

    # Early stopping para evitar overfitting
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    history_ffn = model_ffn.fit(
        X_train,
        {"error_type": y_error_train, "will_mistake_next": y_next_train},
        validation_data=(X_test, {"error_type": y_error_test, "will_mistake_next": y_next_test}),
        epochs=50,
        batch_size=32,
        callbacks=[early_stop],
        verbose=1
    )
    
    # Evaluar modelo FFN
    eval_results = model_ffn.evaluate(
        X_test,
        {"error_type": y_error_test, "will_mistake_next": y_next_test},
        verbose=0
    )
    print(f"\n✅ Modelo FFN entrenado")
    print(f"   - Precisión tipo de error: {eval_results[3]:.2%}")
    print(f"   - Precisión próximo error: {eval_results[4]:.2%}")

    # =========================
    # 4. MODELO RNN MEJORADO
    # =========================
    print("\nEntrenando modelo RNN...")
    seq_length = 5  # Aumentado a 5 para mejor contexto
    sequences, targets = [], []

    for sid, group in df.groupby("student_id"):
        g = group.sort_values("item_id")
        Xg = g[num_features].values
        yg = g["focus_score"].values

        if len(Xg) >= seq_length:
            for i in range(len(Xg) - seq_length + 1):
                sequences.append(Xg[i:i+seq_length])
                targets.append(yg[i:i+seq_length])

    X_seq = np.array(sequences)
    y_seq = np.array(targets)

    X_seq = np.array([scaler.transform(x) for x in X_seq])
    
    print(f"Secuencias generadas: {len(X_seq)}")

    # Split para validación
    split_idx = int(len(X_seq) * 0.8)
    X_seq_train, X_seq_test = X_seq[:split_idx], X_seq[split_idx:]
    y_seq_train, y_seq_test = y_seq[:split_idx], y_seq[split_idx:]

    seq_in = layers.Input(shape=(seq_length, len(num_features)))
    h = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(seq_in)
    h = layers.Dropout(0.3)(h)
    h = layers.Bidirectional(layers.LSTM(32, return_sequences=True))(h)
    h = layers.Dropout(0.2)(h)
    h = layers.TimeDistributed(layers.Dense(16, activation="relu"))(h)
    out_focus = layers.TimeDistributed(layers.Dense(1, activation="sigmoid"))(h)

    model_rnn = Model(seq_in, out_focus)
    model_rnn.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="mean_squared_error",
        metrics=["mae"]
    )

    early_stop_rnn = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    history_rnn = model_rnn.fit(
        X_seq_train, y_seq_train,
        validation_data=(X_seq_test, y_seq_test),
        epochs=50,
        batch_size=32,
        callbacks=[early_stop_rnn],
        verbose=1
    )
    
    # Evaluar modelo RNN
    rnn_loss, rnn_mae = model_rnn.evaluate(X_seq_test, y_seq_test, verbose=0)
    print(f"\n✅ Modelo RNN entrenado")
    print(f"   - MSE: {rnn_loss:.4f}")
    print(f"   - MAE: {rnn_mae:.4f}")

    # =========================
    # 5. GUARDAR TODO
    # =========================
    model_ffn.save(os.path.join(MODEL_DIR, "ffn_model.h5"))
    model_rnn.save(os.path.join(MODEL_DIR, "rnn_model.h5"))

    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(le, os.path.join(MODEL_DIR, "encoder.pkl"))

    print("\n" + "="*60)
    print("ENTRENAMIENTO COMPLETADO")
    print("="*60)
    print(f"Modelos guardados en: {MODEL_DIR}")
    print(f"Dataset: {len(df)} registros")
    print(f"FFN - Error type accuracy: {eval_results[3]:.2%}")
    print(f"FFN - Next mistake accuracy: {eval_results[4]:.2%}")
    print(f"RNN - Focus prediction MAE: {rnn_mae:.4f}")
    print("="*60)


if __name__ == "__main__":
    train_models()