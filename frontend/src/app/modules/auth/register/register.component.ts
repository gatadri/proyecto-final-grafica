import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './register.component.html'
})
export class RegisterComponent {
  form: FormGroup;
  loading = false;
  error = '';

  constructor(private fb: FormBuilder, private api: ApiService, private router: Router) {
    this.form = this.fb.group({
      nombre:            ['', Validators.required],
      apellido:          ['', Validators.required],
      carnet:            ['', Validators.required],
      email:             ['', [Validators.required, Validators.email]],
      numero:            ['', Validators.required],
      role:              ['', Validators.required],
      password:          ['', [Validators.required, Validators.minLength(6)]],
      password_confirmation: ['', Validators.required]
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';

    this.api.post<any>('register', this.form.value).subscribe({
      next: () => this.router.navigate(['/auth/login']),
      error: err => {
        this.error = err.error?.message ?? 'Error al registrarse';
        this.loading = false;
      }
    });
  }
}
