import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from django.test import RequestFactory
from rest_framework.test import force_authenticate
from users.views import UsuariosView
from users.models import User
import json

print("=== PROBANDO ENDPOINT DE USUARIOS ===\n")

# Obtener el director
director = User.objects.filter(role='director').first()
print(f"Director encontrado: {director.email}")

# Crear una request simulada
factory = RequestFactory()
request = factory.get('/usuarios')
force_authenticate(request, user=director)

# Instanciar la vista
view = UsuariosView.as_view()

# Hacer la llamada
response = view(request)

print(f"\nStatus Code: {response.status_code}")
print(f"Data Type: {type(response.data)}")

if response.status_code == 200:
    print(f"\nTotal usuarios devueltos: {len(response.data)}")
    print("\nPrimeros 3 usuarios:")
    for usuario in response.data[:3]:
        print(f"  - ID: {usuario['id']} | {usuario['nombre']} {usuario['apellido']} | Role: {usuario['role']}")
    
    # Contar por rol
    roles = {}
    for usuario in response.data:
        role = usuario['role']
        roles[role] = roles.get(role, 0) + 1
    
    print("\nUsuarios por rol:")
    for role, count in roles.items():
        print(f"  - {role}: {count}")
else:
    print(f"Error: {response.data}")
