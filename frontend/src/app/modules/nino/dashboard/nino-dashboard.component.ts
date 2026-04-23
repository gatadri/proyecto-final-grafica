import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { MockDataService } from '../../../core/services/mock-data.service';
import { Tarea } from '../../../core/models';

@Component({ selector: 'app-nino-dashboard', standalone: true, imports: [CommonModule, RouterModule], templateUrl: './nino-dashboard.component.html' })
export class NinoDashboardComponent implements OnInit {
  nino: any = null;
  tareas: Tarea[] = [];
  progreso: any[] = [];
  loading = true;

  constructor(private auth: AuthService, private mock: MockDataService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino();
    if (this.nino) {
      const todasTareas = this.mock.getTareasByNino(this.nino.id);
      this.progreso     = this.mock.getProgresoNino(this.nino.id);
      this.tareas       = todasTareas.filter((t: Tarea) => !this.progreso.find((p:any) => p.tarea_id === t.id && p.completada));
      // Sincronizar datos actualizados del niño
      const ninoActual = this.mock.getNinoById(this.nino.id);
      if (ninoActual) {
        this.nino = ninoActual;
        localStorage.setItem('nino', JSON.stringify(ninoActual));
      }
    }
    this.loading = false;
  }

  get tareasCompletadas(): number {
    return this.progreso.filter((p:any) => p.completada).length;
  }

  get totalTareas(): number {
    return this.mock.getTareasByNino(this.nino?.id ?? 0).length;
  }

  logout(): void { this.auth.ninoLogout(); }
}
