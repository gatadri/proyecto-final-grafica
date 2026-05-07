import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Paso {
  titulo: string;
  texto: string;
  total: number;
  dividirEn: number;
  mostrarResultado: boolean;
  pregunta?: { enunciado: string; opciones: string[]; correcta: string };
}

@Component({
  selector: 'app-leccion-division',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./leccion-base.css'],
  template: `
<div class="leccion-wrapper">
  <div class="leccion-header">
    <div style="font-size:3rem">➗</div>
    <h2 class="leccion-titulo" style="color:#a855f7">La División</h2>
    <p class="leccion-subtitulo">Repartir en partes iguales</p>
  </div>

  <div class="barra-progreso-wrap">
    <div class="barra-labels">
      <span>Paso {{ pasoActual + 1 }} de {{ pasos.length }}</span>
      <span>{{ progreso }}%</span>
    </div>
    <div class="barra-track">
      <div class="barra-fill" [style.width.%]="progreso" style="background:#a855f7"></div>
    </div>
  </div>

  <div class="paso-card" style="background:#f3e8ff">
    <span class="paso-numero" style="background:#e9d5ff;color:#7e22ce">
      Paso {{ pasoActual + 1 }}
    </span>
    <h3 class="paso-titulo">{{ paso.titulo }}</h3>
    <p class="paso-texto">{{ paso.texto }}</p>

    <div class="bloques-wrap" style="flex-direction: column; align-items: center;">
      <div class="total-div" style="display: flex; gap: 5px; margin-bottom: 20px;">
        <div *ngFor="let i of range(paso.total)" class="bloque" style="background:#d8b4fe">🍕</div>
      </div>
      
      <div *ngIf="paso.mostrarResultado" class="reparto-div" style="display: flex; gap: 20px;">
        <div *ngFor="let g of range(paso.dividirEn)" class="grupo-div" style="border: 2px solid #a855f7; padding: 10px; border-radius: 10px; display: flex; flex-direction: column; align-items: center;">
          <div style="font-size: 0.8rem; color: #7e22ce; margin-bottom: 5px;">Grupo {{ g + 1 }}</div>
          <div style="display: flex; gap: 3px;">
            <div *ngFor="let i of range(paso.total / paso.dividirEn)" class="bloque" style="background:#f5d0fe">🍕</div>
          </div>
        </div>
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
      {{ seleccion === paso.pregunta.correcta ? '🎉 ¡Impresionante! ¡Sabes repartir muy bien!' : '😅 ¡Casi! La respuesta era ' + paso.pregunta.correcta }}
    </div>
  </div>

  <div *ngIf="finalizado" class="mensaje-motivacion" style="background:#f3e8ff;color:#7e22ce">
    🏆 ¡Eres un maestro de la división! ¡Bravo!
  </div>

  <div class="nav-pasos">
    <button class="btn-nav btn-anterior" (click)="anterior()" [disabled]="pasoActual === 0">← Anterior</button>
    <div class="puntos-nav">
      <div *ngFor="let p of pasos; let i = index" class="punto"
           [class.activo]="i === pasoActual"
           [style.background]="i === pasoActual ? '#a855f7' : '#e2e8f0'"></div>
    </div>
    <button class="btn-nav btn-siguiente" style="background:#a855f7"
            (click)="siguiente()"
            [disabled]="(!!paso.pregunta && !respondido) || finalizado">
      {{ finalizado ? '✓ Listo' : 'Siguiente →' }}
    </button>
  </div>
</div>
  `
})
export class LeccionDivisionComponent {
  pasos: Paso[] = [
    { titulo: '¿Qué es dividir?', texto: 'Es repartir un total en partes iguales. Si tienes 4 pizzas y 2 amigos, ¿cuántas le tocan a cada uno?', total: 4, dividirEn: 2, mostrarResultado: false },
    { titulo: 'Repartiendo...', texto: 'Si repartimos 4 entre 2, a cada amigo le tocan 2 pizzas. ¡4 ÷ 2 = 2!', total: 4, dividirEn: 2, mostrarResultado: true },
    { titulo: 'Practica el reparto', texto: 'Tenemos 6 pizzas y queremos repartirlas entre 3 cajas. ¿Cuántas van en cada caja?', total: 6, dividirEn: 3, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 6 ÷ 3?', opciones: ['1', '2', '3', '4'], correcta: '2' } },
    { titulo: '¡Excelente!', texto: '6 repartido en 3 grupos da 2 en cada grupo. ¡6 ÷ 3 = 2!', total: 6, dividirEn: 3, mostrarResultado: true },
    { titulo: 'Un reto más', texto: '8 pizzas para 2 amigos hambrientos. ¿Cuántas para cada uno?', total: 8, dividirEn: 2, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 8 ÷ 2?', opciones: ['2', '4', '6', '8'], correcta: '4' } },
    { titulo: '¡Logrado!', texto: '8 repartido entre 2 es igual a 4. ¡Has terminado la lección!', total: 8, dividirEn: 2, mostrarResultado: true }
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
