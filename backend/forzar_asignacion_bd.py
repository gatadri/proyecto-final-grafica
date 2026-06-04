import os
import sys
import django
import mysql.connector

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Tarea, Nino
from django.conf import settings


def verificar_asignacion_bd():
    """Verifica y fuerza la asignación directamente en la base de datos"""
    
    print("="*80)
    print("VERIFICACION Y ASIGNACION DIRECTA EN BASE DE DATOS")
    print("="*80)
    
    # Conectar directamente a MySQL
    try:
        conn = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )
        cursor = conn.cursor()
        
        print("\n[OK] Conectado a la base de datos")
        
        # Verificar tareas ML
        cursor.execute("SELECT id, titulo FROM tareas_tarea WHERE id IN (11, 12, 13, 14)")
        tareas = cursor.fetchall()
        
        if not tareas:
            print("\n[ERROR] No se encontraron las tareas ML")
            return
        
        print(f"\n[OK] Tareas ML encontradas: {len(tareas)}")
        for tarea_id, titulo in tareas:
            print(f"  - ID {tarea_id}: {titulo}")
        
        # Obtener todos los niños
        cursor.execute("SELECT id, nombre, apellido FROM tareas_nino")
        ninos = cursor.fetchall()
        
        print(f"\n[OK] Niños encontrados: {len(ninos)}")
        
        # Limpiar asignaciones existentes de estas tareas
        print("\n[*] Limpiando asignaciones anteriores...")
        cursor.execute("DELETE FROM tareas_tarea_ninos WHERE tarea_id IN (11, 12, 13, 14)")
        conn.commit()
        print(f"[OK] Eliminadas {cursor.rowcount} asignaciones antiguas")
        
        # Asignar cada tarea a TODOS los niños
        print("\n[*] Asignando tareas a todos los niños...")
        
        total_asignaciones = 0
        for tarea_id, titulo in tareas:
            for nino_id, nombre, apellido in ninos:
                cursor.execute(
                    "INSERT INTO tareas_tarea_ninos (tarea_id, nino_id) VALUES (%s, %s)",
                    (tarea_id, nino_id)
                )
                total_asignaciones += 1
            
            print(f"  - Tarea {tarea_id} asignada a {len(ninos)} niños")
        
        conn.commit()
        print(f"\n[OK] Total de asignaciones creadas: {total_asignaciones}")
        
        # Verificar
        print("\n" + "="*80)
        print("VERIFICACION DE ASIGNACIONES")
        print("="*80)
        
        primer_nino = ninos[0]
        nino_id = primer_nino[0]
        nombre = primer_nino[1]
        
        cursor.execute("""
            SELECT t.id, t.titulo 
            FROM tareas_tarea t
            INNER JOIN tareas_tarea_ninos tn ON t.id = tn.tarea_id
            WHERE tn.nino_id = %s AND t.id IN (11, 12, 13, 14)
        """, (nino_id,))
        
        tareas_asignadas = cursor.fetchall()
        
        print(f"\n[VERIFICACION] Niño: {nombre} (ID: {nino_id})")
        print(f"[VERIFICACION] Tareas ML asignadas: {len(tareas_asignadas)}")
        
        for tarea_id, titulo in tareas_asignadas:
            print(f"  - {titulo} (ID: {tarea_id})")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*80)
        print("PRUEBA DEL ENDPOINT")
        print("="*80)
        
        # Probar el endpoint
        import requests
        
        try:
            response = requests.get(f'http://localhost:8000/api/tareas/nino/tareas?nino_id={nino_id}', timeout=2)
            
            if response.status_code == 200:
                tareas_response = response.json()
                print(f"\n[OK] Endpoint funcionando")
                print(f"[OK] Total de tareas devueltas: {len(tareas_response)}")
                
                tareas_ml = [t for t in tareas_response if t['id'] in [11, 12, 13, 14]]
                print(f"[OK] Tareas ML devueltas: {len(tareas_ml)}")
                
                if len(tareas_ml) == 4:
                    print("\n*** EXITO: Las 4 tareas ML estan disponibles para el niño ***")
                    print("\nTareas disponibles:")
                    for t in tareas_ml:
                        print(f"  - {t['titulo']} (ID: {t['id']}) - {len(t['ejercicios'])} ejercicios")
                else:
                    print(f"\n[!] ATENCION: Solo {len(tareas_ml)} tareas ML devueltas en el endpoint")
            else:
                print(f"\n[!] Endpoint respondio con: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"\n[!] Servidor no esta corriendo")
            print("    Inicia con: python manage.py runserver")
        
        print("\n" + "="*80)
        print("INFORMACION PARA PROBAR EN LA INTERFAZ")
        print("="*80)
        
        print(f"\n1. El niño {nombre} (ID: {nino_id}) ahora tiene las 4 tareas ML")
        print(f"\n2. Todos los {len(ninos)} niños tienen las 4 tareas asignadas")
        
        print("\n3. Para probar:")
        print("   - Inicia el servidor: cd backend && python manage.py runserver")
        print("   - Inicia el frontend: cd frontend && ng serve")
        print("   - Login como niño y verás las 4 tareas ML")
        
        print("\n4. Niños disponibles para probar:")
        for nino_id, nombre, apellido in ninos[:5]:
            cursor2 = conn.cursor() if conn.is_connected() else mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            ).cursor()
            
            # Obtener PIN del niño
            cursor2.execute("SELECT pin FROM tareas_nino WHERE id = %s", (nino_id,))
            pin_result = cursor2.fetchone()
            pin = pin_result[0] if pin_result else "N/A"
            
            print(f"   - {nombre} {apellido} (ID: {nino_id}, PIN: {pin})")
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    verificar_asignacion_bd()
