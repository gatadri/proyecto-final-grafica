import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Nino } from '../../../core/models';

@Component({
  selector: 'app-padre-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-tachometer-alt text-primary me-2"></i>Dashboard Padre</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let h of hijos" class="col-md-6">
        <div class="card">
          <div class="card-body d-flex align-items-center gap-3">
            <img [src]="'/images/avatares/' + h.avatar + '.png'" width="60" height="60" class="rounded-circle border">
            <div>
              <h5 class="mb-1">{{ h.nombre }} {{ h.apellido }}</h5>
              <div class="d-flex gap-2 flex-wrap">
                <span class="badge bg-warning"><i class="fas fa-coins"></i> {{ h.monedas }}</span>
                <span class="badge bg-info">Nivel {{ h.nivel }}</span>
                <span class="badge bg-success">{{ h.experiencia }} XP</span>
                <span class="badge bg-danger"><i class="fas fa-fire"></i> {{ h.racha_dias }} días</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class PadreDashboardComponent implements OnInit {
  hijos: Nino[] = [];
  loading = true;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.get<{ hijos: Nino[] }>('dashboard/padre').subscribe({
      next: d => { this.hijos = d.hijos; this.loading = false; },
      error: () => this.loading = false
    });
  }
}
