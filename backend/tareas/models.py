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


class ProgresoTarea(models.Model):
    nino             = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='progreso_tareas')
    tarea            = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    completada       = models.BooleanField(default=False)
    puntos_obtenidos = models.IntegerField(default=0)
    cantidad_aciertos = models.IntegerField(default=0)
    cantidad_errores  = models.IntegerField(default=0)
    tiempo_total_ms   = models.IntegerField(default=0)
    fecha_completada = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('nino', 'tarea')


class EjercicioPractica(models.Model):
    TIPOS = [
        ('multiple', 'Opción múltiple'),
        ('completar', 'Completar'),
        ('verdadero_falso', 'Verdadero/Falso'),
    ]
    CATEGORIAS = [
        ('matematicas', 'Matemáticas'),
        ('lengua', 'Lengua'),
        ('ciencias', 'Ciencias'),
        ('ingles', 'Inglés'),
    ]
    
    pregunta           = models.TextField()
    opciones           = models.JSONField(default=list)
    respuesta_correcta = models.CharField(max_length=200)
    tipo_ejercicio     = models.CharField(max_length=50, choices=TIPOS, default='multiple')
    categoria          = models.CharField(max_length=50, choices=CATEGORIAS, default='matematicas')
    dificultad         = models.IntegerField(default=1)
    activo             = models.BooleanField(default=True)
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.categoria} - {self.pregunta[:50]}"


class ProgresoPractica(models.Model):
    TIPOS = [
        ('multiple', 'Opción múltiple'),
        ('completar', 'Completar'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('practica_libre', 'Práctica Libre'),
    ]
    nino              = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='progresos_practica')
    completada        = models.BooleanField(default=False)
    puntos_obtenidos  = models.IntegerField(default=0)
    cantidad_aciertos = models.IntegerField(default=0)
    cantidad_errores  = models.IntegerField(default=0)
    tiempo_total_ms   = models.IntegerField(default=0)
    dificultad        = models.IntegerField(default=1)
    tipo_ejercicio    = models.CharField(max_length=50, choices=TIPOS, default='practica_libre')
    fecha_practica    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Práctica {self.nino.nombre} - {self.fecha_practica.strftime('%Y-%m-%d')}"


class EjercicioProgreso(models.Model):
    id               = models.BigAutoField(primary_key=True)
    student          = models.ForeignKey(Nino, db_column='student_id', on_delete=models.CASCADE, related_name='ejercicio_progresos')
    item             = models.ForeignKey(Ejercicio, db_column='item_id', on_delete=models.CASCADE, related_name='progreso')
    skill_id         = models.IntegerField(null=True, blank=True)
    difficulty       = models.IntegerField(null=True, blank=True)
    time_spent_ms    = models.IntegerField(default=0)
    attempts         = models.IntegerField(default=1)
    used_hint        = models.BooleanField(default=False)
    n_hints          = models.IntegerField(default=0)
    fast_response    = models.BooleanField(default=False)
    correct          = models.BooleanField(default=False)
    tab_blur_count   = models.IntegerField(default=0)
    idle_ms          = models.IntegerField(default=0)
    erratic_clicks   = models.IntegerField(default=0)
    error_type       = models.CharField(max_length=100, blank=True)
    will_mistake_next = models.BooleanField(default=False)
    focus_score      = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tareas_progreso'
        managed = False


class Logro(models.Model):
    RAREZA_CHOICES = [('bronce', 'Bronce'), ('plata', 'Plata'), ('oro', 'Oro'), ('legendario', 'Legendario')]
    CONDICION_CHOICES = [
        ('tareas_completadas', 'Tareas Completadas'),
        ('tareas_perfectas', 'Tareas Sin Errores'),
        ('racha_dias', 'Racha de Días'),
        ('respuestas_rapidas', 'Respuestas Rápidas'),
        ('nivel_alcanzado', 'Nivel Alcanzado'),
        ('monedas_acumuladas', 'Monedas Acumuladas'),
        ('practicas_completadas', 'Prácticas Completadas'),
        ('experiencia_total', 'Experiencia Total'),
    ]

    nombre            = models.CharField(max_length=100)
    descripcion       = models.TextField()
    icono             = models.CharField(max_length=50, default='star')
    rareza            = models.CharField(max_length=20, choices=RAREZA_CHOICES, default='bronce')
    condicion         = models.CharField(max_length=50, choices=CONDICION_CHOICES)
    valor_requerido   = models.IntegerField()
    puntos_bonus      = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class LogroNino(models.Model):
    nino              = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='logros_desbloqueados')
    logro             = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_desbloqueado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nino', 'logro')

    def __str__(self):
        return f'{self.logro.nombre} - {self.nino.nombre}'


class Skin(models.Model):
    RAREZA_CHOICES = [('comun', 'Común'), ('raro', 'Raro'), ('legendario', 'Legendario')]
    
    nombre        = models.CharField(max_length=100)
    descripcion   = models.TextField()
    imagen        = models.CharField(max_length=200)  # ruta relativa desde /imagenes/avatares/
    avatar_key    = models.CharField(max_length=50, unique=True)  # valor que se guarda en nino.avatar
    precio        = models.IntegerField(default=0)
    rareza        = models.CharField(max_length=20, choices=RAREZA_CHOICES, default='comun')
    activo        = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class SkinComprada(models.Model):
    nino           = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='skins_compradas')
    skin           = models.ForeignKey(Skin, on_delete=models.CASCADE)
    fecha_compra   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nino', 'skin')

    def __str__(self):
        return f'{self.nino.nombre} - {self.skin.nombre}'


class Sticker(models.Model):
    RAREZA_CHOICES = [('comun', 'Común'), ('raro', 'Raro'), ('legendario', 'Legendario')]
    
    nombre        = models.CharField(max_length=100)
    descripcion   = models.TextField()
    imagen        = models.CharField(max_length=200)  # ruta relativa desde /imagenes/stickers/
    precio        = models.IntegerField(default=0)
    rareza        = models.CharField(max_length=20, choices=RAREZA_CHOICES, default='comun')
    activo        = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class StickerComprado(models.Model):
    nino           = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='stickers_comprados')
    sticker        = models.ForeignKey(Sticker, on_delete=models.CASCADE)
    fecha_compra   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nino', 'sticker')

    def __str__(self):
        return f'{self.nino.nombre} - {self.sticker.nombre}'
