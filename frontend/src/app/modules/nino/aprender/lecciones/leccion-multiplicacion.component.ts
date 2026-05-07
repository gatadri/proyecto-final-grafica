import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Paso {
  titulo: string;
  texto: string;
  grupoA: number;
  grupoB: number;
  mostrarResultado: boolean;
  pregunta?: { enunciado: string; opciones: string[]; correcta: string };
}

@Component({
  selector: 'app-leccion-multiplicacion',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./leccion-base.css'],
  template: `
<div class="leccion-wrapper">
  <div class="leccion-header">
    <div style="font-size:3rem">✖️</div>
    <h2 class="leccion-titulo" style="color:#3b82f6">La Multiplicación</h2>
    <p class="leccion-subtitulo">Sumar el mismo número varias veces</p>
  </div>

  <div class="barra-progreso-wrap">
    <div class="barra-labels">
      <span>Paso {{ pasoActual + 1 }} de {{ pasos.length }}</span>
      <span>{{ progreso }}%</span>
    </div>
    <div class="barra-track">
      <div class="barra-fill" [style.width.%]="progreso" style="background:#3b82f6"></div>
    </div>
  </div>

  <div class="paso-card" style="background:#eff6ff">
    <span class="paso-numero" style="background:#dbeafe;color:#1d4ed8">
      Paso {{ pasoActual + 1 }}
    </span>
    <h3 class="paso-titulo">{{ paso.titulo }}</h3>
    <p class="paso-texto">{{ paso.texto }}</p>

    <div class="bloques-wrap">
      <div *ngFor="let g of range(paso.grupoB)" class="grupo-multi" style="border: 2px dashed #3b82f6; padding: 5px; margin: 5px; border-radius: 8px; display: flex;">
        <div *ngFor="let i of range(paso.grupoA)" class="bloque" style="background:#bfdbfe">⭐</div>
      </div>
      <ng-container *ngIf="paso.mostrarResultado">
        <span class="operador">=</span>
        <div class="resultado-box" style="background:#1d4ed8">{{ paso.grupoA * paso.grupoB }}</div>
      </ng-container>
    </div>

    <div *ngIf="paso.pregunta && !respondido" class="ejemplo-interactivo">
      <p class="ejemplo-pregunta">🤔 {{ paso.pregunta.enunciado }}</p>
      <div class="opciones-grid">
        <button *ngFor="let op of paso.pregunta.opciones"
                class="opcion-btn"
                [class.correcta]="respondido && op === paso.pregunta!.correcta"
                [class.incorrecta]="respondido && seleccion === op && op !== paso.pregunta!.correcta"
                (click)="responder(op)">
          {{ op }}
        </button>
      </div>
    </div>

    <div *ngIf="respondido && paso.pregunta" class="feedback-texto"
         [style.background]="seleccion === paso.pregunta.correcta ? '#dcfce7' : '#fee2e2'"
         [style.color]="seleccion === paso.pregunta.correcta ? '#15803d' : '#b91c1c'">
      {{ seleccion === paso.pregunta.correcta ? '🎉 ¡Fantástico! ¡Eres un genio!' : '😅 ¡Casi! La respuesta correcta era ' + paso.pregunta.correcta }}
    </div>
  </div>

  <div *ngIf="finalizado" class="mensaje-motivacion" style="background:#dbeafe;color:#1d4ed8">
    🏆 ¡Dominas las tablas de multiplicar! ¡Increíble!
  </div>

  <div class="nav-pasos">
    <button class="btn-nav btn-anterior" (click)="anterior()" [disabled]="pasoActual === 0">← Anterior</button>
    <div class="puntos-nav">
      <div *ngFor="let p of pasos; let i = index" class="punto"
           [class.activo]="i === pasoActual"
           [style.background]="i === pasoActual ? '#3b82f6' : '#e2e8f0'"></div>
    </div>
    <button class="btn-nav btn-siguiente" style="background:#3b82f6"
            (click)="siguiente()"
            [disabled]="(!!paso.pregunta && !respondido) || finalizado">
      {{ finalizado ? '✓ Listo' : 'Siguiente →' }}
    </button>
  </div>
</div>
  `
})
export class LeccionMultiplicacionComponent {
  pasos: Paso[] = [
    { titulo: '¿Qué es multiplicar?', texto: 'Es sumar grupos iguales. Si tienes 3 grupos de 2 estrellas cada uno, ¿cuántas estrellas hay?', grupoA: 2, grupoB: 3, mostrarResultado: false },
    { titulo: 'Contamos por grupos', texto: '3 veces 2 es lo mismo que 2 + 2 + 2 = 6. ¡Así de fácil!', grupoA: 2, grupoB: 3, mostrarResultado: true },
    { titulo: 'Practica con el 4', texto: 'Si tienes 2 grupos de 4 estrellas, ¿cuántas hay en total?', grupoA: 4, grupoB: 2, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 4 × 2?', opciones: ['6', '8', '10', '12'], correcta: '8' } },
    { titulo: '¡Muy bien!', texto: '4 + 4 = 8. Dos veces cuatro es ocho.', grupoA: 4, grupoB: 2, mostrarResultado: true },
    { titulo: 'Un reto mayor', texto: '3 grupos de 3 estrellas. ¡Piénsalo bien!', grupoA: 3, grupoB: 3, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 3 × 3?', opciones: ['6', '9', '12', '15'], correcta: '9' } },
    { titulo: '¡Eres un experto!', texto: '3 + 3 + 3 = 9. ¡Has completado la lección!', grupoA: 3, grupoB: 3, mostrarResultado: true }
  ];

  pasoActual = 0;
  seleccion = '';
  respondido = false;

  get paso(): Paso { return this.pasos[this.pasoActual]; }
  get progreso(): number { return Math.round(((this.pasoActual + 1) / this.pasos.length) * 100); }
  get finalizado(): boolean { return this.pasoActual === this.pasos.length - 1; }

  range(n: number): number[] { return Array.from({ length: n }, (_, i) => i); }

  responder(op: string): void {
    if (this.respondido) return;
    this.seleccion = op;
    this.respondido = true;
  }

  siguiente(): void {
    if (this.finalizado) return;
    this.pasoActual++;
    this.seleccion = '';
    this.respondido = false;
  }

  anterior(): void {
    if (this.pasoActual === 0) return;
    this.pasoActual--;
    this.seleccion = '';
    this.respondido = false;
  }
}
