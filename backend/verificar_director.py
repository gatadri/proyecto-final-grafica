import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User

print("=== VERIFICACION USUARIO DIRECTOR ===\n")

try:
    director = User.objects.get(email='director@correo.com')
    print("[OK] Usuario encontrado:")
    print(f"  ID: {director.id}")
    print(f"  Nombre: {director.nombre}")
    print(f"  Apellido: {director.apellido}")
    print(f"  Email: {director.email}")
    print(f"  Role: {director.role}")
    print(f"  Activo: {director.activo}")
    print(f"  Is Staff: {director.is_staff}")
    print(f"  Is Superuser: {director.is_superuser}")
    print(f"  Password Hash: {director.password[:50]}...")
    
    print("\n=== PRUEBA DE CONTRASENA ===")
    if director.check_password('password'):
        print("[OK] La contrasena 'password' es correcta")
    else:
        print("[ERROR] La contrasena 'password' NO es correcta")
        print("\nIntentando corregir...")
        director.set_password('password')
        director.save()
        print("[OK] Contrasena actualizada exitosamente")
        
except User.DoesNotExist:
    print("[ERROR] Usuario director@correo.com NO existe")
    print("\nCreando usuario director...")
    director = User.objects.create_user(
        email='director@correo.com',
        password='password',
        nombre='Director',
        apellido='Sistema',
        role='director',
        activo=True,
        is_staff=True,
        is_superuser=True
    )
    print("[OK] Usuario director creado exitosamente")
