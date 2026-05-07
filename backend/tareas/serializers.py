from rest_framework import serializers
from .models import Tarea, Ejercicio, Nino, EjercicioProgreso, Logro, LogroNino, ProgresoPractica, EjercicioPractica


class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nino
        fields = ['id', 'nombre', 'apellido', 'grado', 'nivel', 'pin', 'monedas', 'experiencia', 'avatar', 'racha_dias']


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id', 'pregunta', 'opciones', 'respuesta_correcta', 'explicacion', 'orden']


class EjercicioProgresoSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Nino.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Ejercicio.objects.all())

    class Meta:
        model = EjercicioProgreso
        fields = ['id', 'student', 'item', 'skill_id', 'difficulty', 'time_spent_ms', 'attempts', 'used_hint', 'n_hints', 'fast_response', 'correct', 'tab_blur_count', 'idle_ms', 'erratic_clicks', 'error_type', 'will_mistake_next', 'focus_score', 'created_at']


class ProgresoPracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoPractica
        fields = ['id', 'nino', 'completada', 'puntos_obtenidos', 'cantidad_aciertos',
                  'cantidad_errores', 'tiempo_total_ms', 'dificultad', 'tipo_ejercicio', 'fecha_practica']


class EjercicioPracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EjercicioPractica
        fields = ['id', 'pregunta', 'opciones', 'respuesta_correcta', 'tipo_ejercicio', 'categoria', 'dificultad']


class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = ['id', 'nombre', 'descripcion', 'icono', 'rareza', 'condicion', 'valor_requerido', 'puntos_bonus']


class LogroNinoSerializer(serializers.ModelSerializer):
    logro = LogroSerializer(read_only=True)

    class Meta:
        model = LogroNino
        fields = ['id', 'logro', 'fecha_desbloqueado']


class TareaSerializer(serializers.ModelSerializer):
    ejercicios  = EjercicioSerializer(many=True, read_only=True)
    profesor_id = serializers.IntegerField(source='profesor.id', read_only=True)

    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'tipo_ejercicio', 'profesor_id', 'ejercicios', 'created_at']


class TareaCreateSerializer(serializers.ModelSerializer):
    ejercicios = EjercicioSerializer(many=True, required=False)
    nino_ids   = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'tipo_ejercicio', 'ejercicios', 'nino_ids']

    def create(self, validated_data):
        ejercicios_data = validated_data.pop('ejercicios', [])
        nino_ids        = validated_data.pop('nino_ids', [])
        tarea = Tarea.objects.create(**validated_data)
        for i, ej in enumerate(ejercicios_data):
            ej['orden'] = ej.get('orden', i)
            Ejercicio.objects.create(tarea=tarea, **ej)
        if nino_ids:
            tarea.ninos.set(Nino.objects.filter(id__in=nino_ids))
        return tarea

    def update(self, instance, validated_data):
        ejercicios_data = validated_data.pop('ejercicios', None)
        nino_ids        = validated_data.pop('nino_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if ejercicios_data is not None:
            instance.ejercicios.all().delete()
            for i, ej in enumerate(ejercicios_data):
                ej['orden'] = ej.get('orden', i)
                Ejercicio.objects.create(tarea=instance, **ej)
        if nino_ids is not None:
            instance.ninos.set(Nino.objects.filter(id__in=nino_ids))
        return instance
