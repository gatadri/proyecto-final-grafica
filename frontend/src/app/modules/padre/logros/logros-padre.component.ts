import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino } from '../../../core/models';
import { forkJoin } from 'rxjs';

interface Logro {
  id: number;
  nombre: string;
  descripcion: string;
  icono: string;
  rareza: string;
  desbloqueado: boolean;
  fecha_desbloqueado?: string;
}

interface HijoConLogros {
  id: number;
  nombre: string;
  apellido: string;
  logros: Logro[];
  logrosObtenidos: number;
}

@Component({
  selector: 'app-logros-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './logros-padre.component.html'
})
export class LogrosPadreComponent implements OnInit {
  hijosConLogros: HijoConLogros[] = [];
  loading = true;

  constructor(
    private api: ApiService,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    const user = this.auth.getUser();
    if (user) {
      this.cargarHijosYLogros(user.id);
    } else {
      this.loading = false;
    }
  }

  cargarHijosYLogros(padreId: number): void {
    this.api.get<Nino[]>(`usuarios/${padreId}/hijos`).subscribe({
      next: hijos => {
        if (hijos.length === 0) {
          this.loading = false;
          return;
        }

        // Cargar logros de cada hijo
        const requests = hijos.map(hijo =>
          this.api.get<Logro[]>(`logros?nino_id=${hijo.id}`)
        );

        forkJoin(requests).subscribe({
          next: logrosArray => {
            this.hijosConLogros = hijos.map((hijo, index) => ({
              id: hijo.id,
              nombre: hijo.nombre,
              apellido: hijo.apellido,
              logros: logrosArray[index],
              logrosObtenidos: logrosArray[index].filter(l => l.desbloqueado).length
            }));
            this.loading = false;
          },
          error: err => {
            console.error('Error cargando logros', err);
            this.loading = false;
          }
        });
      },
      error: err => {
        console.error('Error cargando hijos', err);
        this.loading = false;
      }
    });
  }
}
