"""
Script para probar los endpoints del módulo director
Ejecutar después de levantar el servidor Django
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def login_director():
    """Obtener token del director"""
    print("🔑 Iniciando sesión como director...")
    response = requests.post(f'{BASE_URL}/login', json={
        'email': 'director@correo.com',
        'password': 'password'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login exitoso: {data['user']['nombre']} {data['user']['apellido']}")
        return data['token']
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.text)
        return None

def test_usuarios(token):
    """Probar endpoint de usuarios"""
    print("\n📋 Probando /api/usuarios...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/usuarios', headers=headers)
    
    if response.status_code == 200:
        usuarios = response.json()
        print(f"✅ Usuarios obtenidos: {len(usuarios)}")
        print("\nDesglose por rol:")
        roles = {}
        for usuario in usuarios:
            role = usuario['role']
            roles[role] = roles.get(role, 0) + 1
            print(f"  - {usuario['nombre']} {usuario['apellido']} ({role})")
            if usuario.get('hijos'):
                print(f"    Hijos: {len(usuario['hijos'])}")
        
        print("\nResumen:")
        for role, count in roles.items():
            print(f"  {role}: {count}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def test_estadisticas(token):
    """Probar endpoint de estadísticas"""
    print("\n📊 Probando /api/director/estadisticas-generales...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/director/estadisticas-generales', headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ Estadísticas obtenidas:")
        print(f"  Total Estudiantes: {stats.get('total_estudiantes', 0)}")
        print(f"  Estudiantes Activos: {stats.get('estudiantes_activos', 0)}")
        print(f"  Tareas Completadas: {stats.get('total_tareas_completadas', 0)}")
        print(f"  Promedio Aciertos: {stats.get('promedio_aciertos', 0):.2f}")
        print(f"  Promedio Errores: {stats.get('promedio_errores', 0):.2f}")
        print(f"  Total Monedas: {stats.get('total_monedas_sistema', 0)}")
        print(f"  Total XP: {stats.get('total_xp_sistema', 0)}")
        
        if stats.get('tareas_por_tipo'):
            print("\nTareas por tipo:")
            for tipo in stats['tareas_por_tipo']:
                print(f"  - {tipo['tipo_ejercicio']}: {tipo['cantidad']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def test_logs(token):
    """Probar endpoint de logs"""
    print("\n📝 Probando /api/director/logs...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/director/logs', headers=headers)
    
    if response.status_code == 200:
        logs = response.json()
        print(f"✅ Logs obtenidos: {len(logs)}")
        
        # Contar por tipo
        tipos = {}
        for log in logs:
            tipo = log['tipo']
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print("\nEventos por tipo:")
        for tipo, count in tipos.items():
            print(f"  {tipo}: {count}")
        
        print("\nÚltimos 5 eventos:")
        for log in logs[:5]:
            print(f"  [{log['tipo']}] {log['fecha']} - {log['usuario']}")
            print(f"     {log['descripcion']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def main():
    print("=" * 60)
    print("PRUEBA DE ENDPOINTS DEL MÓDULO DIRECTOR")
    print("=" * 60)
    print("\n⚠️  Asegúrate de que el servidor Django esté corriendo:")
    print("   cd backend && python manage.py runserver\n")
    
    input("Presiona ENTER para continuar...")
    
    # Login
    token = login_director()
    if not token:
        print("\n❌ No se pudo obtener el token. Verifica que:")
        print("  1. El servidor Django esté corriendo")
        print("  2. El usuario director@correo.com existe con password 'password'")
        print("\nPuedes ejecutar: python verificar_director.py")
        return
    
    # Probar endpoints
    test_usuarios(token)
    test_estadisticas(token)
    test_logs(token)
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print("\nSi todos los endpoints funcionaron, el sistema está OK ✓")
    print("Ahora puedes probar en el frontend:")
    print("  1. Dashboard: http://localhost:4200/director/dashboard")
    print("  2. Usuarios: http://localhost:4200/director/usuarios")
    print("  3. Reportes: http://localhost:4200/director/reportes")
    print("  4. Logs: http://localhost:4200/director/logs")

if __name__ == '__main__':
    main()
