import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

interface TemaProblematico {
  tema: string;
  tema_legible: string;
  errores: number;
  aciertos: number;
  porcentaje_error: number;
  tiempo_promedio_ms: number;
  tarea_id: number;
  tarea_titulo: string;
}

interface ReportePorSubtema {
  subtema: string;
  total_errores: number;
  total_aciertos: number;
  temas_problematicos: TemaProblematico[];
  tiempo_promedio_ms: number;
}

interface Reporte {
  nino: {
    id: number;
    nombre: string;
    apellido: string;
    edad: number;
    grado: number;
  };
  padre: {
    email: string;
    nombre: string;
  } | null;
  profesor: {
    email: string;
    nombre: string;
  } | null;
  reporte_por_subtema: ReportePorSubtema[];
  resumen: {
    total_errores: number;
    total_aciertos: number;
    subtemas_con_dificultad: number;
  };
}

@Component({
  selector: 'app-reporte-detallado',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container py-5">
      <div class="card shadow-lg">
        <div class="card-header bg-primary text-white">
          <h3 class="mb-0">
            <i class="fas fa-chart-bar me-2"></i>
            Reporte Detallado de Errores
          </h3>
        </div>
        
        <div class="card-body" *ngIf="reporte">
          <!-- Info del niño -->
          <div class="alert alert-info mb-4">
            <h5>
              <i class="fas fa-user me-2"></i>
              {{ reporte.nino.nombre }} {{ reporte.nino.apellido }}
            </h5>
            <p class="mb-0">
              <strong>Edad:</strong> {{ reporte.nino.edad }} años | 
              <strong>Grado:</strong> {{ reporte.nino.grado }}°
            </p>
          </div>

          <!-- Resumen general -->
          <div class="row mb-4">
            <div class="col-md-4">
              <div class="card bg-danger text-white">
                <div class="card-body text-center">
                  <h2 class="mb-0">{{ reporte.resumen.total_errores }}</h2>
                  <p class="mb-0">Total Errores</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-success text-white">
                <div class="card-body text-center">
                  <h2 class="mb-0">{{ reporte.resumen.total_aciertos }}</h2>
                  <p class="mb-0">Total Aciertos</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-warning text-white">
                <div class="card-body text-center">
                  <h2 class="mb-0">{{ reporte.resumen.subtemas_con_dificultad }}</h2>
                  <p class="mb-0">Áreas con Dificultad</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Reporte por subtema -->
          <h5 class="mb-3">
            <i class="fas fa-list me-2"></i>
            Análisis Detallado por Área
          </h5>

          <div *ngFor="let subtema of reporte.reporte_por_subtema" class="mb-4">
            <div class="card">
              <div class="card-header" [class.bg-danger]="subtema.total_errores >= 5"
                   [class.bg-warning]="subtema.total_errores >= 3 && subtema.total_errores < 5"
                   [class.bg-info]="subtema.total_errores < 3"
                   [class.text-white]="subtema.total_errores >= 3">
                <h6 class="mb-0">
                  <i class="fas fa-calculator me-2"></i>
                  {{ subtema.subtema | titlecase }}
                  <span class="badge bg-light text-dark ms-2">
                    {{ subtema.total_errores }} errores / {{ subtema.total_aciertos }} aciertos
                  </span>
                </h6>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Tema Específico</th>
                        <th class="text-center">Errores</th>
                        <th class="text-center">Aciertos</th>
                        <th class="text-center">% Error</th>
                        <th class="text-center">Tiempo Promedio</th>
                        <th>Tarea</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr *ngFor="let tema of subtema.temas_problematicos">
                        <td>
                          <i class="fas fa-exclamation-triangle text-warning me-2"></i>
                          <strong>{{ tema.tema_legible }}</strong>
                        </td>
                        <td class="text-center">
                          <span class="badge bg-danger">{{ tema.errores }}</span>
                        </td>
                        <td class="text-center">
                          <span class="badge bg-success">{{ tema.aciertos }}</span>
                        </td>
                        <td class="text-center">
                          <div class="progress" style="height: 20px; min-width: 80px;">
                            <div class="progress-bar bg-danger" 
                                 [style.width.%]="tema.porcentaje_error">
                              {{ tema.porcentaje_error }}%
                            </div>
                          </div>
                        </td>
                        <td class="text-center">
                          {{ formatTiempo(tema.tiempo_promedio_ms) }}
                        </td>
                        <td>
                          <small class="text-muted">{{ tema.tarea_titulo }}</small>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Recomendaciones -->
          <div class="alert alert-success" *ngIf="reporte.reporte_por_subtema.length > 0">
            <h6>
              <i class="fas fa-lightbulb me-2"></i>
              Recomendaciones
            </h6>
            <ul class="mb-0">
              <li *ngFor="let rec of getRecomendaciones()">{{ rec }}</li>
            </ul>
          </div>

          <!-- Contacto -->
          <div class="row mt-4" *ngIf="reporte.padre || reporte.profesor">
            <div class="col-md-6" *ngIf="reporte.padre">
              <div class="card">
                <div class="card-body">
                  <h6><i class="fas fa-user-friends me-2"></i>Padre/Tutor</h6>
                  <p class="mb-0">{{ reporte.padre.nombre }}</p>
                  <small class="text-muted">{{ reporte.padre.email }}</small>
                </div>
              </div>
            </div>
            <div class="col-md-6" *ngIf="reporte.profesor">
              <div class="card">
                <div class="card-body">
                  <h6><i class="fas fa-chalkboard-teacher me-2"></i>Profesor</h6>
                  <p class="mb-0">{{ reporte.profesor.nombre }}</p>
                  <small class="text-muted">{{ reporte.profesor.email }}</small>
                </div>
              </div>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="d-flex gap-2 mt-4">
            <button class="btn btn-primary" (click)="enviarReporte()">
              <i class="fas fa-envelope me-2"></i>
              Enviar Reporte por Email
            </button>
            <button class="btn btn-secondary" (click)="imprimirReporte()">
              <i class="fas fa-print me-2"></i>
              Imprimir
            </button>
          </div>
        </div>

        <div class="card-body text-center py-5" *ngIf="loading">
          <div class="spinner-border text-primary mb-3"></div>
          <p>Cargando reporte...</p>
        </div>

        <div class="card-body" *ngIf="!loading && !reporte">
          <div class="alert alert-warning">
            <i class="fas fa-info-circle me-2"></i>
            No hay datos disponibles para este estudiante.
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .progress {
      background-color: #e9ecef;
    }
    .card-header h6 {
      font-weight: bold;
    }
    .table td {
      vertical-align: middle;
    }
  `]
})
export class ReporteDetalladoComponent implements OnInit {
  reporte: Reporte | null = null;
  loading = true;
  ninoId: number = 0;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.ninoId = Number(this.route.snapshot.paramMap.get('ninoId'));
    if (this.ninoId) {
      this.cargarReporte();
    }
  }

  cargarReporte(): void {
    this.http.get<Reporte>(`http://localhost:8000/api/tareas/ml/reporte-detallado?nino_id=${this.ninoId}`)
      .subscribe({
        next: (data) => {
          this.reporte = data;
          this.loading = false;
        },
        error: (err) => {
          console.error('Error cargando reporte', err);
          this.loading = false;
        }
      });
  }

  formatTiempo(ms: number): string {
    const segundos = Math.round(ms / 1000);
    if (segundos < 60) return `${segundos}s`;
    const minutos = Math.floor(segundos / 60);
    const segs = segundos % 60;
    return `${minutos}m ${segs}s`;
  }

  getRecomendaciones(): string[] {
    if (!this.reporte) return [];
    
    const recs: string[] = [];
    
    for (const subtema of this.reporte.reporte_por_subtema) {
      if (subtema.total_errores >= 5) {
        const temasTop = subtema.temas_problematicos
          .slice(0, 2)
          .map(t => t.tema_legible)
          .join(' y ');
        
        recs.push(`Reforzar ${subtema.subtema}: especialmente ${temasTop}.`);
      }
    }
    
    if (recs.length === 0) {
      recs.push('Continuar practicando regularmente para mantener el nivel.');
    }
    
    return recs;
  }

  enviarReporte(): void {
    if (!this.reporte) return;
    
    this.http.post('http://localhost:8000/api/tareas/ml/notificar', {
      nino_id: this.reporte.nino.id
    }).subscribe({
      next: () => {
        alert('Reporte enviado por email exitosamente');
      },
      error: (err) => {
        console.error('Error enviando reporte', err);
        alert('Error al enviar el reporte');
      }
    });
  }

  imprimirReporte(): void {
    window.print();
  }
}
