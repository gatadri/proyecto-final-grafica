import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, transition, style, animate, state } from '@angular/animations';
import { AudioService, AudioType } from '../../../core/services/audio.service';

interface TutorialStep {
  titulo: string;
  descripcion: string;
  icono: string;
  imagen?: string;
  pasos?: string[];
  demo?: string;
  color?: string;
}

@Component({
  selector: 'app-nino-tutorial',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nino-tutorial.component.html',
  styleUrls: ['./nino-tutorial.component.css'],
  animations: [
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('500ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('500ms ease-in', style({ transform: 'translateX(-100%)', opacity: 0 }))
      ])
    ]),
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.9)' }),
        animate('400ms ease-out', style({ opacity: 1, transform: 'scale(1)' }))
      ])
    ]),
    trigger('bounce', [
      state('normal', style({ transform: 'scale(1)' })),
      state('bounced', style({ transform: 'scale(1.1)' })),
      transition('normal <=> bounced', animate('300ms ease-in-out'))
    ])
  ]
})
export class NinoTutorialComponent {
  pasoActual = 0;
  animacionEstado = 'normal';
  mostrarConfeti = false;

  constructor(public audioService: AudioService) {}
  
  tutoriales: TutorialStep[] = [
    {
      titulo: '¡Bienvenido! 🎉',
      descripcion: 'Aprende a usar el sistema educativo paso a paso',
      icono: 'hand-wave',
      color: '#6366f1',
      demo: 'bienvenida',
      pasos: [
        'Este tutorial te enseñará todo lo que necesitas saber',
        'Usa las flechas para navegar entre los pasos',
        '¡Vamos a empezar!'
      ]
    },
    {
      titulo: 'Dashboard - Tu Inicio 🏠',
      descripcion: 'Aquí verás tu progreso y estadísticas',
      icono: 'tachometer-alt',
      color: '#10b981',
      demo: 'dashboard',
      pasos: [
        'En el Dashboard puedes ver tus monedas 🪙',
        'También verás tu nivel y experiencia ⭐',
        'Mira tu racha de días consecutivos 🔥',
        'Revisa cuántas tareas tienes pendientes 📚'
      ]
    },
    {
      titulo: 'Mis Tareas 📝',
      descripcion: 'Completa tareas asignadas por tu profesor',
      icono: 'tasks',
      color: '#f59e0b',
      demo: 'tareas',
      pasos: [
        'Haz clic en "Mis Tareas" en el menú lateral',
        'Verás todas las tareas que tu profesor te asignó',
        'Haz clic en una tarea para empezar',
        'Responde las preguntas correctamente',
        'Al terminar, ganarás monedas y experiencia 🎁'
      ]
    },
    {
      titulo: 'Modo Práctica 🎯',
      descripcion: 'Practica con ejercicios aleatorios',
      icono: 'dumbbell',
      color: '#8b5cf6',
      demo: 'practica',
      pasos: [
        'Haz clic en "Práctica" en el menú',
        'Elige el tipo de ejercicio que quieres practicar',
        'Responde las preguntas',
        'No hay límite, ¡practica todo lo que quieras!',
        'También ganas monedas practicando 💰'
      ]
    },
    {
      titulo: 'Tienda 🛒',
      descripcion: 'Compra skins y stickers con tus monedas',
      icono: 'store',
      color: '#ec4899',
      demo: 'tienda',
      pasos: [
        'Ve a la "Tienda" en el menú',
        'Verás skins (avatares) y stickers disponibles',
        'Usa tus monedas para comprar lo que te guste',
        'Las skins cambian tu avatar 👤',
        'Los stickers los puedes descargar e imprimir 🖨️'
      ]
    },
    {
      titulo: 'Logros 🏆',
      descripcion: 'Desbloquea logros completando objetivos',
      icono: 'trophy',
      color: '#eab308',
      demo: 'logros',
      pasos: [
        'Haz clic en "Logros" en el menú',
        'Verás todos los logros disponibles',
        'Los logros desbloqueados aparecen en color',
        'Cada logro te da monedas extra como recompensa',
        'Completa tareas y mantén tu racha para desbloquear más'
      ]
    },
    {
      titulo: 'Consejos Finales 💡',
      descripcion: 'Tips para aprovechar al máximo el sistema',
      icono: 'lightbulb',
      color: '#06b6d4',
      demo: 'consejos',
      pasos: [
        '✅ Completa tus tareas todos los días para mantener tu racha',
        '✅ Practica regularmente para mejorar tus habilidades',
        '✅ Ahorra monedas para comprar las mejores skins',
        '✅ Intenta desbloquear todos los logros',
        '✅ ¡Diviértete aprendiendo! 🎉'
      ]
    }
  ];

  get tutorialActual(): TutorialStep {
    return this.tutoriales[this.pasoActual];
  }

  siguiente(): void {
    if (this.pasoActual < this.tutoriales.length - 1) {
      this.pasoActual++;
      this.animarIcono();
      if (this.pasoActual === this.tutoriales.length - 1) {
        this.mostrarConfeti = true;
        setTimeout(() => this.mostrarConfeti = false, 3000);
      }
    }
  }

  anterior(): void {
    if (this.pasoActual > 0) {
      this.pasoActual--;
      this.animarIcono();
    }
  }

  irAPaso(index: number): void {
    this.pasoActual = index;
    this.animarIcono();
  }

  animarIcono(): void {
    this.animacionEstado = 'bounced';
    setTimeout(() => this.animacionEstado = 'normal', 300);
  }

  toggleAudioTutorial(): void {
    this.audioService.toggle(AudioType.TUTORIALES);
  }

  get isAudioPlaying(): boolean {
    return this.audioService.isPlaying(AudioType.TUTORIALES);
  }

  ngOnInit(): void {
    // Reproducir audio si estaba activado
    if (this.audioService.isEnabled(AudioType.TUTORIALES)) {
      this.audioService.play(AudioType.TUTORIALES);
    }
  }

  ngOnDestroy(): void {
    // Pausar audio de tutoriales y volver al general
    this.audioService.pauseAndReturnToGeneral(AudioType.TUTORIALES);
  }

  get progreso(): number {
    return ((this.pasoActual + 1) / this.tutoriales.length) * 100;
  }
}
