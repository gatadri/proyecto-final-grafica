import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino, Tarea, ProgresoTarea, Logro, LogroNino
from django.db.models import Sum, Count, Avg

print("=" * 70)
print("DIAGNÓSTICO COMPLETO - DASHBOARD DEL DIRECTOR (MySQL)")
print("=" * 70)

# 1. Verificar conexión
print("\n1. CONEXIÓN A BASE DE DATOS:")
print("-" * 70)
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE()")
        db = cursor.fetchone()
        print(f"✅ Conectado a: {db[0]}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# 2. Contar usuarios por rol
print("\n2. USUARIOS POR ROL:")
print("-" * 70)
total_usuarios = User.objects.count()
directores = User.objects.filter(role='director').count()
profesores = User.objects.filter(role='profesor').count()
padres = User.objects.filter(role='padre').count()

print(f"Total usuarios: {total_usuarios}")
print(f"  ├─ Directores: {directores}")
print(f"  ├─ Profesores: {profesores}")
print(f"  └─ Padres: {padres}")

if padres == 0:
    print("\n⚠️  PROBLEMA DETECTADO: No hay padres en la base de datos")
    print("   Solución: Ejecutar 'python crear_padres_mysql.py'")

# 3. Listar todos los usuarios
print("\n3. LISTADO DETALLADO DE USUARIOS:")
print("-" * 70)
usuarios = User.objects.all().order_by('role', 'nombre')
for usuario in usuarios:
    icono = "👔" if usuario.role == 'director' else "👨‍🏫" if usuario.role == 'profesor' else "👨‍👩‍👧"
    print(f"{icono} [{usuario.role.upper()}] {usuario.nombre} {usuario.apellido}")
    print(f"   Email: {usuario.email} | Activo: {'✅' if usuario.activo else '❌'}")
    
    if usuario.role == 'padre':
        hijos = usuario.hijos.all()
        if hijos.exists():
            print(f"   Hijos ({hijos.count()}):")
            for hijo in hijos:
                print(f"     • {hijo.nombre} {hijo.apellido} (PIN: {hijo.pin})")
        else:
            print(f"   ⚠️  Sin hijos asignados")
    
    if usuario.role == 'profesor':
        estudiantes = usuario.estudiantes.all()
        print(f"   Estudiantes: {estudiantes.count()}")

# 4. Estadísticas de estudiantes
print("\n4. ESTADÍSTICAS DE ESTUDIANTES:")
print("-" * 70)
total_estudiantes = Nino.objects.count()
print(f"Total estudiantes: {total_estudiantes}")

estudiantes_con_padre = Nino.objects.filter(padre__isnull=False).count()
estudiantes_sin_padre = Nino.objects.filter(padre__isnull=True).count()

print(f"  ├─ Con padre asignado: {estudiantes_con_padre}")
print(f"  └─ Sin padre asignado: {estudiantes_sin_padre}")

if estudiantes_sin_padre > 0:
    print("\n⚠️  Estudiantes sin padre:")
    ninos_sin_padre = Nino.objects.filter(padre__isnull=True)
    for nino in ninos_sin_padre:
        print(f"   • {nino.nombre} {nino.apellido} (ID: {nino.id})")

# 5. Estadísticas de tareas
print("\n5. ESTADÍSTICAS DE TAREAS:")
print("-" * 70)
total_tareas = Tarea.objects.count()
tareas_completadas = ProgresoTarea.objects.filter(completada=True).count()

print(f"Total tareas creadas: {total_tareas}")
print(f"Tareas completadas: {tareas_completadas}")

if total_tareas > 0:
    print("\nTareas por profesor:")
    tareas_por_profesor = Tarea.objects.values(
        'profesor__nombre', 'profesor__apellido'
    ).annotate(cantidad=Count('id')).order_by('-cantidad')
    
    for item in tareas_por_profesor:
        print(f"  • {item['profesor__nombre']} {item['profesor__apellido']}: {item['cantidad']} tareas")

# 6. Estadísticas generales (las que usa el dashboard)
print("\n6. DATOS PARA EL DASHBOARD:")
print("-" * 70)
stats_ninos = Nino.objects.aggregate(
    total_monedas=Sum('monedas'),
    total_xp=Sum('experiencia'),
    promedio_nivel=Avg('nivel')
)

print(f"Total Estudiantes: {total_estudiantes}")
print(f"Total Tareas Completadas: {tareas_completadas}")
print(f"Total Monedas en Sistema: {stats_ninos['total_monedas'] or 0}")
print(f"Total XP en Sistema: {stats_ninos['total_xp'] or 0}")
print(f"Promedio de Nivel: {stats_ninos['promedio_nivel'] or 0:.2f}")

# 7. Verificar endpoint de estadísticas
print("\n7. SIMULACIÓN DE ENDPOINT /api/director/estadisticas-generales:")
print("-" * 70)

from django.db.models import Q

estudiantes_activos = Nino.objects.filter(
    progreso_tareas__completada=True
).distinct().count()

progresos = ProgresoTarea.objects.filter(completada=True).aggregate(
    promedio_aciertos=Avg('cantidad_aciertos'),
    promedio_errores=Avg('cantidad_errores')
)

response_simulado = {
    'total_estudiantes': total_estudiantes,
    'total_tareas_completadas': tareas_completadas,
    'promedio_aciertos': progresos['promedio_aciertos'] or 0,
    'promedio_errores': progresos['promedio_errores'] or 0,
    'total_monedas_sistema': stats_ninos['total_monedas'] or 0,
    'total_xp_sistema': stats_ninos['total_xp'] or 0,
    'estudiantes_activos': estudiantes_activos,
}

print("Respuesta del endpoint:")
for key, value in response_simulado.items():
    print(f"  {key}: {value}")

# 8. Verificar endpoint de usuarios
print("\n8. SIMULACIÓN DE ENDPOINT /api/usuarios:")
print("-" * 70)
usuarios_response = []
for usuario in User.objects.all():
    user_data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'email': usuario.email,
        'role': usuario.role,
        'activo': usuario.activo
    }
    if usuario.role == 'padre':
        hijos = usuario.hijos.all()
        user_data['hijos'] = hijos.count()
    usuarios_response.append(user_data)

print(f"Total usuarios en respuesta: {len(usuarios_response)}")
print("\nDesglose:")
roles_count = {}
for u in usuarios_response:
    roles_count[u['role']] = roles_count.get(u['role'], 0) + 1

for role, count in roles_count.items():
    print(f"  {role}: {count}")

# 9. Diagnóstico de problemas
print("\n9. DIAGNÓSTICO DE PROBLEMAS:")
print("-" * 70)
problemas = []

if padres == 0:
    problemas.append("❌ No hay padres registrados")
else:
    print(f"✅ Hay {padres} padres registrados")

if estudiantes_sin_padre > 0:
    problemas.append(f"⚠️  Hay {estudiantes_sin_padre} estudiantes sin padre asignado")
else:
    print("✅ Todos los estudiantes tienen padre asignado")

if total_tareas == 0:
    problemas.append("⚠️  No hay tareas creadas")
else:
    print(f"✅ Hay {total_tareas} tareas creadas")

if tareas_completadas == 0:
    problemas.append("⚠️  No hay tareas completadas")
else:
    print(f"✅ Hay {tareas_completadas} tareas completadas")

if profesores == 0:
    problemas.append("❌ No hay profesores registrados")
else:
    print(f"✅ Hay {profesores} profesores registrados")

if directores == 0:
    problemas.append("❌ No hay director registrado")
else:
    print(f"✅ Hay {directores} director(es) registrado(s)")

# 10. Resumen y recomendaciones
print("\n10. RESUMEN Y RECOMENDACIONES:")
print("=" * 70)

if problemas:
    print("\n🔴 PROBLEMAS ENCONTRADOS:")
    for problema in problemas:
        print(f"  {problema}")
    
    print("\n📝 ACCIONES RECOMENDADAS:")
    if padres == 0:
        print("  1. Ejecutar: python crear_padres_mysql.py")
    if estudiantes_sin_padre > 0:
        print("  2. Ejecutar: python crear_padres_mysql.py (asigna padres automáticamente)")
    if total_tareas == 0:
        print("  3. Crear tareas desde el panel del profesor")
    if profesores == 0:
        print("  4. Crear profesores desde el panel del director")
else:
    print("\n✅ NO SE ENCONTRARON PROBLEMAS")
    print("   El sistema está correctamente configurado")

# 11. SQL directo para verificación
print("\n11. CONSULTAS SQL DIRECTAS:")
print("-" * 70)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT role, COUNT(*) as cantidad 
        FROM users_user 
        GROUP BY role
    """)
    results = cursor.fetchall()
    print("Usuarios por rol (directo de MySQL):")
    for row in results:
        print(f"  {row[0]}: {row[1]}")

print("\n" + "=" * 70)
print("✅ DIAGNÓSTICO COMPLETADO")
print("=" * 70)
