import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';

interface Logro {
  id: number;
  nombre: string;
  descripcion: string;
  icono: string;
  rareza: string;
  condicion: string;
  valor_requerido: number;
  puntos_bonus: number;
  desbloqueado: boolean;
  progreso_actual: number;
  porcentaje: number;
  fecha_desbloqueado?: string;
}

@Component({
  selector: 'app-nino-logros',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './nino-logros.component.html'
})
export class NinoLogrosComponent implements OnInit {
  nino: any;
  logros: Logro[] = [];
  loading = true;
  rarezas: ('bronce' | 'plata' | 'oro' | 'legendario')[] = ['bronce', 'plata', 'oro', 'legendario'];

  constructor(
    private auth: AuthService,
    private api: ApiService
  ) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino();
    if (this.nino) {
      this.cargarLogros();
    }
  }

  cargarLogros(): void {
    this.api.get<Logro[]>(`logros?nino_id=${this.nino.id}`).subscribe({
      next: data => {
        this.logros = data;
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando logros', err);
        this.loading = false;
      }
    });
  }

  get logrosObtenidos(): Logro[] {
    return this.logros.filter(l => l.desbloqueado);
  }

  get logrosNoObtenidos(): Logro[] {
    return this.logros.filter(l => !l.desbloqueado);
  }

  get logrosPorRareza(): { [key: string]: Logro[] } {
    return {
      bronce: this.logros.filter(l => l.rareza === 'bronce'),
      plata: this.logros.filter(l => l.rareza === 'plata'),
      oro: this.logros.filter(l => l.rareza === 'oro'),
      legendario: this.logros.filter(l => l.rareza === 'legendario')
    };
  }

  getLogrosDesbloqueadosPorRareza(rareza: string): number {
    return this.logrosPorRareza[rareza]?.filter(l => l.desbloqueado).length || 0;
  }

  getTotalLogrosPorRareza(rareza: string): number {
    return this.logrosPorRareza[rareza]?.length || 0;
  }

  getRarezaColor(rareza: string): string {
    const colores: any = {
      'bronce': '#cd7f32',
      'plata': '#c0c0c0',
      'oro': '#ffd700',
      'legendario': '#9b59b6'
    };
    return colores[rareza] || '#6c757d';
  }

  getRarezaIcon(rareza: string): string {
    const iconos: any = {
      'bronce': 'medal',
      'plata': 'award',
      'oro': 'crown',
      'legendario': 'gem'
    };
    return iconos[rareza] || 'trophy';
  }
}
