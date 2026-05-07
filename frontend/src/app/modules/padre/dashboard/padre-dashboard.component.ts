import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino } from '../../../core/models';

@Component({
  selector: 'app-padre-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-tachometer-alt text-primary me-2"></i>Dashboard Padre</h5>
    
    <div class="mb-4">
      <a routerLink="/padre/reportes" class="btn btn-primary">
        <i class="fas fa-chart-line me-2"></i>Ver Reportes de Mis Hijos
      </a>
    </div>
    
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let h of hijos" class="col-md-6">
        <div class="card border-start border-primary border-3">
          <div class="card-body">
            <h5 class="mb-2">{{ h.nombre }} {{ h.apellido }}</h5>
            <div class="d-flex gap-2 flex-wrap mb-2">
              <span class="badge bg-warning"><i class="fas fa-coins me-1"></i>{{ h.estadisticas.monedas }}</span>
              <span class="badge bg-info">Nivel {{ h.estadisticas.nivel }}</span>
              <span class="badge bg-success">{{ h.estadisticas.experiencia }} XP</span>
              <span class="badge bg-danger"><i class="fas fa-fire me-1"></i>{{ h.estadisticas.racha_dias }} días</span>
            </div>
            <div class="mb-1"><small class="text-muted">Tareas asignadas: <strong>{{ h.tareas.length || 0 }}</strong></small></div>
            <div class="mb-1"><small class="text-muted">Logros obtenidos: <strong>Próximamente</strong></small></div>
            <div class="progress mt-2" style="height:6px">
              <div class="progress-bar bg-success" [style.width.%]="(h.estadisticas.experiencia % 100)"></div>
            </div>
            <small class="text-muted">XP para siguiente nivel: {{ h.estadisticas.experiencia % 100 }}/100</small>
          </div>
        </div>
      </div>
      <div *ngIf="hijos.length === 0" class="col-12 text-center py-4 text-muted">
        <i class="fas fa-child fa-3x mb-3"></i><p>No tienes hijos registrados</p>
      </div>
    </div>
  `
})
export class PadreDashboardComponent implements OnInit {
  hijos: Nino[] = [];
  loading = true;
  constructor(private api: ApiService, private auth: AuthService) {}
  ngOnInit(): void {
    const user = this.auth.getUser();
    if (user) {
      this.api.get<Nino[]>('usuarios/' + user.id + '/hijos').subscribe({
        next: data => { this.hijos = data; this.loading = false; },
        error: () => this.loading = false
      });
    } else {
      this.loading = false;
    }
  }
}
