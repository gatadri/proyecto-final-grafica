from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, NinoSerializer
from .permissions import IsDirector, IsPadre
from tareas.models import Nino, ProgresoTarea, ProgresoPractica, LogroNino, Tarea
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuariosView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsDirector]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDirector]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SuspenderUsuarioView(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        user.activo = False
        user.save()
        return Response({'message': 'Usuario suspendido'})


class ActivarUsuarioView(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        user.activo = True
        user.save()
        return Response({'message': 'Usuario activado'})


class NinoLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        nombre = request.data.get('nombre', '').strip()
        pin    = request.data.get('pin', '').strip()
        try:
            nino = Nino.objects.get(nombre__iexact=nombre, pin=pin)
            return Response({'nino': NinoSerializer(nino).data})
        except Nino.DoesNotExist:
            return Response({'message': 'Nombre o PIN incorrecto'}, status=status.HTTP_400_BAD_REQUEST)


class HijosPadreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            padre = User.objects.get(pk=pk, role='padre')
            hijos = Nino.objects.filter(padre=padre).select_related('profesor')
            serializer = NinoSerializer(hijos, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'Padre no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class EstadisticasGeneralesView(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    def get(self, request):
        # Total de estudiantes
        total_estudiantes = Nino.objects.count()
        
        # Tareas completadas
        total_tareas_completadas = ProgresoTarea.objects.filter(completada=True).count()
        
        # Promedios de aciertos y errores
        progresos = ProgresoTarea.objects.filter(completada=True).aggregate(
            promedio_aciertos=Avg('cantidad_aciertos'),
            promedio_errores=Avg('cantidad_errores')
        )
        
        # Monedas y XP total
        totales = Nino.objects.aggregate(
            total_monedas=Sum('monedas'),
            total_xp=Sum('experiencia')
        )
        
        # Estudiantes activos (con al menos una tarea completada)
        estudiantes_activos = Nino.objects.filter(
            progreso_tareas__completada=True
        ).distinct().count()
        
        # Tareas por tipo
        from tareas.models import Tarea
        tareas_por_tipo = Tarea.objects.values('tipo_ejercicio').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad')
        
        # Distribución de niveles
        distribucion_niveles = Nino.objects.values('nivel').annotate(
            cantidad=Count('id')
        ).order_by('nivel')
        
        # Rendimiento semanal (últimos 7 días)
        hoy = datetime.now().date()
        rendimiento_semanal = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        for i in range(7):
            dia = hoy - timedelta(days=6-i)
            progresos_dia = ProgresoTarea.objects.filter(
                fecha_completada__date=dia,
                completada=True
            ).aggregate(
                aciertos=Sum('cantidad_aciertos'),
                errores=Sum('cantidad_errores')
            )
            
            rendimiento_semanal.append({
                'dia': dias_semana[dia.weekday()],
                'aciertos': progresos_dia['aciertos'] or 0,
                'errores': progresos_dia['errores'] or 0
            })
        
        return Response({
            'total_estudiantes': total_estudiantes,
            'total_tareas_completadas': total_tareas_completadas,
            'promedio_aciertos': progresos['promedio_aciertos'] or 0,
            'promedio_errores': progresos['promedio_errores'] or 0,
            'total_monedas_sistema': totales['total_monedas'] or 0,
            'total_xp_sistema': totales['total_xp'] or 0,
            'estudiantes_activos': estudiantes_activos,
            'tareas_por_tipo': list(tareas_por_tipo),
            'distribucion_niveles': list(distribucion_niveles),
            'rendimiento_semanal': rendimiento_semanal
        })


class EstadisticasHijosPadreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            padre = User.objects.get(pk=pk, role='padre')
            
            # Verificar que el usuario autenticado es el padre
            if request.user.id != padre.id and request.user.role != 'director':
                return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
            
            hijos = Nino.objects.filter(padre=padre)
            
            if not hijos.exists():
                return Response({'error': 'No tiene hijos registrados'}, status=status.HTTP_404_NOT_FOUND)
            
            # Estadísticas individuales de cada hijo
            estadisticas_individuales = []
            
            for hijo in hijos:
                progresos = ProgresoTarea.objects.filter(nino=hijo, completada=True)
                
                stats = progresos.aggregate(
                    total_aciertos=Sum('cantidad_aciertos'),
                    total_errores=Sum('cantidad_errores'),
                    promedio_tiempo=Avg('tiempo_total_ms')
                )
                
                total_aciertos = stats['total_aciertos'] or 0
                total_errores = stats['total_errores'] or 0
                total = total_aciertos + total_errores
                tasa_exito = (total_aciertos / total * 100) if total > 0 else 0
                
                ultima_actividad = progresos.order_by('-fecha_completada').first()
                
                estadisticas_individuales.append({
                    'id': hijo.id,
                    'nombre': hijo.nombre,
                    'apellido': hijo.apellido,
                    'edad': hijo.edad,
                    'grado': hijo.grado,
                    'avatar': hijo.avatar,
                    'nivel': hijo.nivel,
                    'experiencia': hijo.experiencia,
                    'monedas': hijo.monedas,
                    'racha_dias': hijo.racha_dias,
                    'tareas_completadas': progresos.count(),
                    'total_aciertos': total_aciertos,
                    'total_errores': total_errores,
                    'promedio_tiempo_ms': int(stats['promedio_tiempo'] or 0),
                    'tasa_exito': round(tasa_exito, 1),
                    'ultima_actividad': ultima_actividad.fecha_completada.strftime('%d/%m/%Y') if ultima_actividad else None
                })
            
            # Estadísticas grupales
            total_tareas = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).count()
            
            totales_grupales = ProgresoTarea.objects.filter(nino__in=hijos, completada=True).aggregate(
                total_aciertos=Sum('cantidad_aciertos'),
                total_errores=Sum('cantidad_errores')
            )
            
            totales_hijos = hijos.aggregate(
                total_monedas=Sum('monedas'),
                promedio_nivel=Avg('nivel')
            )
            
            # Hijo más activo
            hijo_mas_activo = hijos.annotate(
                num_tareas=Count('progreso_tareas', filter=Q(progreso_tareas__completada=True))
            ).order_by('-num_tareas').first()
            
            # Mejor rendimiento
            mejor_hijo = None
            mejor_tasa = 0
            for stats in estadisticas_individuales:
                if stats['tasa_exito'] > mejor_tasa:
                    mejor_tasa = stats['tasa_exito']
                    mejor_hijo = f"{stats['nombre']} {stats['apellido']}"
            
            # Rendimiento semanal
            hoy = datetime.now().date()
            rendimiento_semanal = []
            dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            
            for i in range(7):
                dia = hoy - timedelta(days=6-i)
                progresos_dia = ProgresoTarea.objects.filter(
                    nino__in=hijos,
                    fecha_completada__date=dia,
                    completada=True
                ).aggregate(
                    aciertos=Sum('cantidad_aciertos'),
                    errores=Sum('cantidad_errores')
                )
                
                rendimiento_semanal.append({
                    'dia': dias_semana[dia.weekday()],
                    'aciertos': progresos_dia['aciertos'] or 0,
                    'errores': progresos_dia['errores'] or 0
                })
            
            estadisticas_grupales = {
                'total_hijos': hijos.count(),
                'total_tareas_completadas': total_tareas,
                'total_aciertos': totales_grupales['total_aciertos'] or 0,
                'total_errores': totales_grupales['total_errores'] or 0,
                'promedio_nivel': round(totales_hijos['promedio_nivel'] or 0, 1),
                'total_monedas': totales_hijos['total_monedas'] or 0,
                'hijo_mas_activo': f"{hijo_mas_activo.nombre} {hijo_mas_activo.apellido}" if hijo_mas_activo else 'N/A',
                'mejor_rendimiento': mejor_hijo or 'N/A',
                'rendimiento_semanal': rendimiento_semanal
            }
            
            return Response({
                'estadisticas_individuales': estadisticas_individuales,
                'estadisticas_grupales': estadisticas_grupales
            })
            
        except User.DoesNotExist:
            return Response({'error': 'Padre no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class EstadisticasClaseProfesorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profesor = User.objects.get(pk=pk, role='profesor')
            
            # Verificar que el usuario autenticado es el profesor
            if request.user.id != profesor.id and request.user.role != 'director':
                return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
            
            estudiantes = Nino.objects.filter(profesor=profesor)
            
            if not estudiantes.exists():
                return Response({'error': 'No tiene estudiantes asignados'}, status=status.HTTP_404_NOT_FOUND)
            
            # Estadísticas individuales de cada estudiante
            estadisticas_individuales = []
            
            for estudiante in estudiantes:
                progresos = ProgresoTarea.objects.filter(nino=estudiante, completada=True)
                
                stats = progresos.aggregate(
                    total_aciertos=Sum('cantidad_aciertos'),
                    total_errores=Sum('cantidad_errores'),
                    promedio_tiempo=Avg('tiempo_total_ms')
                )
                
                total_aciertos = stats['total_aciertos'] or 0
                total_errores = stats['total_errores'] or 0
                total = total_aciertos + total_errores
                tasa_exito = (total_aciertos / total * 100) if total > 0 else 0
                
                ultima_actividad = progresos.order_by('-fecha_completada').first()
                
                estadisticas_individuales.append({
                    'id': estudiante.id,
                    'nombre': estudiante.nombre,
                    'apellido': estudiante.apellido,
                    'edad': estudiante.edad,
                    'grado': estudiante.grado,
                    'avatar': estudiante.avatar,
                    'nivel': estudiante.nivel,
                    'experiencia': estudiante.experiencia,
                    'monedas': estudiante.monedas,
                    'racha_dias': estudiante.racha_dias,
                    'tareas_completadas': progresos.count(),
                    'total_aciertos': total_aciertos,
                    'total_errores': total_errores,
                    'promedio_tiempo_ms': int(stats['promedio_tiempo'] or 0),
                    'tasa_exito': round(tasa_exito, 1),
                    'ultima_actividad': ultima_actividad.fecha_completada.strftime('%d/%m/%Y') if ultima_actividad else None
                })
            
            # Estadísticas de la clase
            total_tareas = ProgresoTarea.objects.filter(nino__in=estudiantes, completada=True).count()
            
            totales_clase = ProgresoTarea.objects.filter(nino__in=estudiantes, completada=True).aggregate(
                total_aciertos=Sum('cantidad_aciertos'),
                total_errores=Sum('cantidad_errores')
            )
            
            totales_estudiantes = estudiantes.aggregate(
                total_monedas=Sum('monedas'),
                promedio_nivel=Avg('nivel')
            )
            
            # Estudiante más activo
            estudiante_mas_activo = estudiantes.annotate(
                num_tareas=Count('progreso_tareas', filter=Q(progreso_tareas__completada=True))
            ).order_by('-num_tareas').first()
            
            # Mejor rendimiento
            mejor_estudiante = None
            mejor_tasa = 0
            for stats in estadisticas_individuales:
                if stats['tasa_exito'] > mejor_tasa:
                    mejor_tasa = stats['tasa_exito']
                    mejor_estudiante = f"{stats['nombre']} {stats['apellido']}"
            
            # Rendimiento semanal
            hoy = datetime.now().date()
            rendimiento_semanal = []
            dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            
            for i in range(7):
                dia = hoy - timedelta(days=6-i)
                progresos_dia = ProgresoTarea.objects.filter(
                    nino__in=estudiantes,
                    fecha_completada__date=dia,
                    completada=True
                ).aggregate(
                    aciertos=Sum('cantidad_aciertos'),
                    errores=Sum('cantidad_errores')
                )
                
                rendimiento_semanal.append({
                    'dia': dias_semana[dia.weekday()],
                    'aciertos': progresos_dia['aciertos'] or 0,
                    'errores': progresos_dia['errores'] or 0
                })
            
            estadisticas_clase = {
                'total_estudiantes': estudiantes.count(),
                'total_tareas_completadas': total_tareas,
                'total_aciertos': totales_clase['total_aciertos'] or 0,
                'total_errores': totales_clase['total_errores'] or 0,
                'promedio_nivel': round(totales_estudiantes['promedio_nivel'] or 0, 1),
                'total_monedas': totales_estudiantes['total_monedas'] or 0,
                'estudiante_mas_activo': f"{estudiante_mas_activo.nombre} {estudiante_mas_activo.apellido}" if estudiante_mas_activo else 'N/A',
                'mejor_rendimiento': mejor_estudiante or 'N/A',
                'rendimiento_semanal': rendimiento_semanal
            }
            
            return Response({
                'estadisticas_individuales': estadisticas_individuales,
                'estadisticas_clase': estadisticas_clase
            })
            
        except User.DoesNotExist:
            return Response({'error': 'Profesor no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class LogsActividadView(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    def get(self, request):
        logs = []
        
        # Tareas completadas recientes
        progresos_tareas = ProgresoTarea.objects.filter(
            completada=True,
            fecha_completada__isnull=False
        ).select_related('nino', 'tarea', 'tarea__profesor').order_by('-fecha_completada')[:30]
        
        for progreso in progresos_tareas:
            logs.append({
                'fecha': progreso.fecha_completada.strftime('%Y-%m-%d %H:%M'),
                'usuario': f"{progreso.nino.nombre} {progreso.nino.apellido}",
                'descripcion': f'Completó tarea "{progreso.tarea.titulo}" ({progreso.puntos_obtenidos} pts)',
                'tipo': 'tarea'
            })
        
        # Prácticas completadas recientes
        progresos_practica = ProgresoPractica.objects.filter(
            completada=True
        ).select_related('nino').order_by('-fecha_practica')[:20]
        
        for progreso in progresos_practica:
            logs.append({
                'fecha': progreso.fecha_practica.strftime('%Y-%m-%d %H:%M'),
                'usuario': f"{progreso.nino.nombre} {progreso.nino.apellido}",
                'descripcion': f'Completó práctica libre ({progreso.puntos_obtenidos} pts)',
                'tipo': 'practica'
            })
        
        # Logros obtenidos recientes
        logros = LogroNino.objects.select_related(
            'nino', 'logro'
        ).order_by('-fecha_desbloqueado')[:20]
        
        for logro in logros:
            logs.append({
                'fecha': logro.fecha_desbloqueado.strftime('%Y-%m-%d %H:%M'),
                'usuario': f"{logro.nino.nombre} {logro.nino.apellido}",
                'descripcion': f'Obtuvo logro "{logro.logro.nombre}"',
                'tipo': 'logro'
            })
        
        # Tareas creadas recientemente
        tareas = Tarea.objects.select_related('profesor').order_by('-created_at')[:15]
        
        for tarea in tareas:
            logs.append({
                'fecha': tarea.created_at.strftime('%Y-%m-%d %H:%M'),
                'usuario': f"{tarea.profesor.nombre} {tarea.profesor.apellido}",
                'descripcion': f'Creó la tarea "{tarea.titulo}"',
                'tipo': 'sistema'
            })
        
        # Ordenar todos los logs por fecha descendente
        logs.sort(key=lambda x: x['fecha'], reverse=True)
        
        # Retornar solo los últimos 50
        return Response(logs[:50])
