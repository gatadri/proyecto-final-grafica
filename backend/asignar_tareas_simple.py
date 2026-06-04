import os
import sys
import django

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Nino


def asignar_tareas_simples():
    print("="*80)
    print("ASIGNANDO TAREAS ML A TODOS LOS NINOS")
    print("="*80)
    
    # Obtener las tareas ML
    tareas_ml = Tarea.objects.filter(id__in=[11, 12, 13, 14])
    
    if not tareas_ml.exists():
        print("\n[ERROR] No se encontraron las tareas ML")
        return
    
    print(f"\n[OK] Encontradas {tareas_ml.count()} tareas ML")
    
    # Obtener todos los niños
    todos_ninos = Nino.objects.all()
    print(f"[OK] Total de ninos: {todos_ninos.count()}")
    
    # Asignar cada tarea a todos los niños
    for tarea in tareas_ml:
        print(f"\n[*] Asignando: {tarea.titulo} (ID: {tarea.id})")
        
        # Limpiar y reasignar
        tarea.ninos.clear()
        tarea.ninos.set(todos_ninos)
        
        print(f"    [OK] Asignada a {tarea.ninos.count()} ninos")
    
    print("\n" + "="*80)
    print("VERIFICACION")
    print("="*80)
    
    # Verificar un niño específico
    primer_nino = todos_ninos.first()
    if primer_nino:
        tareas_del_nino = primer_nino.tareas.filter(id__in=[11, 12, 13, 14])
        print(f"\n[VERIFICACION] Nino: {primer_nino.nombre} {primer_nino.apellido} (ID: {primer_nino.id})")
        print(f"[VERIFICACION] Tiene {tareas_del_nino.count()} tareas ML asignadas")
        
        for tarea in tareas_del_nino:
            print(f"  - {tarea.titulo} ({tarea.ejercicios.count()} ejercicios)")
    
    print("\n" + "="*80)
    print("INFORMACION PARA LA INTERFAZ")
    print("="*80)
    
    print("\nPara probar desde la interfaz web:")
    print("\n1. Inicia el servidor:")
    print("   cd backend")
    print("   python manage.py runserver")
    
    print("\n2. Accede a la interfaz:")
    print("   http://localhost:4200")
    
    print("\n3. Inicia sesion como NINO:")
    for nino in todos_ninos[:3]:
        print(f"\n   Nino: {nino.nombre} {nino.apellido}")
        print(f"   PIN: {nino.pin}")
        print(f"   ID: {nino.id}")
    
    print("\n4. El nino vera las 4 tareas nuevas:")
    for tarea in tareas_ml:
        print(f"   - {tarea.titulo}")
    
    print("\n5. Al resolver ejercicios, el sistema ML:")
    print("   - Analizara cada respuesta en tiempo real")
    print("   - Detectara tipos de errores")
    print("   - Medira el nivel de concentracion")
    print("   - Mostrara pantalla de descanso si es necesario")
    
    print("\n" + "="*80)
    print("ENDPOINTS API DISPONIBLES")
    print("="*80)
    
    if primer_nino:
        print(f"\n# Ver todas las tareas del nino")
        print(f"GET http://localhost:8000/api/tareas/nino/tareas?nino_id={primer_nino.id}")
        
        print(f"\n# Ver tarea especifica (Multiplicacion)")
        print(f"GET http://localhost:8000/api/tareas/nino/tareas/11?nino_id={primer_nino.id}")
        
        print(f"\n# Analizar respuesta con ML")
        print(f"POST http://localhost:8000/api/tareas/ml/analizar-respuesta")
        print(f"""Body: {{
  "nino_id": {primer_nino.id},
  "ejercicio_id": 1,
  "tiempo_ms": 5000,
  "correcto": true,
  "tab_blur_count": 0,
  "idle_ms": 500,
  "erratic_clicks": 1
}}""")
    
    print("\n" + "="*80)
    print("LISTO PARA USAR EN LA INTERFAZ")
    print("="*80 + "\n")


if __name__ == "__main__":
    asignar_tareas_simples()
