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
    <h5 class="fw-bold mb-4" style="color: #FF8C42;"><i class="fas fa-tachometer-alt me-2"></i>Dashboard Padre</h5>
    
    <div class="mb-4">
      <a routerLink="/padre/reportes" class="btn" style="background: #4A90E2; color: white; border: none; padding: 10px 20px; border-radius: 8px;">
        <i class="fas fa-chart-line me-2"></i>Ver Reportes de Mis Hijos
      </a>
    </div>
    
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border" style="color: #4A90E2;"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let h of hijos" class="col-md-6">
        <div class="card border-0" style="border-left: 4px solid #FF8C42 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.12); border-radius: 8px;">
          <div class="card-body">
            <h5 class="mb-2" style="color: #2E5C8A;">{{ h.nombre }} {{ h.apellido }}</h5>
            <div *ngIf="h.profesor" class="mb-2">
              <small class="text-muted"><i class="fas fa-chalkboard-teacher me-1" style="color: #4A90E2;"></i>Profesor: <strong>{{ h.profesor.nombre }} {{ h.profesor.apellido }}</strong></small>
            </div>
            <div class="d-flex gap-2 flex-wrap mb-2">
              <span class="badge" style="background-color: #FFA726; color: white;"><i class="fas fa-coins me-1"></i>{{ h.estadisticas.monedas }}</span>
              <span class="badge" style="background-color: #4A90E2; color: white;">Nivel {{ h.estadisticas.nivel }}</span>
              <span class="badge" style="background-color: #4CAF50; color: white;">{{ h.estadisticas.experiencia }} XP</span>
              <span class="badge" style="background-color: #FF8C42; color: white;"><i class="fas fa-fire me-1"></i>{{ h.estadisticas.racha_dias }} días</span>
            </div>
            <div class="mb-1"><small class="text-muted">Tareas asignadas: <strong>{{ h.tareas.length || 0 }}</strong></small></div>
            <div class="mb-1"><small class="text-muted">Logros obtenidos: <strong>Próximamente</strong></small></div>
            <div class="progress mt-2" style="height:8px; background-color: #E8F4F8;">
              <div class="progress-bar" style="background: #4CAF50;" [style.width.%]="(h.estadisticas.experiencia % 100)"></div>
            </div>
            <small class="text-muted">XP para siguiente nivel: {{ h.estadisticas.experiencia % 100 }}/100</small>
          </div>
        </div>
      </div>
      <div *ngIf="hijos.length === 0" class="col-12 text-center py-4 text-muted">
        <i class="fas fa-child fa-3x mb-3" style="color: #4A90E2;"></i><p>No tienes hijos registrados</p>
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
