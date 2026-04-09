from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tarea, Nino
from .serializers import TareaSerializer, TareaCreateSerializer, NinoSerializer
from users.permissions import IsProfesor


class TareaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsProfesor]

    def get_serializer_class(self):
        return TareaCreateSerializer if self.request.method == 'POST' else TareaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'director':
            return Tarea.objects.all()
        return Tarea.objects.filter(profesor=user)

    def perform_create(self, serializer):
        serializer.save(profesor=self.request.user)


class TareaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsProfesor]

    def get_serializer_class(self):
        return TareaCreateSerializer if self.request.method in ['PUT', 'PATCH'] else TareaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'director':
            return Tarea.objects.all()
        return Tarea.objects.filter(profesor=user)


class EstudiantesProfesorView(APIView):
    permission_classes = [IsAuthenticated, IsProfesor]

    def get(self, request):
        ninos = Nino.objects.filter(profesor=request.user)
        return Response(NinoSerializer(ninos, many=True).data)
