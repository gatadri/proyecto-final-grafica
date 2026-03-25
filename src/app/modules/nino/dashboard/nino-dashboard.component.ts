import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino, Tarea } from '../../../core/models';

@Component({ selector: 'app-nino-dashboard', standalone: true, imports: [CommonModule, RouterModule], templateUrl: './nino-dashboard.component.html' })
export class NinoDashboardComponent implements OnInit {
  nino!: Nino;
  tareas: Tarea[] = [];
  loading = true;

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino()!;
    this.api.get<any>(`nino/${this.nino.pin}/dashboard`).subscribe({
      next: data => { this.tareas = data.tareas_pendientes ?? []; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  logout(): void { this.auth.ninoLogout(); }
}
