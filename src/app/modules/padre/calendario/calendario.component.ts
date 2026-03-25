import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-calendario',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-calendar text-primary me-2"></i>Calendario de Tareas</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="card"><div class="card-body">
      <div *ngFor="let item of data" class="border-bottom py-2">
        <strong>{{ item.titulo }}</strong>
        <span class="badge ms-2" [class.bg-success]="item.completada" [class.bg-warning]="!item.completada">
          {{ item.completada ? 'Completada' : 'Pendiente' }}
        </span>
      </div>
      <p *ngIf="data.length === 0" class="text-muted text-center py-3">Sin tareas registradas</p>
    </div></div>
  `
})
export class CalendarioComponent implements OnInit {
  data: any[] = [];
  loading = true;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.get<any>('padre/calendario').subscribe({
      next: d => { this.data = d.tareas ?? d; this.loading = false; },
      error: () => this.loading = false
    });
  }
}
