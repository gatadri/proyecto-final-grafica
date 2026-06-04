"""
Script para verificar usuarios existentes en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User

print("="*70)
print("VERIFICACIÓN DE USUARIOS EN LA BASE DE DATOS")
print("="*70)

usuarios = User.objects.all()

print(f"\nTotal de usuarios: {usuarios.count()}")
print("\nListado de usuarios:")
print("-"*70)

for user in usuarios:
    print(f"ID: {user.id}")
    print(f"Nombre: {user.nombre} {user.apellido}")
    print(f"Email: {user.email}")
    print(f"Rol: {user.role}")
    print(f"Activo: {user.activo}")
    if user.role == 'padre':
        hijos = user.hijos.all()
        print(f"Hijos: {hijos.count()}")
        for hijo in hijos:
            print(f"  - {hijo.nombre} {hijo.apellido}")
    print("-"*70)

if usuarios.count() == 0:
    print("\n⚠️  No hay usuarios en la base de datos.")
    print("   Ejecuta 'python crear_usuarios_demo.py' para crear usuarios de prueba.")
