import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatCardComponent } from '../../../shared/components/stat-card/stat-card.component';
import { ApiService } from '../../../core/services/api.service';
import { Nino } from '../../../core/models';

@Component({ selector: 'app-profesor-dashboard', standalone: true, imports: [CommonModule, StatCardComponent], templateUrl: './profesor-dashboard.component.html' })
export class ProfesorDashboardComponent implements OnInit {
  estudiantes: Nino[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.get<{ estudiantes: Nino[] }>('dashboard/profesor').subscribe({
      next: data => { this.estudiantes = data.estudiantes; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  get promedioXP(): number {
    if (!this.estudiantes.length) return 0;
    return Math.round(this.estudiantes.reduce((s, e) => s + e.experiencia, 0) / this.estudiantes.length);
  }

  get totalMonedas(): number {
    return this.estudiantes.reduce((s, e) => s + e.monedas, 0);
  }

  get rachaMax(): number {
    return this.estudiantes.reduce((max, e) => Math.max(max, e.racha_dias), 0);
  }
}
