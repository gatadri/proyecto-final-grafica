from django.urls import path
from .views import RegisterView, LoginView, UsuariosView, UsuarioDetailView, SuspenderUsuarioView, ActivarUsuarioView, NinoLoginView, HijosPadreView, EstadisticasGeneralesView, EstadisticasHijosPadreView, EstadisticasClaseProfesorView

urlpatterns = [
    path('register',                    RegisterView.as_view()),
    path('login',                       LoginView.as_view()),
    path('nino/login',                  NinoLoginView.as_view()),
    path('usuarios',                    UsuariosView.as_view()),
    path('usuarios/<int:pk>',           UsuarioDetailView.as_view()),
    path('usuarios/<int:pk>/suspender', SuspenderUsuarioView.as_view()),
    path('usuarios/<int:pk>/activar',   ActivarUsuarioView.as_view()),
    path('usuarios/<int:pk>/hijos',     HijosPadreView.as_view()),
    path('director/estadisticas-generales', EstadisticasGeneralesView.as_view()),
    path('padre/<int:pk>/estadisticas-hijos', EstadisticasHijosPadreView.as_view()),
    path('profesor/<int:pk>/estadisticas-clase', EstadisticasClaseProfesorView.as_view()),
]
