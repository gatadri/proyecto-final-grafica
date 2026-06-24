import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';
import { AvatarStateService } from '../../../core/services/avatar-state.service';
import { AudioService, AudioType } from '../../../core/services/audio.service';
import { MLService } from '../../../services/ml.service';
import { PantallaDescansoComponent } from '../../../components/pantalla-descanso.component';

@Component({ selector: 'app-nino-tarea', standalone: true, imports: [CommonModule, RouterModule, PantallaDescansoComponent], templateUrl: './nino-tarea.component.html' })
export class NinoTareaComponent implements OnInit, OnDestroy {
  @ViewChild(PantallaDescansoComponent) pantallaDescanso!: PantallaDescansoComponent;
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
  erroresConsecutivos = 0;
  historialRespuestas: any[] = [];
  tiempoLimiteTimer: any;
  tabBlurCount = 0;
  idleMs = 0;
  erraticClicks = 0;
  lastActivityTime = Date.now();

  constructor(
    private route: ActivatedRoute, 
    private router: Router,
    private auth: AuthService,
    private api: ApiService, 
    private avatarState: AvatarStateService,
    private audioService: AudioService,
    private mlService: MLService
  ) {
    // Detectar cambios de tab/blur
    if (typeof window !== 'undefined') {
      window.addEventListener('blur', () => this.tabBlurCount++);
      window.addEventListener('mousemove', () => {
        this.lastActivityTime = Date.now();
      });
    }
  }

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
        this.iniciarTimerTiempoLimite();
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
    if (this.tiempoLimiteTimer) clearTimeout(this.tiempoLimiteTimer);
  }

  iniciarTimerTiempoLimite(): void {
    if (this.tiempoLimiteTimer) clearTimeout(this.tiempoLimiteTimer);
    this.tiempoLimiteTimer = setTimeout(() => {
      // Tardó más de 1 minuto - mostrar pantalla de descanso
      this.mostrarPantallaDescanso('Tiempo límite excedido (1 minuto)');
    }, 60000); // 1 minuto
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

    if (correcto) {
      this.cantidadAciertos++;
      this.erroresConsecutivos = 0;
    } else {
      this.cantidadErrores++;
      if (this.intentos >= 2) this.erroresConsecutivos++;
    }

    this.avatarState.setExpression(expresión);
    this.feedback = {
      correcto,
      mensaje: correcto
        ? `¡Correcto! +${puntos} puntos`
        : (this.intentos >= 2 ? `Incorrecto. La respuesta era: ${this.ejercicio.respuesta_correcta}` : 'Intenta de nuevo')
    };

    this.idleMs = Date.now() - this.lastActivityTime;

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

    // Analizar con ML
    this.mlService.analizarRespuesta({
      nino_id: this.nino.id,
      ejercicio_id: this.ejercicio.id,
      tiempo_ms: tiempoMs,
      correcto,
      tab_blur_count: this.tabBlurCount,
      idle_ms: this.idleMs,
      erratic_clicks: this.erraticClicks
    }).subscribe({
      next: (resultado) => {
        console.log('═══════════════════════════════════');
        console.log('📊 ANÁLISIS ML COMPLETADO');
        
        const dist = resultado.distraccion || {};
        const debug = resultado.debug || {};
        
        // Mostrar información de debug en consola
        if (debug.tiempo_actual_ms !== undefined) {
          console.log(`⏱️  Tiempo actual: ${debug.tiempo_actual_ms}ms`);
          
          if (resultado.tiempo_promedio_historico) {
            console.log(`📈 Promedio histórico: ${Math.round(resultado.tiempo_promedio_historico)}ms`);
            console.log(`⚠️  Triple del promedio: ${Math.round(debug.triple_promedio_ms)}ms`);
            console.log(`📚 Datos históricos: ${debug.cantidad_datos_historicos} ejercicios`);
            
            const margen = debug.triple_promedio_ms - debug.tiempo_actual_ms;
            if (margen > 0) {
              console.log(`✅ Normal (margen de ${Math.round(margen)}ms)`);
            } else {
              console.log(`🛑 TIEMPO EXCESIVO (excedió por ${Math.round(Math.abs(margen))}ms)`);
            }
          } else {
            console.log(`⚠️  Sin historial suficiente (usando detección básica)`);
          }
        }
        
        if (dist.requiere_descanso) {
          const motivo = dist.motivo || 'Distracción detectada';
          const detalles = dist.detalles || '';
          console.log('═══════════════════════════════════');
          console.log('🛑 PANTALLA DE DESCANSO ACTIVADA');
          console.log(`📋 Razón: ${motivo}`);
          console.log(`   Detalles: ${detalles}`);
          this.mostrarPantallaDescanso(`${motivo} - ${detalles}`);
        } else if (dist.focus_score !== undefined && dist.focus_score < 0.4) {
          console.log('⚠️ Focus score bajo detectado: ' + dist.focus_score);
          this.mostrarPantallaDescanso(`Focus score bajo (${dist.focus_score.toFixed(2)})`);
        } else {
          console.log('✅ Todo normal - sin distracción detectada');
        }
        
        console.log('═══════════════════════════════════');
      },
      error: err => console.error('Error analizando respuesta ML', err)
    });

    // Verificar 3 errores consecutivos
    if (this.erroresConsecutivos >= 3) {
      this.mostrarPantallaDescanso('3 errores consecutivos');
      this.erroresConsecutivos = 0;
    }

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
          this.iniciarTimerTiempoLimite();
          this.tabBlurCount = 0;
          this.erraticClicks = 0;
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
    } else {
      // Primer intento incorrecto - permitir segundo intento
      setTimeout(() => {
        this.feedback = null;
        this.respuestaSeleccionada = '';
      }, 1500);
    }
  }

  mostrarPantallaDescanso(razon: string): void {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🛑 PANTALLA DE DESCANSO ACTIVADA');
    console.log(`📋 Razón: ${razon}`);
    console.log(`👤 Niño: ${this.nino.nombre}`);
    console.log(`📝 Ejercicio: ${this.ejercicioActual + 1}/${this.ejercicios.length}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    if (this.pantallaDescanso) {
      this.pantallaDescanso.iniciarDescanso();
    }
  }
}
