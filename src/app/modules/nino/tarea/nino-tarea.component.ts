import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Ejercicio, Nino, Tarea } from '../../../core/models';

@Component({ selector: 'app-nino-tarea', standalone: true, imports: [CommonModule], templateUrl: './nino-tarea.component.html' })
export class NinoTareaComponent implements OnInit {
  nino!: Nino;
  tarea!: Tarea;
  ejercicios: Ejercicio[] = [];
  ejercicioActual = 0;
  respuestaSeleccionada = '';
  feedback: { correcto: boolean; mensaje: string } | null = null;
  intentos = 0;
  puntosTotal = 0;
  completada = false;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private api: ApiService,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino()!;
    const tareaId = this.route.snapshot.paramMap.get('id');
    this.api.get<any>(`nino/${this.nino.pin}/tarea/${tareaId}`).subscribe({
      next: data => {
        this.tarea = data.tarea;
        this.ejercicios = data.tarea.ejercicios ?? [];
        this.loading = false;
      },
      error: () => this.router.navigate(['/nino/dashboard'])
    });
  }

  get ejercicio(): Ejercicio { return this.ejercicios[this.ejercicioActual]; }
  get progreso(): number { return Math.round((this.ejercicioActual / this.ejercicios.length) * 100); }

  responder(): void {
    if (!this.respuestaSeleccionada) return;
    this.intentos++;

    this.api.post<any>(`nino/${this.nino.pin}/tarea/${this.tarea.id}/responder`, {
      respuesta: this.respuestaSeleccionada,
      ejercicio_id: this.ejercicio.id
    }).subscribe(res => {
      this.feedback = {
        correcto: res.correcto,
        mensaje: res.correcto ? '¡Correcto! +' + res.puntos + ' puntos' : (this.intentos >= 2 ? 'Respuesta incorrecta' : 'Intenta de nuevo')
      };

      if (res.correcto || this.intentos >= 2) {
        this.puntosTotal += res.puntos ?? 0;
        setTimeout(() => {
          this.feedback = null;
          this.respuestaSeleccionada = '';
          this.intentos = 0;
          this.ejercicioActual++;
          if (this.ejercicioActual >= this.ejercicios.length) {
            this.completada = true;
            // Actualizar monedas en local
            const n = this.auth.getNino()!;
            n.monedas += this.puntosTotal;
            localStorage.setItem('nino', JSON.stringify(n));
          }
        }, 1500);
      }
    });
  }
}
