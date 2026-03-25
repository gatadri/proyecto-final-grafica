import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Tarea } from '../../../core/models';

@Component({
  selector: 'app-tareas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tareas.component.html'
})
export class TareasComponent implements OnInit {
  tareas: Tarea[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.get<Tarea[]>('tareas').subscribe({
      next: data => { this.tareas = data; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  eliminar(id: number): void {
    if (!confirm('¿Eliminar esta tarea?')) return;
    this.api.delete(`tareas/${id}`).subscribe(() => {
      this.tareas = this.tareas.filter(t => t.id !== id);
    });
  }
}
