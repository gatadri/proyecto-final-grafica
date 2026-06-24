import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

print("=" * 60)
print("VERIFICACIÓN Y CREACIÓN DE PADRES - MySQL")
print("=" * 60)

# Verificar conexión a MySQL
print("\n1. VERIFICANDO CONEXIÓN A MYSQL...")
print("-" * 60)
from django.db import connection
print(f"Base de datos: {connection.settings_dict['NAME']}")
print(f"Host: {connection.settings_dict['HOST']}")
print(f"Puerto: {connection.settings_dict['PORT']}")
print(f"Usuario: {connection.settings_dict['USER']}")

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version[0]}")
        print("✅ Conexión exitosa a MySQL")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit(1)

# Verificar usuarios actuales
print("\n2. USUARIOS ACTUALES EN LA BASE DE DATOS:")
print("-" * 60)
usuarios = User.objects.all()
print(f"Total usuarios: {usuarios.count()}")

directores = usuarios.filter(role='director')
profesores = usuarios.filter(role='profesor')
padres = usuarios.filter(role='padre')

print(f"\n  Directores: {directores.count()}")
for u in directores:
    print(f"    - {u.nombre} {u.apellido} ({u.email})")

print(f"\n  Profesores: {profesores.count()}")
for u in profesores:
    print(f"    - {u.nombre} {u.apellido} ({u.email})")

print(f"\n  Padres: {padres.count()}")
for u in padres:
    print(f"    - {u.nombre} {u.apellido} ({u.email})")
    hijos = u.hijos.all()
    print(f"      Hijos: {hijos.count()}")

# Verificar niños sin padre asignado
print("\n3. VERIFICANDO NIÑOS EN LA BASE DE DATOS:")
print("-" * 60)
ninos = Nino.objects.all()
print(f"Total niños: {ninos.count()}")

ninos_sin_padre = ninos.filter(padre__isnull=True)
print(f"Niños sin padre: {ninos_sin_padre.count()}")

if ninos_sin_padre.exists():
    print("\nNiños sin padre asignado:")
    for nino in ninos_sin_padre:
        print(f"  - {nino.nombre} {nino.apellido} (ID: {nino.id})")
        print(f"    Profesor: {nino.profesor.nombre if nino.profesor else 'N/A'}")

# CREAR PADRES SI NO EXISTEN
print("\n4. CREANDO PADRES SI ES NECESARIO:")
print("-" * 60)

padres_data = [
    {
        'nombre': 'José',
        'apellido': 'García',
        'email': 'jose.garcia@correo.com',
        'password': 'password',
        'numero': '78945612'
    },
    {
        'nombre': 'María',
        'apellido': 'López',
        'email': 'maria.lopez@correo.com',
        'password': 'password',
        'numero': '78945613'
    },
    {
        'nombre': 'Carlos',
        'apellido': 'Martínez',
        'email': 'carlos.martinez@correo.com',
        'password': 'password',
        'numero': '78945614'
    },
    {
        'nombre': 'Ana',
        'apellido': 'Rodríguez',
        'email': 'ana.rodriguez@correo.com',
        'password': 'password',
        'numero': '78945615'
    },
    {
        'nombre': 'Pedro',
        'apellido': 'Fernández',
        'email': 'pedro.fernandez@correo.com',
        'password': 'password',
        'numero': '78945616'
    }
]

padres_creados = []
for padre_info in padres_data:
    try:
        # Verificar si ya existe
        if User.objects.filter(email=padre_info['email']).exists():
            padre = User.objects.get(email=padre_info['email'])
            print(f"✓ Padre ya existe: {padre.nombre} {padre.apellido}")
            padres_creados.append(padre)
        else:
            # Crear nuevo padre
            padre = User.objects.create_user(
                email=padre_info['email'],
                password=padre_info['password'],
                nombre=padre_info['nombre'],
                apellido=padre_info['apellido'],
                numero=padre_info.get('numero', ''),
                role='padre',
                activo=True
            )
            print(f"✅ Padre creado: {padre.nombre} {padre.apellido} ({padre.email})")
            padres_creados.append(padre)
    except Exception as e:
        print(f"❌ Error creando padre {padre_info['nombre']}: {e}")

# ASIGNAR PADRES A NIÑOS SIN PADRE
if ninos_sin_padre.exists() and padres_creados:
    print("\n5. ASIGNANDO PADRES A NIÑOS:")
    print("-" * 60)
    
    ninos_list = list(ninos_sin_padre)
    for i, nino in enumerate(ninos_list):
        # Asignar padre de forma circular
        padre = padres_creados[i % len(padres_creados)]
        nino.padre = padre
        nino.save()
        print(f"✅ Asignado {nino.nombre} {nino.apellido} → Padre: {padre.nombre} {padre.apellido}")

# VERIFICACIÓN FINAL
print("\n6. VERIFICACIÓN FINAL:")
print("-" * 60)

# Recargar datos
usuarios = User.objects.all()
ninos = Nino.objects.all()

print(f"Total usuarios: {usuarios.count()}")
print(f"  - Directores: {usuarios.filter(role='director').count()}")
print(f"  - Profesores: {usuarios.filter(role='profesor').count()}")
print(f"  - Padres: {usuarios.filter(role='padre').count()}")
print(f"\nTotal niños: {ninos.count()}")
print(f"  - Con padre asignado: {ninos.filter(padre__isnull=False).count()}")
print(f"  - Sin padre: {ninos.filter(padre__isnull=True).count()}")

# Mostrar relación padres-hijos
print("\n7. RELACIÓN PADRES-HIJOS:")
print("-" * 60)
padres = User.objects.filter(role='padre')
for padre in padres:
    hijos = padre.hijos.all()
    print(f"\n{padre.nombre} {padre.apellido} ({padre.email})")
    if hijos.exists():
        print(f"  Hijos ({hijos.count()}):")
        for hijo in hijos:
            print(f"    - {hijo.nombre} {hijo.apellido} (Grado: {hijo.grado})")
    else:
        print("  Sin hijos asignados")

print("\n" + "=" * 60)
print("✅ PROCESO COMPLETADO")
print("=" * 60)

# Mostrar credenciales
print("\n📝 CREDENCIALES DE PADRES CREADOS:")
print("-" * 60)
for padre_info in padres_data:
    print(f"Email: {padre_info['email']}")
    print(f"Password: password")
    print()
