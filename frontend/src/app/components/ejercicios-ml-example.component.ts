import { Component, ViewChild, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MLService } from '../services/ml.service';
import { PantallaDescansoComponent } from './pantalla-descanso.component';

@Component({
  selector: 'app-ejercicios-ml',
  standalone: true,
  imports: [CommonModule, PantallaDescansoComponent],
  template: `
    <app-pantalla-descanso></app-pantalla-descanso>

    <div class="ejercicios-container" *ngIf="!descansando">
      <div class="ejercicio-actual" *ngIf="ejercicioActual">
        <h2>{{ ejercicioActual.pregunta }}</h2>
        
        <div class="opciones">
          <button *ngFor="let opcion of ejercicioActual.opciones" 
                  (click)="responder(opcion)"
                  class="btn-opcion">
            {{ opcion }}
          </button>
        </div>

        <div class="info-debug" *ngIf="debugMode">
          <p>Tiempo: {{ tiempoActual }}ms</p>
          <p>Tabs blur: {{ tabBlurCount }}</p>
          <p>Idle: {{ idleMs }}ms</p>
          <p>Clicks erráticos: {{ erraticClicks }}</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .ejercicios-container {
      padding: 20px;
      max-width: 800px;
      margin: 0 auto;
    }
    .ejercicio-actual {
      background: white;
      border-radius: 12px;
      padding: 30px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h2 {
      font-size: 24px;
      margin-bottom: 30px;
      color: #333;
    }
    .opciones {
      display: grid;
      gap: 15px;
    }
    .btn-opcion {
      padding: 15px;
      font-size: 18px;
      border: 2px solid #667eea;
      background: white;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s;
    }
    .btn-opcion:hover {
      background: #667eea;
      color: white;
      transform: translateY(-2px);
    }
    .info-debug {
      margin-top: 20px;
      padding: 15px;
      background: #f5f5f5;
      border-radius: 8px;
      font-size: 12px;
    }
  `]
})
export class EjerciciosMLComponent implements OnInit, OnDestroy {
  @ViewChild(PantallaDescansoComponent) pantallaDescanso!: PantallaDescansoComponent;

  ejercicioActual: any = null;
  ninoId = 1; // Cambiar por el ID real
  descansando = false;
  debugMode = true;

  // Métricas de seguimiento
  tiempoInicio = 0;
  tiempoActual = 0;
  tabBlurCount = 0;
  idleMs = 0;
  erraticClicks = 0;
  lastActivity = Date.now();

  private intervalTimer: any;
  private idleTimer: any;

  constructor(private mlService: MLService) {}

  ngOnInit() {
    this.cargarEjercicio();
    this.iniciarMonitoreo();
  }

  ngOnDestroy() {
    if (this.intervalTimer) clearInterval(this.intervalTimer);
    if (this.idleTimer) clearInterval(this.idleTimer);
    this.removerListeners();
  }

  cargarEjercicio() {
    // Simulación - reemplazar con tu lógica
    this.ejercicioActual = {
      id: 1,
      pregunta: '¿Cuánto es 2 + 2?',
      opciones: ['3', '4', '5', '6'],
      respuesta_correcta: '4'
    };
    this.tiempoInicio = Date.now();
  }

  iniciarMonitoreo() {
    // Monitorear tiempo
    this.intervalTimer = setInterval(() => {
      this.tiempoActual = Date.now() - this.tiempoInicio;
    }, 100);

    // Monitorear idle
    this.idleTimer = setInterval(() => {
      const ahora = Date.now();
      this.idleMs = ahora - this.lastActivity;
    }, 500);

    // Listeners de actividad
    document.addEventListener('click', this.onActivity);
    document.addEventListener('keypress', this.onActivity);
    document.addEventListener('mousemove', this.onActivity);
    document.addEventListener('visibilitychange', this.onVisibilityChange);

    // Detectar clicks erráticos
    document.addEventListener('click', this.onDocumentClick);
  }

  onActivity = () => {
    this.lastActivity = Date.now();
    this.idleMs = 0;
  }

  onVisibilityChange = () => {
    if (document.hidden) {
      this.tabBlurCount++;
    }
  }

  onDocumentClick = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    // Si el click no es en un botón/input, es errático
    if (!target.closest('button, input, a, [role="button"]')) {
      this.erraticClicks++;
    }
  }

  removerListeners() {
    document.removeEventListener('click', this.onActivity);
    document.removeEventListener('keypress', this.onActivity);
    document.removeEventListener('mousemove', this.onActivity);
    document.removeEventListener('visibilitychange', this.onVisibilityChange);
    document.removeEventListener('click', this.onDocumentClick);
  }

  responder(opcion: string) {
    const correcto = opcion === this.ejercicioActual.respuesta_correcta;
    const tiempoRespuesta = Date.now() - this.tiempoInicio;

    // Preparar datos para ML
    const datos = {
      nino_id: this.ninoId,
      ejercicio_id: this.ejercicioActual.id,
      tiempo_ms: tiempoRespuesta,
      correcto: correcto,
      tab_blur_count: this.tabBlurCount,
      idle_ms: this.idleMs,
      erratic_clicks: this.erraticClicks
    };

    // Analizar con ML
    this.mlService.analizarRespuesta(datos).subscribe(
      result => {
        console.log('Análisis ML:', result);

        // Si requiere descanso
        if (result.distraccion?.requiere_descanso) {
          this.descansando = true;
          this.pantallaDescanso.iniciarDescanso();
          
          // Esperar 10 segundos antes de continuar
          setTimeout(() => {
            this.descansando = false;
            this.resetearMetricas();
            this.cargarEjercicio();
          }, 10500);
        } else {
          // Continuar normalmente
          this.resetearMetricas();
          this.cargarEjercicio();
        }

        // Si hay predicción de error
        if (result.prediccion && !correcto) {
          console.log('Tipo de error detectado:', result.prediccion.error_type);
          // Aquí puedes mostrar feedback específico
        }
      },
      error => {
        console.error('Error al analizar:', error);
        // Continuar sin análisis
        this.resetearMetricas();
        this.cargarEjercicio();
      }
    );
  }

  resetearMetricas() {
    this.tabBlurCount = 0;
    this.idleMs = 0;
    this.erraticClicks = 0;
    this.tiempoActual = 0;
    this.lastActivity = Date.now();
  }
}
