import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino
from users.models import User
from django.db import connection

print("="*60)
print("CONTANDO NIÑOS POR PROFESOR")
print("="*60)

# Usar SQL directo para evitar problemas de conversión
with connection.cursor() as cursor:
    # Contar profesores
    cursor.execute("SELECT COUNT(*) FROM users_user WHERE role='profesor'")
    total_profesores = cursor.fetchone()[0]
    print(f"\nTotal de profesores: {total_profesores}")
    
    # Obtener profesores y sus niños
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido, u.email, COUNT(n.id) as num_ninos
        FROM users_user u
        LEFT JOIN tareas_nino n ON n.profesor_id = u.id
        WHERE u.role = 'profesor'
        GROUP BY u.id, u.nombre, u.apellido, u.email
    """)
    
    profesores_data = cursor.fetchall()
    
    for prof_id, nombre, apellido, email, num_ninos in profesores_data:
        print(f"\nProfesor: {nombre} {apellido} ({email})")
        print(f"  - Niños asignados: {num_ninos}")
        
        if num_ninos > 0:
            cursor.execute("""
                SELECT nombre, apellido, grado
                FROM tareas_nino
                WHERE profesor_id = %s
            """, [prof_id])
            
            ninos = cursor.fetchall()
            for nombre, apellido, grado in ninos:
                print(f"    * {nombre} {apellido} (Grado {grado})")
    
    # Contar niños sin profesor
    cursor.execute("SELECT COUNT(*) FROM tareas_nino WHERE profesor_id IS NULL")
    ninos_sin_profesor = cursor.fetchone()[0]
    
    print(f"\n{'='*60}")
    print(f"Niños SIN profesor asignado: {ninos_sin_profesor}")
    
    if ninos_sin_profesor > 0:
        print("\nAsignando niños sin profesor al primer profesor...")
        
        if total_profesores > 0:
            cursor.execute("SELECT id, nombre, apellido FROM users_user WHERE role='profesor' LIMIT 1")
            primer_prof = cursor.fetchone()
            
            if primer_prof:
                prof_id, nombre, apellido = primer_prof
                cursor.execute("UPDATE tareas_nino SET profesor_id = %s WHERE profesor_id IS NULL", [prof_id])
                connection.commit()
                print(f"[OK] {ninos_sin_profesor} niños asignados a {nombre} {apellido}")

print(f"\n{'='*60}")
print("VERIFICACIÓN COMPLETADA")
print("="*60)
