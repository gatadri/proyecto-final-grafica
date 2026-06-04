"""
Script maestro para generar dataset masivo y entrenar modelos
Ejecuta todo el pipeline de ML en un solo comando
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("="*70)
    print("PIPELINE DE ENTRENAMIENTO ML - DATASET MASIVO")
    print("="*70)
    
    # Paso 1: Generar dataset
    print("\nPASO 1: Generando dataset masivo...")
    print("-"*70)
    try:
        import generar_dataset_masivo
        print("Dataset generado exitosamente\n")
    except Exception as e:
        print(f"Error generando dataset: {e}")
        return
    
    # Paso 2: Entrenar modelos
    print("\nPASO 2: Entrenando modelos de ML...")
    print("-"*70)
    try:
        from train import train_models
        train_models()
        print("\nModelos entrenados exitosamente\n")
    except Exception as e:
        print(f"Error entrenando modelos: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Paso 3: Validar modelos
    print("\nPASO 3: Validando modelos...")
    print("-"*70)
    try:
        import joblib
        import tensorflow as tf
        
        MODEL_DIR = os.path.join(BASE_DIR, "models")
        
        # Cargar modelos
        model_ffn = tf.keras.models.load_model(os.path.join(MODEL_DIR, "ffn_model.h5"))
        model_rnn = tf.keras.models.load_model(os.path.join(MODEL_DIR, "rnn_model.h5"))
        scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
        encoder = joblib.load(os.path.join(MODEL_DIR, "encoder.pkl"))
        
        print(f"Modelo FFN cargado correctamente")
        print(f"   - Inputs: {model_ffn.input_shape}")
        print(f"   - Outputs: {len(model_ffn.output)}")
        
        print(f"Modelo RNN cargado correctamente")
        print(f"   - Inputs: {model_rnn.input_shape}")
        print(f"   - Outputs: {model_rnn.output_shape}")
        
        print(f"Scaler y Encoder listos")
        print(f"   - Clases de error: {list(encoder.classes_)}")
        
    except Exception as e:
        print(f"Advertencia al validar: {e}")
    
    print("\n" + "="*70)
    print("PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*70)
    print("\nProximos pasos:")
    print("   1. Los modelos estan en: ml/models/")
    print("   2. Reinicia el servidor Django: python manage.py runserver")
    print("   3. El sistema esta listo para detectar distracciones")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
