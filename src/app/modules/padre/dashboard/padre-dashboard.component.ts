import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-padre-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-tachometer-alt text-primary me-2"></i>Dashboard Padre</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let h of hijos" class="col-md-6">
        <div class="card border-start border-primary border-3">
          <div class="card-body">
            <h5 class="mb-2">{{ h.nombre }} {{ h.apellido }}</h5>
            <div class="d-flex gap-2 flex-wrap mb-2">
              <span class="badge bg-warning"><i class="fas fa-coins me-1"></i>{{ h.monedas }}</span>
              <span class="badge bg-info">Nivel {{ h.nivel }}</span>
              <span class="badge bg-success">{{ h.experiencia }} XP</span>
              <span class="badge bg-danger"><i class="fas fa-fire me-1"></i>{{ h.racha_dias }} días</span>
            </div>
            <div class="mb-1"><small class="text-muted">Tareas completadas: <strong>{{ h.tareas_completadas }}</strong></small></div>
            <div class="mb-1"><small class="text-muted">Logros obtenidos: <strong>{{ h.logros }}</strong></small></div>
            <div class="progress mt-2" style="height:6px">
              <div class="progress-bar bg-success" [style.width.%]="(h.experiencia % 100)"></div>
            </div>
            <small class="text-muted">XP para siguiente nivel: {{ h.experiencia % 100 }}/100</small>
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
  hijos: any[] = [];
  loading = true;
  constructor(private mock: MockDataService, private auth: AuthService) {}
  ngOnInit(): void {
    const user = this.auth.getUser();
    this.hijos = this.mock.getDashboardPadre(user?.id ?? 4);
    this.loading = false;
  }
}
