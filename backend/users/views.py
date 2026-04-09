from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .permissions import IsDirector
from tareas.models import Nino
from tareas.serializers import NinoSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

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

    def post(self, request):
        nombre = request.data.get('nombre', '').strip()
        pin    = request.data.get('pin', '').strip()
        try:
            nino = Nino.objects.get(nombre__iexact=nombre, pin=pin)
            return Response({'nino': NinoSerializer(nino).data})
        except Nino.DoesNotExist:
            return Response({'message': 'Nombre o PIN incorrecto'}, status=status.HTTP_400_BAD_REQUEST)
