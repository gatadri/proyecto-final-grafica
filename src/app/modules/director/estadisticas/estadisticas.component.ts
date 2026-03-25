import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-estadisticas',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-chart-line text-primary me-2"></i>Estadísticas del Sistema</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="card"><div class="card-body">
      <pre>{{ data | json }}</pre>
    </div></div>
  `
})
export class EstadisticasComponent implements OnInit {
  data: any = {};
  loading = true;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.get<any>('estadisticas').subscribe({ next: d => { this.data = d; this.loading = false; }, error: () => this.loading = false });
  }
}
