import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User

director = User.objects.get(email='director@correo.com')
director.is_staff = True
director.is_superuser = True
director.save()

print("=== ACTUALIZACION COMPLETA ===")
print(f"Email: {director.email}")
print(f"Password: password")
print(f"Role: {director.role}")
print(f"Activo: {director.activo}")
print(f"Is Staff: {director.is_staff}")
print(f"Is Superuser: {director.is_superuser}")
print("\n[OK] Usuario director listo para usar")
