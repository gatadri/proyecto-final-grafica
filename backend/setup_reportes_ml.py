import os
import sys
import subprocess

# Configurar path de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')

def main():
    print("=" * 60)
    print("CONFIGURACION DE SISTEMA DE REPORTES ML")
    print("=" * 60)
    print()
    
    # Paso 1: Ejecutar migraciones
    print("\nPaso 1: Ejecutando migraciones...")
    try:
        result = subprocess.run(
            ['python', 'manage.py', 'makemigrations'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error en makemigrations: {result.stderr}")
            return
        
        result = subprocess.run(
            ['python', 'manage.py', 'migrate'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error en migrate: {result.stderr}")
            return
        
        print("Migraciones completadas\n")
    except Exception as e:
        print(f"Error ejecutando migraciones: {e}")
        return
    
    # Paso 2: Etiquetar ejercicios
    print("Paso 2: Etiquetando ejercicios existentes...")
    try:
        import django
        django.setup()
        
        from etiquetar_ejercicios import etiquetar_ejercicios
        etiquetar_ejercicios()
        print("\nEjercicios etiquetados correctamente\n")
    except Exception as e:
        print(f"Error etiquetando ejercicios: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Paso 3: Mostrar instrucciones
    print("=" * 60)
    print("CONFIGURACION COMPLETADA")
    print("=" * 60)
    print()
    print("Endpoints disponibles:")
    print("   - GET  /api/tareas/ml/reporte-detallado?nino_id=X")
    print("   - GET  /api/tareas/ml/reporte-detallado?nino_id=X&tarea_id=Y")
    print()
    print("Para probar reportes:")
    print("   1. El nino debe completar tareas")
    print("   2. Acceder a: http://localhost:4200/reporte-detallado/17")
    print("      (reemplazar 17 con el ID del nino)")
    print()
    print("El sistema ahora detecta:")
    print("   - Tabla del 11, tabla del 8, etc. en multiplicaciones")
    print("   - Division entre 7, entre 9, etc.")
    print("   - Suma/resta/multiplicacion de fracciones")
    print("   - Y genera reportes detallados por tema")
    print()

if __name__ == '__main__':
    main()
