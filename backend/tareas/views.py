from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Tarea, Nino, ProgresoTarea, EjercicioProgreso, Logro, LogroNino, ProgresoPractica, EjercicioPractica, Skin, SkinComprada, Sticker, StickerComprado
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
            progreso = serializer.save()
            
            # Actualizar estadísticas del niño
            nino = progreso.nino
            nino.monedas += progreso.puntos_obtenidos
            nino.experiencia += progreso.puntos_obtenidos
            nino.nivel = max(nino.nivel, (nino.experiencia // 100) + 1)
            nino.save()
            
            # Verificar logros
            logros_desbloqueados = verificar_y_desbloquear_logros(nino)
            logros_data = LogroNinoSerializer(logros_desbloqueados, many=True).data
            
            return Response({
                'progreso': serializer.data,
                'monedas': nino.monedas,
                'nivel': nino.nivel,
                'experiencia': nino.experiencia,
                'logros': logros_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EjercicioPracticaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cantidad = int(request.query_params.get('cantidad', 5))
        ejercicios = EjercicioPractica.objects.filter(activo=True).order_by('?')[:cantidad]
        serializer = EjercicioPracticaSerializer(ejercicios, many=True)
        return Response(serializer.data)


class SkinsListView(APIView):
    permission_classes = [AllowAny]

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

    def get(self, request):
        nino_id = request.query_params.get('nino_id')
        stickers = Sticker.objects.filter(activo=True)
        serializer = StickerSerializer(stickers, many=True, context={'nino_id': nino_id})
        return Response(serializer.data)


class ComprarStickerView(APIView):
    permission_classes = [AllowAny]

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
