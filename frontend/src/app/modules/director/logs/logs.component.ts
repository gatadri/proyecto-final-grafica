import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';

interface Log {
  fecha: string;
  usuario: string;
  descripcion: string;
  tipo: string;
}

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-history text-primary me-2"></i>Log de Actividades</h5>
    
    <div *ngIf="loading" class="text-center py-5">
      <div class="spinner-border" style="color: #4A90E2;"></div>
      <p class="mt-3">Cargando historial...</p>
    </div>

    <div *ngIf="!loading" class="card">
      <div class="card-body p-0">
        <div *ngIf="logs.length === 0" class="text-center py-5 text-muted">
          <i class="fas fa-history fa-3x mb-3"></i>
          <p>No hay actividades registradas</p>
        </div>
        <div *ngIf="logs.length > 0" class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Fecha</th>
                <th>Usuario</th>
                <th>Actividad</th>
                <th>Tipo</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let log of logs">
                <td><small class="text-muted">{{ log.fecha }}</small></td>
                <td><strong>{{ log.usuario }}</strong></td>
                <td>{{ log.descripcion }}</td>
                <td>
                  <span class="badge" 
                    [class.bg-success]="log.tipo==='tarea'" 
                    [class.bg-info]="log.tipo==='practica'"
                    [class.bg-warning]="log.tipo==='logro'" 
                    [class.bg-secondary]="log.tipo==='sistema'">
                    {{ log.tipo | titlecase }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `
})
export class LogsComponent implements OnInit {
  logs: Log[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(): void {
    this.loading = true;
    this.api.get<Log[]>('director/logs').subscribe({
      next: data => {
        this.logs = data;
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando logs:', err);
        this.loading = false;
      }
    });
  }
}
