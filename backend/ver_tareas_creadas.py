import os
import sys
import django

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Ejercicio, Nino

def listar_tareas():
    """Lista todas las tareas disponibles"""
    print("="*80)
    print("TAREAS DISPONIBLES EN LA BASE DE DATOS")
    print("="*80)
    
    tareas = Tarea.objects.all().order_by('-id')
    
    if not tareas:
        print("\n[!] No hay tareas en la base de datos")
        print("\nCrea tareas con:")
        print("  python generar_tareas_ml.py")
        return
    
    print(f"\nTotal de tareas: {tareas.count()}")
    
    for tarea in tareas:
        print(f"\n{'='*80}")
        print(f"ID: {tarea.id}")
        print(f"Titulo: {tarea.titulo}")
        print(f"Descripcion: {tarea.descripcion}")
        print(f"Tipo: {tarea.tipo_ejercicio}")
        print(f"Profesor: {tarea.profesor.nombre} {tarea.profesor.apellido}")
        print(f"Total ejercicios: {tarea.ejercicios.count()}")
        print(f"Asignada a: {tarea.ninos.count()} ninos")
        
        # Mostrar algunos ejercicios
        ejercicios = tarea.ejercicios.all()[:5]
        print(f"\nPrimeros ejercicios:")
        for ej in ejercicios:
            print(f"  {ej.orden}. {ej.pregunta}")
            print(f"     Opciones: {', '.join(ej.opciones)}")
            print(f"     Respuesta: {ej.respuesta_correcta}")
        
        if tarea.ejercicios.count() > 5:
            print(f"  ... y {tarea.ejercicios.count() - 5} ejercicios mas")
        
        # Mostrar ninos asignados
        print(f"\nNinos asignados:")
        for nino in tarea.ninos.all():
            print(f"  - {nino.nombre} {nino.apellido} (ID: {nino.id})")
        
        # Endpoints
        primer_nino = tarea.ninos.first()
        if primer_nino:
            print(f"\nEndpoints API:")
            print(f"  GET http://localhost:8000/api/tareas/nino/tareas/{tarea.id}?nino_id={primer_nino.id}")
    
    print(f"\n{'='*80}")
    print("COMANDOS UTILES")
    print("="*80)
    print("\n1. Ver todas las tareas de un nino:")
    print("   GET http://localhost:8000/api/tareas/nino/tareas?nino_id=17")
    
    print("\n2. Simular prueba completa:")
    print("   python simular_prueba_ml.py")
    
    print("\n3. Crear mas tareas:")
    print("   python generar_tareas_ml.py")
    
    print("\n4. Ver estadisticas ML:")
    print("   GET http://localhost:8000/api/tareas/ml/estadisticas?nino_id=17")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    listar_tareas()
