import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Paso {
  titulo: string;
  texto: string;
  multiplosA: number[];
  multiplosB: number[];
  mostrarResultado: boolean;
  pregunta?: { enunciado: string; opciones: string[]; correcta: string };
}

@Component({
  selector: 'app-leccion-mcm',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./leccion-base.css'],
  template: `
<div class="leccion-wrapper">
  <div class="leccion-header">
    <div style="font-size:3rem">🔁</div>
    <h2 class="leccion-titulo" style="color:#06b6d4">Mínimo Común Múltiplo (MCM)</h2>
    <p class="leccion-subtitulo">El número más pequeño que comparten</p>
  </div>

  <div class="barra-progreso-wrap">
    <div class="barra-labels">
      <span>Paso {{ pasoActual + 1 }} de {{ pasos.length }}</span>
      <span>{{ progreso }}%</span>
    </div>
    <div class="barra-track">
      <div class="barra-fill" [style.width.%]="progreso" style="background:#06b6d4"></div>
    </div>
  </div>

  <div class="paso-card" style="background:#cffafe">
    <span class="paso-numero" style="background:#a5f3fc;color:#0891b2">
      Paso {{ pasoActual + 1 }}
    </span>
    <h3 class="paso-titulo">{{ paso.titulo }}</h3>
    <p class="paso-texto">{{ paso.texto }}</p>

    <div class="mcm-viz" style="display: flex; flex-direction: column; gap: 15px; margin: 20px 0;">
      <div class="fila-multiplos">
        <span style="font-weight: bold; width: 100px; display: inline-block;">Múltiplos de A:</span>
        <span *ngFor="let m of paso.multiplosA" 
              class="m-tag" 
              [style.background]="paso.mostrarResultado && esComun(m) ? '#06b6d4' : '#e2e8f0'"
              [style.color]="paso.mostrarResultado && esComun(m) ? 'white' : 'black'"
              style="padding: 2px 8px; margin: 0 3px; border-radius: 4px; display: inline-block;">
          {{ m }}
        </span>
      </div>
      <div class="fila-multiplos">
        <span style="font-weight: bold; width: 100px; display: inline-block;">Múltiplos de B:</span>
        <span *ngFor="let m of paso.multiplosB" 
              class="m-tag" 
              [style.background]="paso.mostrarResultado && esComun(m) ? '#06b6d4' : '#e2e8f0'"
              [style.color]="paso.mostrarResultado && esComun(m) ? 'white' : 'black'"
              style="padding: 2px 8px; margin: 0 3px; border-radius: 4px; display: inline-block;">
          {{ m }}
        </span>
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
      {{ seleccion === paso.pregunta.correcta ? '🎉 ¡Magnífico! Has encontrado el MCM.' : '😅 ¡Casi! La respuesta era ' + paso.pregunta.correcta }}
    </div>
  </div>

  <div *ngIf="finalizado" class="mensaje-motivacion" style="background:#cffafe;color:#0891b2">
    🏆 ¡Eres un experto en múltiplos! ¡Enhorabuena!
  </div>

  <div class="nav-pasos">
    <button class="btn-nav btn-anterior" (click)="anterior()" [disabled]="pasoActual === 0">← Anterior</button>
    <div class="puntos-nav">
      <div *ngFor="let p of pasos; let i = index" class="punto"
           [class.activo]="i === pasoActual"
           [style.background]="i === pasoActual ? '#06b6d4' : '#e2e8f0'"></div>
    </div>
    <button class="btn-nav btn-siguiente" style="background:#06b6d4"
            (click)="siguiente()"
            [disabled]="(!!paso.pregunta && !respondido) || finalizado">
      {{ finalizado ? '✓ Listo' : 'Siguiente →' }}
    </button>
  </div>
</div>
  `
})
export class LeccionMcmComponent {
  pasos: Paso[] = [
    { titulo: '¿Qué son los múltiplos?', texto: 'Los múltiplos de un número son los resultados de su tabla de multiplicar. Por ejemplo, de 2 y 3.', multiplosA: [2, 4, 6, 8, 10], multiplosB: [3, 6, 9, 12, 15], mostrarResultado: false },
    { titulo: 'Buscamos el común', texto: 'El MCM es el número más pequeño que aparece en las dos listas. ¡Aquí es el 6!', multiplosA: [2, 4, 6, 8, 10], multiplosB: [3, 6, 9, 12, 15], mostrarResultado: true },
    { titulo: 'Practica con 4 y 2', texto: '¿Cuál es el primer número que comparten el 4 y el 2?', multiplosA: [4, 8, 12, 16], multiplosB: [2, 4, 6, 8, 10], mostrarResultado: false,
      pregunta: { enunciado: '¿Cuál es el MCM de 4 y 2?', opciones: ['2', '4', '6', '8'], correcta: '4' } },
    { titulo: '¡Correcto!', texto: 'El 4 es el primer múltiplo común. ¡4 es el MCM!', multiplosA: [4, 8, 12, 16], multiplosB: [2, 4, 6, 8, 10], mostrarResultado: true },
    { titulo: 'Reto final: 3 y 4', texto: 'Busca el primer número que esté en la tabla del 3 y del 4.', multiplosA: [3, 6, 9, 12, 15], multiplosB: [4, 8, 12, 16, 20], mostrarResultado: false,
      pregunta: { enunciado: '¿Cuál es el MCM de 3 y 4?', opciones: ['6', '8', '12', '15'], correcta: '12' } },
    { titulo: '¡Impresionante!', texto: 'El 12 es el MCM de 3 y 4. ¡Has terminado todas las lecciones! 🌟', multiplosA: [3, 6, 9, 12, 15], multiplosB: [4, 8, 12, 16, 20], mostrarResultado: true }
  ];

  pasoActual = 0;
  seleccion = '';
  respondido = false;

  get paso(): Paso { return this.pasos[this.pasoActual]; }
  get progreso(): number { return Math.round(((this.pasoActual + 1) / this.pasos.length) * 100); }
  get finalizado(): boolean { return this.pasoActual === this.pasos.length - 1; }

  esComun(n: number): boolean {
    return this.paso.multiplosA.includes(n) && this.paso.multiplosB.includes(n);
  }

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
