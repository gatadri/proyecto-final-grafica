import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterModule, CommonModule],
  template: `
    <div class="landing-page">
      <!-- Fondo animado -->
      <div class="background-animation">
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
        <div class="floating-shape shape-4"></div>
        <div class="floating-shape shape-5"></div>
        <div class="floating-shape shape-6"></div>
      </div>

      <!-- Botón de login superior -->
      <header class="header-top">
        <a routerLink="/auth/login" class="btn-login-top">
          <i class="fas fa-sign-in-alt me-2"></i>Iniciar Sesión
        </a>
      </header>

      <!-- Contenido principal -->
      <main class="main-content">
        <div class="welcome-container">
          <!-- Icono principal animado -->
          <div class="hero-icon">
            <div class="icon-main">
              <i class="fas fa-calculator"></i>
            </div>
            <div class="math-symbols">
              <span class="math-symbol symbol-1">+</span>
              <span class="math-symbol symbol-2">×</span>
              <span class="math-symbol symbol-3">÷</span>
              <span class="math-symbol symbol-4">−</span>
              <span class="math-symbol symbol-5">=</span>
            </div>
          </div>

          <!-- Título principal -->
          <h1 class="title-hero">
            <span class="title-line-1">¡Aprende Matemáticas</span>
            <span class="title-line-2">Jugando!</span>
          </h1>

          <!-- Subtítulo -->
          <p class="subtitle-hero">
            Resuelve problemas, practica operaciones y conviértete en un genio de las matemáticas
          </p>

          <!-- Iconos de características -->
          <div class="features-icons">
            <div class="feature-icon" [style.animation-delay]="'0s'">
              <div class="icon-circle">
                <i class="fas fa-plus"></i>
              </div>
              <span>Sumar</span>
            </div>
            <div class="feature-icon" [style.animation-delay]="'0.2s'">
              <div class="icon-circle">
                <i class="fas fa-times"></i>
              </div>
              <span>Multiplicar</span>
            </div>
            <div class="feature-icon" [style.animation-delay]="'0.4s'">
              <div class="icon-circle">
                <i class="fas fa-divide"></i>
              </div>
              <span>Dividir</span>
            </div>
            <div class="feature-icon" [style.animation-delay]="'0.6s'">
              <div class="icon-circle">
                <i class="fas fa-minus"></i>
              </div>
              <span>Restar</span>
            </div>
          </div>

          <!-- Botón principal grande -->
          <div class="cta-container">
            <a routerLink="/auth/nino-login" class="btn-main-cta">
              <span class="btn-text">¡Comenzar Ahora!</span>
              <span class="btn-icon">🚀</span>
            </a>
            <p class="cta-hint">
              <i class="fas fa-hand-point-up me-2"></i>
              Presiona para ingresar como estudiante
            </p>
          </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="footer-landing">
        <p>
          <i class="fas fa-graduation-cap me-2"></i>
          Sistema educativo con IA para niños
        </p>
      </footer>
    </div>
  `,
  styles: [`
    .landing-page {
      min-height: 100vh;
      background: linear-gradient(135deg, #4A90E2 0%, #2E5C8A 50%, #FF8C42 100%);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* Fondo animado */
    .background-animation {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      z-index: 1;
    }

    .floating-shape {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      animation: float 20s infinite ease-in-out;
    }

    .shape-1 {
      width: 80px;
      height: 80px;
      top: 10%;
      left: 10%;
      animation-delay: 0s;
    }

    .shape-2 {
      width: 120px;
      height: 120px;
      top: 60%;
      left: 80%;
      animation-delay: 2s;
    }

    .shape-3 {
      width: 60px;
      height: 60px;
      top: 80%;
      left: 20%;
      animation-delay: 4s;
    }

    .shape-4 {
      width: 100px;
      height: 100px;
      top: 20%;
      left: 70%;
      animation-delay: 1s;
    }

    .shape-5 {
      width: 70px;
      height: 70px;
      top: 50%;
      left: 5%;
      animation-delay: 3s;
    }

    .shape-6 {
      width: 90px;
      height: 90px;
      top: 70%;
      left: 60%;
      animation-delay: 5s;
    }

    @keyframes float {
      0%, 100% {
        transform: translateY(0) translateX(0) rotate(0deg);
        opacity: 0.3;
      }
      33% {
        transform: translateY(-30px) translateX(20px) rotate(120deg);
        opacity: 0.6;
      }
      66% {
        transform: translateY(30px) translateX(-20px) rotate(240deg);
        opacity: 0.4;
      }
    }

    /* Header */
    .header-top {
      position: relative;
      z-index: 10;
      padding: 20px 30px;
      display: flex;
      justify-content: flex-end;
    }

    .btn-login-top {
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      border: 2px solid rgba(255, 255, 255, 0.4);
      color: white;
      padding: 12px 28px;
      border-radius: 50px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.3s ease;
      font-size: 16px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .btn-login-top:hover {
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
      color: white;
    }

    /* Contenido principal */
    .main-content {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      z-index: 10;
      padding: 20px;
    }

    .welcome-container {
      text-align: center;
      max-width: 700px;
      animation: fadeInUp 1s ease-out;
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Hero icon */
    .hero-icon {
      position: relative;
      display: inline-block;
      margin-bottom: 30px;
    }

    .icon-main {
      width: 180px;
      height: 180px;
      border-radius: 50%;
      background: linear-gradient(135deg, #FF8C42 0%, #E67932 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 15px 40px rgba(255, 140, 66, 0.5), 0 0 60px rgba(255, 140, 66, 0.3);
      animation: floatIcon 3s infinite ease-in-out;
      border: 5px solid rgba(255, 255, 255, 0.5);
    }

    .icon-main i {
      font-size: 80px;
      color: white;
      text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    @keyframes floatIcon {
      0%, 100% { transform: translateY(0) rotate(0deg); }
      50% { transform: translateY(-15px) rotate(5deg); }
    }

    .math-symbols {
      position: absolute;
      top: -20px;
      left: -20px;
      width: calc(100% + 40px);
      height: calc(100% + 40px);
    }

    .math-symbol {
      position: absolute;
      font-size: 40px;
      font-weight: bold;
      color: white;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
      animation: floatMath 3s infinite ease-in-out;
    }

    .symbol-1 {
      top: -10%;
      left: 50%;
      transform: translateX(-50%);
      animation-delay: 0s;
    }

    .symbol-2 {
      top: 20%;
      right: -15%;
      animation-delay: 0.6s;
    }

    .symbol-3 {
      bottom: 20%;
      right: -10%;
      animation-delay: 1.2s;
    }

    .symbol-4 {
      bottom: -5%;
      left: 50%;
      transform: translateX(-50%);
      animation-delay: 1.8s;
    }

    .symbol-5 {
      top: 20%;
      left: -15%;
      animation-delay: 2.4s;
    }

    @keyframes floatMath {
      0%, 100% {
        transform: translateY(0) scale(1);
        opacity: 0.8;
      }
      50% {
        transform: translateY(-10px) scale(1.1);
        opacity: 1;
      }
    }

    /* Títulos */
    .title-hero {
      color: white;
      margin: 20px 0;
      font-weight: 800;
      display: flex;
      flex-direction: column;
      gap: 5px;
      text-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    .title-line-1 {
      font-size: 36px;
      animation: slideInLeft 0.8s ease-out;
    }

    .title-line-2 {
      font-size: 64px;
      background: linear-gradient(135deg, #FF8C42 0%, #FFD700 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      animation: slideInRight 0.8s ease-out;
    }

    @keyframes slideInLeft {
      from {
        opacity: 0;
        transform: translateX(-50px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideInRight {
      from {
        opacity: 0;
        transform: translateX(50px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    .subtitle-hero {
      color: rgba(255, 255, 255, 0.95);
      font-size: 22px;
      margin: 20px 0 40px 0;
      text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      animation: fadeIn 1s ease-out 0.3s both;
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    /* Iconos de características */
    .features-icons {
      display: flex;
      justify-content: center;
      gap: 30px;
      margin: 40px 0;
      flex-wrap: wrap;
    }

    .feature-icon {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      animation: popIn 0.6s ease-out both;
    }

    @keyframes popIn {
      0% {
        transform: scale(0);
        opacity: 0;
      }
      50% {
        transform: scale(1.2);
      }
      100% {
        transform: scale(1);
        opacity: 1;
      }
    }

    .icon-circle {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: linear-gradient(135deg, #4A90E2 0%, #2E5C8A 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      color: white;
      box-shadow: 0 8px 20px rgba(74, 144, 226, 0.4), 0 0 40px rgba(74, 144, 226, 0.2);
      transition: all 0.3s ease;
      border: 3px solid rgba(255, 255, 255, 0.4);
    }

    .feature-icon:hover .icon-circle {
      transform: translateY(-5px) scale(1.1);
      box-shadow: 0 12px 30px rgba(74, 144, 226, 0.6), 0 0 60px rgba(74, 144, 226, 0.4);
      background: linear-gradient(135deg, #5BA0F2 0%, #3E6C9A 100%);
    }

    .feature-icon span {
      color: white;
      font-weight: 600;
      font-size: 16px;
      text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    /* Botón principal */
    .cta-container {
      margin-top: 50px;
    }

    .btn-main-cta {
      display: inline-flex;
      align-items: center;
      gap: 15px;
      background: linear-gradient(135deg, #FF8C42 0%, #E67932 100%);
      color: white;
      padding: 20px 50px;
      border-radius: 60px;
      font-size: 28px;
      font-weight: 800;
      text-decoration: none;
      box-shadow: 0 10px 30px rgba(255, 140, 66, 0.5), 0 0 60px rgba(255, 140, 66, 0.3);
      transition: all 0.3s ease;
      border: 4px solid rgba(255, 255, 255, 0.4);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% {
        transform: scale(1);
        box-shadow: 0 10px 30px rgba(255, 140, 66, 0.5), 0 0 60px rgba(255, 140, 66, 0.3);
      }
      50% {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(255, 140, 66, 0.6), 0 0 80px rgba(255, 140, 66, 0.4);
      }
    }

    .btn-main-cta:hover {
      transform: translateY(-5px) scale(1.05);
      box-shadow: 0 15px 40px rgba(255, 140, 66, 0.6), 0 0 80px rgba(255, 140, 66, 0.4);
      animation: none;
    }

    .btn-main-cta:active {
      transform: translateY(-2px) scale(1.02);
    }

    .btn-text {
      letter-spacing: 1px;
    }

    .btn-icon {
      font-size: 32px;
      animation: rocket 1s infinite alternate;
    }

    @keyframes rocket {
      from { transform: translateY(0); }
      to { transform: translateY(-5px); }
    }

    .cta-hint {
      color: rgba(255, 255, 255, 0.9);
      font-size: 16px;
      margin-top: 20px;
      text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      animation: blink 2s infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.6; }
    }

    /* Footer */
    .footer-landing {
      position: relative;
      z-index: 10;
      padding: 20px;
      text-align: center;
      color: rgba(255, 255, 255, 0.8);
      font-size: 14px;
      text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    .footer-landing p {
      margin: 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .title-line-1 {
        font-size: 28px;
      }
      .title-line-2 {
        font-size: 48px;
      }
      .subtitle-hero {
        font-size: 18px;
      }
      .features-icons {
        gap: 15px;
      }
      .icon-circle {
        width: 65px;
        height: 65px;
        font-size: 26px;
      }
      .feature-icon span {
        font-size: 13px;
      }
      .btn-main-cta {
        font-size: 22px;
        padding: 16px 40px;
      }
      .icon-main {
        width: 140px;
        height: 140px;
      }
      .icon-main i {
        font-size: 60px;
      }
    }
  `]
})
export class LandingComponent implements OnInit {
  ngOnInit() {
    // Cualquier inicialización necesaria
  }
}
