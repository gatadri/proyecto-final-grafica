import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AvatarStateService } from '../../../core/services/avatar-state.service';
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

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private mock: MockDataService,
    private avatarState: AvatarStateService
  ) {}

  ngOnInit(): void {
    this.avatarState.resetExpression();
    this.nino = this.auth.getNino()!;
    // Simular carga de ejercicios de práctica
    setTimeout(() => {
      this.ejercicios = [
        { pregunta: '¿Cuánto es 2 + 2?', respuesta_correcta: '4', explicacion: '2 + 2 = 4' },
        { pregunta: '¿Cuánto es 5 - 3?', respuesta_correcta: '2', explicacion: '5 - 3 = 2' },
        { pregunta: '¿Cuánto es 3 * 2?', respuesta_correcta: '6', explicacion: '3 * 2 = 6' }
      ];
      this.loading = false;
    }, 1000);
  }

  get ejercicio(): any { return this.ejercicios[this.actual]; }
  get terminado(): boolean { return this.actual >= this.ejercicios.length; }

  responder(): void {
    if (!this.respuesta.trim()) return;

    // Simular respuesta
    const correcto = this.respuesta.trim().toLowerCase() === this.ejercicio.respuesta_correcta.toLowerCase();
    const expresión = correcto ? 'feliz' : (Math.random() > 0.5 ? 'enojado' : 'triste');
    this.avatarState.setExpression(expresión);
    this.feedback = { correcto, explicacion: correcto ? '¡Correcto!' : `Incorrecto. La respuesta es ${this.ejercicio.respuesta_correcta}` };
    if (correcto) {
      this.puntosGanados++;
      this.nino.monedas++;
      localStorage.setItem('nino', JSON.stringify(this.nino));
    }
    setTimeout(() => {
      this.feedback = null;
      this.respuesta = '';
      this.actual++;
      this.avatarState.resetExpression();
    }, 1800);
  }

  reiniciar(): void {
    this.actual = 0;
    this.puntosGanados = 0;
    this.loading = true;
    this.ngOnInit();
  }
}
