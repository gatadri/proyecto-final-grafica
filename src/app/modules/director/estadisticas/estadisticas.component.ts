import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';

@Component({
  selector: 'app-estadisticas',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-chart-line text-primary me-2"></i>Estadísticas del Sistema</h5>
    <div class="row g-3 mb-4">
      <div class="col-md-3" *ngFor="let s of stats">
        <div class="card text-center border-0 shadow-sm">
          <div class="card-body">
            <i class="fas fa-{{ s.icon }} fa-2x mb-2" [class]="'text-' + s.color"></i>
            <h3 class="fw-bold">{{ s.valor }}</h3>
            <small class="text-muted">{{ s.label }}</small>
          </div>
        </div>
      </div>
    </div>
    <div class="row g-3">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header fw-bold"><i class="fas fa-users text-primary me-2"></i>Ranking Estudiantes</div>
          <div class="card-body p-0">
            <table class="table table-hover mb-0">
              <thead class="table-light"><tr><th>#</th><th>Nombre</th><th>XP</th><th>Nivel</th><th>Racha</th></tr></thead>
              <tbody>
                <tr *ngFor="let n of ranking; let i = index">
                  <td><span class="badge" [class.bg-warning]="i===0" [class.bg-secondary]="i===1" [class.bg-danger]="i===2" [class.bg-light]="i>2">{{i+1}}</span></td>
                  <td>{{ n.nombre }} {{ n.apellido }}</td>
                  <td><strong>{{ n.experiencia }}</strong></td>
                  <td><span class="badge bg-info">{{ n.nivel }}</span></td>
                  <td><i class="fas fa-fire text-danger me-1"></i>{{ n.racha_dias }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-header fw-bold"><i class="fas fa-tasks text-success me-2"></i>Tareas por Profesor</div>
          <div class="card-body p-0">
            <table class="table table-hover mb-0">
              <thead class="table-light"><tr><th>Profesor</th><th>Tareas</th><th>Estudiantes</th></tr></thead>
              <tbody>
                <tr *ngFor="let p of profesores">
                  <td>{{ p.nombre }} {{ p.apellido }}</td>
                  <td><span class="badge bg-primary">{{ p.tareas }}</span></td>
                  <td><span class="badge bg-success">{{ p.estudiantes }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `
})
export class EstadisticasComponent implements OnInit {
  stats: any[] = [];
  ranking: any[] = [];
  profesores: any[] = [];

  constructor(private mock: MockDataService) {}

  ngOnInit(): void {
    const ninos    = this.mock.getNinos();
    const tareas   = this.mock.getTareas();
    const usuarios = this.mock.getUsuarios();
    const logros   = this.mock.getLogros();

    const totalXP      = ninos.reduce((s: number, n: any) => s + n.experiencia, 0);
    const totalMonedas = ninos.reduce((s: number, n: any) => s + n.monedas, 0);
    const totalLogros  = ninos.reduce((s: number, n: any) => s + this.mock.getLogrosNino(n.id).length, 0);

    this.stats = [
      { label: 'Total Estudiantes', valor: ninos.length,    icon: 'child',      color: 'primary' },
      { label: 'Total Tareas',      valor: tareas.length,   icon: 'tasks',      color: 'success' },
      { label: 'XP Total',          valor: totalXP,         icon: 'star',       color: 'warning' },
      { label: 'Monedas Totales',   valor: totalMonedas,    icon: 'coins',      color: 'info'    },
      { label: 'Logros Otorgados',  valor: totalLogros,     icon: 'trophy',     color: 'danger'  },
      { label: 'Profesores',        valor: usuarios.filter((u:any) => u.role === 'profesor').length, icon: 'chalkboard-teacher', color: 'secondary' },
    ];

    this.ranking = [...ninos].sort((a: any, b: any) => b.experiencia - a.experiencia);

    this.profesores = usuarios
      .filter((u: any) => u.role === 'profesor')
      .map((p: any) => ({
        ...p,
        tareas:      tareas.filter((t: any) => t.profesor_id === p.id).length,
        estudiantes: ninos.filter((n: any) => n.profesor_id === p.id).length,
      }));
  }
}
