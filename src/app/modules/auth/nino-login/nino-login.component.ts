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
      nombre: ['', Validators.required],
      pin:    ['', [Validators.required, Validators.pattern(/^\d{4}$/)]]
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';

    const { nombre, pin } = this.form.value;

    // TEMPORAL: Comentando validación real para usar usuarios falsos
    // this.auth.ninoLogin(nombre, pin).subscribe({
    //   next: () => this.router.navigate(['/nino/dashboard']),
    //   error: err => {
    //     this.error = err.error?.message ?? 'Nombre o PIN incorrecto';
    //     this.loading = false;
    //   }
    // });

    // Usuario falso para testing
    if (nombre === 'Juan' && pin === '1234') {
      this.loading = false;
      this.router.navigate(['/nino/dashboard']);
    } else {
      this.error = 'Nombre o PIN incorrecto';
      this.loading = false;
    }
  }

  quickLogin(nombre: string, pin: string): void {
    this.form.patchValue({ nombre, pin });
    this.submit();
  }
}
