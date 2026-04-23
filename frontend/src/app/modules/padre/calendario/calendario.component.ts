import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino } from '../../../core/models';

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
            <div class="card border-start border-warning border-3">
              <div class="card-body py-2 d-flex justify-content-between align-items-center">
                <div>
                  <div class="fw-bold small">{{ t.titulo }}</div>
                  <small class="text-muted">{{ t.descripcion }}</small>
                </div>
                <div class="text-end">
                  <span class="badge bg-warning">Pendiente</span>
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
