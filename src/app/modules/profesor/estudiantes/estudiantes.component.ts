import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Nino } from '../../../core/models';

@Component({
  selector: 'app-estudiantes',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-users text-primary me-2"></i>Mis Estudiantes</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let e of estudiantes" class="col-md-6">
        <div class="card border-start border-primary border-3">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <h6 class="mb-1">{{ e.nombre }} {{ e.apellido }}</h6>
              <div class="d-flex gap-2">
                <span class="badge bg-warning">{{ e.monedas }} monedas</span>
                <span class="badge bg-info">Nivel {{ e.nivel }}</span>
                <span class="badge bg-success">{{ e.experiencia }} XP</span>
                <span class="badge bg-danger"><i class="fas fa-fire"></i> {{ e.racha_dias }}</span>
              </div>
            </div>
            <img [src]="'/images/avatares/' + e.avatar + '.png'" width="50" height="50" class="rounded-circle border">
          </div>
        </div>
      </div>
      <div *ngIf="estudiantes.length === 0" class="col-12 text-center py-4 text-muted">
        <i class="fas fa-users fa-3x mb-3"></i><p>No tienes estudiantes asignados</p>
      </div>
    </div>
  `
})
export class EstudiantesComponent implements OnInit {
  estudiantes: Nino[] = [];
  loading = true;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.get<{ estudiantes: Nino[] }>('profesor/estudiantes').subscribe({
      next: d => { this.estudiantes = d.estudiantes ?? (d as any); this.loading = false; },
      error: () => this.loading = false
    });
  }
}
