import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from users.models import User
from tareas.models import Nino

print('=== PADRES Y SUS HIJOS ===\n')
padres = User.objects.filter(role='padre')
for p in padres:
    print(f'{p.nombre} {p.apellido} ({p.email}):')
    hijos = p.hijos.all()
    if hijos.exists():
        for h in hijos:
            prof = h.profesor.nombre + ' ' + h.profesor.apellido if h.profesor else 'Sin profesor'
            print(f'  - {h.nombre} {h.apellido} (PIN: {h.pin}, Profesor: {prof})')
    else:
        print('  Sin hijos registrados')
    print()

print('\n=== TODOS LOS USUARIOS ===\n')
usuarios = User.objects.all()
for u in usuarios:
    print(f'{u.nombre} {u.apellido} | Email: {u.email} | Role: {u.role} | Activo: {u.activo}')
