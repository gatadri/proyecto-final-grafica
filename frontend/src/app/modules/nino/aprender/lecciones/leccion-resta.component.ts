import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Paso {
  titulo: string;
  texto: string;
  total: number;
  quitar: number;
  mostrarResultado: boolean;
  pregunta?: { enunciado: string; opciones: string[]; correcta: string };
}

@Component({
  selector: 'app-leccion-resta',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./leccion-base.css'],
  template: `
<div class="leccion-wrapper">
  <div class="leccion-header">
    <div style="font-size:3rem">➖</div>
    <h2 class="leccion-titulo" style="color:#f97316">La Resta</h2>
    <p class="leccion-subtitulo">Quitar cosas para saber cuántas quedan</p>
  </div>

  <div class="barra-progreso-wrap">
    <div class="barra-labels">
      <span>Paso {{ pasoActual + 1 }} de {{ pasos.length }}</span>
      <span>{{ progreso }}%</span>
    </div>
    <div class="barra-track">
      <div class="barra-fill" [style.width.%]="progreso" style="background:#f97316"></div>
    </div>
  </div>

  <div class="paso-card" style="background:#fff7ed">
    <span class="paso-numero" style="background:#ffedd5;color:#c2410c">Paso {{ pasoActual + 1 }}</span>
    <h3 class="paso-titulo">{{ paso.titulo }}</h3>
    <p class="paso-texto">{{ paso.texto }}</p>

    <!-- Visual: bloques que se tachan -->
    <div class="bloques-wrap">
      <div *ngFor="let i of range(paso.total)" class="bloque"
           [style.background]="i < paso.total - paso.quitar || !paso.mostrarResultado ? '#fed7aa' : '#fecaca'"
           [style.opacity]="paso.mostrarResultado && i >= paso.total - paso.quitar ? '0.35' : '1'"
           [style.text-decoration]="paso.mostrarResultado && i >= paso.total - paso.quitar ? 'line-through' : 'none'">
        🍬
      </div>
      <ng-container *ngIf="paso.mostrarResultado">
        <span class="operador">=</span>
        <div class="resultado-box" style="background:#c2410c">{{ paso.total - paso.quitar }}</div>
      </ng-container>
    </div>

    <div *ngIf="paso.mostrarResultado" style="font-size:0.9rem;color:#9a3412;margin-top:0.3rem">
      🔴 Los caramelos tachados son los que quitamos ({{ paso.quitar }})
    </div>

    <div *ngIf="paso.pregunta && !respondido" class="ejemplo-interactivo">
      <p class="ejemplo-pregunta">🤔 {{ paso.pregunta.enunciado }}</p>
      <div class="opciones-grid">
        <button *ngFor="let op of paso.pregunta.opciones" class="opcion-btn"
                [class.correcta]="respondido && op === paso.pregunta!.correcta"
                [class.incorrecta]="respondido && seleccion === op && op !== paso.pregunta!.correcta"
                (click)="responder(op)">{{ op }}</button>
      </div>
    </div>

    <div *ngIf="respondido && paso.pregunta" class="feedback-texto"
         [style.background]="seleccion === paso.pregunta.correcta ? '#dcfce7' : '#fee2e2'"
         [style.color]="seleccion === paso.pregunta.correcta ? '#15803d' : '#b91c1c'">
      {{ seleccion === paso.pregunta.correcta ? '🎉 ¡Correcto!' : '😅 La respuesta era ' + paso.pregunta.correcta }}
    </div>
  </div>

  <div *ngIf="finalizado" class="mensaje-motivacion" style="background:#ffedd5;color:#c2410c">
    🏆 ¡Completaste la lección de Resta! ¡Genial!
  </div>

  <div class="nav-pasos">
    <button class="btn-nav btn-anterior" (click)="anterior()" [disabled]="pasoActual === 0">← Anterior</button>
    <div class="puntos-nav">
      <div *ngFor="let p of pasos; let i = index" class="punto"
           [class.activo]="i === pasoActual"
           [style.background]="i === pasoActual ? '#f97316' : '#e2e8f0'"></div>
    </div>
    <button class="btn-nav btn-siguiente" style="background:#f97316"
            (click)="siguiente()"
            [disabled]="(!!paso.pregunta && !respondido) || finalizado">
      {{ finalizado ? '✓ Listo' : 'Siguiente →' }}
    </button>
  </div>
</div>
  `
})
export class LeccionRestaComponent {
  pasos: Paso[] = [
    { titulo: '¿Qué es restar?', texto: 'Restar es quitar cosas de un grupo. Tenemos 7 caramelos y quitamos 3.', total: 7, quitar: 3, mostrarResultado: false },
    { titulo: 'Quitamos 3 caramelos', texto: 'Los caramelos tachados son los que quitamos. Quedan 4 caramelos: 7 - 3 = 4', total: 7, quitar: 3, mostrarResultado: true },
    { titulo: 'Otro ejemplo', texto: 'Tenemos 8 caramelos y comemos 5. ¿Cuántos quedan?', total: 8, quitar: 5, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 8 - 5?', opciones: ['2', '3', '4', '5'], correcta: '3' } },
    { titulo: '¡Correcto! 8 - 5 = 3', texto: 'Quitamos 5 caramelos y quedan 3. ¡Muy bien!', total: 8, quitar: 5, mostrarResultado: true },
    { titulo: 'Tu turno', texto: 'Tenemos 9 caramelos y regalamos 4. ¿Cuántos quedan?', total: 9, quitar: 4, mostrarResultado: false,
      pregunta: { enunciado: '¿Cuánto es 9 - 4?', opciones: ['4', '5', '6', '7'], correcta: '5' } },
    { titulo: '¡Perfecto! 9 - 4 = 5', texto: '¡Lo lograste! Restaste 9 - 4 = 5. ¡Eres un experto en la resta! 🌟', total: 9, quitar: 4, mostrarResultado: true }
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
