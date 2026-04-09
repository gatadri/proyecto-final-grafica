import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { MockDataService } from '../../../core/services/mock-data.service';

@Component({
  selector: 'app-nino-logros',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './nino-logros.component.html'
})
export class NinoLogrosComponent implements OnInit {
  nino: any;
  logrosObtenidos: any[] = [];
  todoLogros: any[] = [];
  loading = true;

  constructor(private auth: AuthService, private mock: MockDataService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino();
    this.logrosObtenidos = this.mock.getLogrosNino(this.nino?.id ?? 0);
    this.todoLogros      = this.mock.getLogros();
    this.loading = false;
  }

  tieneLogro(id: number): boolean {
    return this.logrosObtenidos.some(l => l.id === id);
  }

  getFechaLogro(id: number): string {
    return this.logrosObtenidos.find(l => l.id === id)?.pivot?.fecha_obtenido ?? '';
  }
}
