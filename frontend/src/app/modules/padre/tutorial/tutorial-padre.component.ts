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
  selector: 'app-tutorial-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tutorial-padre.component.html',
  styleUrls: ['./tutorial-padre.component.css']
})
export class TutorialPadreComponent implements OnInit, OnDestroy {
  pasoActual = 0;
  
  constructor(public audioService: AudioService) {}
  
  tutoriales: TutorialStep[] = [
    {
      titulo: 'Bienvenido Padre/Madre 👨‍👩‍👧‍👦',
      descripcion: 'Guía para monitorear el progreso de tus hijos',
      icono: 'users',
      pasos: [
        'Este tutorial te enseñará a usar el sistema',
        'Aprenderás a monitorear el progreso de tus hijos',
        'Podrás ver estadísticas detalladas y reportes',
        'Usa las flechas para navegar',
        '¡Empecemos!'
      ]
    },
    {
      titulo: 'Dashboard - Vista de Tus Hijos 🏠',
      descripcion: 'Resumen del progreso de cada hijo',
      icono: 'tachometer-alt',
      pasos: [
        'El Dashboard muestra tarjetas de cada uno de tus hijos',
        'Verás el nombre del profesor asignado a cada hijo',
        'Observa sus monedas, nivel y experiencia',
        'Revisa su racha de días consecutivos',
        'Ve cuántas tareas tienen asignadas',
        'Accede rápidamente a los reportes detallados'
      ]
    },
    {
      titulo: 'Entendiendo las Estadísticas 📊',
      descripcion: 'Qué significan los números',
      icono: 'chart-line',
      pasos: [
        'Monedas 🪙: Recompensas ganadas por completar tareas',
        'Nivel ⭐: Progreso general basado en experiencia',
        'Experiencia (XP): Puntos acumulados por aprender',
        'Racha de días 🔥: Días consecutivos con actividad',
        'Tareas asignadas 📚: Trabajos pendientes del profesor',
        'Estos indicadores muestran el compromiso y progreso'
      ]
    },
    {
      titulo: 'Reportes Detallados 📈',
      descripcion: 'Análisis profundo del rendimiento',
      icono: 'chart-bar',
      pasos: [
        'Haz clic en "Ver Reportes de Mis Hijos" en el Dashboard',
        'O accede desde "Reportes" en el menú lateral',
        'Verás dos vistas: Grupal e Individual',
        'La vista grupal compara a todos tus hijos',
        'La vista individual muestra detalles de cada hijo',
        'Usa los botones superiores para cambiar entre vistas'
      ]
    },
    {
      titulo: 'Vista Grupal 👥',
      descripcion: 'Compara el rendimiento de tus hijos',
      icono: 'users',
      pasos: [
        'Muestra estadísticas combinadas de todos tus hijos',
        'Ve quién es el más activo',
        'Identifica quién tiene mejor rendimiento',
        'Revisa el rendimiento semanal conjunto',
        'Compara niveles, monedas y tareas completadas',
        'Útil para ver el panorama general familiar'
      ]
    },
    {
      titulo: 'Vista Individual 👤',
      descripcion: 'Detalles específicos de cada hijo',
      icono: 'user',
      pasos: [
        'Haz clic en el nombre de un hijo en los botones superiores',
        'Verás sus estadísticas personales detalladas',
        'Revisa su tasa de éxito (% de respuestas correctas)',
        'Observa el tiempo promedio que toma en las tareas',
        'Ve su última actividad registrada',
        'Identifica áreas donde necesita apoyo'
      ]
    },
    {
      titulo: 'Descargar Reportes en PDF 📄',
      descripcion: 'Guarda y comparte los reportes',
      icono: 'file-pdf',
      pasos: [
        'En la página de reportes, busca el botón "Descargar PDF"',
        'Haz clic para generar el reporte',
        'El sistema creará un PDF con toda la información visible',
        'Puedes descargar reportes grupales o individuales',
        'Útil para compartir con profesores o guardar registros',
        'El PDF incluye gráficos y estadísticas completas'
      ]
    },
    {
      titulo: 'Interpretando el Rendimiento 🎯',
      descripcion: 'Cómo usar la información',
      icono: 'bullseye',
      pasos: [
        'Tasa de éxito alta (>80%): Excelente comprensión',
        'Tasa de éxito media (60-80%): Buen progreso',
        'Tasa de éxito baja (<60%): Necesita apoyo adicional',
        'Racha alta: Buen hábito de estudio',
        'Racha baja o cero: Falta de constancia',
        'Usa estos datos para motivar y apoyar a tus hijos'
      ]
    },
    {
      titulo: 'Logros de Tus Hijos 🏆',
      descripcion: 'Celebra sus éxitos',
      icono: 'trophy',
      pasos: [
        'Ve a "Logros" en el menú lateral',
        'Verás los logros desbloqueados por cada hijo',
        'Los logros motivan a seguir aprendiendo',
        'Cada logro otorga monedas extra como recompensa',
        'Celebra cuando desbloqueen logros importantes',
        'Pregúntales sobre sus logros para mostrar interés'
      ]
    },
    {
      titulo: 'Consejos para Padres 💡',
      descripcion: 'Cómo apoyar el aprendizaje',
      icono: 'lightbulb',
      pasos: [
        '✅ Revisa el dashboard diariamente',
        '✅ Celebra los logros y el progreso',
        '✅ Motiva a mantener la racha de días',
        '✅ Si ves bajo rendimiento, ofrece ayuda',
        '✅ Comunícate con el profesor si es necesario',
        '✅ Establece horarios regulares de estudio',
        '✅ Usa las monedas como sistema de recompensas',
        '✅ Descarga reportes mensuales para seguimiento'
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
