import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatCardComponent } from '../../../shared/components/stat-card/stat-card.component';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-profesor-dashboard',
  standalone: true,
  imports: [CommonModule, StatCardComponent],
  templateUrl: './profesor-dashboard.component.html'
})
export class ProfesorDashboardComponent implements OnInit {
  estudiantes: any[] = [];
  loading = true;
  constructor(private mock: MockDataService, private auth: AuthService) {}
  ngOnInit(): void {
    const user = this.auth.getUser();
    const profId = Number(user?.id ?? 2);
    this.estudiantes = this.mock.getDashboardProfesor(profId);
    this.loading = false;
  }
  get promedioXP(): number {
    if (!this.estudiantes.length) return 0;
    return Math.round(this.estudiantes.reduce((s, e) => s + e.experiencia, 0) / this.estudiantes.length);
  }
  get totalMonedas(): number { return this.estudiantes.reduce((s, e) => s + e.monedas, 0); }
  get rachaMax(): number     { return this.estudiantes.reduce((max, e) => Math.max(max, e.racha_dias), 0); }
}
