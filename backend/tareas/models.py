from django.db import models
from users.models import User


class Nino(models.Model):
    nombre    = models.CharField(max_length=100)
    apellido  = models.CharField(max_length=100)
    edad      = models.IntegerField(default=0)
    grado     = models.IntegerField(default=1)
    pin       = models.CharField(max_length=10)
    padre     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hijos')
    profesor  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    monedas   = models.IntegerField(default=0)
    nivel     = models.IntegerField(default=1)
    experiencia = models.IntegerField(default=0)
    avatar    = models.CharField(max_length=50, default='nino')
    racha_dias = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Tarea(models.Model):
    TIPOS = [
        ('multiple', 'Opción múltiple'),
        ('completar', 'Completar'),
        ('verdadero_falso', 'Verdadero/Falso'),
    ]

    titulo         = models.CharField(max_length=200)
    descripcion    = models.TextField(blank=True)
    tipo_ejercicio = models.CharField(max_length=50, choices=TIPOS, default='multiple')
    profesor       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    ninos          = models.ManyToManyField(Nino, blank=True, related_name='tareas')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Ejercicio(models.Model):
    tarea              = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='ejercicios')
    pregunta           = models.TextField()
    opciones           = models.JSONField(default=list)
    respuesta_correcta = models.CharField(max_length=200)
    explicacion        = models.TextField(blank=True)
    orden              = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f'{self.tarea.titulo} - Ejercicio {self.orden}'
