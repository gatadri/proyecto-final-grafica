import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino

print('=== ASIGNANDO MONEDAS ===\n')

# Buscar a Jose con PIN 7895
jose = Nino.objects.filter(nombre='Jose', pin='7895').first()
if jose:
    monedas_anteriores = jose.monedas
    jose.monedas = 50
    jose.save()
    print(f'Jose (PIN: 7895)')
    print(f'  Monedas anteriores: {monedas_anteriores}')
    print(f'  Monedas nuevas: {jose.monedas}')
    print(f'  OK - Actualizado\n')
else:
    print('ERROR: No se encontro a Jose con PIN 7895\n')

# Buscar a Alejandra con PIN 8778
alejandra = Nino.objects.filter(nombre='Alejandra', pin='8778').first()
if alejandra:
    monedas_anteriores = alejandra.monedas
    alejandra.monedas = 100
    alejandra.save()
    print(f'Alejandra (PIN: 8778)')
    print(f'  Monedas anteriores: {monedas_anteriores}')
    print(f'  Monedas nuevas: {alejandra.monedas}')
    print(f'  OK - Actualizado\n')
else:
    print('ERROR: No se encontro a Alejandra con PIN 8778\n')

print('=== RESUMEN ===')
if jose:
    print(f'Jose: {jose.monedas} monedas')
if alejandra:
    print(f'Alejandra: {alejandra.monedas} monedas')
