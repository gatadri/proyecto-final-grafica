import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from django.contrib.auth import authenticate
from users.models import User

print("=== PRUEBA DE AUTENTICACION ===\n")

# Casos de prueba
test_users = [
    ('director@correo.com', 'password'),
    ('profecarlos@correo.com', 'password'),
    ('jose@correo.com', 'password'),
    ('juan@correo.com', '123456789'),
]

for email, password in test_users:
    print(f"\nProbando: {email}")
    print(f"Password: {password}")
    
    # Método 1: authenticate() directo
    user = authenticate(email=email, password=password)
    if user:
        print(f"  [OK] Authenticate directo: EXITO")
        print(f"       Role: {user.role}, Activo: {user.activo}")
    else:
        print(f"  [ERROR] Authenticate directo: FALLO")
        
        # Debug: verificar si el usuario existe
        try:
            db_user = User.objects.get(email=email)
            print(f"  [DEBUG] Usuario existe en BD: {db_user.email}")
            print(f"          Activo: {db_user.activo}")
            print(f"          Role: {db_user.role}")
            
            # Verificar password
            if db_user.check_password(password):
                print(f"  [DEBUG] Password es correcta pero authenticate() falla")
            else:
                print(f"  [DEBUG] Password NO coincide en BD")
        except User.DoesNotExist:
            print(f"  [DEBUG] Usuario NO existe en BD")

print("\n=== FIN DE PRUEBAS ===")
