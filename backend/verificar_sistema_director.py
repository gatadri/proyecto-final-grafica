import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino, Tarea, ProgresoTarea, ProgresoPractica, LogroNino

print("=" * 60)
print("VERIFICACIÓN DEL SISTEMA - DIRECTOR (MySQL)")
print("=" * 60)

# Verificar conexión MySQL
print("\n0. CONEXIÓN A BASE DE DATOS:")
print("-" * 60)
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE(), VERSION()")
        db_info = cursor.fetchone()
        print(f"Base de datos: {db_info[0]}")
        print(f"MySQL Version: {db_info[1]}")
        print("✅ Conexión exitosa")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit(1)

# 1. Verificar usuarios
print("\n1. USUARIOS EN EL SISTEMA:")
print("-" * 60)
usuarios = User.objects.all()
for user in usuarios:
    print(f"  [{user.role.upper()}] {user.nombre} {user.apellido} - {user.email}")
    print(f"    Activo: {user.activo}, Staff: {user.is_staff}")
    if user.role == 'padre':
        hijos = user.hijos.all()
        print(f"    Hijos: {hijos.count()}")
        for hijo in hijos:
            print(f"      - {hijo.nombre} {hijo.apellido} (PIN: {hijo.pin})")
    if user.role == 'profesor':
        estudiantes = user.estudiantes.all()
        print(f"    Estudiantes: {estudiantes.count()}")

print(f"\nTotal usuarios: {usuarios.count()}")
print(f"  - Directores: {usuarios.filter(role='director').count()}")
print(f"  - Profesores: {usuarios.filter(role='profesor').count()}")
print(f"  - Padres: {usuarios.filter(role='padre').count()}")

if usuarios.filter(role='padre').count() == 0:
    print("\n⚠️  ADVERTENCIA: No hay padres en el sistema")
    print("   Ejecuta: python crear_padres_mysql.py")

# 2. Verificar niños
print("\n2. ESTUDIANTES (NIÑOS):")
print("-" * 60)
ninos = Nino.objects.all()
print(f"  Total: {ninos.count()}")
for nino in ninos:
    print(f"  - {nino.nombre} {nino.apellido}")
    print(f"    Nivel: {nino.nivel}, XP: {nino.experiencia}, Monedas: {nino.monedas}")
    print(f"    Padre: {nino.padre.nombre if nino.padre else 'N/A'}")
    print(f"    Profesor: {nino.profesor.nombre if nino.profesor else 'N/A'}")

ninos_sin_padre = ninos.filter(padre__isnull=True).count()
if ninos_sin_padre > 0:
    print(f"\n⚠️  {ninos_sin_padre} estudiantes sin padre asignado")
    print("   Ejecuta: python crear_padres_mysql.py")

# 3. Verificar tareas
print("\n3. TAREAS CREADAS:")
print("-" * 60)
tareas = Tarea.objects.all()
print(f"  Total: {tareas.count()}")
for tarea in tareas:
    print(f"  - {tarea.titulo} (Tipo: {tarea.tipo_ejercicio})")
    print(f"    Profesor: {tarea.profesor.nombre} {tarea.profesor.apellido}")
    print(f"    Estudiantes asignados: {tarea.ninos.count()}")

# 4. Verificar progreso de tareas
print("\n4. PROGRESO DE TAREAS:")
print("-" * 60)
progresos = ProgresoTarea.objects.filter(completada=True)
print(f"  Tareas completadas: {progresos.count()}")
for progreso in progresos[:10]:  # Mostrar solo las primeras 10
    print(f"  - {progreso.nino.nombre}: {progreso.tarea.titulo}")
    print(f"    Puntos: {progreso.puntos_obtenidos}, Aciertos: {progreso.cantidad_aciertos}, Errores: {progreso.cantidad_errores}")

# 5. Verificar prácticas
print("\n5. PRÁCTICAS COMPLETADAS:")
print("-" * 60)
practicas = ProgresoPractica.objects.filter(completada=True)
print(f"  Total: {practicas.count()}")
for practica in practicas[:10]:  # Mostrar solo las primeras 10
    print(f"  - {practica.nino.nombre}: {practica.puntos_obtenidos} pts")
    print(f"    Aciertos: {practica.cantidad_aciertos}, Errores: {practica.cantidad_errores}")

# 6. Verificar logros
print("\n6. LOGROS DESBLOQUEADOS:")
print("-" * 60)
logros = LogroNino.objects.all()
print(f"  Total: {logros.count()}")
for logro in logros[:10]:  # Mostrar solo los primeros 10
    print(f"  - {logro.nino.nombre}: {logro.logro.nombre}")
    print(f"    Fecha: {logro.fecha_desbloqueado.strftime('%Y-%m-%d')}")

# 7. Resumen general
print("\n7. RESUMEN GENERAL:")
print("-" * 60)
print(f"  Total Usuarios: {User.objects.count()}")
print(f"    - Directores: {User.objects.filter(role='director').count()}")
print(f"    - Profesores: {User.objects.filter(role='profesor').count()}")
print(f"    - Padres: {User.objects.filter(role='padre').count()}")
print(f"  Total Estudiantes: {Nino.objects.count()}")
print(f"  Total Tareas: {Tarea.objects.count()}")
print(f"  Tareas Completadas: {ProgresoTarea.objects.filter(completada=True).count()}")
print(f"  Prácticas Completadas: {ProgresoPractica.objects.filter(completada=True).count()}")
print(f"  Logros Desbloqueados: {LogroNino.objects.count()}")

# 8. Verificar estadísticas
print("\n8. ESTADÍSTICAS DEL SISTEMA:")
print("-" * 60)
from django.db.models import Sum, Avg

stats = Nino.objects.aggregate(
    total_monedas=Sum('monedas'),
    total_xp=Sum('experiencia'),
    promedio_nivel=Avg('nivel')
)
print(f"  Total Monedas en Sistema: {stats['total_monedas'] or 0}")
print(f"  Total XP en Sistema: {stats['total_xp'] or 0}")
print(f"  Nivel Promedio: {stats['promedio_nivel'] or 0:.2f}")

progreso_stats = ProgresoTarea.objects.filter(completada=True).aggregate(
    promedio_aciertos=Avg('cantidad_aciertos'),
    promedio_errores=Avg('cantidad_errores')
)
print(f"  Promedio Aciertos por Tarea: {progreso_stats['promedio_aciertos'] or 0:.2f}")
print(f"  Promedio Errores por Tarea: {progreso_stats['promedio_errores'] or 0:.2f}")

print("\n" + "=" * 60)
print("VERIFICACIÓN COMPLETADA")
print("=" * 60)
