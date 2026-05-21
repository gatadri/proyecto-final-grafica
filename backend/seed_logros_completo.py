import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Logro

# Limpiar logros existentes
Logro.objects.all().delete()
print("[OK] Logros anteriores eliminados")

# Definir logros completos y estructurados
logros = [
    # ========== LOGROS DE BRONCE (Principiantes) ==========
    {
        'nombre': '¡Primer Paso!',
        'descripcion': 'Completa tu primera tarea',
        'icono': 'star',
        'rareza': 'bronce',
        'condicion': 'tareas_completadas',
        'valor_requerido': 1,
        'puntos_bonus': 10
    },
    {
        'nombre': 'Aprendiz',
        'descripcion': 'Completa 5 tareas',
        'icono': 'book',
        'rareza': 'bronce',
        'condicion': 'tareas_completadas',
        'valor_requerido': 5,
        'puntos_bonus': 25
    },
    {
        'nombre': 'Perfeccionista Novato',
        'descripcion': 'Completa una tarea sin errores',
        'icono': 'check-circle',
        'rareza': 'bronce',
        'condicion': 'tareas_perfectas',
        'valor_requerido': 1,
        'puntos_bonus': 15
    },
    {
        'nombre': 'Practicante',
        'descripcion': 'Completa 5 sesiones de práctica',
        'icono': 'dumbbell',
        'rareza': 'bronce',
        'condicion': 'practicas_completadas',
        'valor_requerido': 5,
        'puntos_bonus': 20
    },
    {
        'nombre': 'Ahorrador',
        'descripcion': 'Acumula 100 monedas',
        'icono': 'coins',
        'rareza': 'bronce',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 100,
        'puntos_bonus': 10
    },
    {
        'nombre': 'Rayo Principiante',
        'descripcion': 'Responde 10 preguntas rápidamente',
        'icono': 'bolt',
        'rareza': 'bronce',
        'condicion': 'respuestas_rapidas',
        'valor_requerido': 10,
        'puntos_bonus': 15
    },
    
    # ========== LOGROS DE PLATA (Intermedios) ==========
    {
        'nombre': 'Estudiante Dedicado',
        'descripcion': 'Completa 10 tareas',
        'icono': 'graduation-cap',
        'rareza': 'plata',
        'condicion': 'tareas_completadas',
        'valor_requerido': 10,
        'puntos_bonus': 50
    },
    {
        'nombre': 'Racha de Fuego',
        'descripcion': 'Mantén una racha de 7 días',
        'icono': 'fire',
        'rareza': 'plata',
        'condicion': 'racha_dias',
        'valor_requerido': 7,
        'puntos_bonus': 75
    },
    {
        'nombre': 'Maestro de la Precisión',
        'descripcion': 'Completa 5 tareas sin errores',
        'icono': 'bullseye',
        'rareza': 'plata',
        'condicion': 'tareas_perfectas',
        'valor_requerido': 5,
        'puntos_bonus': 60
    },
    {
        'nombre': 'Nivel 5',
        'descripcion': 'Alcanza el nivel 5',
        'icono': 'arrow-up',
        'rareza': 'plata',
        'condicion': 'nivel_alcanzado',
        'valor_requerido': 5,
        'puntos_bonus': 50
    },
    {
        'nombre': 'Coleccionista',
        'descripcion': 'Acumula 500 monedas',
        'icono': 'piggy-bank',
        'rareza': 'plata',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 500,
        'puntos_bonus': 50
    },
    {
        'nombre': 'Practicante Experto',
        'descripcion': 'Completa 20 sesiones de práctica',
        'icono': 'chart-line',
        'rareza': 'plata',
        'condicion': 'practicas_completadas',
        'valor_requerido': 20,
        'puntos_bonus': 60
    },
    {
        'nombre': 'Velocista',
        'descripcion': 'Responde 50 preguntas rápidamente',
        'icono': 'rocket',
        'rareza': 'plata',
        'condicion': 'respuestas_rapidas',
        'valor_requerido': 50,
        'puntos_bonus': 55
    },
    {
        'nombre': 'Experiencia Sólida',
        'descripcion': 'Acumula 1000 puntos de experiencia',
        'icono': 'star-half-alt',
        'rareza': 'plata',
        'condicion': 'experiencia_total',
        'valor_requerido': 1000,
        'puntos_bonus': 50
    },
    
    # ========== LOGROS DE ORO (Avanzados) ==========
    {
        'nombre': 'Maestro del Conocimiento',
        'descripcion': 'Completa 25 tareas',
        'icono': 'crown',
        'rareza': 'oro',
        'condicion': 'tareas_completadas',
        'valor_requerido': 25,
        'puntos_bonus': 100
    },
    {
        'nombre': 'Racha Imparable',
        'descripcion': 'Mantén una racha de 30 días',
        'icono': 'fire-alt',
        'rareza': 'oro',
        'condicion': 'racha_dias',
        'valor_requerido': 30,
        'puntos_bonus': 150
    },
    {
        'nombre': 'Perfección Absoluta',
        'descripcion': 'Completa 15 tareas sin errores',
        'icono': 'medal',
        'rareza': 'oro',
        'condicion': 'tareas_perfectas',
        'valor_requerido': 15,
        'puntos_bonus': 120
    },
    {
        'nombre': 'Nivel 10',
        'descripcion': 'Alcanza el nivel 10',
        'icono': 'trophy',
        'rareza': 'oro',
        'condicion': 'nivel_alcanzado',
        'valor_requerido': 10,
        'puntos_bonus': 100
    },
    {
        'nombre': 'Millonario',
        'descripcion': 'Acumula 1000 monedas',
        'icono': 'gem',
        'rareza': 'oro',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 1000,
        'puntos_bonus': 100
    },
    {
        'nombre': 'Maestro de la Práctica',
        'descripcion': 'Completa 50 sesiones de práctica',
        'icono': 'brain',
        'rareza': 'oro',
        'condicion': 'practicas_completadas',
        'valor_requerido': 50,
        'puntos_bonus': 120
    },
    {
        'nombre': 'Relámpago',
        'descripcion': 'Responde 100 preguntas rápidamente',
        'icono': 'bolt',
        'rareza': 'oro',
        'condicion': 'respuestas_rapidas',
        'valor_requerido': 100,
        'puntos_bonus': 110
    },
    {
        'nombre': 'Experiencia Maestra',
        'descripcion': 'Acumula 2500 puntos de experiencia',
        'icono': 'star',
        'rareza': 'oro',
        'condicion': 'experiencia_total',
        'valor_requerido': 2500,
        'puntos_bonus': 100
    },
    
    # ========== LOGROS LEGENDARIOS (Élite) ==========
    {
        'nombre': 'Leyenda del Aprendizaje',
        'descripcion': 'Completa 50 tareas',
        'icono': 'dragon',
        'rareza': 'legendario',
        'condicion': 'tareas_completadas',
        'valor_requerido': 50,
        'puntos_bonus': 250
    },
    {
        'nombre': 'Racha Legendaria',
        'descripcion': 'Mantén una racha de 100 días',
        'icono': 'infinity',
        'rareza': 'legendario',
        'condicion': 'racha_dias',
        'valor_requerido': 100,
        'puntos_bonus': 500
    },
    {
        'nombre': 'Perfección Divina',
        'descripcion': 'Completa 30 tareas sin errores',
        'icono': 'award',
        'rareza': 'legendario',
        'condicion': 'tareas_perfectas',
        'valor_requerido': 30,
        'puntos_bonus': 300
    },
    {
        'nombre': 'Nivel Máximo',
        'descripcion': 'Alcanza el nivel 20',
        'icono': 'mountain',
        'rareza': 'legendario',
        'condicion': 'nivel_alcanzado',
        'valor_requerido': 20,
        'puntos_bonus': 250
    },
    {
        'nombre': 'Magnate',
        'descripcion': 'Acumula 5000 monedas',
        'icono': 'crown',
        'rareza': 'legendario',
        'condicion': 'monedas_acumuladas',
        'valor_requerido': 5000,
        'puntos_bonus': 250
    },
    {
        'nombre': 'Gurú de la Práctica',
        'descripcion': 'Completa 100 sesiones de práctica',
        'icono': 'infinity',
        'rareza': 'legendario',
        'condicion': 'practicas_completadas',
        'valor_requerido': 100,
        'puntos_bonus': 300
    },
    {
        'nombre': 'Velocidad de la Luz',
        'descripcion': 'Responde 500 preguntas rápidamente',
        'icono': 'meteor',
        'rareza': 'legendario',
        'condicion': 'respuestas_rapidas',
        'valor_requerido': 500,
        'puntos_bonus': 350
    },
    {
        'nombre': 'Experiencia Legendaria',
        'descripcion': 'Acumula 10000 puntos de experiencia',
        'icono': 'star',
        'rareza': 'legendario',
        'condicion': 'experiencia_total',
        'valor_requerido': 10000,
        'puntos_bonus': 500
    },
]

# Crear logros
contador = 0
for logro_data in logros:
    logro = Logro.objects.create(**logro_data)
    contador += 1
    print(f"[OK] Creado: [{logro.rareza.upper()}] {logro.nombre} - {logro.descripcion}")

print(f"\n{'='*60}")
print(f"[OK] Total de logros creados: {contador}")
print(f"  - Bronce: {len([l for l in logros if l['rareza'] == 'bronce'])}")
print(f"  - Plata: {len([l for l in logros if l['rareza'] == 'plata'])}")
print(f"  - Oro: {len([l for l in logros if l['rareza'] == 'oro'])}")
print(f"  - Legendario: {len([l for l in logros if l['rareza'] == 'legendario'])}")
print(f"{'='*60}")
print("[OK] Sistema de logros completamente configurado")
