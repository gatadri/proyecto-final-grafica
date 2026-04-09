import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AuthService } from '../../../core/services/auth.service';

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
          <div *ngFor="let l of hijo.logros" class="col-md-4 col-6">
            <div class="card text-center border-warning">
              <div class="card-body py-2">
                <i class="fas fa-{{ l.icono }} fa-2x mb-1"
                   [class.text-warning]="l.tipo==='oro'"
                   [class.text-secondary]="l.tipo==='plata'"
                   [class.text-danger]="l.tipo==='bronce'"></i>
                <div class="fw-bold small">{{ l.nombre }}</div>
                <small class="text-muted">{{ l.pivot?.fecha_obtenido }}</small>
              </div>
            </div>
          </div>
          <div *ngIf="hijo.logros.length === 0" class="col-12 text-muted small">Sin logros aún</div>
        </div>
      </div>
    </div>
  `
})
export class LogrosPadreComponent implements OnInit {
  hijos: any[] = [];
  loading = true;
  constructor(private mock: MockDataService, private auth: AuthService) {}
  ngOnInit(): void {
    const user = this.auth.getUser();
    const ninos = this.mock.getNinosByPadre(user?.id ?? 4);
    this.hijos = ninos.map((n: any) => ({ ...n, logros: this.mock.getLogrosNino(n.id) }));
    this.loading = false;
  }
}
