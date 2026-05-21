import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, LogroNino

print('=== DESHACIENDO LOGROS ASIGNADOS ===\n')

# Buscar a Jose y Alejandra
jose = Nino.objects.filter(nombre='Jose', pin='7895').first()
alejandra = Nino.objects.filter(nombre='Alejandra', pin='8778').first()

if jose:
    logros_jose = LogroNino.objects.filter(nino=jose)
    count = logros_jose.count()
    
    # Restar las monedas de bonificación
    total_bonus = sum([l.logro.puntos_bonus for l in logros_jose])
    jose.monedas -= total_bonus
    jose.save()
    
    # Eliminar logros
    logros_jose.delete()
    
    print(f'Jose (PIN: 7895):')
    print(f'  Logros eliminados: {count}')
    print(f'  Monedas devueltas: -{total_bonus}')
    print(f'  Monedas actuales: {jose.monedas}\n')

if alejandra:
    logros_alejandra = LogroNino.objects.filter(nino=alejandra)
    count = logros_alejandra.count()
    
    # Restar las monedas de bonificación
    total_bonus = sum([l.logro.puntos_bonus for l in logros_alejandra])
    alejandra.monedas -= total_bonus
    alejandra.save()
    
    # Eliminar logros
    logros_alejandra.delete()
    
    print(f'Alejandra (PIN: 8778):')
    print(f'  Logros eliminados: {count}')
    print(f'  Monedas devueltas: -{total_bonus}')
    print(f'  Monedas actuales: {alejandra.monedas}\n')

print('OK - Logros eliminados correctamente')
