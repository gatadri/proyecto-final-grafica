import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-history text-primary me-2"></i>Log de Actividades</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="card"><div class="card-body">
      <div *ngFor="let log of logs" class="border-bottom py-2">
        <small class="text-muted">{{ log.created_at }}</small>
        <p class="mb-0">{{ log.descripcion ?? log.message ?? (log | json) }}</p>
      </div>
    </div></div>
  `
})
export class LogsComponent implements OnInit {
  logs: any[] = [];
  loading = true;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.get<any>('logs').subscribe({ next: d => { this.logs = d.logs ?? d; this.loading = false; }, error: () => this.loading = false });
  }
}
