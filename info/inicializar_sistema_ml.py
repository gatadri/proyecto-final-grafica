#!/usr/bin/env python
"""
Script de inicialización del Sistema ML
Verifica y configura todo lo necesario
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, PrediccionError, EventoDistraccion
from users.models import User


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n" + "="*60)
    print("VERIFICANDO DEPENDENCIAS")
    print("="*60)
    
    dependencias = [
        'pandas', 'numpy', 'sklearn', 'tensorflow', 'joblib'
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"[OK] {dep} instalado")
        except ImportError:
            print(f"[ERROR] {dep} NO instalado")
            return False
    
    return True


def verificar_modelos():
    """Verifica que los modelos ML estén entrenados"""
    print("\n" + "="*60)
    print("VERIFICANDO MODELOS ML")
    print("="*60)
    
    modelos_requeridos = [
        'ml/models/ffn_model.h5',
        'ml/models/rnn_model.h5',
        'ml/models/scaler.pkl',
        'ml/models/encoder.pkl'
    ]
    
    todos_ok = True
    for modelo in modelos_requeridos:
        if os.path.exists(modelo):
            size = os.path.getsize(modelo)
            print(f"[OK] {modelo} ({size} bytes)")
        else:
            print(f"[ERROR] {modelo} NO encontrado")
            todos_ok = False
    
    return todos_ok


def verificar_base_datos():
    """Verifica que las tablas estén creadas"""
    print("\n" + "="*60)
    print("VERIFICANDO BASE DE DATOS")
    print("="*60)
    
    try:
        # Verificar tabla PrediccionError
        count = PrediccionError.objects.count()
        print(f"[OK] Tabla PrediccionError OK ({count} registros)")
        
        # Verificar tabla EventoDistraccion
        count = EventoDistraccion.objects.count()
        print(f"[OK] Tabla EventoDistraccion OK ({count} registros)")
        
        # Verificar tabla Nino
        count = Nino.objects.count()
        print(f"[OK] Tabla Nino OK ({count} registros)")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error en base de datos: {e}")
        return False


def crear_datos_prueba():
    """Crea datos de prueba si no existen"""
    print("\n" + "="*60)
    print("CREANDO DATOS DE PRUEBA")
    print("="*60)
    
    # Verificar si hay niños
    if Nino.objects.count() == 0:
        print("No hay niños en la base de datos.")
        print("Necesitas crear al menos un niño para probar el sistema.")
        print("\nPuedes hacerlo desde:")
        print("1. El admin de Django (http://localhost:8000/admin)")
        print("2. O ejecutando un script de seed")
        return False
    
    nino = Nino.objects.first()
    print(f"[OK] Usando nino de prueba: {nino.nombre} {nino.apellido} (ID: {nino.id})")
    
    if nino.padre:
        print(f"  - Padre: {nino.padre.email}")
    else:
        print("  - Sin padre asignado")
    
    if nino.profesor:
        print(f"  - Profesor: {nino.profesor.email}")
    else:
        print("  - Sin profesor asignado")
    
    return True


def prueba_prediccion():
    """Prueba el sistema de predicción"""
    print("\n" + "="*60)
    print("PROBANDO SISTEMA DE PREDICCIÓN")
    print("="*60)
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'ml'))
        from ml.predict import predict_ffn, num_features
        
        # Datos de prueba
        datos_prueba = {
            'difficulty': 2,
            'time_spent_ms': 15000,
            'attempts': 2,
            'used_hint': 0,
            'n_hints': 0,
            'fast_response': 0,
            'correct': 0,
            'tab_blur_count': 3,
            'idle_ms': 5000,
            'erratic_clicks': 8
        }
        
        resultado = predict_ffn(datos_prueba)
        print(f"[OK] Prediccion exitosa:")
        print(f"  - Tipo de error: {resultado['error_type']}")
        print(f"  - Probabilidad siguiente error: {resultado['prob_mistake_next']:.2%}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error en prediccion: {e}")
        import traceback
        traceback.print_exc()
        return False


def mostrar_endpoints():
    """Muestra los endpoints disponibles"""
    print("\n" + "="*60)
    print("ENDPOINTS API DISPONIBLES")
    print("="*60)
    
    endpoints = [
        ("POST", "/api/tareas/ml/analizar-respuesta", "Analizar respuesta y detectar errores/distracción"),
        ("GET", "/api/tareas/ml/reporte-errores?nino_id=X", "Obtener reporte de errores del niño"),
        ("POST", "/api/tareas/ml/notificar", "Notificar a padre y profesor"),
        ("GET", "/api/tareas/ml/estadisticas?nino_id=X", "Estadísticas ML del niño"),
    ]
    
    for metodo, url, desc in endpoints:
        print(f"\n{metodo:6} {url}")
        print(f"       -> {desc}")


def mostrar_ejemplo_uso():
    """Muestra ejemplo de uso"""
    print("\n" + "="*60)
    print("EJEMPLO DE USO")
    print("="*60)
    
    print("""
# Desde el frontend (Angular), después de que el niño responda:

this.mlService.analizarRespuesta({
  nino_id: 1,
  ejercicio_id: 1,
  tiempo_ms: 15000,
  correcto: false,
  tab_blur_count: 3,
  idle_ms: 5000,
  erratic_clicks: 8
}).subscribe(result => {
  // Si requiere descanso
  if (result.distraccion.requiere_descanso) {
    this.pantallaDescanso.iniciarDescanso(); // Muestra pantalla 10 seg
  }
  
  // Si hay error detectado
  if (result.prediccion) {
    console.log('Error en:', result.prediccion.error_type);
  }
});

# Para probar desde terminal:

cd backend
python test_ml_system.py
""")


def main():
    print("\n" + "="*60)
    print("SISTEMA ML - PREDICCIÓN DE ERRORES Y DETECCIÓN DE DISTRACCIONES")
    print("="*60)
    
    # 1. Verificar dependencias
    if not verificar_dependencias():
        print("\n⚠️  Instala las dependencias con: pip install -r ml/requirements.txt")
        return
    
    # 2. Verificar modelos
    if not verificar_modelos():
        print("\n⚠️  Entrena los modelos con: python ml/train.py")
        return
    
    # 3. Verificar BD
    if not verificar_base_datos():
        print("\n⚠️  Aplica las migraciones con: cd backend && python manage.py migrate")
        return
    
    # 4. Datos de prueba
    crear_datos_prueba()
    
    # 5. Prueba de predicción
    prueba_prediccion()
    
    # 6. Mostrar endpoints
    mostrar_endpoints()
    
    # 7. Ejemplo de uso
    mostrar_ejemplo_uso()
    
    print("\n" + "="*60)
    print("[OK] SISTEMA LISTO PARA USAR")
    print("="*60)
    print("\nProximos pasos:")
    print("1. Inicia el servidor: cd backend && python manage.py runserver")
    print("2. Prueba el sistema: cd backend && python test_ml_system.py")
    print("3. Integra en el frontend usando el servicio MLService")
    print("\n")


if __name__ == "__main__":
    main()
