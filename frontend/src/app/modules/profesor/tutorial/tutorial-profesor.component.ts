import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AudioService, AudioType } from '../../../core/services/audio.service';

interface TutorialStep {
  titulo: string;
  descripcion: string;
  icono: string;
  pasos?: string[];
}

@Component({
  selector: 'app-tutorial-profesor',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tutorial-profesor.component.html',
  styleUrls: ['./tutorial-profesor.component.css']
})
export class TutorialProfesorComponent implements OnInit, OnDestroy {
  pasoActual = 0;
  
  constructor(public audioService: AudioService) {}
  
  tutoriales: TutorialStep[] = [
    {
      titulo: 'Bienvenido Profesor 👨‍🏫',
      descripcion: 'Guía completa para gestionar tu clase',
      icono: 'chalkboard-teacher',
      pasos: [
        'Este tutorial te mostrará cómo usar todas las herramientas',
        'Aprenderás a crear tareas, gestionar estudiantes y más',
        'Usa las flechas para navegar',
        '¡Comencemos!'
      ]
    },
    {
      titulo: 'Dashboard - Vista General 📊',
      descripcion: 'Resumen de tu clase y actividades',
      icono: 'tachometer-alt',
      pasos: [
        'El Dashboard muestra estadísticas de tus estudiantes',
        'Verás el número total de estudiantes asignados',
        'Revisa las tareas pendientes y completadas',
        'Observa el progreso general de tu clase',
        'Accede rápidamente a las funciones principales'
      ]
    },
    {
      titulo: 'Gestión de Tareas 📝',
      descripcion: 'Crea y asigna tareas a tus estudiantes',
      icono: 'tasks',
      pasos: [
        'Haz clic en "Mis Tareas" en el menú lateral',
        'Presiona el botón "Crear Nueva Tarea"',
        'Completa el formulario con título y descripción',
        'Elige el tipo de ejercicio (múltiple, completar, verdadero/falso)',
        'Añade las preguntas con sus respuestas correctas',
        'Selecciona los estudiantes a quienes asignar la tarea',
        'Guarda y la tarea estará disponible para los estudiantes'
      ]
    },
    {
      titulo: 'Editar y Eliminar Tareas ✏️',
      descripcion: 'Modifica o elimina tareas existentes',
      icono: 'edit',
      pasos: [
        'En la lista de tareas, haz clic en el botón "Editar"',
        'Modifica cualquier campo de la tarea',
        'Puedes añadir o quitar ejercicios',
        'Cambia los estudiantes asignados si es necesario',
        'Para eliminar, usa el botón "Eliminar" (con confirmación)',
        'Los cambios se aplican inmediatamente'
      ]
    },
    {
      titulo: 'Mis Estudiantes 👥',
      descripcion: 'Visualiza y gestiona tus estudiantes',
      icono: 'users',
      pasos: [
        'Ve a "Mis Estudiantes" en el menú',
        'Verás la lista de todos tus estudiantes asignados',
        'Revisa su nivel, monedas y experiencia',
        'Observa cuántas tareas han completado',
        'Identifica estudiantes que necesitan apoyo',
        'Usa esta información para personalizar la enseñanza'
      ]
    },
    {
      titulo: 'Inventario de Tienda 🛒',
      descripcion: 'Gestiona skins y stickers disponibles',
      icono: 'store',
      pasos: [
        'Accede a "Inventario Tienda" en el menú',
        'Verás todas las skins y stickers del sistema',
        'Haz clic en "Crear Nuevo Item" para añadir contenido',
        'Completa el formulario (nombre, descripción, precio, rareza)',
        'Para skins, especifica la clave del avatar',
        'Puedes editar o desactivar items existentes',
        'Los estudiantes verán los cambios en su tienda'
      ]
    },
    {
      titulo: 'Reporte de Clase 📈',
      descripcion: 'Analiza el rendimiento de tu clase',
      icono: 'chart-bar',
      pasos: [
        'Ve a "Reporte de Clase" en el menú',
        'Visualiza estadísticas generales de toda la clase',
        'Revisa el rendimiento semanal',
        'Identifica al estudiante más activo',
        'Ve quién tiene el mejor rendimiento',
        'Haz clic en un estudiante para ver su reporte individual',
        'Descarga el reporte en PDF para compartir o archivar'
      ]
    },
    {
      titulo: 'Interpretando Estadísticas 📊',
      descripcion: 'Entiende los datos de tus estudiantes',
      icono: 'chart-line',
      pasos: [
        'Tasa de éxito: Porcentaje de respuestas correctas',
        'Tiempo promedio: Cuánto tardan en completar tareas',
        'Racha de días: Días consecutivos con actividad',
        'Nivel y XP: Progreso general del estudiante',
        'Monedas: Recompensas acumuladas',
        'Usa estos datos para identificar fortalezas y áreas de mejora'
      ]
    },
    {
      titulo: 'Mejores Prácticas 💡',
      descripcion: 'Consejos para aprovechar el sistema',
      icono: 'lightbulb',
      pasos: [
        '✅ Crea tareas variadas con diferentes tipos de ejercicios',
        '✅ Asigna tareas regularmente para mantener el compromiso',
        '✅ Revisa los reportes semanalmente',
        '✅ Añade contenido nuevo a la tienda como incentivo',
        '✅ Identifica estudiantes con bajo rendimiento tempranamente',
        '✅ Celebra los logros de tus estudiantes',
        '✅ Usa las estadísticas para personalizar tu enseñanza'
      ]
    }
  ];

  get tutorialActual(): TutorialStep {
    return this.tutoriales[this.pasoActual];
  }

  siguiente(): void {
    if (this.pasoActual < this.tutoriales.length - 1) {
      this.pasoActual++;
    }
  }

  anterior(): void {
    if (this.pasoActual > 0) {
      this.pasoActual--;
    }
  }

  irAPaso(index: number): void {
    this.pasoActual = index;
  }

  get progreso(): number {
    return ((this.pasoActual + 1) / this.tutoriales.length) * 100;
  }

  toggleAudioTutorial(): void {
    this.audioService.toggle(AudioType.TUTORIALES);
  }

  get isAudioPlaying(): boolean {
    return this.audioService.isPlaying(AudioType.TUTORIALES);
  }

  ngOnInit(): void {
    if (this.audioService.isEnabled(AudioType.TUTORIALES)) {
      this.audioService.play(AudioType.TUTORIALES);
    }
  }

  ngOnDestroy(): void {
    this.audioService.pause(AudioType.TUTORIALES);
  }
}
