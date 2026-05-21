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
  selector: 'app-tutorial-director',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tutorial-director.component.html',
  styleUrls: ['./tutorial-director.component.css']
})
export class TutorialDirectorComponent implements OnInit, OnDestroy {
  pasoActual = 0;
  
  constructor(public audioService: AudioService) {}
  
  tutoriales: TutorialStep[] = [
    {
      titulo: 'Bienvenido Director 🎓',
      descripcion: 'Guía completa para administrar el sistema',
      icono: 'user-tie',
      pasos: [
        'Este tutorial te mostrará todas las funciones administrativas',
        'Aprenderás a gestionar usuarios, ver estadísticas y más',
        'Tienes control total sobre el sistema educativo',
        'Usa las flechas para navegar',
        '¡Comencemos!'
      ]
    },
    {
      titulo: 'Dashboard - Vista Administrativa 📊',
      descripcion: 'Resumen general del sistema',
      icono: 'tachometer-alt',
      pasos: [
        'El Dashboard muestra estadísticas globales del sistema',
        'Ve el número total de usuarios (profesores y padres)',
        'Revisa el total de estudiantes registrados',
        'Observa las tareas creadas y completadas',
        'Accede rápidamente a las funciones principales',
        'Identifica tendencias y áreas que necesitan atención'
      ]
    },
    {
      titulo: 'Gestión de Usuarios 👥',
      descripcion: 'Administra profesores y padres',
      icono: 'users',
      pasos: [
        'Haz clic en "Gestión de Usuarios" en el menú',
        'Verás la lista completa de usuarios del sistema',
        'Puedes ver profesores y padres con sus detalles',
        'Cada usuario muestra su rol, email y estado',
        'Usa los filtros para encontrar usuarios específicos'
      ]
    },
    {
      titulo: 'Crear Nuevos Usuarios ➕',
      descripcion: 'Añade profesores y padres al sistema',
      icono: 'user-plus',
      pasos: [
        'En Gestión de Usuarios, haz clic en "Crear Usuario"',
        'Completa el formulario con nombre, apellido y email',
        'Establece una contraseña segura',
        'Selecciona el rol (Profesor o Padre)',
        'Si es padre, puedes añadir sus hijos inmediatamente',
        'Para cada hijo, asigna un profesor y crea un PIN',
        'Guarda y el usuario podrá acceder al sistema'
      ]
    },
    {
      titulo: 'Gestionar Estados de Usuario 🔄',
      descripcion: 'Suspender, activar o eliminar usuarios',
      icono: 'user-cog',
      pasos: [
        'En la lista de usuarios, cada uno tiene botones de acción',
        'Botón rojo (Ban): Suspende temporalmente al usuario',
        'Botón verde (Check): Reactiva un usuario suspendido',
        'Botón "Ver Detalles": Muestra información completa',
        'Botón rojo (Trash): Elimina permanentemente (con confirmación)',
        'Los usuarios suspendidos no pueden acceder al sistema',
        'Usa estas funciones con responsabilidad'
      ]
    },
    {
      titulo: 'Ver Detalles de Padres 👨👩👧👦',
      descripcion: 'Información completa de familias',
      icono: 'info-circle',
      pasos: [
        'Haz clic en "Ver Detalles" en un usuario padre',
        'Se abrirá un modal con información completa',
        'Verás la lista de todos sus hijos',
        'Para cada hijo se muestra su nombre y PIN',
        'También verás qué profesor está asignado',
        'Útil para verificar asignaciones y resolver dudas'
      ]
    },
    {
      titulo: 'Estadísticas del Sistema 📈',
      descripcion: 'Análisis completo del rendimiento',
      icono: 'chart-line',
      pasos: [
        'Ve a "Estadísticas" en el menú lateral',
        'Visualiza métricas clave del sistema completo',
        'Total de estudiantes activos vs inactivos',
        'Promedio de aciertos y errores general',
        'Distribución de estudiantes por nivel',
        'Tareas completadas por tipo de ejercicio',
        'Usa estos datos para tomar decisiones informadas'
      ]
    },
    {
      titulo: 'Reportes Generales 📄',
      descripcion: 'Informes descargables del sistema',
      icono: 'file-alt',
      pasos: [
        'Accede a "Reportes" en el menú',
        'Verás estadísticas generales del sistema',
        'Incluye total de estudiantes, tareas y monedas',
        'Gráficos de rendimiento semanal',
        'Distribución de niveles de estudiantes',
        'Haz clic en "Descargar PDF" para generar el reporte',
        'Útil para presentaciones y reuniones administrativas'
      ]
    },
    {
      titulo: 'Log de Actividades 📋',
      descripcion: 'Historial de acciones en el sistema',
      icono: 'history',
      pasos: [
        'Ve a "Log de Actividades" en el menú',
        'Visualiza un registro de todas las acciones importantes',
        'Incluye creación de usuarios, tareas y cambios',
        'Cada entrada muestra fecha, hora y usuario responsable',
        'Útil para auditorías y seguimiento',
        'Identifica patrones de uso del sistema'
      ]
    },
    {
      titulo: 'Interpretando Métricas 🎯',
      descripcion: 'Cómo usar los datos efectivamente',
      icono: 'bullseye',
      pasos: [
        'Estudiantes activos: Han completado al menos una tarea',
        'Tasa de participación: % de estudiantes activos',
        'Promedio de aciertos alto: Buen nivel académico general',
        'Distribución de niveles: Identifica grupos que necesitan apoyo',
        'Rendimiento semanal: Detecta días con más/menos actividad',
        'Usa estos insights para mejorar el sistema educativo'
      ]
    },
    {
      titulo: 'Mejores Prácticas Administrativas 💡',
      descripcion: 'Consejos para gestionar efectivamente',
      icono: 'lightbulb',
      pasos: [
        '✅ Revisa las estadísticas semanalmente',
        '✅ Mantén actualizada la lista de usuarios',
        '✅ Verifica que todos los estudiantes tengan profesor asignado',
        '✅ Descarga reportes mensuales para archivo',
        '✅ Comunica hallazgos importantes a los profesores',
        '✅ Suspende usuarios solo cuando sea necesario',
        '✅ Mantén respaldos de los reportes importantes',
        '✅ Usa el log de actividades para resolver incidencias'
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
