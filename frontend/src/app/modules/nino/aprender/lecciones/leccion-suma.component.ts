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
  selector: 'app-leccion-suma',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./leccion-base.css'],
  template: `
<div class="leccion-wrapper">
  <div class="leccion-header">
    <div style="font-size:3rem">➕</div>
    <h2 class="leccion-titulo" style="color:#22c55e">La Suma</h2>
    <p class="leccion-subtitulo">Juntar cosas para saber cuántas hay en total</p>
  </div>

  <!-- Barra de progreso -->
  <div class="barra-progreso-wrap">
    <div class="barra-labels">
      <span>Paso {{ pasoActual + 1 }} de {{ pasos.length }}</span>
      <span>{{ progreso }}%</span>
    </div>
    <div class="barra-track">
      <div class="barra-fill" [style.width.%]="progreso" style="background:#22c55e"></div>
    </div>
  </div>

  <!-- Paso actual -->
  <div class="paso-card" style="background:#f0fdf4">
    <span class="paso-numero" style="background:#dcfce7;color:#15803d">
      Paso {{ pasoActual + 1 }}
    </span>
    <h3 class="paso-titulo">{{ paso.titulo }}</h3>
    <p class="paso-texto">{{ paso.texto }}</p>

    <!-- Visual: bloques -->
    <div class="bloques-wrap">
      <div *ngFor="let i of range(paso.grupoA)" class="bloque" style="background:#bbf7d0">🍎</div>
      <span class="operador">+</span>
      <div *ngFor="let i of range(paso.grupoB)" class="bloque bloque-nuevo" style="background:#86efac">🍎</div>
      <ng-container *ngIf="paso.mostrarResultado">
        <span class="operador">=</span>
        <div class="resultado-box" style="background:#15803d">{{ paso.grupoA + paso.grupoB }}</div>
      </ng-container>
    </div>

    <!-- Ejemplo interactivo -->
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
      {{ seleccion === paso.pregunta.correcta ? '🎉 ¡Muy bien! ¡Eso es correcto!' : '😅 ¡Casi! La respuesta era ' + paso.pregunta.correcta }}
    </div>
  </div>

  <!-- Mensaje final -->
  <div *ngIf="finalizado" class="mensaje-motivacion" style="background:#dcfce7;color:#15803d">
    🏆 ¡Completaste la lección de Suma! ¡Eres increíble!
  </div>

  <!-- Navegación -->
  <div class="nav-pasos">
    <button class="btn-nav btn-anterior" (click)="anterior()" [disabled]="pasoActual === 0">← Anterior</button>
    <div class="puntos-nav">
      <div *ngFor="let p of pasos; let i = index" class="punto"
           [class.activo]="i === pasoActual"
           [style.background]="i === pasoActual ? '#22c55e' : '#e2e8f0'"></div>
    </div>
    <button class="btn-nav btn-siguiente" style="background:#22c55e"
            (click)="siguiente()"
            [disabled]="(!!paso.pregunta && !respondido) || finalizado">
      {{ finalizado ? '✓ Listo' : 'Siguiente →' }}
    </button>
  </div>
</div>
  `
})
export class LeccionSumaComponent {
  pasos: Paso[] = [
    { titulo: '¿Qué es sumar?', texto: 'Sumar es juntar dos grupos de cosas. Aquí tenemos 2 manzanas y 3 manzanas.', grupoA: 2, grupoB: 3, mostrarResultado: false },
    { titulo: 'Contamos todo junto', texto: 'Cuando juntamos los dos grupos, contamos todas las manzanas: 2 + 3 = 5', grupoA: 2, grupoB: 3, mostrarResultado: true },
    { titulo: 'Otro ejemplo', texto: 'Ahora tenemos 4 manzanas y 2 manzanas. ¿Cuántas hay en total?', grupoA: 4, grupoB: 2, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 4 + 2?', opciones: ['5', '6', '7', '8'], correcta: '6' } },
    { titulo: '¡Correcto! 4 + 2 = 6', texto: 'Juntamos los dos grupos y contamos: 1, 2, 3, 4, 5, 6. ¡Seis manzanas en total!', grupoA: 4, grupoB: 2, mostrarResultado: true },
    { titulo: 'Practica tú solo', texto: 'Tenemos 3 manzanas y 5 manzanas. ¡Tú puedes calcularlo!', grupoA: 3, grupoB: 5, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 3 + 5?', opciones: ['6', '7', '8', '9'], correcta: '8' } },
    { titulo: '¡Excelente! 3 + 5 = 8', texto: '¡Lo lograste! Sumaste 3 + 5 = 8. ¡Eres un campeón de la suma! 🏆', grupoA: 3, grupoB: 5, mostrarResultado: true }
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
