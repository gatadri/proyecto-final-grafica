import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-director-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './director-dashboard.component.html'
})
export class DirectorDashboardComponent implements OnInit {
  stats: any = {
    total_profesores: 0,
    total_padres: 0,
    total_ninos: 0,
    total_tareas: 0,
    tareas_completadas: 0,
    xp_total: 0,
    monedas_total: 0,
    logros_total: 0
  };
  loading = true;
  
  constructor(private api: ApiService) {}
  
  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.loading = true;
    console.log('Iniciando carga del dashboard...');
    
    forkJoin({
      estadisticas: this.api.get<any>('director/estadisticas-generales'),
      usuarios: this.api.get<any[]>('usuarios')
    }).subscribe({
      next: ({ estadisticas, usuarios }) => {
        console.log('=== RESPUESTA DEL BACKEND ===')
        console.log('Estadísticas recibidas:', estadisticas);
        console.log('Usuarios recibidos:', usuarios);
        console.log('Total usuarios array:', usuarios?.length || 0);
        
        const profesores = usuarios?.filter(u => u.role === 'profesor').length || 0;
        const padres = usuarios?.filter(u => u.role === 'padre').length || 0;
        
        console.log('Profesores contados:', profesores);
        console.log('Padres contados:', padres);
        
        this.stats = {
          total_profesores: profesores,
          total_padres: padres,
          total_ninos: estadisticas?.total_estudiantes || 0,
          total_tareas: estadisticas?.total_tareas || 0,
          tareas_completadas: estadisticas?.total_tareas_completadas || 0,
          xp_total: estadisticas?.total_xp_sistema || 0,
          monedas_total: estadisticas?.total_monedas_sistema || 0,
          logros_total: estadisticas?.logros_total || 0
        };
        
        console.log('Stats finales asignadas:', this.stats);
        this.loading = false;
      },
      error: err => {
        console.error('=== ERROR EN DASHBOARD ===');
        console.error('Error completo:', err);
        console.error('Status:', err.status);
        console.error('Mensaje:', err.message);
        this.loading = false;
      }
    });
  }
}
