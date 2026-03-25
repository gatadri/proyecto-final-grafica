import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino } from '../../../core/models';

@Component({ selector: 'app-nino-practica', standalone: true, imports: [CommonModule, FormsModule], templateUrl: './nino-practica.component.html' })
export class NinoPracticaComponent implements OnInit {
  nino!: Nino;
  ejercicios: any[] = [];
  actual = 0;
  respuesta = '';
  feedback: { correcto: boolean; explicacion: string } | null = null;
  puntosGanados = 0;
  loading = true;

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino()!;
    this.api.get<any>(`nino/${this.nino.pin}/practica`).subscribe({
      next: d => { this.ejercicios = d.ejercicios ?? []; this.loading = false; },
      error: () => this.loading = false
    });
  }

  get ejercicio(): any { return this.ejercicios[this.actual]; }
  get terminado(): boolean { return this.actual >= this.ejercicios.length; }

  responder(): void {
    if (!this.respuesta.trim()) return;

    this.api.post<any>(`nino/${this.nino.pin}/practica/ejercicio`, {
      respuesta: this.respuesta,
      respuesta_correcta: this.ejercicio.respuesta_correcta,
      explicacion: this.ejercicio.explicacion
    }).subscribe(res => {
      this.feedback = { correcto: res.correcto, explicacion: res.explicacion };
      if (res.correcto) {
        this.puntosGanados++;
        this.nino.monedas = res.monedas;
        localStorage.setItem('nino', JSON.stringify(this.nino));
      }
      setTimeout(() => {
        this.feedback = null;
        this.respuesta = '';
        this.actual++;
      }, 1800);
    });
  }

  reiniciar(): void {
    this.actual = 0;
    this.puntosGanados = 0;
    this.loading = true;
    this.ngOnInit();
  }
}
