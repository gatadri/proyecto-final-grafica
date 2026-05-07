from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Tarea, Nino, ProgresoTarea, EjercicioProgreso, Logro, LogroNino, ProgresoPractica, EjercicioPractica
from .serializers import TareaSerializer, TareaCreateSerializer, NinoSerializer, EjercicioProgresoSerializer, LogroNinoSerializer, ProgresoPracticaSerializer, EjercicioPracticaSerializer
from users.permissions import IsProfesor
from django.utils import timezone
from django.db.models import Count


def verificar_y_desbloquear_logros(nino):
    """Verifica y desbloquea logros para un niño basado en sus estadísticas."""
    logros_desbloqueados = []
    tareas_completadas = ProgresoTarea.objects.filter(nino=nino, completada=True).count()
    
    for logro in Logro.objects.exclude(logronino__nino=nino):
        cumple = False
        
        if logro.condicion == 'tareas_completadas' and tareas_completadas >= logro.valor_requerido:
            cumple = True
        elif logro.condicion == 'monedas_acumuladas' and nino.monedas >= logro.valor_requerido:
            cumple = True
        elif logro.condicion == 'nivel_alcanzado' and nino.nivel >= logro.valor_requerido:
            cumple = True
        elif logro.condicion == 'racha_dias' and nino.racha_dias >= logro.valor_requerido:
            cumple = True
        
        if cumple:
            logro_nino = LogroNino.objects.create(nino=nino, logro=logro)
            logros_desbloqueados.append(logro_nino)
            nino.monedas += logro.puntos_bonus
    
    if logros_desbloqueados:
        nino.save()
    
    return logros_desbloqueados


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


class NinoTareasView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        if not nino_id:
            return Response({'error': 'nino_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nino = Nino.objects.get(id=nino_id)
            tareas = nino.tareas.all()
            serializer = TareaSerializer(tareas, many=True)
            return Response(serializer.data)
        except Nino.DoesNotExist:
            return Response({'error': 'Nino not found'}, status=status.HTTP_404_NOT_FOUND)


class NinoTareaDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        nino_id = request.query_params.get('nino_id')
        if not nino_id:
            return Response({'error': 'nino_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nino = Nino.objects.get(id=nino_id)
            tarea = nino.tareas.get(id=pk)
            serializer = TareaSerializer(tarea)
            return Response(serializer.data)
        except Nino.DoesNotExist:
            return Response({'error': 'Nino not found'}, status=status.HTTP_404_NOT_FOUND)
        except Tarea.DoesNotExist:
            return Response({'error': 'Tarea not found for this niño'}, status=status.HTTP_404_NOT_FOUND)


class CompletarTareaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        nino_id           = request.data.get('nino_id')
        tarea_id          = request.data.get('tarea_id')
        puntos            = request.data.get('puntos', 0)
        cantidad_aciertos = request.data.get('cantidad_aciertos', 0)
        cantidad_errores  = request.data.get('cantidad_errores', 0)
        tiempo_total_ms   = request.data.get('tiempo_total_ms', 0)

        if not nino_id or not tarea_id:
            return Response({'error': 'nino_id and tarea_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nino  = Nino.objects.get(id=nino_id)
            tarea = Tarea.objects.get(id=tarea_id)
            progreso, created = ProgresoTarea.objects.get_or_create(
                nino=nino, tarea=tarea,
                defaults={
                    'completada': True,
                    'puntos_obtenidos': puntos,
                    'fecha_completada': timezone.now(),
                    'cantidad_aciertos': cantidad_aciertos,
                    'cantidad_errores':  cantidad_errores,
                    'tiempo_total_ms':   tiempo_total_ms,
                }
            )
            if not created:
                progreso.completada        = True
                progreso.puntos_obtenidos  = puntos
                progreso.fecha_completada  = timezone.now()
                progreso.cantidad_aciertos = cantidad_aciertos
                progreso.cantidad_errores  = cantidad_errores
                progreso.tiempo_total_ms   = tiempo_total_ms
                progreso.save()

            nino.monedas     += puntos
            nino.racha_dias  += 1
            nino.experiencia += puntos
            nino.nivel        = max(nino.nivel, (nino.experiencia // 100) + 1)
            nino.save()

            logros_desbloqueados = verificar_y_desbloquear_logros(nino)
            logros_data = LogroNinoSerializer(logros_desbloqueados, many=True).data

            return Response({'message': 'Tarea completada', 'monedas': nino.monedas, 'logros': logros_data})
        except (Nino.DoesNotExist, Tarea.DoesNotExist):
            return Response({'error': 'Nino or Tarea not found'}, status=status.HTTP_404_NOT_FOUND)


class NinoLogrosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        if not nino_id:
            return Response({'error': 'nino_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nino = Nino.objects.get(id=nino_id)
            logros_desbloqueados = LogroNino.objects.filter(nino=nino)
            serializer = LogroNinoSerializer(logros_desbloqueados, many=True)
            return Response(serializer.data)
        except Nino.DoesNotExist:
            return Response({'error': 'Nino not found'}, status=status.HTTP_404_NOT_FOUND)


class LogroListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logros = Logro.objects.all()
        serializer = LogroNinoSerializer if 'nino_id' in request.query_params else None
        if serializer is None:
            data = [{'id': l.id, 'nombre': l.nombre, 'descripcion': l.descripcion, 'icono': l.icono, 'rareza': l.rareza} for l in logros]
            return Response(data)
        nino_id = request.query_params.get('nino_id')
        try:
            nino = Nino.objects.get(id=nino_id)
            logros_nino = set(LogroNino.objects.filter(nino=nino).values_list('logro_id', flat=True))
            data = []
            for logro in logros:
                data.append({
                    'id': logro.id,
                    'nombre': logro.nombre,
                    'descripcion': logro.descripcion,
                    'icono': logro.icono,
                    'rareza': logro.rareza,
                    'desbloqueado': logro.id in logros_nino
                })
            return Response(data)
        except Nino.DoesNotExist:
            return Response({'error': 'Nino not found'}, status=status.HTTP_404_NOT_FOUND)


class EjercicioProgresoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EjercicioProgresoSerializer(data=request.data)
        if serializer.is_valid():
            progreso = serializer.save()
            return Response(EjercicioProgresoSerializer(progreso).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NinoProgresoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        if not nino_id:
            return Response({'error': 'nino_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nino = Nino.objects.get(id=nino_id)
            progreso = ProgresoTarea.objects.filter(nino=nino)
            data = [{'tarea_id': p.tarea.id, 'completada': p.completada} for p in progreso]
            return Response(data)
        except Nino.DoesNotExist:
            return Response({'error': 'Nino not found'}, status=status.HTTP_404_NOT_FOUND)


class ProgresoPracticaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProgresoPracticaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EjercicioPracticaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cantidad = int(request.query_params.get('cantidad', 5))
        ejercicios = EjercicioPractica.objects.filter(activo=True).order_by('?')[:cantidad]
        serializer = EjercicioPracticaSerializer(ejercicios, many=True)
        return Response(serializer.data)
