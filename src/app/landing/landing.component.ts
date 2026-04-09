import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterModule],
  template: `
    <div class="landing-page d-flex flex-column min-vh-100 text-white">
      <header class="d-flex justify-content-end p-3">
        <a routerLink="/auth/login" class="btn btn-outline-light">Iniciar sesión</a>
      </header>

      <main class="flex-fill d-flex align-items-center justify-content-center px-3">
        <div class="text-center card shadow-lg p-4" style="max-width: 440px; background: rgba(255,255,255,0.12); backdrop-filter: blur(10px);">
          <h1 class="display-5 fw-bold mb-4">Bienvenido</h1>
          <p class="lead mb-4">Presiona iniciar para ingresar como estudiante.</p>
          <a routerLink="/auth/nino-login" class="btn btn-light btn-lg px-5 py-3 fw-bold text-primary">Iniciar</a>
        </div>
      </main>
    </div>
  `,
  styles: [
    `.landing-page { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }`,
    `a.btn-outline-light { border-color: rgba(255,255,255,0.8); color: white; }`,
    `a.btn-outline-light:hover { background: rgba(255,255,255,0.16); color: white; }`
  ]
})
export class LandingComponent {}
