from django.urls import path
from .views import TareaListCreateView, TareaDetailView, EstudiantesProfesorView, NinoTareasView, NinoTareaDetailView, EjercicioProgresoView, CompletarTareaView, NinoProgresoView, NinoLogrosView, LogroListView, ProgresoPracticaView, EjercicioPracticaView

urlpatterns = [
    path('tareas',                  TareaListCreateView.as_view()),
    path('tareas/<int:pk>',         TareaDetailView.as_view()),
    path('profesor/estudiantes',    EstudiantesProfesorView.as_view()),
    path('nino/tareas',             NinoTareasView.as_view()),
    path('nino/tareas/<int:pk>',    NinoTareaDetailView.as_view()),
    path('nino/ejercicio-progreso', EjercicioProgresoView.as_view()),
    path('nino/completar-tarea',    CompletarTareaView.as_view()),
    path('nino/progreso',           NinoProgresoView.as_view()),
    path('nino/progreso-practica',  ProgresoPracticaView.as_view()),
    path('nino/ejercicios-practica', EjercicioPracticaView.as_view()),
    path('nino/logros',             NinoLogrosView.as_view()),
    path('logros',                  LogroListView.as_view()),
]
