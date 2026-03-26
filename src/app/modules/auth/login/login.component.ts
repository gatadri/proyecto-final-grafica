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
      email:    ['', /*[Validators.required, Validators.email]*/],
      password: ['', /*Validators.required*/]
    });
  }

  submit(): void {
    // if (this.form.invalid) return;
    // this.loading = true;
    // this.error = '';

    // const { email, password } = this.form.value;

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
  }

  loginAsDirector(): void {
    const fakeUser: any = { id: 1, name: 'Director Test', nombre: 'Director', apellido: 'Test', email: 'director@test.com', role: 'director', activo: true };
    localStorage.setItem('token', 'fake-token');
    localStorage.setItem('user', JSON.stringify(fakeUser));
    this.router.navigate(['/director/dashboard']);
  }

  loginAsProfesor(): void {
    const fakeUser: any = { id: 2, name: 'Profesor Test', nombre: 'Profesor', apellido: 'Test', email: 'profesor@test.com', role: 'profesor', activo: true };
    localStorage.setItem('token', 'fake-token');
    localStorage.setItem('user', JSON.stringify(fakeUser));
    this.router.navigate(['/profesor/dashboard']);
  }

  loginAsPadre(): void {
    const fakeUser: any = { id: 3, name: 'Padre Test', nombre: 'Padre', apellido: 'Test', email: 'padre@test.com', role: 'padre', activo: true };
    localStorage.setItem('token', 'fake-token');
    localStorage.setItem('user', JSON.stringify(fakeUser));
    this.router.navigate(['/padre/dashboard']);
  }
}
