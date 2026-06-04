import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-pantalla-descanso',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="descanso-overlay" *ngIf="mostrar">
      <div class="descanso-container">
        <div class="icono-descanso">😌</div>
        <h1>¡Hora de un descanso!</h1>
        <p>Relájate por unos segundos...</p>
        <div class="contador">
          <div class="circulo-progreso">
            <svg width="200" height="200">
              <circle cx="100" cy="100" r="90" class="circulo-fondo"/>
              <circle cx="100" cy="100" r="90" class="circulo-progreso-barra"
                      [attr.stroke-dashoffset]="dashOffset"/>
            </svg>
            <div class="numero-contador">{{ segundosRestantes }}</div>
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
      background: linear-gradient(135deg, #FFD4A3 0%, #B3E0FF 100%);
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
    }
    @keyframes slideUp {
      from { transform: translateY(50px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    .icono-descanso {
      font-size: 80px;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.1); }
    }
    h1 {
      font-size: 48px;
      margin: 20px 0;
      font-weight: bold;
      text-shadow: 3px 3px 6px rgba(255, 155, 118, 0.3);
    }
    p {
      font-size: 24px;
      margin: 10px 0;
      text-shadow: 2px 2px 4px rgba(107, 182, 224, 0.3);
    }
    .contador {
      margin: 40px 0;
    }
    .circulo-progreso {
      position: relative;
      display: inline-block;
    }
    .circulo-fondo {
      fill: none;
      stroke: rgba(255, 255, 255, 0.3);
      stroke-width: 12;
    }
    .circulo-progreso-barra {
      fill: none;
      stroke: white;
      stroke-width: 12;
      stroke-linecap: round;
      transform: rotate(-90deg);
      transform-origin: 50% 50%;
      stroke-dasharray: 565.48;
      transition: stroke-dashoffset 1s linear;
      filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
    }
    .numero-contador {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 72px;
      font-weight: bold;
      text-shadow: 3px 3px 8px rgba(255, 180, 140, 0.4);
    }
    .mensaje-motivacion {
      font-size: 22px;
      font-style: italic;
      opacity: 0.9;
      text-shadow: 2px 2px 4px rgba(135, 206, 235, 0.3);
    }
  `]
})
export class PantallaDescansoComponent implements OnInit {
  mostrar = false;
  segundosRestantes = 10;
  dashOffset = 0;
  mensajeMotivacion = '';
  
  mensajes = [
    '¡Respira profundo! 🌟',
    '¡Lo estás haciendo genial! 💪',
    'Tómate un momento para ti 🎯',
    '¡Vuelve con más energía! ⚡',
    'Un pequeño descanso ayuda mucho 🌈'
  ];

  ngOnInit() {
    this.mensajeMotivacion = this.mensajes[Math.floor(Math.random() * this.mensajes.length)];
  }

  iniciarDescanso() {
    this.mostrar = true;
    this.segundosRestantes = 10;
    this.dashOffset = 0;
    
    const intervalo = setInterval(() => {
      this.segundosRestantes--;
      this.dashOffset = 565.48 * (1 - this.segundosRestantes / 10);
      
      if (this.segundosRestantes <= 0) {
        clearInterval(intervalo);
        setTimeout(() => {
          this.mostrar = false;
        }, 500);
      }
    }, 1000);
  }
}
