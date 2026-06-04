import os
import numpy as np
import joblib
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Cargar una sola vez (IMPORTANTE)
model_ffn = tf.keras.models.load_model(os.path.join(MODEL_DIR, "ffn_model.h5"))
model_rnn = tf.keras.models.load_model(os.path.join(MODEL_DIR, "rnn_model.h5"))

scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
encoder = joblib.load(os.path.join(MODEL_DIR, "encoder.pkl"))


num_features = [
    "difficulty", "time_spent_ms", "attempts", "used_hint",
    "n_hints", "fast_response", "correct", "tab_blur_count",
    "idle_ms", "erratic_clicks", "consecutive_errors", "excessive_time"
]


def predict_ffn(data):
    """
    data = dict con las features
    """

    X = np.array([[data[f] for f in num_features]])
    X = scaler.transform(X)

    pred_error, pred_next = model_ffn.predict(X)

    error_class = encoder.inverse_transform([np.argmax(pred_error)])

    return {
        "error_type": error_class[0],
        "prob_mistake_next": float(pred_next[0][0])
    }


def predict_rnn(sequence):
    """
    sequence = lista de registros (últimos 3)
    """

    X = np.array([sequence])
    X = np.array([scaler.transform(x) for x in X])

    pred = model_rnn.predict(X)[0]

    return pred.flatten().tolist()