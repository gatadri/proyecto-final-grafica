# -*- coding: utf-8 -*-
"""
Script para verificar que los modelos ML se carguen correctamente
"""
import sys
import os

# Agregar rutas
backend_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_path)
ml_path = os.path.join(project_root, 'ml')

sys.path.insert(0, ml_path)
sys.path.insert(0, backend_path)

print("=" * 70)
print("VERIFICACION DE MODELOS ML")
print("=" * 70)

print(f"\nRutas configuradas:")
print(f"  Backend: {backend_path}")
print(f"  ML: {ml_path}")
print(f"  Python: {sys.executable}")

# Verificar dependencias
print("\n" + "-" * 70)
print("Verificando dependencias...")
print("-" * 70)

dependencias = {
    'numpy': 'numpy',
    'tensorflow': 'tensorflow',
    'joblib': 'joblib',
    'scikit-learn': 'sklearn'
}

faltantes = []
for nombre, modulo in dependencias.items():
    try:
        __import__(modulo)
        print(f"  [OK] {nombre}")
    except ImportError:
        print(f"  [ERROR] {nombre} - NO INSTALADO")
        faltantes.append(nombre)

if faltantes:
    print(f"\n[ERROR] Faltan dependencias: {', '.join(faltantes)}")
    print("\nPara instalar:")
    print("  pip install " + " ".join(faltantes))
    sys.exit(1)

# Verificar archivos de modelos
print("\n" + "-" * 70)
print("Verificando archivos de modelos...")
print("-" * 70)

model_dir = os.path.join(ml_path, 'models')
archivos_necesarios = [
    'ffn_model.h5',
    'rnn_model.h5',
    'scaler.pkl',
    'encoder.pkl'
]

falta_archivo = False
for archivo in archivos_necesarios:
    ruta = os.path.join(model_dir, archivo)
    if os.path.exists(ruta):
        tamanio = os.path.getsize(ruta) / 1024  # KB
        print(f"  [OK] {archivo} ({tamanio:.1f} KB)")
    else:
        print(f"  [ERROR] {archivo} - NO ENCONTRADO")
        falta_archivo = True

if falta_archivo:
    print(f"\n[ERROR] Faltan archivos de modelos en: {model_dir}")
    print("\nPara generar los modelos:")
    print(f"  cd {ml_path}")
    print("  python entrenar_todo.py")
    sys.exit(1)

# Intentar cargar los modelos
print("\n" + "-" * 70)
print("Cargando modelos ML...")
print("-" * 70)

try:
    from predict import predict_ffn, predict_rnn, num_features
    print("  [OK] Modelos cargados exitosamente")
    print(f"  [OK] Features esperados: {len(num_features)}")
    print(f"       {num_features}")
    
    # Probar prediccion
    print("\n" + "-" * 70)
    print("Probando prediccion...")
    print("-" * 70)
    
    data_test = {
        "difficulty": 1,
        "time_spent_ms": 5000,
        "attempts": 1,
        "used_hint": 0,
        "n_hints": 0,
        "fast_response": 1,
        "correct": 1,
        "tab_blur_count": 0,
        "idle_ms": 0,
        "erratic_clicks": 0,
        "consecutive_errors": 0,
        "excessive_time": 0
    }
    
    resultado = predict_ffn(data_test)
    print(f"  [OK] Prediccion FFN exitosa")
    print(f"       Tipo error: {resultado['error_type']}")
    print(f"       Prob siguiente error: {resultado['prob_mistake_next']:.2f}")
    
    # Probar RNN
    sequence_test = [[data_test[f] for f in num_features]] * 5  # RNN requiere 5 elementos
    focus_scores = predict_rnn(sequence_test)
    print(f"  [OK] Prediccion RNN exitosa")
    print(f"       Focus scores: {focus_scores}")
    
    print("\n" + "=" * 70)
    print("TODOS LOS MODELOS ML FUNCIONAN CORRECTAMENTE")
    print("=" * 70)
    
except Exception as e:
    print(f"  [ERROR] No se pudieron cargar los modelos: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Ahora probar con Django
print("\n" + "-" * 70)
print("Probando integracion con Django...")
print("-" * 70)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
    import django
    django.setup()
    
    from tareas.ml_utils import ML_LOADED, detectar_distraccion
    
    if ML_LOADED:
        print("  [OK] Modelos ML cargados en Django")
    else:
        print("  [ERROR] Modelos ML NO cargados en Django")
        sys.exit(1)
    
    # Probar deteccion
    historial_test = [
        {
            'difficulty': 1,
            'time_spent_ms': 5000,
            'attempts': 1,
            'used_hint': 0,
            'n_hints': 0,
            'fast_response': 1,
            'correct': 1,
            'tab_blur_count': 0,
            'idle_ms': 0,
            'erratic_clicks': 0
        }
    ] * 5  # Necesita 5 elementos para RNN
    
    resultado = detectar_distraccion(historial_test, 5000)
    print(f"  [OK] Deteccion funcional")
    print(f"       Requiere descanso: {resultado['requiere_descanso']}")
    print(f"       Focus score: {resultado.get('focus_score', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("INTEGRACION CON DJANGO EXITOSA")
    print("=" * 70)
    
except Exception as e:
    print(f"  [ERROR] Problema con Django: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("VERIFICACION COMPLETA - TODO FUNCIONAL")
print("=" * 70)
print("\nLos modelos ML estan listos para usar en produccion")
print("La deteccion de distraccion funcionara con ML incluido")
