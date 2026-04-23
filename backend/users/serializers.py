from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from tareas.models import Nino, Tarea
from tareas.serializers import TareaSerializer


class UserSerializer(serializers.ModelSerializer):
    hijos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido', 'email', 'carnet', 'numero', 'role', 'activo', 'hijos']

    def get_hijos(self, obj):
        if obj.role == 'padre':
            return NinoSerializer(obj.hijos.all(), many=True).data
        return []


class NinoSerializer(serializers.ModelSerializer):
    tareas = TareaSerializer(many=True, read_only=True)
    estadisticas = serializers.SerializerMethodField()

    class Meta:
        model = Nino
        fields = ['id', 'nombre', 'apellido', 'pin', 'profesor_id', 'profesor', 'tareas', 'estadisticas']

    def get_estadisticas(self, obj):
        return {
            'monedas': obj.monedas,
            'nivel': obj.nivel,
            'experiencia': obj.experiencia,
            'racha_dias': obj.racha_dias
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    hijos = NinoSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'carnet', 'email', 'numero', 'role', 'password', 'hijos']

    def create(self, validated_data):
        hijos_data = validated_data.pop('hijos', [])
        user = User.objects.create_user(**validated_data)
        if user.role == 'padre':
            for hijo_data in hijos_data:
                profesor_id = hijo_data.pop('profesor_id')
                profesor = User.objects.get(id=profesor_id, role='profesor')
                Nino.objects.create(padre=user, profesor=profesor, **hijo_data)
        return user


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales incorrectas')
        if not user.activo:
            raise serializers.ValidationError('Usuario suspendido')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido', 'email', 'carnet', 'numero', 'role', 'activo']
