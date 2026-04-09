import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';

@Component({ selector: 'app-usuarios', standalone: true, imports: [CommonModule], templateUrl: './usuarios.component.html' })
export class UsuariosComponent implements OnInit {
  usuarios: any[] = [];
  loading = true;
  constructor(private mock: MockDataService) {}
  ngOnInit(): void { this.load(); }
  load(): void { this.usuarios = this.mock.getUsuarios(); this.loading = false; }
  suspender(id: number): void { this.mock.suspenderUsuario(id); this.load(); }
  activar(id: number):   void { this.mock.activarUsuario(id);   this.load(); }
  eliminar(id: number):  void {
    if (!confirm('¿Eliminar este usuario?')) return;
    this.mock.eliminarUsuario(id); this.load();
  }
}
