import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Paso {
  titulo: string;
  texto: string;
  partes: number;
  pintadas: number;
  mostrarResultado: boolean;
  pregunta?: { enunciado: string; opciones: string[]; correcta: string };
}

@Component({
  selector: 'app-leccion-fracciones',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./leccion-base.css'],
  template: `
<div class="leccion-wrapper">
  <div class="leccion-header">
    <div style="font-size:3rem">🔢</div>
    <h2 class="leccion-titulo" style="color:#ec4899">Las Fracciones</h2>
    <p class="leccion-subtitulo">Partes de un todo</p>
  </div>

  <div class="barra-progreso-wrap">
    <div class="barra-labels">
      <span>Paso {{ pasoActual + 1 }} de {{ pasos.length }}</span>
      <span>{{ progreso }}%</span>
    </div>
    <div class="barra-track">
      <div class="barra-fill" [style.width.%]="progreso" style="background:#ec4899"></div>
    </div>
  </div>

  <div class="paso-card" style="background:#fce7f3">
    <span class="paso-numero" style="background:#fbcfe8;color:#be185d">
      Paso {{ pasoActual + 1 }}
    </span>
    <h3 class="paso-titulo">{{ paso.titulo }}</h3>
    <p class="paso-texto">{{ paso.texto }}</p>

    <div class="bloques-wrap" style="justify-content: center;">
      <div class="circulo-fraccion" style="width: 150px; height: 150px; border-radius: 50%; border: 4px solid #ec4899; overflow: hidden; position: relative; display: flex; flex-wrap: wrap;">
        <div *ngFor="let i of range(paso.partes)" 
             [style.width.%]="100 / (paso.partes === 4 ? 2 : (paso.partes === 2 ? 1 : 1))"
             [style.height.%]="100 / (paso.partes === 4 ? 2 : (paso.partes === 2 ? 2 : 1))"
             [style.background]="i < paso.pintadas ? '#f472b6' : 'white'"
             style="border: 1px solid #ec4899; box-sizing: border-box;">
        </div>
      </div>
      <div *ngIf="paso.mostrarResultado" class="simbolo-fraccion" style="font-size: 3rem; margin-left: 20px; display: flex; flex-direction: column; align-items: center;">
        <div style="border-bottom: 3px solid black; padding: 0 10px;">{{ paso.pintadas }}</div>
        <div>{{ paso.partes }}</div>
      </div>
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
      {{ seleccion === paso.pregunta.correcta ? '🎉 ¡Genial! Entiendes las fracciones perfectamente.' : '😅 ¡Casi! La respuesta era ' + paso.pregunta.correcta }}
    </div>
  </div>

  <div *ngIf="finalizado" class="mensaje-motivacion" style="background:#fce7f3;color:#ec4899">
    🏆 ¡Dominas las fracciones! ¡Sigue así!
  </div>

  <div class="nav-pasos">
    <button class="btn-nav btn-anterior" (click)="anterior()" [disabled]="pasoActual === 0">← Anterior</button>
    <div class="puntos-nav">
      <div *ngFor="let p of pasos; let i = index" class="punto"
           [class.activo]="i === pasoActual"
           [style.background]="i === pasoActual ? '#ec4899' : '#e2e8f0'"></div>
    </div>
    <button class="btn-nav btn-siguiente" style="background:#ec4899"
            (click)="siguiente()"
            [disabled]="(!!paso.pregunta && !respondido) || finalizado">
      {{ finalizado ? '✓ Listo' : 'Siguiente →' }}
    </button>
  </div>
</div>
  `
})
export class LeccionFraccionesComponent {
  pasos: Paso[] = [
    { titulo: '¿Qué es una fracción?', texto: 'Es una parte de algo completo. Si dividimos una tarta en 2 y tomamos 1, tenemos la mitad.', partes: 2, pintadas: 1, mostrarResultado: false },
    { titulo: 'La mitad: 1/2', texto: 'El número de arriba (1) es lo que tenemos. El de abajo (2) son las partes totales.', partes: 2, pintadas: 1, mostrarResultado: true },
    { titulo: 'Dividir en 4', texto: 'Si dividimos la tarta en 4 trozos and comemos 1, ¿cómo se llama esa fracción?', partes: 4, pintadas: 1, mostrarResultado: false,
      pregunta: { enunciado: '¿Qué fracción es 1 trozo de 4?', opciones: ['1/2', '1/4', '2/4', '3/4'], correcta: '1/4' } },
    { titulo: 'Un cuarto: 1/4', texto: '¡Eso es! Un trozo de cuatro es 1/4.', partes: 4, pintadas: 1, mostrarResultado: true },
    { titulo: 'Varios trozos', texto: 'Si de los 4 trozos, pintamos 3... ¿qué fracción tenemos?', partes: 4, pintadas: 3, mostrarResultado: false,
      pregunta: { enunciado: '¿Qué fracción son 3 trozos de 4?', opciones: ['1/4', '2/4', '3/4', '4/4'], correcta: '3/4' } },
    { titulo: 'Tres cuartos: 3/4', texto: '¡Perfecto! Has aprendido lo más importante de las fracciones.', partes: 4, pintadas: 3, mostrarResultado: true }
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
