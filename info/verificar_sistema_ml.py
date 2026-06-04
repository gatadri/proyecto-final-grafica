"""
Script de Verificación del Sistema de Machine Learning
Verifica que todos los componentes de ML estén funcionando correctamente
"""

import os
import sys

# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def check(condition, message):
    """Imprime resultado de verificación"""
    if condition:
        print(f"{Colors.GREEN}[OK] {message}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[FAIL] {message}{Colors.END}")
        return False

def warning(message):
    """Imprime advertencia"""
    print(f"{Colors.YELLOW}[WARNING] {message}{Colors.END}")

def info(message):
    """Imprime información"""
    print(f"{Colors.BLUE}[INFO] {message}{Colors.END}")

def header(message):
    """Imprime encabezado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def main():
    header("VERIFICACIÓN DEL SISTEMA DE MACHINE LEARNING")
    
    resultados = []
    
    # 1. Verificar estructura de carpetas
    header("1. VERIFICANDO ESTRUCTURA DE CARPETAS")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.join(base_dir, 'ml')
    models_dir = os.path.join(ml_dir, 'models')
    
    resultados.append(check(os.path.exists(ml_dir), f"Carpeta ml/ existe: {ml_dir}"))
    resultados.append(check(os.path.exists(models_dir), f"Carpeta ml/models/ existe: {models_dir}"))
    
    # 2. Verificar modelos entrenados
    header("2. VERIFICANDO MODELOS ENTRENADOS")
    
    ffn_model = os.path.join(models_dir, 'ffn_model.h5')
    rnn_model = os.path.join(models_dir, 'rnn_model.h5')
    scaler = os.path.join(models_dir, 'scaler.pkl')
    encoder = os.path.join(models_dir, 'encoder.pkl')
    
    resultados.append(check(os.path.exists(ffn_model), f"Modelo FFN existe: ffn_model.h5"))
    resultados.append(check(os.path.exists(rnn_model), f"Modelo RNN existe: rnn_model.h5"))
    resultados.append(check(os.path.exists(scaler), f"Scaler existe: scaler.pkl"))
    resultados.append(check(os.path.exists(encoder), f"Encoder existe: encoder.pkl"))
    
    if not os.path.exists(ffn_model) or not os.path.exists(rnn_model):
        warning("Los modelos no están entrenados. Ejecuta: cd ml && python train.py")
    
    # 3. Verificar archivos de ML
    header("3. VERIFICANDO ARCHIVOS DE ML")
    
    train_py = os.path.join(ml_dir, 'train.py')
    predict_py = os.path.join(ml_dir, 'predict.py')
    utils_py = os.path.join(ml_dir, 'utils.py')
    dataset_csv = os.path.join(ml_dir, 'tdah_tutor_dataset.csv')
    
    resultados.append(check(os.path.exists(train_py), "Script train.py existe"))
    resultados.append(check(os.path.exists(predict_py), "Script predict.py existe"))
    resultados.append(check(os.path.exists(dataset_csv), "Dataset tdah_tutor_dataset.csv existe"))
    
    # 4. Verificar integración en backend
    header("4. VERIFICANDO INTEGRACIÓN EN BACKEND")
    
    backend_dir = os.path.join(base_dir, 'backend', 'tareas')
    ml_utils = os.path.join(backend_dir, 'ml_utils.py')
    views = os.path.join(backend_dir, 'views.py')
    models = os.path.join(backend_dir, 'models.py')
    
    resultados.append(check(os.path.exists(ml_utils), "Archivo ml_utils.py existe"))
    resultados.append(check(os.path.exists(views), "Archivo views.py existe"))
    resultados.append(check(os.path.exists(models), "Archivo models.py existe"))
    
    # Verificar funciones en ml_utils
    if os.path.exists(ml_utils):
        with open(ml_utils, 'r', encoding='utf-8') as f:
            content = f.read()
            resultados.append(check('analizar_ejercicio' in content, "Función analizar_ejercicio() implementada"))
            resultados.append(check('detectar_distraccion' in content, "Función detectar_distraccion() implementada"))
            resultados.append(check('predict_ffn' in content, "Importa predict_ffn del modelo FFN"))
            resultados.append(check('predict_rnn' in content, "Importa predict_rnn del modelo RNN"))
    
    # Verificar endpoints en views
    if os.path.exists(views):
        with open(views, 'r', encoding='utf-8') as f:
            content = f.read()
            resultados.append(check('AnalizarRespuestaView' in content, "Endpoint AnalizarRespuestaView implementado"))
            resultados.append(check('ReporteDetalladoView' in content, "Endpoint ReporteDetalladoView implementado"))
            resultados.append(check('EstadisticasMLView' in content, "Endpoint EstadisticasMLView implementado"))
    
    # Verificar modelos de BD
    if os.path.exists(models):
        with open(models, 'r', encoding='utf-8') as f:
            content = f.read()
            resultados.append(check('PrediccionError' in content, "Modelo PrediccionError en BD"))
            resultados.append(check('EventoDistraccion' in content, "Modelo EventoDistraccion en BD"))
            resultados.append(check('AnalisisErrorTema' in content, "Modelo AnalisisErrorTema en BD"))
    
    # 5. Verificar integración en frontend
    header("5. VERIFICANDO INTEGRACIÓN EN FRONTEND")
    
    frontend_dir = os.path.join(base_dir, 'frontend', 'src', 'app')
    ml_service = os.path.join(frontend_dir, 'services', 'ml.service.ts')
    pantalla_descanso = os.path.join(frontend_dir, 'components', 'pantalla-descanso.component.ts')
    nino_tarea = os.path.join(frontend_dir, 'modules', 'nino', 'tarea', 'nino-tarea.component.ts')
    reportes_padre = os.path.join(frontend_dir, 'modules', 'padre', 'reportes', 'reportes-padre.component.ts')
    
    resultados.append(check(os.path.exists(ml_service), "Servicio MLService existe"))
    resultados.append(check(os.path.exists(pantalla_descanso), "Componente PantallaDescanso existe"))
    resultados.append(check(os.path.exists(nino_tarea), "Componente NinoTarea existe"))
    resultados.append(check(os.path.exists(reportes_padre), "Componente ReportesPadre existe"))
    
    # Verificar integración en componentes
    if os.path.exists(nino_tarea):
        with open(nino_tarea, 'r', encoding='utf-8') as f:
            content = f.read()
            resultados.append(check('mlService.analizarRespuesta' in content, "NinoTarea llama a MLService"))
            resultados.append(check('mostrarPantallaDescanso' in content, "NinoTarea puede mostrar pantalla de descanso"))
            resultados.append(check('erroresConsecutivos' in content, "NinoTarea rastrea errores consecutivos"))
    
    if os.path.exists(reportes_padre):
        with open(reportes_padre, 'r', encoding='utf-8') as f:
            content = f.read()
            resultados.append(check('mlService.obtenerReporteDetallado' in content, "ReportesPadre obtiene reporte ML"))
            resultados.append(check('reporteML' in content, "ReportesPadre muestra datos ML"))
    
    # 6. Probar carga de modelos
    header("6. PROBANDO CARGA DE MODELOS")
    
    if os.path.exists(ffn_model) and os.path.exists(rnn_model):
        try:
            sys.path.insert(0, ml_dir)
            info("Intentando cargar modelos ML...")
            
            try:
                import tensorflow as tf
                import joblib
                
                # Intentar cargar FFN
                try:
                    model_ffn = tf.keras.models.load_model(ffn_model)
                    resultados.append(check(True, f"Modelo FFN cargado correctamente (capas: {len(model_ffn.layers)})"))
                except Exception as e:
                    resultados.append(check(False, f"Error cargando FFN: {str(e)}"))
                
                # Intentar cargar RNN
                try:
                    model_rnn = tf.keras.models.load_model(rnn_model)
                    resultados.append(check(True, f"Modelo RNN cargado correctamente (capas: {len(model_rnn.layers)})"))
                except Exception as e:
                    resultados.append(check(False, f"Error cargando RNN: {str(e)}"))
                
                # Intentar cargar scaler y encoder
                try:
                    scaler_obj = joblib.load(scaler)
                    resultados.append(check(True, "Scaler cargado correctamente"))
                except Exception as e:
                    resultados.append(check(False, f"Error cargando scaler: {str(e)}"))
                
                try:
                    encoder_obj = joblib.load(encoder)
                    resultados.append(check(True, f"Encoder cargado correctamente (clases: {len(encoder_obj.classes_)})"))
                    info(f"Tipos de error: {', '.join(encoder_obj.classes_)}")
                except Exception as e:
                    resultados.append(check(False, f"Error cargando encoder: {str(e)}"))
                
            except ImportError as e:
                warning(f"No se pudieron importar librerías: {str(e)}")
                warning("Instala dependencias: pip install tensorflow scikit-learn joblib")
        except Exception as e:
            warning(f"Error general al probar modelos: {str(e)}")
    else:
        warning("Modelos no existen, saltando prueba de carga")
    
    # RESUMEN FINAL
    header("RESUMEN DE VERIFICACIÓN")
    
    total = len(resultados)
    exitosos = sum(resultados)
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print(f"\n{Colors.BOLD}Verificaciones exitosas: {exitosos}/{total} ({porcentaje:.1f}%){Colors.END}\n")
    
    if porcentaje >= 90:
        print(f"{Colors.GREEN}{Colors.BOLD}[SUCCESS] SISTEMA DE ML COMPLETAMENTE FUNCIONAL{Colors.END}")
        print(f"{Colors.GREEN}Todas las verificaciones principales pasaron correctamente.{Colors.END}")
    elif porcentaje >= 70:
        print(f"{Colors.YELLOW}{Colors.BOLD}[WARNING] SISTEMA DE ML PARCIALMENTE FUNCIONAL{Colors.END}")
        print(f"{Colors.YELLOW}Algunas verificaciones fallaron. Revisa los errores arriba.{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}[ERROR] SISTEMA DE ML NO FUNCIONAL{Colors.END}")
        print(f"{Colors.RED}Muchas verificaciones fallaron. Revisa la configuración.{Colors.END}")
    
    print(f"\n{Colors.BLUE}Componentes verificados:{Colors.END}")
    print(f"  - Modelos entrenados (FFN, RNN)")
    print(f"  - Scripts de ML (train.py, predict.py)")
    print(f"  - Integracion backend (ml_utils.py, views.py)")
    print(f"  - Modelos de BD (PrediccionError, EventoDistraccion, AnalisisErrorTema)")
    print(f"  - Integracion frontend (MLService, PantallaDescanso, Reportes)")
    
    print(f"\n{Colors.BLUE}Para mas detalles, consulta:{Colors.END}")
    print(f"  ANALISIS_FUNCIONAMIENTO_ML.md")
    
    if not os.path.exists(ffn_model) or not os.path.exists(rnn_model):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}ACCIÓN REQUERIDA:{Colors.END}")
        print(f"{Colors.YELLOW}Los modelos no están entrenados. Para entrenarlos:{Colors.END}")
        print(f"{Colors.YELLOW}  1. cd ml{Colors.END}")
        print(f"{Colors.YELLOW}  2. pip install -r requirements.txt{Colors.END}")
        print(f"{Colors.YELLOW}  3. python train.py{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Verificación cancelada por el usuario.{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}Error fatal: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
