import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h5 class="fw-bold mb-4"><i class="fas fa-history text-primary me-2"></i>Log de Actividades</h5>
    <div class="card">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Fecha</th><th>Usuario</th><th>Actividad</th><th>Tipo</th></tr>
          </thead>
          <tbody>
            <tr *ngFor="let log of logs">
              <td><small class="text-muted">{{ log.fecha }}</small></td>
              <td><strong>{{ log.usuario }}</strong></td>
              <td>{{ log.descripcion }}</td>
              <td><span class="badge" [class.bg-success]="log.tipo==='tarea'" [class.bg-warning]="log.tipo==='logro'" [class.bg-info]="log.tipo==='login'" [class.bg-primary]="log.tipo==='otro'">{{ log.tipo }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `
})
export class LogsComponent implements OnInit {
  logs: any[] = [];
  constructor(private mock: MockDataService) {}
  ngOnInit(): void {
    const ninos    = this.mock.getNinos();
    const usuarios = this.mock.getUsuarios();

    const getNombre = (id: number, tipo: 'nino'|'user') => {
      if (tipo === 'nino') { const n = ninos.find((n:any) => n.id === id); return n ? n.nombre : 'Desconocido'; }
      const u = usuarios.find((u:any) => u.id === id); return u ? `${u.nombre} ${u.apellido}` : 'Desconocido';
    };

    this.logs = [
      { fecha: '2025-04-08 09:00', usuario: getNombre(2, 'user'), descripcion: 'Creó la tarea "Sumas y Restas"',       tipo: 'otro'  },
      { fecha: '2025-04-08 09:15', usuario: getNombre(3, 'user'), descripcion: 'Creó la tarea "Lectura Comprensiva"',  tipo: 'otro'  },
      { fecha: '2025-04-08 10:00', usuario: getNombre(1, 'nino'), descripcion: 'Completó tarea "Sumas y Restas" (90pts)', tipo: 'tarea' },
      { fecha: '2025-04-08 10:05', usuario: getNombre(1, 'nino'), descripcion: 'Obtuvo logro "Primera Tarea"',         tipo: 'logro' },
      { fecha: '2025-04-08 10:30', usuario: getNombre(5, 'nino'), descripcion: 'Completó tarea "Sumas y Restas" (80pts)', tipo: 'tarea' },
      { fecha: '2025-04-08 11:00', usuario: getNombre(3, 'nino'), descripcion: 'Completó tarea "Lectura Comprensiva" (100pts)', tipo: 'tarea' },
      { fecha: '2025-04-08 11:05', usuario: getNombre(3, 'nino'), descripcion: 'Obtuvo logro "Primera Tarea"',         tipo: 'logro' },
      { fecha: '2025-04-08 11:10', usuario: getNombre(3, 'nino'), descripcion: 'Obtuvo logro "Racha de 7 días"',       tipo: 'logro' },
      { fecha: '2025-04-08 12:00', usuario: getNombre(4, 'user'), descripcion: 'Inició sesión en el sistema',          tipo: 'login' },
      { fecha: '2025-04-08 12:30', usuario: getNombre(1, 'user'), descripcion: 'Revisó estadísticas del sistema',      tipo: 'otro'  },
    ].reverse();
  }
}
