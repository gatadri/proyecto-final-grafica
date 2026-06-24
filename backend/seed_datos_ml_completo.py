"""
Script para llenar la base de datos con datos completos de ML para Alejandra y Elena
Incluye: EjercicioProgreso, PrediccionError, EventoDistraccion, AnalisisErrorTema
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import (
    Nino, Tarea, Ejercicio, ProgresoTarea, EjercicioProgreso,
    PrediccionError, EventoDistraccion, AnalisisErrorTema
)
from users.models import User

def crear_datos_ml():
    print("=" * 80)
    print("GENERANDO DATOS DE ML PARA ALEJANDRA Y ELENA")
    print("=" * 80)
    
    # Obtener Alejandra y Elena
    try:
        alejandra = Nino.objects.get(nombre='Alejandra')
        elena = Nino.objects.get(nombre='Elena')
    except Nino.DoesNotExist:
        print("ERROR: No se encontraron Alejandra o Elena en la base de datos")
        print("Asegúrate de ejecutar seed.py primero")
        return
    
    # Obtener todas las tareas
    tareas = list(Tarea.objects.all())
    if not tareas:
        print("ERROR: No hay tareas en la base de datos")
        return
    
    print(f"\n[OK] Encontrados: Alejandra (ID: {alejandra.id}), Elena (ID: {elena.id})")
    print(f"[OK] Tareas disponibles: {len(tareas)}")
    
    # Limpiar datos anteriores de ML
    print("\nLimpiando datos anteriores...")
    EjercicioProgreso.objects.filter(student__in=[alejandra, elena]).delete()
    PrediccionError.objects.filter(nino__in=[alejandra, elena]).delete()
    EventoDistraccion.objects.filter(nino__in=[alejandra, elena]).delete()
    AnalisisErrorTema.objects.filter(nino__in=[alejandra, elena]).delete()
    ProgresoTarea.objects.filter(nino__in=[alejandra, elena]).delete()
    
    # Generar datos para cada niña
    for nino in [alejandra, elena]:
        print(f"\n{'=' * 80}")
        print(f"GENERANDO DATOS PARA: {nino.nombre}")
        print(f"{'=' * 80}")
        
        # Configuración de perfil
        if nino.nombre == 'Alejandra':
            # Alejandra: Buena en sumas y restas, problemas con multiplicación y división
            perfil = {
                'tareas_a_completar': 8,
                'temas_fuertes': ['suma', 'resta'],
                'temas_debiles': ['multiplicacion', 'division'],
                'nivel_distraccion': 'medio',  # Algunos eventos de distracción
                'velocidad': 'rapida'
            }
        else:  # Elena
            # Elena: Buena en multiplicación, problemas con fracciones y división
            perfil = {
                'tareas_a_completar': 6,
                'temas_fuertes': ['suma', 'multiplicacion'],
                'temas_debiles': ['division', 'fracciones'],
                'nivel_distraccion': 'alto',  # Más eventos de distracción
                'velocidad': 'lenta'
            }
        
        total_ejercicios = 0
        total_aciertos = 0
        total_errores = 0
        
        # Seleccionar tareas para completar
        tareas_seleccionadas = random.sample(tareas, min(perfil['tareas_a_completar'], len(tareas)))
        
        for idx, tarea in enumerate(tareas_seleccionadas, 1):
            ejercicios = list(tarea.ejercicios.all())
            if not ejercicios:
                continue
            
            print(f"\n  [{idx}/{len(tareas_seleccionadas)}] Procesando tarea: {tarea.titulo}")
            print(f"      Ejercicios: {len(ejercicios)}")
            
            puntos_tarea = 0
            aciertos_tarea = 0
            errores_tarea = 0
            tiempo_tarea_total = 0
            
            # Análisis por tema/subtema para esta tarea
            analisis_temas = {}
            
            for ej_idx, ejercicio in enumerate(ejercicios, 1):
                # Determinar tema y subtema
                tema = ejercicio.tema or 'general'
                subtema = ejercicio.subtema or 'matematicas'
                
                # Determinar si es correcto basado en el perfil
                es_tema_fuerte = any(tf in tema.lower() or tf in subtema.lower() for tf in perfil['temas_fuertes'])
                es_tema_debil = any(td in tema.lower() or td in subtema.lower() for td in perfil['temas_debiles'])
                
                if es_tema_fuerte:
                    prob_acierto = 0.85  # 85% de acierto en temas fuertes
                elif es_tema_debil:
                    prob_acierto = 0.40  # 40% de acierto en temas débiles
                else:
                    prob_acierto = 0.65  # 65% en temas neutros
                
                correcto = random.random() < prob_acierto
                
                # Tiempo de respuesta
                if perfil['velocidad'] == 'rapida':
                    tiempo_base = random.randint(8000, 15000)  # 8-15 segundos
                else:
                    tiempo_base = random.randint(15000, 30000)  # 15-30 segundos
                
                # Más tiempo si es incorrecto
                tiempo_ms = tiempo_base if correcto else int(tiempo_base * 1.5)
                
                # Intentos
                intentos = 1 if correcto else random.choice([2, 2, 2, 3])
                
                # Métricas de distracción
                if perfil['nivel_distraccion'] == 'alto':
                    tab_blur = random.randint(0, 5)
                    idle_ms = random.randint(0, 8000)
                    erratic_clicks = random.randint(0, 4)
                elif perfil['nivel_distraccion'] == 'medio':
                    tab_blur = random.randint(0, 2)
                    idle_ms = random.randint(0, 3000)
                    erratic_clicks = random.randint(0, 2)
                else:
                    tab_blur = 0
                    idle_ms = random.randint(0, 1000)
                    erratic_clicks = 0
                
                # Fast response si fue rápido
                fast_response = tiempo_ms < 10000
                
                # Error type si es incorrecto
                error_type = ''
                if not correcto:
                    if es_tema_debil:
                        error_type = random.choice(['procedimiento', 'conceptual', 'procedimiento'])
                    else:
                        error_type = random.choice(['inatencion', 'procedimiento', 'aleatorio'])
                
                # Focus score (inverso de distracción)
                focus_score = max(0.1, min(1.0, 1.0 - (tab_blur * 0.15 + idle_ms / 10000 + erratic_clicks * 0.1)))
                
                # Crear EjercicioProgreso
                EjercicioProgreso.objects.create(
                    student=nino,
                    item=ejercicio,
                    time_spent_ms=tiempo_ms,
                    attempts=intentos,
                    correct=correcto,
                    fast_response=fast_response,
                    tab_blur_count=tab_blur,
                    idle_ms=idle_ms,
                    erratic_clicks=erratic_clicks,
                    error_type=error_type,
                    focus_score=round(focus_score, 2)
                )
                
                # Actualizar contadores
                if correcto:
                    aciertos_tarea += 1
                    total_aciertos += 1
                    puntos_tarea += 10
                else:
                    errores_tarea += 1
                    total_errores += 1
                
                tiempo_tarea_total += tiempo_ms
                total_ejercicios += 1
                
                # Acumular para análisis por tema
                if tema not in analisis_temas:
                    analisis_temas[tema] = {
                        'subtema': subtema,
                        'errores': 0,
                        'aciertos': 0,
                        'tiempos': []
                    }
                
                if correcto:
                    analisis_temas[tema]['aciertos'] += 1
                else:
                    analisis_temas[tema]['errores'] += 1
                analisis_temas[tema]['tiempos'].append(tiempo_ms)
                
                # Crear evento de distracción si focus_score es muy bajo
                if focus_score < 0.5:
                    EventoDistraccion.objects.create(
                        nino=nino,
                        focus_score=focus_score,
                        tab_blur_count=tab_blur,
                        idle_ms=idle_ms,
                        erratic_clicks=erratic_clicks,
                        descanso_mostrado=random.choice([True, False])
                    )
            
            # Crear ProgresoTarea
            ProgresoTarea.objects.create(
                nino=nino,
                tarea=tarea,
                completada=True,
                puntos_obtenidos=puntos_tarea,
                cantidad_aciertos=aciertos_tarea,
                cantidad_errores=errores_tarea,
                tiempo_total_ms=tiempo_tarea_total,
                fecha_completada=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            
            # Crear AnalisisErrorTema para cada tema
            for tema, datos in analisis_temas.items():
                tiempo_prom = int(sum(datos['tiempos']) / len(datos['tiempos']))
                AnalisisErrorTema.objects.create(
                    nino=nino,
                    tarea=tarea,
                    tema=tema,
                    subtema=datos['subtema'],
                    cantidad_errores=datos['errores'],
                    cantidad_aciertos=datos['aciertos'],
                    tiempo_promedio_ms=tiempo_prom
                )
            
            print(f"      [OK] Aciertos: {aciertos_tarea}, Errores: {errores_tarea}, Puntos: {puntos_tarea}")
        
        # Crear predicciones de error basadas en temas débiles
        print(f"\n  Generando predicciones de error...")
        for tema_debil in perfil['temas_debiles']:
            if tema_debil == 'multiplicacion':
                tipo_error = 'multiplicacion'
                prob = random.uniform(0.65, 0.85)
            elif tema_debil == 'division':
                tipo_error = 'division'
                prob = random.uniform(0.60, 0.80)
            elif tema_debil == 'fracciones':
                tipo_error = 'fracciones'
                prob = random.uniform(0.70, 0.90)
            else:
                tipo_error = 'procedimiento'
                prob = random.uniform(0.50, 0.70)
            
            PrediccionError.objects.create(
                nino=nino,
                tipo_error=tipo_error,
                probabilidad=round(prob, 2),
                notificado=random.choice([True, False])
            )
        
        # Agregar algunas predicciones adicionales
        if perfil['nivel_distraccion'] in ['alto', 'medio']:
            PrediccionError.objects.create(
                nino=nino,
                tipo_error='inatencion',
                probabilidad=round(random.uniform(0.55, 0.75), 2),
                notificado=False
            )
        
        # Crear algunos eventos de distracción adicionales
        eventos_distraccion = 8 if perfil['nivel_distraccion'] == 'alto' else 4
        for _ in range(eventos_distraccion):
            EventoDistraccion.objects.create(
                nino=nino,
                focus_score=round(random.uniform(0.2, 0.6), 2),
                tab_blur_count=random.randint(1, 6),
                idle_ms=random.randint(2000, 10000),
                erratic_clicks=random.randint(0, 5),
                descanso_mostrado=random.choice([True, False])
            )
        
        # Actualizar estadísticas del niño
        nino.monedas += total_aciertos * 10
        nino.experiencia += total_aciertos * 15
        nino.nivel = min(10, 1 + (nino.experiencia // 100))
        nino.save()
        
        print(f"\n  {'=' * 70}")
        print(f"  RESUMEN PARA {nino.nombre}:")
        print(f"  {'=' * 70}")
        print(f"    Total ejercicios realizados: {total_ejercicios}")
        print(f"    Total aciertos: {total_aciertos}")
        print(f"    Total errores: {total_errores}")
        print(f"    Tasa de éxito: {(total_aciertos / total_ejercicios * 100):.1f}%")
        print(f"    Monedas: {nino.monedas}")
        print(f"    Experiencia: {nino.experiencia}")
        print(f"    Nivel: {nino.nivel}")
        print(f"    Predicciones de error: {PrediccionError.objects.filter(nino=nino).count()}")
        print(f"    Eventos de distracción: {EventoDistraccion.objects.filter(nino=nino).count()}")
        print(f"    Analisis de temas: {AnalisisErrorTema.objects.filter(nino=nino).count()}")
    
    # Resumen final
    print(f"\n{'=' * 80}")
    print("GENERACIÓN COMPLETA - RESUMEN GENERAL")
    print(f"{'=' * 80}")
    print(f"  Total EjercicioProgreso creados: {EjercicioProgreso.objects.filter(student__in=[alejandra, elena]).count()}")
    print(f"  Total PrediccionError creadas: {PrediccionError.objects.filter(nino__in=[alejandra, elena]).count()}")
    print(f"  Total EventoDistraccion creados: {EventoDistraccion.objects.filter(nino__in=[alejandra, elena]).count()}")
    print(f"  Total AnalisisErrorTema creados: {AnalisisErrorTema.objects.filter(nino__in=[alejandra, elena]).count()}")
    print(f"\n[OK] Los reportes de IA ahora estaran disponibles en la interfaz del profesor")
    print(f"[OK] Puedes revisar los reportes en: Profesor > Reportes")
    print(f"{'=' * 80}\n")

if __name__ == '__main__':
    try:
        crear_datos_ml()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
