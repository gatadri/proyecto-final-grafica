import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

print("=== VERIFICANDO USUARIOS ===\n")

# Total de usuarios
total_usuarios = User.objects.count()
print(f"Total usuarios en DB: {total_usuarios}")

# Usuarios por rol
for role in ['director', 'profesor', 'padre']:
    count = User.objects.filter(role=role).count()
    print(f"  - {role}: {count}")

print("\n=== LISTADO DE USUARIOS ===\n")

usuarios = User.objects.all()
for usuario in usuarios:
    print(f"ID: {usuario.id} | Nombre: {usuario.nombre} {usuario.apellido} | Email: {usuario.email} | Role: {usuario.role} | Activo: {usuario.activo}")

print(f"\n=== NIÑOS EN LA BASE DE DATOS ===\n")
ninos = Nino.objects.count()
print(f"Total niños: {ninos}")

print("\n=== VERIFICANDO ENDPOINT ===")
print("El endpoint 'usuarios' debería retornar todos estos usuarios")
