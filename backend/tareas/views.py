from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Tarea, Nino, ProgresoTarea, EjercicioProgreso, Logro, LogroNino, ProgresoPractica, EjercicioPractica, Skin, SkinComprada, Sticker, StickerComprado, Ejercicio, PrediccionError, EventoDistraccion, AnalisisErrorTema
from .serializers import TareaSerializer, TareaCreateSerializer, NinoSerializer, EjercicioProgresoSerializer, LogroSerializer, LogroNinoSerializer, ProgresoPracticaSerializer, EjercicioPracticaSerializer, SkinSerializer, SkinCompradaSerializer, StickerSerializer, StickerCompradoSerializer
from users.permissions import IsProfesor
from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg
from django.conf import settings
from datetime import timedelta
import os
import time


def verificar_y_desbloquear_logros(nino):
    """Verifica y desbloquea logros para un niño basado en sus estadísticas."""
    logros_desbloqueados = []
    
    # Obtener estadísticas del niño
    tareas_completadas = ProgresoTarea.objects.filter(nino=nino, completada=True).count()
    tareas_perfectas = ProgresoTarea.objects.filter(nino=nino, completada=True, cantidad_errores=0).count()
    practicas_completadas = ProgresoPractica.objects.filter(nino=nino, completada=True).count()
    
    # Calcular respuestas rápidas (menos de 5 segundos por ejercicio)
    respuestas_rapidas = EjercicioProgreso.objects.filter(
        student=nino, 
        correct=True, 
        time_spent_ms__lt=5000
    ).count()
    
    # Obtener todos los logros que el niño NO ha desbloqueado
    logros_disponibles = Logro.objects.exclude(logronino__nino=nino)
    
    for logro in logros_disponibles:
        cumple = False
        
        # Verificar cada tipo de condición
        if logro.condicion == 'tareas_completadas':
            cumple = tareas_completadas >= logro.valor_requerido
            
        elif logro.condicion == 'tareas_perfectas':
            cumple = tareas_perfectas >= logro.valor_requerido
            
        elif logro.condicion == 'racha_dias':
            cumple = nino.racha_dias >= logro.valor_requerido
            
        elif logro.condicion == 'respuestas_rapidas':
            cumple = respuestas_rapidas >= logro.valor_requerido
            
        elif logro.condicion == 'nivel_alcanzado':
            cumple = nino.nivel >= logro.valor_requerido
            
        elif logro.condicion == 'monedas_acumuladas':
            cumple = nino.monedas >= logro.valor_requerido
            
        elif logro.condicion == 'practicas_completadas':
            cumple = practicas_completadas >= logro.valor_requerido
            
        elif logro.condicion == 'experiencia_total':
            cumple = nino.experiencia >= logro.valor_requerido
        
        # Si cumple la condición, desbloquear el logro
        if cumple:
            logro_nino = LogroNino.objects.create(nino=nino, logro=logro)
            logros_desbloqueados.append(logro_nino)
            
            # Dar monedas de bonus
            nino.monedas += logro.puntos_bonus
    
    # Guardar cambios si se desbloquearon logros
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
    authentication_classes = []

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
    authentication_classes = []

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
    authentication_classes = []

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

            # Sistema de recompensas mejorado
            monedas_base = puntos
            
            # Bonus por completar sin errores (tarea perfecta)
            bonus_perfecto = 0
            if cantidad_errores == 0 and cantidad_aciertos > 0:
                bonus_perfecto = int(puntos * 0.5)  # 50% bonus
            
            # Bonus por racha
            bonus_racha = 0
            if nino.racha_dias > 0:
                bonus_racha = min(nino.racha_dias * 2, 50)  # Max 50 monedas por racha
            
            total_monedas = monedas_base + bonus_perfecto + bonus_racha
            
            nino.monedas     += total_monedas
            nino.racha_dias  += 1
            nino.experiencia += puntos
            nino.nivel        = max(nino.nivel, (nino.experiencia // 100) + 1)
            nino.save()

            logros_desbloqueados = verificar_y_desbloquear_logros(nino)
            logros_data = LogroNinoSerializer(logros_desbloqueados, many=True).data

            return Response({
                'message': 'Tarea completada',
                'monedas': nino.monedas,
                'monedas_ganadas': {
                    'base': monedas_base,
                    'bonus_perfecto': bonus_perfecto,
                    'bonus_racha': bonus_racha,
                    'total': total_monedas
                },
                'logros': logros_data
            })
        except (Nino.DoesNotExist, Tarea.DoesNotExist):
            return Response({'error': 'Nino or Tarea not found'}, status=status.HTTP_404_NOT_FOUND)


class NinoLogrosView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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
    authentication_classes = []

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        logros = Logro.objects.all().order_by('valor_requerido', 'rareza')
        
        if nino_id:
            try:
                nino = Nino.objects.get(id=nino_id)
                
                # Verificar logros antes de mostrar
                verificar_y_desbloquear_logros(nino)
                
                # Obtener logros desbloqueados
                logros_desbloqueados = set(LogroNino.objects.filter(nino=nino).values_list('logro_id', flat=True))
                
                # Calcular progreso para cada logro
                data = []
                for logro in logros:
                    progreso_actual = 0
                    
                    if logro.condicion == 'tareas_completadas':
                        progreso_actual = ProgresoTarea.objects.filter(nino=nino, completada=True).count()
                    elif logro.condicion == 'tareas_perfectas':
                        progreso_actual = ProgresoTarea.objects.filter(nino=nino, completada=True, cantidad_errores=0).count()
                    elif logro.condicion == 'racha_dias':
                        progreso_actual = nino.racha_dias
                    elif logro.condicion == 'respuestas_rapidas':
                        progreso_actual = EjercicioProgreso.objects.filter(student=nino, correct=True, time_spent_ms__lt=5000).count()
                    elif logro.condicion == 'nivel_alcanzado':
                        progreso_actual = nino.nivel
                    elif logro.condicion == 'monedas_acumuladas':
                        progreso_actual = nino.monedas
                    elif logro.condicion == 'practicas_completadas':
                        progreso_actual = ProgresoPractica.objects.filter(nino=nino, completada=True).count()
                    elif logro.condicion == 'experiencia_total':
                        progreso_actual = nino.experiencia
                    
                    desbloqueado = logro.id in logros_desbloqueados
                    fecha_desbloqueo = None
                    
                    if desbloqueado:
                        logro_nino = LogroNino.objects.filter(nino=nino, logro=logro).first()
                        if logro_nino:
                            fecha_desbloqueo = logro_nino.fecha_desbloqueado
                    
                    data.append({
                        'id': logro.id,
                        'nombre': logro.nombre,
                        'descripcion': logro.descripcion,
                        'icono': logro.icono,
                        'rareza': logro.rareza,
                        'condicion': logro.condicion,
                        'valor_requerido': logro.valor_requerido,
                        'puntos_bonus': logro.puntos_bonus,
                        'desbloqueado': desbloqueado,
                        'progreso_actual': progreso_actual,
                        'porcentaje': min(100, int((progreso_actual / logro.valor_requerido) * 100)) if logro.valor_requerido > 0 else 0,
                        'fecha_desbloqueado': fecha_desbloqueo
                    })
                
                return Response(data)
            except Nino.DoesNotExist:
                return Response({'error': 'Nino not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Sin nino_id, devolver solo información básica
            serializer = LogroSerializer(logros, many=True)
            return Response(serializer.data)


class EjercicioProgresoView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = EjercicioProgresoSerializer(data=request.data)
        if serializer.is_valid():
            progreso = serializer.save()
            return Response(EjercicioProgresoSerializer(progreso).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NinoProgresoView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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
    authentication_classes = []

    def post(self, request):
        serializer = ProgresoPracticaSerializer(data=request.data)
        if serializer.is_valid():
            progreso = serializer.save()
            
            # Actualizar estadísticas del niño con sistema de bonus
            nino = progreso.nino
            monedas_base = progreso.puntos_obtenidos
            
            # Bonus por práctica perfecta
            bonus_perfecto = 0
            if progreso.cantidad_errores == 0 and progreso.cantidad_aciertos > 0:
                bonus_perfecto = int(monedas_base * 0.3)  # 30% bonus en práctica
            
            total_monedas = monedas_base + bonus_perfecto
            
            nino.monedas += total_monedas
            nino.experiencia += progreso.puntos_obtenidos
            nino.nivel = max(nino.nivel, (nino.experiencia // 100) + 1)
            nino.save()
            
            # Verificar logros
            logros_desbloqueados = verificar_y_desbloquear_logros(nino)
            logros_data = LogroNinoSerializer(logros_desbloqueados, many=True).data
            
            # Actualizar recomendaciones si hay errores
            actualizar_recomendaciones = False
            if progreso.cantidad_errores > 0:
                actualizar_recomendaciones = True
            
            return Response({
                'progreso': serializer.data,
                'monedas': nino.monedas,
                'monedas_ganadas': {
                    'base': monedas_base,
                    'bonus_perfecto': bonus_perfecto,
                    'total': total_monedas
                },
                'nivel': nino.nivel,
                'experiencia': nino.experiencia,
                'logros': logros_data,
                'actualizar_recomendaciones': actualizar_recomendaciones
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EjercicioPracticaView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        cantidad = int(request.query_params.get('cantidad', 5))
        ejercicios = EjercicioPractica.objects.filter(activo=True).order_by('?')[:cantidad]
        serializer = EjercicioPracticaSerializer(ejercicios, many=True)
        return Response(serializer.data)


class SkinsListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        skins = Skin.objects.filter(activo=True)
        
        nino = None
        if nino_id:
            try:
                nino = Nino.objects.get(id=nino_id)
            except Nino.DoesNotExist:
                pass
        
        serializer = SkinSerializer(skins, many=True, context={'nino_id': nino_id, 'nino': nino})
        return Response(serializer.data)


class ComprarSkinView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        nino_id = request.data.get('nino_id')
        skin_id = request.data.get('skin_id')

        if not nino_id or not skin_id:
            return Response({'error': 'nino_id y skin_id son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nino = Nino.objects.get(id=nino_id)
            skin = Skin.objects.get(id=skin_id, activo=True)

            # Verificar si ya tiene la skin
            if SkinComprada.objects.filter(nino=nino, skin=skin).exists():
                return Response({'error': 'Ya tienes esta skin'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar monedas
            if nino.monedas < skin.precio:
                return Response({'error': 'No tienes suficientes monedas'}, status=status.HTTP_400_BAD_REQUEST)

            # Realizar compra
            nino.monedas -= skin.precio
            nino.save()

            SkinComprada.objects.create(nino=nino, skin=skin)

            return Response({
                'message': 'Skin comprada exitosamente',
                'monedas': nino.monedas,
                'skin': SkinSerializer(skin).data
            })

        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Skin.DoesNotExist:
            return Response({'error': 'Skin no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class EquiparSkinView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        nino_id = request.data.get('nino_id')
        skin_id = request.data.get('skin_id')

        if not nino_id or not skin_id:
            return Response({'error': 'nino_id y skin_id son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nino = Nino.objects.get(id=nino_id)
            skin = Skin.objects.get(id=skin_id, activo=True)

            # Verificar si tiene la skin
            if not SkinComprada.objects.filter(nino=nino, skin=skin).exists():
                return Response({'error': 'No tienes esta skin'}, status=status.HTTP_400_BAD_REQUEST)

            # Equipar skin
            nino.avatar = skin.avatar_key
            nino.save()

            return Response({
                'message': 'Skin equipada exitosamente',
                'avatar': nino.avatar
            })

        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Skin.DoesNotExist:
            return Response({'error': 'Skin no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class StickersListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        stickers = Sticker.objects.filter(activo=True)
        serializer = StickerSerializer(stickers, many=True, context={'nino_id': nino_id})
        return Response(serializer.data)


class ComprarStickerView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        nino_id = request.data.get('nino_id')
        sticker_id = request.data.get('sticker_id')

        if not nino_id or not sticker_id:
            return Response({'error': 'nino_id y sticker_id son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nino = Nino.objects.get(id=nino_id)
            sticker = Sticker.objects.get(id=sticker_id, activo=True)

            # Verificar si ya tiene el sticker
            if StickerComprado.objects.filter(nino=nino, sticker=sticker).exists():
                return Response({'error': 'Ya tienes este sticker'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar monedas
            if nino.monedas < sticker.precio:
                return Response({'error': 'No tienes suficientes monedas'}, status=status.HTTP_400_BAD_REQUEST)

            # Realizar compra
            nino.monedas -= sticker.precio
            nino.save()

            StickerComprado.objects.create(nino=nino, sticker=sticker)

            return Response({
                'message': 'Sticker comprado exitosamente',
                'monedas': nino.monedas,
                'sticker': StickerSerializer(sticker).data
            })

        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Sticker.DoesNotExist:
            return Response({'error': 'Sticker no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class InventarioTiendaView(APIView):
    permission_classes = [IsAuthenticated, IsProfesor]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        skins = Skin.objects.filter(activo=True)
        stickers = Sticker.objects.filter(activo=True)
        
        return Response({
            'skins': SkinSerializer(skins, many=True).data,
            'stickers': StickerSerializer(stickers, many=True).data
        })

    def post(self, request):
        tipo = request.data.get('tipo')  # 'skin' o 'sticker'
        imagen_file = request.FILES.get('imagen')
        
        if tipo == 'skin':
            # Guardar imagen si se proporciona
            imagen_nombre = ''
            if imagen_file:
                # Generar nombre único
                import time
                file_name = f"skin_{int(time.time())}_{imagen_file.name}"
                
                # Guardar directamente en la carpeta public/imagenes/avatares/
                file_path = os.path.join(settings.MEDIA_ROOT, 'imagenes', 'avatares', file_name)
                
                # Asegurar que el directorio existe
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Guardar el archivo
                with open(file_path, 'wb+') as destination:
                    for chunk in imagen_file.chunks():
                        destination.write(chunk)
                
                # Guardar solo el nombre del archivo en la BD
                imagen_nombre = file_name
            else:
                imagen_nombre = request.data.get('imagen', 'nino.png')
            
            skin = Skin.objects.create(
                nombre=request.data.get('nombre'),
                descripcion=request.data.get('descripcion', ''),
                imagen=imagen_nombre,
                avatar_key=request.data.get('avatar_key', request.data.get('nombre', '').lower().replace(' ', '_')),
                precio=int(request.data.get('precio', 0)),
                rareza=request.data.get('rareza', 'comun')
            )
            return Response(SkinSerializer(skin).data, status=status.HTTP_201_CREATED)
        
        elif tipo == 'sticker':
            # Guardar imagen si se proporciona
            imagen_nombre = ''
            if imagen_file:
                # Generar nombre único
                import time
                file_name = f"sticker_{int(time.time())}_{imagen_file.name}"
                
                # Guardar directamente en la carpeta public/imagenes/stickers/
                file_path = os.path.join(settings.MEDIA_ROOT, 'imagenes', 'stickers', file_name)
                
                # Asegurar que el directorio existe
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Guardar el archivo
                with open(file_path, 'wb+') as destination:
                    for chunk in imagen_file.chunks():
                        destination.write(chunk)
                
                # Guardar solo el nombre del archivo en la BD
                imagen_nombre = file_name
            else:
                imagen_nombre = request.data.get('imagen', 'sticker1.png')
            
            sticker = Sticker.objects.create(
                nombre=request.data.get('nombre'),
                descripcion=request.data.get('descripcion', ''),
                imagen=imagen_nombre,
                precio=int(request.data.get('precio', 0)),
                rareza=request.data.get('rareza', 'comun')
            )
            return Response(StickerSerializer(sticker).data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Tipo inválido'}, status=status.HTTP_400_BAD_REQUEST)


class InventarioItemView(APIView):
    permission_classes = [IsAuthenticated, IsProfesor]

    def patch(self, request, tipo, pk):
        try:
            if tipo == 'skin':
                item = Skin.objects.get(pk=pk)
            elif tipo == 'sticker':
                item = Sticker.objects.get(pk=pk)
            else:
                return Response({'error': 'Tipo inválido'}, status=status.HTTP_400_BAD_REQUEST)

            for field in ['nombre', 'descripcion', 'imagen', 'precio', 'rareza', 'activo']:
                if field in request.data:
                    setattr(item, field, request.data[field])
            
            if tipo == 'skin' and 'avatar_key' in request.data:
                item.avatar_key = request.data['avatar_key']
            
            item.save()
            
            serializer = SkinSerializer(item) if tipo == 'skin' else StickerSerializer(item)
            return Response(serializer.data)

        except (Skin.DoesNotExist, Sticker.DoesNotExist):
            return Response({'error': 'Item no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, tipo, pk):
        try:
            if tipo == 'skin':
                item = Skin.objects.get(pk=pk)
            elif tipo == 'sticker':
                item = Sticker.objects.get(pk=pk)
            else:
                return Response({'error': 'Tipo inválido'}, status=status.HTTP_400_BAD_REQUEST)

            item.delete()
            return Response({'message': 'Item eliminado'}, status=status.HTTP_204_NO_CONTENT)

        except (Skin.DoesNotExist, Sticker.DoesNotExist):
            return Response({'error': 'Item no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class AnalizarRespuestaView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        from .ml_utils import analizar_ejercicio, crear_features_desde_respuesta, detectar_distraccion
        from .models import PrediccionError, EventoDistraccion, AnalisisErrorTema
        
        nino_id = request.data.get('nino_id')
        ejercicio_id = request.data.get('ejercicio_id')
        tiempo_ms = request.data.get('tiempo_ms', 0)
        correcto = request.data.get('correcto', False)
        tab_blur_count = request.data.get('tab_blur_count', 0)
        idle_ms = request.data.get('idle_ms', 0)
        erratic_clicks = request.data.get('erratic_clicks', 0)
        
        if not nino_id:
            return Response({'error': 'nino_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nino = Nino.objects.get(id=nino_id)
            ejercicio = Ejercicio.objects.get(id=ejercicio_id) if ejercicio_id else None
            
            # Calcular tiempo promedio histórico del niño (últimos 30 ejercicios)
            historial_tiempos = EjercicioProgreso.objects.filter(
                student=nino,
                time_spent_ms__gt=0,
                time_spent_ms__lt=180000  # Excluir tiempos mayores a 3 minutos (outliers)
            ).order_by('-created_at')[:30].values_list('time_spent_ms', flat=True)
            
            tiempo_promedio_historico = None
            if historial_tiempos and len(historial_tiempos) >= 5:
                tiempo_promedio_historico = sum(historial_tiempos) / len(historial_tiempos)
            
            # Obtener historial reciente para calcular errores consecutivos
            historial_raw = list(EjercicioProgreso.objects.filter(student=nino).order_by('-created_at')[:10].values(
                'difficulty', 'time_spent_ms', 'attempts', 'used_hint', 'n_hints',
                'fast_response', 'correct', 'tab_blur_count', 'idle_ms', 'erratic_clicks'
            ))
            historial_raw.reverse()  # Ordenar cronológicamente
            
            # Calcular errores consecutivos
            consecutive_errors = 0
            for h in historial_raw:
                if h.get('correct', 1) == 0:
                    consecutive_errors += 1
                else:
                    consecutive_errors = 0
            if not correcto:
                consecutive_errors += 1
            
            # Calcular si el tiempo es excesivo basado en promedio histórico
            excessive_time = 0
            if tiempo_promedio_historico and tiempo_promedio_historico > 0:
                excessive_time = 1 if tiempo_ms > (tiempo_promedio_historico * 3) else 0
            elif historial_raw:
                # Fallback: usar historial reciente si no hay suficiente histórico
                tiempos = [h.get('time_spent_ms', 0) for h in historial_raw if h.get('time_spent_ms', 0) > 0]
                if tiempos and len(tiempos) > 0:
                    tiempo_promedio = sum(tiempos) / len(tiempos)
                    excessive_time = 1 if tiempo_ms > (tiempo_promedio * 3) else 0
            
            # Crear features para el ML
            features = {
                'difficulty': 1,
                'time_spent_ms': tiempo_ms,
                'attempts': 1,
                'used_hint': 0,
                'n_hints': 0,
                'fast_response': 1 if tiempo_ms < 2000 else 0,
                'correct': 1 if correcto else 0,
                'tab_blur_count': tab_blur_count,
                'idle_ms': idle_ms,
                'erratic_clicks': erratic_clicks,
                'consecutive_errors': consecutive_errors,
                'excessive_time': excessive_time
            }
            
            # Predecir tipo de error
            resultado = analizar_ejercicio(features)
            
            if resultado and not correcto:
                # Guardar predicción
                PrediccionError.objects.create(
                    nino=nino,
                    tipo_error=resultado['error_type'],
                    probabilidad=resultado['prob_mistake_next']
                )
            
            # Actualizar análisis por tema si hay ejercicio
            if ejercicio and ejercicio.tema:
                analisis, created = AnalisisErrorTema.objects.get_or_create(
                    nino=nino,
                    tarea=ejercicio.tarea,
                    tema=ejercicio.tema,
                    defaults={
                        'subtema': ejercicio.subtema or 'general',
                        'cantidad_errores': 0 if correcto else 1,
                        'cantidad_aciertos': 1 if correcto else 0,
                        'tiempo_promedio_ms': tiempo_ms
                    }
                )
                if not created:
                    if correcto:
                        analisis.cantidad_aciertos += 1
                    else:
                        analisis.cantidad_errores += 1
                    # Calcular promedio ponderado
                    total = analisis.cantidad_aciertos + analisis.cantidad_errores
                    analisis.tiempo_promedio_ms = int(
                        (analisis.tiempo_promedio_ms * (total - 1) + tiempo_ms) / total
                    )
                    analisis.save()
            
            # Preparar historial con nuevas características para detección de distracción
            historial_completo = []
            for h in historial_raw[-5:]:
                historial_completo.append(h)
            historial_completo.append(features)
            
            # Detectar distracción con tiempo promedio histórico
            distraccion = detectar_distraccion(historial_completo, tiempo_promedio_historico)
            
            # Guardar evento de distracción si es necesario
            if distraccion['requiere_descanso']:
                EventoDistraccion.objects.create(
                    nino=nino,
                    focus_score=distraccion['focus_score'],
                    tab_blur_count=tab_blur_count,
                    idle_ms=idle_ms,
                    erratic_clicks=erratic_clicks,
                    descanso_mostrado=True
                )
            
            return Response({
                'prediccion': resultado,
                'distraccion': distraccion,
                'consecutive_errors': consecutive_errors,
                'excessive_time': excessive_time,
                'tiempo_promedio_historico': tiempo_promedio_historico,
                'debug': {
                    'tiempo_actual_ms': tiempo_ms,
                    'triple_promedio_ms': tiempo_promedio_historico * 3 if tiempo_promedio_historico else None,
                    'cantidad_datos_historicos': len(historial_tiempos) if historial_tiempos else 0
                }
            })
            
        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ReporteErroresView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        
        if not nino_id:
            return Response({'error': 'nino_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nino = Nino.objects.get(id=nino_id)
            
            # Obtener predicciones no notificadas
            predicciones = PrediccionError.objects.filter(nino=nino, notificado=False)
            
            # Agrupar por tipo de error
            errores_agrupados = {}
            for pred in predicciones:
                tipo = pred.tipo_error
                if tipo not in errores_agrupados:
                    errores_agrupados[tipo] = {
                        'tipo': tipo,
                        'cantidad': 0,
                        'probabilidad_promedio': 0,
                        'predicciones': []
                    }
                errores_agrupados[tipo]['cantidad'] += 1
                errores_agrupados[tipo]['predicciones'].append({
                    'id': pred.id,
                    'probabilidad': pred.probabilidad,
                    'fecha': pred.fecha_prediccion
                })
            
            # Calcular promedios
            for tipo, data in errores_agrupados.items():
                probs = [p['probabilidad'] for p in data['predicciones']]
                data['probabilidad_promedio'] = sum(probs) / len(probs)
            
            return Response({
                'nino': NinoSerializer(nino).data,
                'errores': list(errores_agrupados.values())
            })
            
        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class NotificarPadreProfesorView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        nino_id = request.data.get('nino_id')
        
        if not nino_id:
            return Response({'error': 'nino_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nino = Nino.objects.get(id=nino_id)
            
            # Marcar predicciones como notificadas
            predicciones = PrediccionError.objects.filter(nino=nino, notificado=False)
            predicciones.update(notificado=True)
            
            # Obtener información del padre y profesor
            notificaciones = {
                'nino': NinoSerializer(nino).data,
                'padre': None,
                'profesor': None,
                'errores_detectados': []
            }
            
            if nino.padre:
                notificaciones['padre'] = {
                    'email': nino.padre.email,
                    'nombre': f'{nino.padre.nombre} {nino.padre.apellido}'
                }
            
            if nino.profesor:
                notificaciones['profesor'] = {
                    'email': nino.profesor.email,
                    'nombre': f'{nino.profesor.nombre} {nino.profesor.apellido}'
                }
            
            # Agrupar errores
            errores_agrupados = {}
            for pred in predicciones:
                tipo = pred.tipo_error
                if tipo not in errores_agrupados:
                    errores_agrupados[tipo] = []
                errores_agrupados[tipo].append(pred.probabilidad)
            
            for tipo, probs in errores_agrupados.items():
                notificaciones['errores_detectados'].append({
                    'tipo': tipo,
                    'cantidad': len(probs),
                    'probabilidad_promedio': sum(probs) / len(probs)
                })
            
            # Aquí puedes implementar el envío real de emails
            # Por ahora solo retornamos la información
            
            return Response({
                'message': 'Notificaciones preparadas',
                'data': notificaciones
            })
            
        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class EstadisticasMLView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        
        if not nino_id:
            return Response({'error': 'nino_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from .models import AnalisisErrorTema
            nino = Nino.objects.get(id=nino_id)
            
            # Estadísticas de errores
            errores = PrediccionError.objects.filter(nino=nino)
            errores_por_tipo = errores.values('tipo_error').annotate(
                total=Count('id'),
                prob_promedio=Avg('probabilidad')
            )
            
            # Estadísticas de distracción
            distracciones = EventoDistraccion.objects.filter(nino=nino)
            focus_promedio = distracciones.aggregate(Avg('focus_score'))['focus_score__avg'] or 1.0
            total_distracciones = distracciones.count()
            
            # Últimos eventos
            ultimos_eventos = distracciones.order_by('-fecha_evento')[:10].values(
                'focus_score', 'tab_blur_count', 'idle_ms', 'erratic_clicks', 'fecha_evento'
            )
            
            return Response({
                'nino': NinoSerializer(nino).data,
                'errores_por_tipo': list(errores_por_tipo),
                'total_errores': errores.count(),
                'focus_promedio': focus_promedio,
                'total_distracciones': total_distracciones,
                'ultimos_eventos': list(ultimos_eventos)
            })
            
        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ReporteDetalladoView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        """Genera reporte detallado por temas donde el niño comete más errores."""
        from .models import AnalisisErrorTema
        
        nino_id = request.query_params.get('nino_id')
        tarea_id = request.query_params.get('tarea_id')  # Opcional
        
        if not nino_id:
            return Response({'error': 'nino_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nino = Nino.objects.get(id=nino_id)
            
            # Filtrar análisis
            query = AnalisisErrorTema.objects.filter(nino=nino)
            if tarea_id:
                query = query.filter(tarea_id=tarea_id)
            
            # Obtener análisis con errores
            analisis_list = query.filter(cantidad_errores__gt=0).order_by('-cantidad_errores')
            
            # Agrupar por subtema
            reporte_por_subtema = {}
            for analisis in analisis_list:
                subtema = analisis.subtema
                if subtema not in reporte_por_subtema:
                    reporte_por_subtema[subtema] = {
                        'subtema': subtema,
                        'total_errores': 0,
                        'total_aciertos': 0,
                        'temas_problematicos': [],
                        'tiempo_promedio_ms': 0
                    }
                
                reporte_por_subtema[subtema]['total_errores'] += analisis.cantidad_errores
                reporte_por_subtema[subtema]['total_aciertos'] += analisis.cantidad_aciertos
                
                # Solo incluir temas con más de 2 errores
                if analisis.cantidad_errores >= 2:
                    total = analisis.cantidad_aciertos + analisis.cantidad_errores
                    porcentaje_error = (analisis.cantidad_errores / total * 100) if total > 0 else 0
                    
                    reporte_por_subtema[subtema]['temas_problematicos'].append({
                        'tema': analisis.tema,
                        'tema_legible': analisis.tema.replace('_', ' ').title(),
                        'errores': analisis.cantidad_errores,
                        'aciertos': analisis.cantidad_aciertos,
                        'porcentaje_error': round(porcentaje_error, 1),
                        'tiempo_promedio_ms': analisis.tiempo_promedio_ms,
                        'tarea_id': analisis.tarea.id,
                        'tarea_titulo': analisis.tarea.titulo
                    })
            
            # Ordenar temas problemáticos por cantidad de errores
            for subtema_data in reporte_por_subtema.values():
                subtema_data['temas_problematicos'].sort(key=lambda x: x['errores'], reverse=True)
            
            # Convertir a lista y ordenar por total de errores
            reporte_final = sorted(
                reporte_por_subtema.values(),
                key=lambda x: x['total_errores'],
                reverse=True
            )
            
            return Response({
                'nino': {
                    'id': nino.id,
                    'nombre': nino.nombre,
                    'apellido': nino.apellido,
                    'edad': nino.edad,
                    'grado': nino.grado
                },
                'padre': {
                    'email': nino.padre.email if nino.padre else None,
                    'nombre': f'{nino.padre.nombre} {nino.padre.apellido}' if nino.padre else None
                } if nino.padre else None,
                'profesor': {
                    'email': nino.profesor.email if nino.profesor else None,
                    'nombre': f'{nino.profesor.nombre} {nino.profesor.apellido}' if nino.profesor else None
                } if nino.profesor else None,
                'reporte_por_subtema': reporte_final,
                'resumen': {
                    'total_errores': sum(s['total_errores'] for s in reporte_final),
                    'total_aciertos': sum(s['total_aciertos'] for s in reporte_final),
                    'subtemas_con_dificultad': len([s for s in reporte_final if s['total_errores'] >= 3])
                }
            })
            
        except Nino.DoesNotExist:
            return Response({'error': 'Niño no encontrado'}, status=status.HTTP_404_NOT_FOUND)
