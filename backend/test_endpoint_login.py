import requests
import json

# URL del endpoint
url = 'http://127.0.0.1:8000/api/login'

# Casos de prueba
test_cases = [
    {'email': 'director@correo.com', 'password': 'password'},
    {'email': 'profecarlos@correo.com', 'password': 'password'},
    {'email': 'jose@correo.com', 'password': 'password'},
    {'email': 'juan@correo.com', 'password': '123456789'},
]

print("=== PRUEBA DE ENDPOINT LOGIN ===\n")
print(f"URL: {url}\n")

for credentials in test_cases:
    print(f"\nProbando: {credentials['email']}")
    print(f"Password: {credentials['password']}")
    
    try:
        response = requests.post(url, json=credentials, timeout=5)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] LOGIN EXITOSO")
            print(f"     Token: {data.get('token', 'N/A')[:50]}...")
            print(f"     Usuario: {data.get('user', {}).get('nombre')} {data.get('user', {}).get('apellido')}")
            print(f"     Role: {data.get('user', {}).get('role')}")
        else:
            print(f"[ERROR] LOGIN FALLIDO")
            print(f"        Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] No se puede conectar al servidor")
        print("        ¿El servidor Django está corriendo en http://127.0.0.1:8000?")
        break
    except Exception as e:
        print(f"[ERROR] Excepción: {str(e)}")

print("\n=== FIN DE PRUEBAS ===")
