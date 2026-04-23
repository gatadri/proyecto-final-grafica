import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AvatarStateService } from '../../../core/services/avatar-state.service';

@Component({ selector: 'app-nino-tarea', standalone: true, imports: [CommonModule, RouterModule], templateUrl: './nino-tarea.component.html' })
export class NinoTareaComponent implements OnInit {
  nino: any;
  tarea: any;
  ejercicios: any[] = [];
  ejercicioActual = 0;
  respuestaSeleccionada = '';
  feedback: { correcto: boolean; mensaje: string } | null = null;
  intentos = 0;
  puntosTotal = 0;
  completada = false;
  loading = true;

  constructor(private route: ActivatedRoute, private router: Router,
              private auth: AuthService, private mock: MockDataService,
              private avatarState: AvatarStateService) {}

  ngOnInit(): void {
    this.avatarState.resetExpression();
    this.nino = this.auth.getNino();
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.tarea = this.mock.getTareaById(id);
    if (!this.tarea) { this.router.navigate(['/nino/dashboard']); return; }
    this.ejercicios = this.tarea.ejercicios ?? [];
    this.loading = false;
  }

  get ejercicio(): any { return this.ejercicios[this.ejercicioActual]; }
  get progreso(): number { return Math.round((this.ejercicioActual / this.ejercicios.length) * 100); }

  responder(): void {
    if (!this.respuestaSeleccionada || this.feedback) return;
    this.intentos++;
    const correcto = this.respuestaSeleccionada === this.ejercicio.respuesta_correcta;
    const puntos = correcto ? (this.intentos === 1 ? 10 : 5) : 0;
    const expresión = correcto ? 'feliz' : (Math.random() > 0.5 ? 'enojado' : 'triste');

    this.avatarState.setExpression(expresión);
    this.feedback = {
      correcto,
      mensaje: correcto
        ? `¡Correcto! +${puntos} puntos`
        : (this.intentos >= 2 ? `Incorrecto. La respuesta era: ${this.ejercicio.respuesta_correcta}` : 'Intenta de nuevo')
    };

    if (correcto || this.intentos >= 2) {
      this.puntosTotal += puntos;
      setTimeout(() => {
        this.feedback = null;
        this.respuestaSeleccionada = '';
        this.intentos = 0;
        this.ejercicioActual++;
        this.avatarState.resetExpression();
        if (this.ejercicioActual >= this.ejercicios.length) {
          this.completada = true;
          this.mock.completarTarea(this.nino.id, this.tarea.id, this.puntosTotal);
          const ninoActual = this.mock.getNinoById(this.nino.id);
          if (ninoActual) localStorage.setItem('nino', JSON.stringify(ninoActual));
        }
      }, 1500);
    }
  }
}
