import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-estudiantes',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-users text-primary me-2"></i>Mis Estudiantes</h5>
    <div *ngIf="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div *ngIf="!loading" class="row g-3">
      <div *ngFor="let e of estudiantes" class="col-md-6">
        <div class="card border-start border-primary border-3">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6 class="mb-0 fw-bold">{{ e.nombre }} {{ e.apellido }}</h6>
              <span class="badge bg-secondary">Grado {{ e.grado }}</span>
            </div>
            <div class="d-flex gap-2 flex-wrap mb-2">
              <span class="badge bg-warning"><i class="fas fa-coins me-1"></i>{{ e.monedas }}</span>
              <span class="badge bg-info">Nivel {{ e.nivel }}</span>
              <span class="badge bg-success">{{ e.experiencia }} XP</span>
              <span class="badge bg-danger"><i class="fas fa-fire me-1"></i>{{ e.racha_dias }}</span>
            </div>
            <div class="progress" style="height:6px">
              <div class="progress-bar bg-success" [style.width.%]="e.experiencia % 100"></div>
            </div>
          </div>
        </div>
      </div>
      <div *ngIf="estudiantes.length === 0" class="col-12 text-center py-4 text-muted">
        <i class="fas fa-users fa-3x mb-3"></i><p>No tienes estudiantes asignados</p>
      </div>
    </div>
  `
})
export class EstudiantesComponent implements OnInit {
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
        console.log('Estudiantes cargados:', data);
      },
      error: (err) => {
        console.error('Error cargando estudiantes:', err);
        this.loading = false;
      }
    });
  }
}
