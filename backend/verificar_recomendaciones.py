import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, AnalisisErrorTema, Tarea
from django.db.models import Sum

print("=" * 60)
print("VERIFICACION SISTEMA DE RECOMENDACIONES")
print("=" * 60)

# Obtener todos los niños
ninos = Nino.objects.all()

for nino in ninos:
    print(f"\n[NINO] {nino.nombre} {nino.apellido} (ID: {nino.id})")
    print("-" * 60)
    
    # Obtener analisis de errores por tema
    analisis = AnalisisErrorTema.objects.filter(nino=nino)
    
    if not analisis.exists():
        print("   [AVISO] No hay datos de analisis de errores aun")
        continue
    
    # Agrupar por subtema
    subtemas = {}
    for a in analisis:
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
                'errores': a.cantidad_errores,
                'aciertos': a.cantidad_aciertos
            })
    
    # Mostrar resumen
    total_errores = sum(s['errores'] for s in subtemas.values())
    total_aciertos = sum(s['aciertos'] for s in subtemas.values())
    
    print(f"   Total Errores: {total_errores}")
    print(f"   Total Aciertos: {total_aciertos}")
    
    if total_errores > 0:
        print(f"\n   [ANALISIS] Areas con Dificultad:")
        for subtema, datos in sorted(subtemas.items(), key=lambda x: x[1]['errores'], reverse=True):
            if datos['errores'] >= 3:
                print(f"\n      [ALERTA] {subtema.upper()}")
                print(f"         Errores: {datos['errores']} | Aciertos: {datos['aciertos']}")
                if datos['temas']:
                    print(f"         Temas problematicos:")
                    for tema in datos['temas'][:2]:
                        print(f"            - {tema['tema']} ({tema['errores']} errores)")
        
        print(f"\n   [RECOMENDACIONES] Generadas:")
        for subtema, datos in sorted(subtemas.items(), key=lambda x: x[1]['errores'], reverse=True):
            if datos['errores'] >= 5:
                temas_top = [t['tema'] for t in datos['temas'][:2]]
                if temas_top:
                    print(f"      - Reforzar {subtema}: especialmente {' y '.join(temas_top)}")
    else:
        print("   [OK] Sin errores registrados - Excelente trabajo!")
    
    # Informacion de padre/profesor
    if nino.padre:
        print(f"\n   [PADRE] {nino.padre.nombre} {nino.padre.apellido} ({nino.padre.email})")
    if nino.profesor:
        print(f"   [PROFESOR] {nino.profesor.nombre} {nino.profesor.apellido} ({nino.profesor.email})")

print("\n" + "=" * 60)
print("[OK] VERIFICACION COMPLETADA")
print("=" * 60)
print("\nPara ver el reporte completo en la interfaz:")
print("1. Inicia sesion como padre o profesor")
print("2. Ve a la seccion de Reportes")
print("3. Selecciona un nino/estudiante")
print("4. Las recomendaciones se actualizan automaticamente")
print("   cada vez que se completan tareas o practicas con errores")
