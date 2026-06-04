import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-profesor-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profesor-dashboard.component.html'
})
export class ProfesorDashboardComponent implements OnInit {
  estudiantes: any[] = [];
  loading = true;
  
  constructor(
    private api: ApiService, 
    private auth: AuthService
  ) {}
  
  ngOnInit(): void {
    this.cargarEstudiantes();
  }
  
  cargarEstudiantes(): void {
    this.api.get<any[]>('profesor/estudiantes').subscribe({
      next: (data) => {
        this.estudiantes = data;
        this.loading = false;
        console.log('Dashboard - Estudiantes cargados:', data);
      },
      error: (err) => {
        console.error('Error cargando estudiantes:', err);
        this.loading = false;
      }
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
