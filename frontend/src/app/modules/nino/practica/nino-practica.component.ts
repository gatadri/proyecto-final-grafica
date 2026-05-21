import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { AvatarStateService } from '../../../core/services/avatar-state.service';
import { AudioService, AudioType } from '../../../core/services/audio.service';
import { Nino } from '../../../core/models';

@Component({
  selector: 'app-nino-practica',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './nino-practica.component.html',
  styleUrls: ['./nino-practica.component.css']
})
export class NinoPracticaComponent implements OnInit, OnDestroy {
  nino!: Nino;
  ejercicios: any[] = [];
  actual = 0;
  respuesta = '';
  feedback: { correcto: boolean; mensaje: string } | null = null;
  
  // Estadísticas de la sesión
  puntosGanados = 0;
  aciertos = 0;
  errores = 0;
  inicioSesion = 0;
  
  loading = true;
  terminado = false;

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private avatarState: AvatarStateService,
    private audioService: AudioService
  ) {}

  ngOnInit(): void {
    this.avatarState.resetExpression();
    this.nino = this.auth.getNino()!;
    
    // Reproducir audio de ejercicios automáticamente
    this.audioService.play(AudioType.EJERCICIOS);
    
    this.cargarEjerciciosAleatorios();
  }

  ngOnDestroy(): void {
    // Pausar audio de ejercicios y volver al general
    this.audioService.pauseAndReturnToGeneral(AudioType.EJERCICIOS);
  }

  cargarEjerciciosAleatorios(): void {
    this.loading = true;
    this.api.get<any[]>('nino/ejercicios-practica?cantidad=5').subscribe({
      next: (ejercicios) => {
        this.ejercicios = ejercicios.length > 0 ? ejercicios : this.generarEjerciciosRespaldo();
        this.inicioSesion = Date.now();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando ejercicios', err);
        this.ejercicios = this.generarEjerciciosRespaldo();
        this.inicioSesion = Date.now();
        this.loading = false;
      }
    });
  }

  generarEjerciciosRespaldo(): any[] {
    const backup = [];
    for (let i = 0; i < 5; i++) {
      const a = Math.floor(Math.random() * 10) + 1;
      const b = Math.floor(Math.random() * 10) + 1;
      backup.push({
        pregunta: `¿Cuánto es ${a} + ${b}?`,
        respuesta_correcta: (a + b).toString(),
        tipo_ejercicio: 'multiple',
        opciones: [(a+b).toString(), (a+b+1).toString(), (a+b-1).toString(), (a+b+2).toString()].sort(() => Math.random() - 0.5)
      });
    }
    return backup;
  }

  get ejercicio(): any { return this.ejercicios[this.actual]; }

  responder(opcion?: string): void {
    if (this.feedback) return;
    
    const resp = (opcion || this.respuesta).trim().toLowerCase();
    const correcta = this.ejercicio.respuesta_correcta.toLowerCase();
    const esCorrecto = resp === correcta;

    if (esCorrecto) {
      this.aciertos++;
      this.puntosGanados += 10;
      this.avatarState.setExpression('alegre');
      this.feedback = { correcto: true, mensaje: '¡Excelente! +10 puntos' };
    } else {
      this.errores++;
      this.avatarState.setExpression(Math.random() > 0.5 ? 'sorprendido' : 'triste');
      this.feedback = { correcto: false, mensaje: `Casi... la respuesta era ${correcta}` };
    }

    setTimeout(() => {
      this.feedback = null;
      this.respuesta = '';
      this.actual++;
      this.avatarState.resetExpression();
      
      if (this.actual >= this.ejercicios.length) {
        this.finalizarPractica();
      }
    }, 1500);
  }

  finalizarPractica(): void {
    this.terminado = true;
    const tiempoTotal = Date.now() - this.inicioSesion;

    // Guardar en la base de datos
    const payload = {
      nino: this.nino.id,
      completada: true,
      puntos_obtenidos: this.puntosGanados,
      cantidad_aciertos: this.aciertos,
      cantidad_errores: this.errores,
      tiempo_total_ms: tiempoTotal,
      dificultad: 1,
      tipo_ejercicio: 'practica_libre'
    };

    this.api.post('nino/progreso-practica', payload).subscribe({
      next: () => {
        // Actualizar monedas del niño localmente
        this.nino.monedas += this.puntosGanados;
        this.auth.saveNino(this.nino);
      },
      error: (err) => console.error('Error guardando práctica', err)
    });
  }

  reiniciar(): void {
    this.actual = 0;
    this.puntosGanados = 0;
    this.aciertos = 0;
    this.errores = 0;
    this.terminado = false;
    this.cargarEjerciciosAleatorios();
  }
}
