import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, Tarea, Ejercicio, AnalisisErrorTema

print("=" * 60)
print("SIMULACION DE ERRORES PARA PROBAR RECOMENDACIONES")
print("=" * 60)

# Seleccionar un niño
nino = Nino.objects.filter(nombre='Luis', apellido='Mamani').first()
if not nino:
    nino = Nino.objects.first()

print(f"\n[NINO SELECCIONADO] {nino.nombre} {nino.apellido} (ID: {nino.id})")

# Obtener una tarea con ejercicios etiquetados
tarea = Tarea.objects.filter(
    ejercicios__tema__isnull=False
).distinct().first()

if not tarea:
    print("\n[ERROR] No hay tareas con ejercicios etiquetados")
    print("Por favor, ejecuta primero: python etiquetar_ejercicios.py")
    exit(1)

print(f"[TAREA] {tarea.titulo}")

# Obtener ejercicios de la tarea
ejercicios = Ejercicio.objects.filter(tarea=tarea, tema__isnull=False)

if not ejercicios.exists():
    print("[ERROR] No hay ejercicios etiquetados en esta tarea")
    exit(1)

print(f"[EJERCICIOS] {ejercicios.count()} encontrados")

# Simular errores en diferentes temas
simulaciones = [
    {'tema': 'tabla_11', 'subtema': 'multiplicacion', 'errores': 8, 'aciertos': 2},
    {'tema': 'tabla_12', 'subtema': 'multiplicacion', 'errores': 6, 'aciertos': 4},
    {'tema': 'division_entre_3', 'subtema': 'division', 'errores': 7, 'aciertos': 3},
    {'tema': 'division_entre_4', 'subtema': 'division', 'errores': 5, 'aciertos': 5},
]

print("\n" + "=" * 60)
print("SIMULANDO ERRORES...")
print("=" * 60)

for sim in simulaciones:
    analisis, created = AnalisisErrorTema.objects.get_or_create(
        nino=nino,
        tarea=tarea,
        tema=sim['tema'],
        defaults={
            'subtema': sim['subtema'],
            'cantidad_errores': sim['errores'],
            'cantidad_aciertos': sim['aciertos'],
            'tiempo_promedio_ms': 15000
        }
    )
    
    if not created:
        analisis.cantidad_errores = sim['errores']
        analisis.cantidad_aciertos = sim['aciertos']
        analisis.save()
    
    status = "[CREADO]" if created else "[ACTUALIZADO]"
    print(f"{status} {sim['subtema'].upper()}/{sim['tema']}")
    print(f"         Errores: {sim['errores']} | Aciertos: {sim['aciertos']}")

print("\n" + "=" * 60)
print("VERIFICANDO RECOMENDACIONES GENERADAS")
print("=" * 60)

# Obtener análisis del niño
analisis_list = AnalisisErrorTema.objects.filter(nino=nino)

# Agrupar por subtema
subtemas = {}
for a in analisis_list:
    if a.subtema not in subtemas:
        subtemas[a.subtema] = {
            'errores': 0,
            'aciertos': 0,
            'temas': []
        }
    subtemas[a.subtema]['errores'] += a.cantidad_errores
    subtemas[a.subtema]['aciertos'] += a.cantidad_aciertos
    if a.cantidad_errores >= 2:
        subtemas[a.subtema]['temas'].append({
            'tema': a.tema.replace('_', ' ').title(),
            'errores': a.cantidad_errores
        })

print(f"\n[NINO] {nino.nombre} {nino.apellido}")
print("-" * 60)

for subtema, datos in sorted(subtemas.items(), key=lambda x: x[1]['errores'], reverse=True):
    if datos['errores'] >= 5:
        print(f"\n[AREA PROBLEMATICA] {subtema.upper()}")
        print(f"   Total Errores: {datos['errores']}")
        print(f"   Total Aciertos: {datos['aciertos']}")
        
        temas_top = [t['tema'] for t in sorted(datos['temas'], key=lambda x: x['errores'], reverse=True)[:2]]
        
        if temas_top:
            print(f"\n   [RECOMENDACION GENERADA]")
            print(f"   Reforzar {subtema}: especialmente {' y '.join(temas_top)}")
            print(f"   Considerar practica adicional en estos temas.")

print("\n" + "=" * 60)
print("[OK] SIMULACION COMPLETADA")
print("=" * 60)

print(f"\nAhora puedes verificar en la interfaz:")
print(f"1. Login como padre: {nino.padre.email if nino.padre else 'N/A'} / password")
print(f"2. O como profesor: {nino.profesor.email if nino.profesor else 'N/A'} / password")
print(f"3. Ir a 'Reportes'")
print(f"4. Seleccionar a '{nino.nombre} {nino.apellido}'")
print(f"5. Ver las recomendaciones generadas automaticamente")
print(f"\nO probar el endpoint directamente:")
print(f"GET http://localhost:8000/api/tareas/ml/reporte-detallado?nino_id={nino.id}")
