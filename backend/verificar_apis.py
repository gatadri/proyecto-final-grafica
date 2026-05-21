import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from django.test import Client
from users.models import User
from tareas.models import Nino, Tarea, Skin, Sticker

print('=== VERIFICANDO APIS DEL SISTEMA ===\n')

client = Client()

# Obtener datos de prueba
try:
    director = User.objects.filter(role='director').first()
    profesor = User.objects.filter(role='profesor').first()
    padre = User.objects.filter(role='padre').first()
    nino = Nino.objects.first()
    
    print('Datos de prueba:')
    print(f'  Director: {director.email if director else "No encontrado"}')
    print(f'  Profesor: {profesor.email if profesor else "No encontrado"}')
    print(f'  Padre: {padre.email if padre else "No encontrado"}')
    print(f'  Niño: {nino.nombre if nino else "No encontrado"}')
    print()
    
    # APIs de Usuarios
    print('=== APIs de Usuarios ===')
    
    # Login
    response = client.post('/api/login', {'email': director.email, 'password': '123456'}, content_type='application/json')
    print(f'POST /api/login: {response.status_code}')
    
    # Usuarios
    response = client.get('/api/usuarios')
    print(f'GET /api/usuarios: {response.status_code}')
    
    # Estadísticas generales
    response = client.get('/api/director/estadisticas-generales')
    print(f'GET /api/director/estadisticas-generales: {response.status_code}')
    
    if padre:
        # Estadísticas de hijos
        response = client.get(f'/api/padre/{padre.id}/estadisticas-hijos')
        print(f'GET /api/padre/{padre.id}/estadisticas-hijos: {response.status_code}')
        
        # Hijos del padre
        response = client.get(f'/api/usuarios/{padre.id}/hijos')
        print(f'GET /api/usuarios/{padre.id}/hijos: {response.status_code}')
    
    if profesor:
        # Estadísticas de clase
        response = client.get(f'/api/profesor/{profesor.id}/estadisticas-clase')
        print(f'GET /api/profesor/{profesor.id}/estadisticas-clase: {response.status_code}')
        
        # Estudiantes del profesor
        response = client.get('/api/profesor/estudiantes')
        print(f'GET /api/profesor/estudiantes: {response.status_code}')
    
    print()
    
    # APIs de Tareas
    print('=== APIs de Tareas ===')
    
    response = client.get('/api/tareas')
    print(f'GET /api/tareas: {response.status_code}')
    
    if nino:
        response = client.get(f'/api/nino/tareas?nino_id={nino.id}')
        print(f'GET /api/nino/tareas?nino_id={nino.id}: {response.status_code}')
        
        response = client.get(f'/api/nino/progreso?nino_id={nino.id}')
        print(f'GET /api/nino/progreso?nino_id={nino.id}: {response.status_code}')
    
    print()
    
    # APIs de Logros
    print('=== APIs de Logros ===')
    
    response = client.get('/api/logros')
    print(f'GET /api/logros: {response.status_code}')
    
    if nino:
        response = client.get(f'/api/nino/logros?nino_id={nino.id}')
        print(f'GET /api/nino/logros?nino_id={nino.id}: {response.status_code}')
    
    print()
    
    # APIs de Práctica
    print('=== APIs de Práctica ===')
    
    response = client.get('/api/nino/ejercicios-practica?cantidad=5')
    print(f'GET /api/nino/ejercicios-practica?cantidad=5: {response.status_code}')
    
    print()
    
    # APIs de Tienda
    print('=== APIs de Tienda ===')
    
    if nino:
        response = client.get(f'/api/tienda/skins?nino_id={nino.id}')
        print(f'GET /api/tienda/skins?nino_id={nino.id}: {response.status_code}')
        
        response = client.get(f'/api/tienda/stickers?nino_id={nino.id}')
        print(f'GET /api/tienda/stickers?nino_id={nino.id}: {response.status_code}')
    
    response = client.get('/api/inventario/tienda')
    print(f'GET /api/inventario/tienda: {response.status_code}')
    
    print()
    
    # Resumen
    print('=== RESUMEN ===')
    print(f'Total Usuarios: {User.objects.count()}')
    print(f'Total Niños: {Nino.objects.count()}')
    print(f'Total Tareas: {Tarea.objects.count()}')
    print(f'Total Skins: {Skin.objects.count()}')
    print(f'Total Stickers: {Sticker.objects.count()}')
    
    print('\n=== VERIFICACIÓN COMPLETADA ===')
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
