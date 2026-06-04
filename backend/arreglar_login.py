import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User

# Contraseñas estándar para todos los usuarios
USUARIOS = {
    'director@correo.com': 'password',
    'profecarlos@correo.com': 'password',
    'ayllon814@correo.com': 'password',
    'carlos@correo.com': '123456798',
    'ana@correo.com': '132465789',
    'luis@correo.com': '123456789',
    'maria@correo.com': '123465789',
    'jose@correo.com': 'password',
    'fabricio@correo.com': 'password',
    'amilcar@correo.com': 'password',
    'carla@correo.com': 'password',
    'juan@correo.com': '123456789',
    'pedro@correo.com': '123456789',
    'lucia@correo.com': '123456789',
    'mario@correo.com': '123456789',
    'sofia@correo.com': '123456789',
    'diego@correo.com': '123456789',
    'elena@correo.com': '123456789',
    'raul@correo.com': '123456789',
    'paola@correo.com': '123456789',
    'andres@correo.com': '123456789',
}

print("=== VERIFICACIÓN Y CORRECCIÓN DE USUARIOS ===\n")

# Verificar y corregir cada usuario
for email, password in USUARIOS.items():
    try:
        user = User.objects.get(email=email)
        
        # Activar usuario si está inactivo
        if not user.activo:
            user.activo = True
            print(f"[OK] Activando usuario: {email}")
        
        # Restablecer contraseña
        user.set_password(password)
        user.save()
        
        # Verificar que la contraseña funciona
        if user.check_password(password):
            print(f"[OK] {email} - Contrasena: {password} - Role: {user.role} - Activo: {user.activo}")
        else:
            print(f"[ERROR] {email} - La contrasena no coincide")
            
    except User.DoesNotExist:
        print(f"[ERROR] {email} - Usuario NO EXISTE en la base de datos")

print("\n=== RESUMEN ===")
print(f"Total usuarios en BD: {User.objects.count()}")
print(f"Usuarios activos: {User.objects.filter(activo=True).count()}")
print(f"Usuarios inactivos: {User.objects.filter(activo=False).count()}")

print("\n=== CREDENCIALES FINALES ===")
print("DIRECTOR: director@correo.com / password")
print("PROFESORES:")
print("  - profecarlos@correo.com / password")
print("  - carlos@correo.com / 123456798")
print("  - ana@correo.com / 132465789")
print("  - luis@correo.com / 123456789")
print("  - maria@correo.com / 123465789")
print("PADRES:")
print("  - jose@correo.com / password")
print("  - juan@correo.com / 123456789")
print("  - pedro@correo.com / 123456789")
print("  (y otros con 123456789)")
