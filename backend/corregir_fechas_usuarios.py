import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

print("=== CORRIGIENDO CAMPOS DE FECHA ===\n")

# Actualizar campos de fecha que pueden estar mal formateados
with connection.cursor() as cursor:
    # Verificar estructura de la tabla users_user
    cursor.execute("DESCRIBE users_user;")
    columns = cursor.fetchall()
    
    print("Estructura de users_user:")
    for col in columns:
        print(f"  {col}")
    
    # Intentar corregir date_joined si existe
    try:
        cursor.execute("""
            UPDATE users_user 
            SET date_joined = NOW() 
            WHERE date_joined IS NULL OR date_joined = '' OR date_joined = '0000-00-00 00:00:00'
        """)
        print(f"\n✓ Corregidos {cursor.rowcount} registros con date_joined inválido")
    except Exception as e:
        print(f"Error al corregir date_joined: {e}")
    
    # Intentar corregir last_login si existe
    try:
        cursor.execute("""
            UPDATE users_user 
            SET last_login = NULL 
            WHERE last_login = '' OR last_login = '0000-00-00 00:00:00'
        """)
        print(f"✓ Corregidos {cursor.rowcount} registros con last_login inválido")
    except Exception as e:
        print(f"Error al corregir last_login: {e}")

print("\n=== VERIFICANDO USUARIOS AHORA ===\n")

from users.models import User

try:
    usuarios = User.objects.all()
    print(f"Total usuarios: {usuarios.count()}")
    
    for usuario in usuarios:
        print(f"ID: {usuario.id} | {usuario.nombre} {usuario.apellido} | {usuario.email} | Role: {usuario.role}")
    
    print("\n✓ ¡CORRECCIÓN EXITOSA!")
except Exception as e:
    print(f"Error al listar usuarios: {e}")
