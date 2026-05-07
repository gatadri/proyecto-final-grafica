import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.views import EstadisticasHijosPadreView
from users.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

# Crear una petición simulada
factory = APIRequestFactory()
padre = User.objects.filter(role='padre').first()

# Simular petición GET
request = factory.get(f'/api/padre/{padre.id}/estadisticas-hijos')
request.user = padre  # Simular autenticación

# Crear vista y obtener respuesta
view = EstadisticasHijosPadreView.as_view()
response = view(Request(request), pk=padre.id)

# Mostrar respuesta JSON
print('=== RESPUESTA JSON DEL ENDPOINT ===\n')
print(json.dumps(response.data, indent=2, ensure_ascii=False))
