from django.contrib import admin
from .models import Nino, Tarea, Ejercicio, ProgresoTarea, EjercicioProgreso, Logro, LogroNino, ProgresoPractica

@admin.register(Nino)
class NinoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monedas', 'nivel', 'experiencia', 'racha_dias')
    search_fields = ('nombre',)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_ejercicio')
    search_fields = ('titulo',)

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'tarea')
    search_fields = ('pregunta',)

@admin.register(ProgresoTarea)
class ProgresoTareaAdmin(admin.ModelAdmin):
    list_display = ('nino', 'tarea', 'completada', 'fecha_completada')
    search_fields = ('nino__nombre', 'tarea__titulo')

@admin.register(ProgresoPractica)
class ProgresoPracticaAdmin(admin.ModelAdmin):
    list_display = ('nino', 'completada', 'puntos_obtenidos', 'cantidad_aciertos', 'cantidad_errores', 'fecha_practica')
    search_fields = ('nino__nombre',)
    list_filter = ('completada', 'tipo_ejercicio', 'fecha_practica')

@admin.register(EjercicioProgreso)
class EjercicioProgresoAdmin(admin.ModelAdmin):
    list_display = ('student', 'item', 'correct', 'time_spent_ms')
    search_fields = ('student__nombre',)

@admin.register(Logro)
class LogroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'condicion', 'valor_requerido', 'rareza', 'puntos_bonus')
    search_fields = ('nombre',)
    list_filter = ('condicion', 'rareza')

@admin.register(LogroNino)
class LogroNinoAdmin(admin.ModelAdmin):
    list_display = ('nino', 'logro', 'fecha_desbloqueado')
    search_fields = ('nino__nombre', 'logro__nombre')
