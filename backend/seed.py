import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

# Limpiar datos anteriores
User.objects.all().delete()
Nino.objects.all().delete()

# Director
director = User.objects.create_user(
    nombre='Director', apellido='Admin',
    email='director@correo.com', password='password',
    role='director', activo=True
)

# Profesores
carlos = User.objects.create_user(
    nombre='Carlos', apellido='Profesor',
    email='profecarlos@correo.com', password='123456789',
    role='profesor', activo=True
)
ayllon = User.objects.create_user(
    nombre='Ayllon', apellido='Profesor',
    email='ayllon814@correo.com', password='123456789',
    role='profesor', activo=True
)

# Padres
jose_padre = User.objects.create_user(
    nombre='Jose', apellido='Padre',
    email='jose@correo.com', password='123456789',
    role='padre', activo=True
)
fabricio = User.objects.create_user(
    nombre='Fabricio', apellido='Padre',
    email='fabricio@correo.com', password='123456789',
    role='padre', activo=True
)
amilcar = User.objects.create_user(
    nombre='Amilcar', apellido='Padre',
    email='amilcar@correo.com', password='123456789',
    role='padre', activo=True
)
carla_padre = User.objects.create_user(
    nombre='Carla', apellido='Padre',
    email='carla@correo.com', password='123456789',
    role='padre', activo=True
)

# Niños
Nino.objects.create(nombre='Alejandra', apellido='', pin='8778', edad=10, grado=4, profesor=carlos, padre=jose_padre)
Nino.objects.create(nombre='Carla',     apellido='', pin='5079', edad=9,  grado=3, profesor=carlos, padre=carla_padre)
Nino.objects.create(nombre='Mariano',   apellido='', pin='1220', edad=11, grado=5, profesor=ayllon, padre=fabricio)
Nino.objects.create(nombre='Cristian',  apellido='', pin='3213', edad=10, grado=4, profesor=ayllon, padre=amilcar)
Nino.objects.create(nombre='Miguel',    apellido='', pin='9685', edad=9,  grado=3, profesor=carlos, padre=fabricio)
Nino.objects.create(nombre='Jose',      apellido='', pin='7895', edad=11, grado=5, profesor=ayllon, padre=jose_padre)

print('Usuarios creados:')
print(f'  Director:  director@correo.com / password')
print(f'  Profesor:  profecarlos@correo.com / 123456789')
print(f'  Profesor:  ayllon814@correo.com / 123456789')
print(f'  Padre:     jose@correo.com / 123456789')
print(f'  Padre:     fabricio@correo.com / 123456789')
print(f'  Padre:     amilcar@correo.com / 123456789')
print(f'  Padre:     carla@correo.com / 123456789')
print('Ninos creados: Alejandra, Carla, Mariano, Cristian, Miguel, Jose')
