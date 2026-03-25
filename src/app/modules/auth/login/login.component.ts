import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html'
})
export class LoginComponent {
  form: FormGroup;
  loading = false;
  error = '';

  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    this.form = this.fb.group({
      email:    ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';

    const { email, password } = this.form.value;

    // TEMPORAL: Comentando validación real para usar usuarios falsos
    // this.auth.login(email, password).subscribe({
    //   next: res => {
    //     const role = res.user.role;
    //     this.router.navigate([`/${role}/dashboard`]);
    //   },
    //   error: err => {
    //     this.error = err.error?.message ?? 'Error al iniciar sesión';
    //     this.loading = false;
    //   }
    // });

    // Usuarios falsos para testing
    let role = '';
    if (email === 'director@test.com' && password === '1234') {
      role = 'director';
    } else if (email === 'profesor@test.com' && password === '1234') {
      role = 'profesor';
    } else if (email === 'padre@test.com' && password === '1234') {
      role = 'padre';
    } else {
      this.error = 'Usuario o contraseña incorrectos';
      this.loading = false;
      return;
    }

    this.loading = false;
    this.router.navigate([`/${role}/dashboard`]);
  }

  quickLogin(email: string, password: string): void {
    this.form.patchValue({ email, password });
    this.submit();
  }
}
