import requests
import json

url = 'http://127.0.0.1:8000/api/login'

# Prueba rápida con director
credentials = {'email': 'director@correo.com', 'password': 'password'}

print("=== PRUEBA DE LOGIN POST-MIGRACIONES ===\n")
print(f"URL: {url}")
print(f"Credenciales: {credentials['email']}")

try:
    response = requests.post(url, json=credentials, timeout=5)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✓ LOGIN EXITOSO")
        print(f"\nToken recibido: {data.get('token', 'N/A')[:50]}...")
        print(f"\nDatos del usuario:")
        user = data.get('user', {})
        print(f"  - ID: {user.get('id')}")
        print(f"  - Nombre: {user.get('nombre')} {user.get('apellido')}")
        print(f"  - Email: {user.get('email')}")
        print(f"  - Role: {user.get('role')}")
        print(f"  - Activo: {user.get('activo')}")
        
        # Si es padre, mostrar hijos
        if user.get('role') == 'padre' and user.get('hijos'):
            print(f"  - Hijos: {len(user.get('hijos', []))} hijo(s)")
            
    else:
        print("\n✗ LOGIN FALLIDO")
        print(f"Response: {response.text[:500]}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: No se puede conectar al servidor")
    print("   ¿El servidor está corriendo en http://127.0.0.1:8000?")
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("\n=== FIN DE LA PRUEBA ===")
