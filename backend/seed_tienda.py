import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Skin, Sticker

print('=== POBLANDO TIENDA CON SKINS Y STICKERS ===\n')

# Crear Skins
skins_data = [
    {
        'nombre': 'Niña',
        'descripcion': 'Avatar de niña',
        'imagen': 'nina.png',
        'avatar_key': 'nina1',
        'precio': 0,
        'rareza': 'comun'
    },
    {
        'nombre': 'Niño',
        'descripcion': 'Avatar de niño',
        'imagen': 'nino.png',
        'avatar_key': 'nino1',
        'precio': 0,
        'rareza': 'comun'
    },
    {
        'nombre': 'Astronauta',
        'descripcion': 'Traje espacial (niña)',
        'imagen': 'astronauta.png',
        'avatar_key': 'nina2',
        'precio': 50,
        'rareza': 'raro'
    },
    {
        'nombre': 'Astronauto',
        'descripcion': 'Traje espacial (niño)',
        'imagen': 'astronauto.png',
        'avatar_key': 'nino2',
        'precio': 60,
        'rareza': 'legendario'
    },
]

print('Creando Skins...')
for skin_data in skins_data:
    skin, created = Skin.objects.get_or_create(
        avatar_key=skin_data['avatar_key'],
        defaults=skin_data
    )
    if created:
        print(f'  OK Creada: {skin.nombre} ({skin.rareza}) - {skin.precio} monedas')
    else:
        print(f'  - Ya existe: {skin.nombre}')

# Crear Stickers
stickers_data = [
    {
        'nombre': 'Sticker Estrella',
        'descripcion': 'Sticker brillante de estrella',
        'imagen': 'sticker1.png',
        'precio': 10,
        'rareza': 'comun'
    },
    {
        'nombre': 'Sticker Cohete',
        'descripcion': 'Sticker de cohete espacial',
        'imagen': 'sticker2.png',
        'precio': 15,
        'rareza': 'comun'
    },
    {
        'nombre': 'Sticker Arcoíris',
        'descripcion': 'Sticker de arcoíris mágico',
        'imagen': 'sticker3.png',
        'precio': 20,
        'rareza': 'raro'
    },
    {
        'nombre': 'Sticker Unicornio',
        'descripcion': 'Sticker de unicornio legendario',
        'imagen': 'sticker4.png',
        'precio': 25,
        'rareza': 'raro'
    },
    {
        'nombre': 'Sticker Galaxia',
        'descripcion': 'Sticker de galaxia brillante',
        'imagen': 'sticker5.png',
        'precio': 30,
        'rareza': 'legendario'
    },
]

print('\nCreando Stickers...')
for sticker_data in stickers_data:
    sticker, created = Sticker.objects.get_or_create(
        nombre=sticker_data['nombre'],
        defaults=sticker_data
    )
    if created:
        print(f'  OK Creado: {sticker.nombre} ({sticker.rareza}) - {sticker.precio} monedas')
    else:
        print(f'  - Ya existe: {sticker.nombre}')

print('\n=== TIENDA POBLADA EXITOSAMENTE ===')
print(f'Total Skins: {Skin.objects.count()}')
print(f'Total Stickers: {Sticker.objects.count()}')
