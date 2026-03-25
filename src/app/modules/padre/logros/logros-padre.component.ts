import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Logro } from '../../../core/models';

@Component({
  selector: 'app-logros-padre',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-trophy text-warning me-2"></i>Logros de mis Hijos</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let l of logros" class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="fas fa-{{ l.icono ?? 'medal' }} fa-2x mb-2"
               [class.text-warning]="l.tipo==='oro'"
               [class.text-secondary]="l.tipo==='plata'"
               [class.text-danger]="l.tipo==='bronce'"></i>
            <h6>{{ l.nombre }}</h6>
            <small class="text-muted">{{ l.descripcion }}</small>
          </div>
        </div>
      </div>
    </div>
  `
})
export class LogrosPadreComponent implements OnInit {
  logros: Logro[] = [];
  loading = true;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.get<any>('padre/logros').subscribe({
      next: d => { this.logros = d.logros ?? d; this.loading = false; },
      error: () => this.loading = false
    });
  }
}
