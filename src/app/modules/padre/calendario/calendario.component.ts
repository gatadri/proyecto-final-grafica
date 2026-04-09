import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-calendario',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-calendar text-primary me-2"></i>Calendario de Tareas</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading">
      <div *ngFor="let hijo of hijos" class="mb-4">
        <h6 class="fw-bold border-bottom pb-2"><i class="fas fa-child text-primary me-2"></i>{{ hijo.nombre }} {{ hijo.apellido }}</h6>
        <div class="row g-2">
          <div *ngFor="let t of hijo.tareas" class="col-md-6">
            <div class="card border-start border-3" [class.border-success]="t.completada" [class.border-warning]="!t.completada">
              <div class="card-body py-2 d-flex justify-content-between align-items-center">
                <div>
                  <div class="fw-bold small">{{ t.titulo }}</div>
                  <small class="text-muted">{{ t.tipo_ejercicio }} · {{ t.ejercicios?.length ?? 0 }} ejercicios</small>
                </div>
                <div class="text-end">
                  <span class="badge" [class.bg-success]="t.completada" [class.bg-warning]="!t.completada">
                    {{ t.completada ? 'Completada' : 'Pendiente' }}
                  </span>
                  <div *ngIf="t.puntuacion" class="small text-muted mt-1">{{ t.puntuacion }} pts</div>
                </div>
              </div>
            </div>
          </div>
          <div *ngIf="hijo.tareas.length === 0" class="col-12 text-muted small">Sin tareas asignadas</div>
        </div>
      </div>
    </div>
  `
})
export class CalendarioComponent implements OnInit {
  hijos: any[] = [];
  loading = true;
  constructor(private mock: MockDataService, private auth: AuthService) {}
  ngOnInit(): void {
    const user  = this.auth.getUser();
    const ninos = this.mock.getNinosByPadre(user?.id ?? 4);
    this.hijos  = ninos.map((n: any) => {
      const tareas   = this.mock.getTareasByNino(n.id);
      const progreso = this.mock.getProgresoNino(n.id);
      return {
        ...n,
        tareas: tareas.map((t: any) => {
          const p = progreso.find((p: any) => p.tarea_id === t.id);
          return { ...t, completada: p?.completada ?? false, puntuacion: p?.puntuacion ?? 0 };
        })
      };
    });
    this.loading = false;
  }
}
