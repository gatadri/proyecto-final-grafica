import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';
import { AvatarStateService } from '../../../core/services/avatar-state.service';
import { AudioService, AudioType } from '../../../core/services/audio.service';

@Component({ selector: 'app-nino-tarea', standalone: true, imports: [CommonModule, RouterModule], templateUrl: './nino-tarea.component.html' })
export class NinoTareaComponent implements OnInit, OnDestroy {
  nino: any;
  tarea: any;
  ejercicios: any[] = [];
  ejercicioActual = 0;
  respuestaSeleccionada = '';
  feedback: { correcto: boolean; mensaje: string } | null = null;
  intentos = 0;
  puntosTotal       = 0;
  cantidadAciertos  = 0;
  cantidadErrores   = 0;
  tiempoTotalMs     = 0;
  tiempoTareaInicio = 0;
  completada = false;
  loading = true;
  ejercicioInicio = 0;
  logrosDesbloqueados: any[] = [];

  constructor(
    private route: ActivatedRoute, 
    private router: Router,
    private auth: AuthService,
    private api: ApiService, 
    private avatarState: AvatarStateService,
    private audioService: AudioService
  ) {}

  ngOnInit(): void {
    this.avatarState.resetExpression();
    this.nino = this.auth.getNino();
    
    // Reproducir audio de ejercicios automáticamente
    this.audioService.play(AudioType.EJERCICIOS);
    
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.api.get<any>(`nino/tareas/${id}?nino_id=${this.nino.id}`).subscribe({
      next: tarea => {
        this.tarea = tarea;
        this.ejercicios = this.tarea.ejercicios ?? [];
        this.ejercicioInicio  = Date.now();
        this.tiempoTareaInicio = Date.now();
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando tarea', err);
        this.router.navigate(['/nino/dashboard']);
      }
    });
  }

  ngOnDestroy(): void {
    // Pausar audio de ejercicios y volver al general
    this.audioService.pauseAndReturnToGeneral(AudioType.EJERCICIOS);
  }

  get ejercicio(): any { return this.ejercicios[this.ejercicioActual]; }
  get progreso(): number { return Math.round((this.ejercicioActual / this.ejercicios.length) * 100); }

  responder(): void {
    if (!this.respuestaSeleccionada || this.feedback) return;
    this.intentos++;
    const correcto = this.respuestaSeleccionada === this.ejercicio.respuesta_correcta;
    const puntos   = correcto ? (this.intentos === 1 ? 10 : 5) : 0;
    const expresión = correcto ? 'feliz' : (Math.random() > 0.5 ? 'enojado' : 'triste');
    const tiempoMs = Date.now() - this.ejercicioInicio;

    if (correcto) this.cantidadAciertos++;
    else          this.cantidadErrores++;

    this.avatarState.setExpression(expresión);
    this.feedback = {
      correcto,
      mensaje: correcto
        ? `¡Correcto! +${puntos} puntos`
        : (this.intentos >= 2 ? `Incorrecto. La respuesta era: ${this.ejercicio.respuesta_correcta}` : 'Intenta de nuevo')
    };

    this.api.post('nino/ejercicio-progreso', {
      student_id: this.nino.id,
      item_id: this.ejercicio.id,
      time_spent_ms: tiempoMs,
      attempts: this.intentos,
      correcto,
      fast_response: tiempoMs <= 10000,
      error_type: correcto ? '' : 'wrong_answer'
    }).subscribe({
      next: () => {},
      error: err => console.error('Error guardando progreso del ejercicio', err)
    });

    if (correcto || this.intentos >= 2) {
      this.puntosTotal += puntos;
      setTimeout(() => {
        this.feedback = null;
        this.respuestaSeleccionada = '';
        this.intentos = 0;
        this.ejercicioActual++;
        this.avatarState.resetExpression();
        if (this.ejercicioActual < this.ejercicios.length) {
          this.ejercicioInicio = Date.now();
        }
        if (this.ejercicioActual >= this.ejercicios.length) {
          this.completada    = true;
          this.tiempoTotalMs = Date.now() - this.tiempoTareaInicio;
          this.api.post('nino/completar-tarea', {
            nino_id:           this.nino.id,
            tarea_id:          this.tarea.id,
            puntos:            this.puntosTotal,
            cantidad_aciertos: this.cantidadAciertos,
            cantidad_errores:  this.cantidadErrores,
            tiempo_total_ms:   this.tiempoTotalMs
          }).subscribe({
            next: (res: any) => {
              this.nino.monedas = res.monedas;
              this.logrosDesbloqueados = res.logros || [];
              localStorage.setItem('nino', JSON.stringify(this.nino));
            },
            error: err => console.error('Error completando tarea', err)
          });
        }
      }, 1500);
    }
  }
}
