import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { User } from '../../../core/models';

@Component({ selector: 'app-usuarios', standalone: true, imports: [CommonModule], templateUrl: './usuarios.component.html' })
export class UsuariosComponent implements OnInit {
  usuarios: User[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.api.get<User[]>('usuarios').subscribe({
      next: data => { this.usuarios = data; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  suspender(id: number): void {
    this.api.patch(`usuarios/${id}/suspender`).subscribe(() => this.load());
  }

  activar(id: number): void {
    this.api.patch(`usuarios/${id}/activar`).subscribe(() => this.load());
  }

  eliminar(id: number): void {
    if (!confirm('¿Eliminar este usuario?')) return;
    this.api.delete(`usuarios/${id}`).subscribe(() => this.load());
  }
}
