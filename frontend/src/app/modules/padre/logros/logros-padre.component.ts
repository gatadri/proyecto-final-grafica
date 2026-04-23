import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino } from '../../../core/models';

@Component({
  selector: 'app-logros-padre',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-trophy text-warning me-2"></i>Logros de mis Hijos</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading">
      <div *ngFor="let hijo of hijos" class="mb-4">
        <h6 class="fw-bold border-bottom pb-2"><i class="fas fa-child text-primary me-2"></i>{{ hijo.nombre }} {{ hijo.apellido }}</h6>
        <div class="row g-2">
          <div class="col-12 text-muted small">Próximamente: Sistema de logros</div>
        </div>
      </div>
    </div>
  `
})
export class LogrosPadreComponent implements OnInit {
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
