import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({ providedIn: 'root' })
export class NinoGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): boolean {
    // TEMPORAL: Comentando validación para testing
    // if (this.auth.isNinoLoggedIn()) return true;
    // this.router.navigate(['/auth/nino-login']);
    // return false;
    return true; // Permitir acceso temporalmente
  }
}
