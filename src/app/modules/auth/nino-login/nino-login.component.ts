import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-nino-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './nino-login.component.html'
})
export class NinoLoginComponent {
  form: FormGroup;
  loading = false;
  error = '';

  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    this.form = this.fb.group({
      nombre: ['', /*Validators.required*/],
      pin:    ['', /*[Validators.required, Validators.pattern(/^\d{4}$/)]*/]
    });
  }

  submit(): void {
    // if (this.form.invalid) return;
    // this.loading = true;
    // this.error = '';

    // const { nombre, pin } = this.form.value;

    // this.auth.ninoLogin(nombre, pin).subscribe({
    //   next: () => this.router.navigate(['/nino/dashboard']),
    //   error: err => {
    //     this.error = err.error?.message ?? 'Nombre o PIN incorrecto';
    //     this.loading = false;
    //   }
    // });
  }

  loginAsNino(): void {
    const fakeNino: any = { id: 1, nombre: 'Nino', apellido: 'Test', pin: '1234', nivel: 1, experiencia: 0, monedas: 100, avatar: 'default', racha_dias: 0, ultima_actividad: null };
    localStorage.setItem('nino', JSON.stringify(fakeNino));
    this.router.navigate(['/nino/dashboard']);
  }
}
