import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface MiniJuego {
  tipo: 'colores' | 'visual' | 'logica';
  pregunta: string;
  opciones: string[];
  respuestaCorrecta: number;
}

@Component({
  selector: 'app-pantalla-descanso',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="descanso-overlay" *ngIf="mostrar">
      <div class="descanso-container">
        <div class="icono-descanso">😌</div>
        <h1>¡Momento de Descanso!</h1>
        <p class="subtitulo">Relaja tu mente con este juego rápido</p>
        
        <!-- Minijuego -->
        <div class="minijuego-container" *ngIf="!juegoCompletado">
          <div class="pregunta-box">
            <h3>{{ juegoActual.pregunta }}</h3>
          </div>
          
          <div class="opciones-grid">
            <button 
              *ngFor="let opcion of juegoActual.opciones; let i = index"
              class="opcion-btn"
              [class.correcta]="respuestaSeleccionada === i && i === juegoActual.respuestaCorrecta"
              [class.incorrecta]="respuestaSeleccionada === i && i !== juegoActual.respuestaCorrecta"
              [disabled]="respuestaSeleccionada !== null"
              (click)="seleccionarRespuesta(i)"
              [style.background]="getColorFondo(opcion, i)"
              [style.border]="getColorBorde(opcion)">
              <span [innerHTML]="getContenidoOpcion(opcion)"></span>
            </button>
          </div>
          
          <div class="feedback" *ngIf="respuestaSeleccionada !== null">
            <div class="feedback-correcto" *ngIf="respuestaSeleccionada === juegoActual.respuestaCorrecta">
              <span class="icono-grande">🎉</span>
              <p>¡Excelente!</p>
            </div>
            <div class="feedback-incorrecto" *ngIf="respuestaSeleccionada !== juegoActual.respuestaCorrecta">
              <span class="icono-grande">💪</span>
              <p>¡Inténtalo de nuevo!</p>
            </div>
          </div>
        </div>
        
        <!-- Mensaje de completado -->
        <div class="completado-box" *ngIf="juegoCompletado">
          <div class="icono-completado">🌟</div>
          <h2>¡Genial! Volvamos a practicar</h2>
          <div class="contador">
            <div class="circulo-progreso">
              <svg width="150" height="150">
                <circle cx="75" cy="75" r="65" class="circulo-fondo"/>
                <circle cx="75" cy="75" r="65" class="circulo-progreso-barra"
                        [attr.stroke-dashoffset]="dashOffset"/>
              </svg>
              <div class="numero-contador">{{ segundosRestantes }}</div>
            </div>
          </div>
        </div>
        
        <p class="mensaje-motivacion">{{ mensajeMotivacion }}</p>
      </div>
    </div>
  `,
  styles: [`
    .descanso-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .descanso-container {
      text-align: center;
      color: white;
      animation: slideUp 0.5s ease-out;
      max-width: 600px;
      padding: 20px;
    }
    @keyframes slideUp {
      from { transform: translateY(50px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    .icono-descanso {
      font-size: 60px;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.1); }
    }
    h1 {
      font-size: 42px;
      margin: 15px 0 5px 0;
      font-weight: bold;
      text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
    }
    .subtitulo {
      font-size: 18px;
      margin: 5px 0 25px 0;
      opacity: 0.9;
    }
    .minijuego-container {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      padding: 30px;
      margin: 20px 0;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    .pregunta-box {
      margin-bottom: 25px;
    }
    .pregunta-box h3 {
      font-size: 24px;
      font-weight: 600;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
      margin: 0;
    }
    .opciones-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
      margin: 20px 0;
    }
    .opcion-btn {
      padding: 30px 20px;
      font-size: 28px;
      font-weight: bold;
      border: 4px solid white;
      border-radius: 15px;
      cursor: pointer;
      transition: all 0.3s ease;
      background: white;
      color: #333;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      min-height: 100px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .opcion-btn:hover:not(:disabled) {
      transform: translateY(-5px) scale(1.05);
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
    }
    .opcion-btn:active:not(:disabled) {
      transform: translateY(-2px) scale(1.02);
    }
    .opcion-btn:disabled {
      cursor: not-allowed;
    }
    .opcion-btn.correcta {
      background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
      color: white !important;
      border-color: #2e7d32 !important;
      animation: correctaAnimation 0.5s ease;
    }
    .opcion-btn.incorrecta {
      background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%) !important;
      color: white !important;
      border-color: #c62828 !important;
      animation: shake 0.5s ease;
    }
    @keyframes correctaAnimation {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.1); }
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-10px); }
      75% { transform: translateX(10px); }
    }
    .feedback {
      margin-top: 20px;
      animation: fadeIn 0.5s ease;
    }
    .feedback-correcto, .feedback-incorrecto {
      padding: 15px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.2);
    }
    .feedback .icono-grande {
      font-size: 48px;
      display: block;
      margin-bottom: 10px;
      animation: bounceIn 0.5s ease;
    }
    @keyframes bounceIn {
      0% { transform: scale(0); }
      50% { transform: scale(1.2); }
      100% { transform: scale(1); }
    }
    .feedback p {
      font-size: 22px;
      font-weight: bold;
      margin: 0;
    }
    .completado-box {
      padding: 20px;
    }
    .icono-completado {
      font-size: 80px;
      animation: rotate 1s ease;
      margin-bottom: 15px;
    }
    @keyframes rotate {
      0% { transform: rotate(0deg) scale(0); }
      50% { transform: rotate(180deg) scale(1.2); }
      100% { transform: rotate(360deg) scale(1); }
    }
    .completado-box h2 {
      font-size: 28px;
      margin: 15px 0 25px 0;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .contador {
      margin: 20px 0;
    }
    .circulo-progreso {
      position: relative;
      display: inline-block;
    }
    .circulo-fondo {
      fill: none;
      stroke: rgba(255, 255, 255, 0.3);
      stroke-width: 10;
    }
    .circulo-progreso-barra {
      fill: none;
      stroke: white;
      stroke-width: 10;
      stroke-linecap: round;
      transform: rotate(-90deg);
      transform-origin: 50% 50%;
      stroke-dasharray: 408.4;
      transition: stroke-dashoffset 1s linear;
      filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
    }
    .numero-contador {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 52px;
      font-weight: bold;
      text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.4);
    }
    .mensaje-motivacion {
      font-size: 20px;
      font-style: italic;
      opacity: 0.9;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
      margin-top: 15px;
    }
  `]
})
export class PantallaDescansoComponent implements OnInit {
  mostrar = false;
  segundosRestantes = 5;
  dashOffset = 0;
  mensajeMotivacion = '';
  
  juegoActual!: MiniJuego;
  respuestaSeleccionada: number | null = null;
  juegoCompletado = false;
  
  mensajes = [
    '¡Lo estás haciendo genial! 💪',
    'Tómate un momento para ti 🎯',
    '¡Vuelve con más energía! ⚡',
    'Un pequeño descanso ayuda mucho 🌈',
    '¡Sigue así, campeón! 🌟'
  ];
  
  juegosDisponibles: MiniJuego[] = [
    { tipo: 'visual', pregunta: '¿Cuál es DIFERENTE?', opciones: ['😀', '😀', '😀', '😎'], respuestaCorrecta: 3 },
    { tipo: 'logica', pregunta: '¿Cuál NO pertenece?', opciones: ['🐶', '🐱', '🐭', '🍕'], respuestaCorrecta: 3 },
    { tipo: 'logica', pregunta: '¿Cuál es el intruso?', opciones: ['⚽', '🏀', '🎾', '🍎'], respuestaCorrecta: 3 },
    { tipo: 'logica', pregunta: '¿Cuál NO es fruta?', opciones: ['🍎', '🍌', '🍇', '🍕'], respuestaCorrecta: 3 },
    { tipo: 'colores', pregunta: '¿Cuál es más OSCURO?', opciones: ['#FFB6C1', '#FF1493', '#8B008B', '#FFE4E1'], respuestaCorrecta: 2 },
    { tipo: 'colores', pregunta: '¿Cuál es más BRILLANTE?', opciones: ['#1a1a1a', '#4a4a4a', '#00ff00', '#2a2a2a'], respuestaCorrecta: 2 },
    { tipo: 'logica', pregunta: '¿Qué sigue? 🌙 ⭐ 🌙 ⭐ 🌙 ...', opciones: ['🌙', '⭐', '☀️', '🌈'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Qué sigue? ❤️ 💛 ❤️ 💛 ❤️ ...', opciones: ['❤️', '💛', '💚', '💙'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Qué sigue? 🔴 🟡 🔵 🔴 🟡 ...', opciones: ['🔴', '🟡', '🔵', '🟢'], respuestaCorrecta: 2 },
    { tipo: 'logica', pregunta: '¿Cuál vive en el AGUA?', opciones: ['🐶', '🐠', '🐦', '🐱'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Cuál puede VOLAR?', opciones: ['🐘', '🐟', '🦅', '🐢'], respuestaCorrecta: 2 },
    { tipo: 'visual', pregunta: '¿Cuál es más GRANDE?', opciones: ['🐜', '🐘', '🐁', '🐇'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: 'Si ☀️ es DÍA, ¿cuál es NOCHE?', opciones: ['⭐', '🌙', '☁️', '🌈'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: 'Si 🔥 es CALIENTE, ¿cuál es FRÍO?', opciones: ['❄️', '⚡', '💧', '🌊'], respuestaCorrecta: 0 },
    { tipo: 'visual', pregunta: 'Si 😊 es FELIZ, ¿cuál es TRISTE?', opciones: ['😁', '😎', '😢', '😴'], respuestaCorrecta: 2 },
    { tipo: 'logica', pregunta: '¿Cuál es DULCE?', opciones: ['🧂', '🍫', '🧄', '🧅'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Con cuál haces JUGO?', opciones: ['🍕', '🍔', '🍊', '🍟'], respuestaCorrecta: 2 },
    { tipo: 'visual', pregunta: '¿Con cuál juegas FÚTBOL?', opciones: ['🏀', '⚽', '🎾', '🏐'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Cuál usas en la PLAYA?', opciones: ['⛷️', '🏄', '⛸️', '🎿'], respuestaCorrecta: 1 },
    { tipo: 'visual', pregunta: '¿Qué ves cuando LLUEVE?', opciones: ['☀️', '⛈️', '❄️', '🌈'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Qué sale después de lluvia?', opciones: ['⚡', '❄️', '🌈', '🌙'], respuestaCorrecta: 2 },
    { tipo: 'logica', pregunta: '¿Cuál vuela por el CIELO?', opciones: ['🚗', '✈️', '🚢', '🚂'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Cuál navega por el MAR?', opciones: ['🚗', '🚁', '🚢', '🚲'], respuestaCorrecta: 2 },
    { tipo: 'visual', pregunta: '¿Con cuál LLAMAS?', opciones: ['📱', '💻', '📺', '⌚'], respuestaCorrecta: 0 },
    { tipo: 'logica', pregunta: '¿Con cuál te ALUMBRAS?', opciones: ['📚', '🔦', '🎮', '🎧'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Cuál es INSTRUMENTO?', opciones: ['📱', '🎸', '📚', '⚽'], respuestaCorrecta: 1 },
    { tipo: 'visual', pregunta: '¿Quién APAGA incendios?', opciones: ['👨‍⚕️', '👨‍🍳', '👨‍🚒', '👨‍🏫'], respuestaCorrecta: 2 },
    { tipo: 'visual', pregunta: '¿Quién ENSEÑA?', opciones: ['👨‍⚕️', '👨‍🏫', '👨‍✈️', '👨‍🍳'], respuestaCorrecta: 1 },
    { tipo: 'colores', pregunta: '¿Cuál color es CALMANTE?', opciones: ['#FF0000', '#87CEEB', '#FFFF00', '#FF6600'], respuestaCorrecta: 1 },
    { tipo: 'colores', pregunta: '¿Color del FUEGO?', opciones: ['#0000FF', '#00FF00', '#FF4500', '#FFFF00'], respuestaCorrecta: 2 },
    { tipo: 'logica', pregunta: '¿Qué continúa? 🟥 🟦 🟥 🟦 🟥 ...', opciones: ['🟥', '🟦', '🟩', '🟨'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Con qué ESCRIBES?', opciones: ['🍴', '✏️', '🔧', '🔑'], respuestaCorrecta: 1 },
    { tipo: 'visual', pregunta: '¿Qué usas para VER mejor?', opciones: ['🎧', '👓', '👟', '🎩'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿En cuál DUERMES?', opciones: ['🪑', '🛏️', '🚪', '🪟'], respuestaCorrecta: 1 },
    { tipo: 'visual', pregunta: '¿Cuándo sale el SOL?', opciones: ['🌙', '🌅', '🌃', '🌆'], respuestaCorrecta: 1 },
    { tipo: 'logica', pregunta: '¿Qué haces de NOCHE?', opciones: ['☀️', '🏖️', '😴', '🏃'], respuestaCorrecta: 2 }
  ];

  ngOnInit() {
    this.mensajeMotivacion = this.mensajes[Math.floor(Math.random() * this.mensajes.length)];
    this.seleccionarJuegoAleatorio();
  }
  
  seleccionarJuegoAleatorio() {
    const indiceAleatorio = Math.floor(Math.random() * this.juegosDisponibles.length);
    this.juegoActual = this.juegosDisponibles[indiceAleatorio];
  }
  
  seleccionarRespuesta(indice: number) {
    this.respuestaSeleccionada = indice;
    
    if (indice === this.juegoActual.respuestaCorrecta) {
      setTimeout(() => {
        this.juegoCompletado = true;
        this.iniciarContador();
      }, 1500);
    } else {
      setTimeout(() => {
        this.respuestaSeleccionada = null;
      }, 1000);
    }
  }
  
  iniciarContador() {
    const intervalo = setInterval(() => {
      this.segundosRestantes--;
      this.dashOffset = 408.4 * (1 - this.segundosRestantes / 5);
      
      if (this.segundosRestantes <= 0) {
        clearInterval(intervalo);
        setTimeout(() => {
          this.mostrar = false;
          this.resetear();
        }, 500);
      }
    }, 1000);
  }
  
  resetear() {
    this.respuestaSeleccionada = null;
    this.juegoCompletado = false;
    this.segundosRestantes = 5;
    this.dashOffset = 0;
    this.seleccionarJuegoAleatorio();
  }
  
  getColorFondo(opcion: string, indice: number): string {
    if (this.juegoActual.tipo === 'colores') {
      return opcion;
    }
    return 'white';
  }
  
  getColorBorde(opcion: string): string {
    if (this.juegoActual.tipo === 'colores') {
      return `4px solid ${opcion}`;
    }
    return '4px solid #ddd';
  }
  
  getContenidoOpcion(opcion: string): string {
    if (this.juegoActual.tipo === 'colores') {
      return '&nbsp;';
    }
    return opcion;
  }

  iniciarDescanso() {
    this.mostrar = true;
    this.resetear();
    this.mensajeMotivacion = this.mensajes[Math.floor(Math.random() * this.mensajes.length)];
  }
}
