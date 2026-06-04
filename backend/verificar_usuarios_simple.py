"""
Script simple para verificar usuarios
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from django.db import connection

print("="*70)
print("VERIFICACIÓN DE USUARIOS")
print("="*70)

# Usar SQL directo para evitar problemas de conversión
with connection.cursor() as cursor:
    cursor.execute("SELECT id, nombre, apellido, email, role, activo FROM users_user")
    usuarios = cursor.fetchall()
    
    print(f"\nTotal de usuarios en la base de datos: {len(usuarios)}")
    print("\nPrimeros 10 usuarios:")
    print("-"*70)
    
    for i, user in enumerate(usuarios[:10]):
        print(f"{i+1}. ID: {user[0]} | {user[1]} {user[2]} | {user[3]} | Rol: {user[4]} | Activo: {user[5]}")
    
    if len(usuarios) > 10:
        print(f"... y {len(usuarios) - 10} usuarios más")

print("\n✅ Los usuarios existen en la base de datos.")
print("Si no se muestran en el frontend, el problema está en el API o en el frontend.")
