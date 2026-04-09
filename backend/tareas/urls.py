from django.urls import path
from .views import TareaListCreateView, TareaDetailView, EstudiantesProfesorView

urlpatterns = [
    path('tareas',                  TareaListCreateView.as_view()),
    path('tareas/<int:pk>',         TareaDetailView.as_view()),
    path('profesor/estudiantes',    EstudiantesProfesorView.as_view()),
]
