import os
import sys
import django

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Nino
from users.models import User


def verificar_y_asignar_tareas():
    print("="*80)
    print("VERIFICACION Y ASIGNACION DE TAREAS ML")
    print("="*80)
    
    # Obtener las tareas ML (IDs 11, 12, 13, 14)
    tareas_ml = Tarea.objects.filter(id__in=[11, 12, 13, 14])
    
    if not tareas_ml.exists():
        print("\n[ERROR] No se encontraron las tareas ML")
        print("Ejecuta primero: python generar_tareas_ml.py")
        return
    
    print(f"\n[OK] Encontradas {tareas_ml.count()} tareas ML")
    
    # Listar todos los profesores
    profesores = User.objects.filter(role='profesor')
    print(f"\n[OK] Profesores disponibles: {profesores.count()}")
    
    for profesor in profesores:
        ninos_profesor = Nino.objects.filter(profesor=profesor)
        print(f"\n  - {profesor.nombre} {profesor.apellido} ({profesor.email})")
        print(f"    Ninos asignados: {ninos_profesor.count()}")
        
        if ninos_profesor.count() > 0:
            print(f"    Lista de ninos:")
            for nino in ninos_profesor:
                print(f"      * {nino.nombre} {nino.apellido} (ID: {nino.id})")
                if nino.padre:
                    print(f"        Padre: {nino.padre.email}")
    
    print("\n" + "="*80)
    print("ASIGNANDO TAREAS A TODOS LOS NINOS")
    print("="*80)
    
    # Obtener TODOS los niños
    todos_ninos = Nino.objects.all()
    print(f"\n[INFO] Total de ninos en el sistema: {todos_ninos.count()}")
    
    # Asignar cada tarea a TODOS los niños
    for tarea in tareas_ml:
        print(f"\n[*] Procesando: {tarea.titulo} (ID: {tarea.id})")
        print(f"    Profesor actual: {tarea.profesor.nombre} {tarea.profesor.apellido}")
        
        # Limpiar asignaciones actuales
        tarea.ninos.clear()
        
        # Asignar a TODOS los niños
        tarea.ninos.set(todos_ninos)
        
        print(f"    [OK] Asignada a {tarea.ninos.count()} ninos")
        
        # Mostrar algunos niños
        for nino in tarea.ninos.all()[:5]:
            print(f"      - {nino.nombre} {nino.apellido} (ID: {nino.id})")
        if tarea.ninos.count() > 5:
            print(f"      ... y {tarea.ninos.count() - 5} mas")
    
    print("\n" + "="*80)
    print("RESUMEN FINAL")
    print("="*80)
    
    for tarea in tareas_ml:
        print(f"\n[ID: {tarea.id}] {tarea.titulo}")
        print(f"  - Profesor: {tarea.profesor.nombre} {tarea.profesor.apellido}")
        print(f"  - Ejercicios: {tarea.ejercicios.count()}")
        print(f"  - Asignada a: {tarea.ninos.count()} ninos")
        
        # Agrupar por profesor
        ninos_por_profesor = {}
        for nino in tarea.ninos.all():
            if nino.profesor:
                prof_nombre = f"{nino.profesor.nombre} {nino.profesor.apellido}"
                if prof_nombre not in ninos_por_profesor:
                    ninos_por_profesor[prof_nombre] = []
                ninos_por_profesor[prof_nombre].append(nino)
        
        if ninos_por_profesor:
            print(f"  - Distribucion por profesor:")
            for prof, ninos_list in ninos_por_profesor.items():
                print(f"    * {prof}: {len(ninos_list)} ninos")
    
    print("\n" + "="*80)
    print("COMO ACCEDER DESDE LA INTERFAZ")
    print("="*80)
    
    print("\n1. LOGIN COMO PROFESOR:")
    for profesor in profesores[:3]:
        ninos_prof = Nino.objects.filter(profesor=profesor)
        if ninos_prof.count() > 0:
            print(f"\n   Profesor: {profesor.email}")
            print(f"   Password: (tu password)")
            print(f"   Podra ver sus {ninos_prof.count()} ninos y las 4 tareas ML")
    
    print("\n2. LOGIN COMO NINO:")
    for nino in todos_ninos[:3]:
        print(f"\n   Nino: {nino.nombre} {nino.apellido}")
        print(f"   PIN: {nino.pin}")
        print(f"   Podra ver las 4 tareas ML asignadas")
    
    print("\n3. VER TAREAS DESDE API:")
    primer_nino = todos_ninos.first()
    print(f"\n   GET http://localhost:8000/api/tareas/nino/tareas?nino_id={primer_nino.id}")
    print(f"   Devolvera las 4 tareas ML")
    
    print("\n4. RESOLVER TAREA:")
    print(f"\n   GET http://localhost:8000/api/tareas/nino/tareas/11?nino_id={primer_nino.id}")
    print(f"   Devolvera la tarea de Multiplicacion con todos sus ejercicios")
    
    print("\n" + "="*80)
    print("VERIFICACION DE ENDPOINTS")
    print("="*80)
    
    # Verificar que funcionen los endpoints
    import requests
    
    try:
        response = requests.get('http://localhost:8000/api/tareas/nino/tareas?nino_id=' + str(primer_nino.id), timeout=2)
        if response.status_code == 200:
            tareas_response = response.json()
            print(f"\n[OK] Endpoint funcionando")
            print(f"[OK] El nino {primer_nino.nombre} tiene {len(tareas_response)} tareas")
            
            # Contar cuantas son las nuevas
            tareas_ml_count = sum(1 for t in tareas_response if t['id'] in [11, 12, 13, 14])
            print(f"[OK] De las cuales {tareas_ml_count} son tareas ML nuevas")
        else:
            print(f"\n[!] Endpoint respondio con codigo: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"\n[!] Servidor no esta corriendo")
        print(f"    Inicia con: python manage.py runserver")
    except Exception as e:
        print(f"\n[!] Error al verificar: {e}")
    
    print("\n" + "="*80)
    print("TAREAS ASIGNADAS CORRECTAMENTE")
    print("="*80)
    print("\nAhora puedes:")
    print("1. Iniciar sesion como profesor en la interfaz")
    print("2. Ver las tareas asignadas a tus ninos")
    print("3. Iniciar sesion como nino")
    print("4. Resolver las tareas de Multiplicacion, Division y Fracciones")
    print("5. El sistema ML analizara automaticamente cada respuesta")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    verificar_y_asignar_tareas()
