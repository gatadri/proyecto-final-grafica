import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { User, Nino } from '../../../core/models';

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './usuarios.component.html'
})
export class UsuariosComponent implements OnInit {
  usuarios: User[] = [];
  profesores: User[] = [];
  loading = true;
  showForm = false;
  form: FormGroup;
  submitting = false;
  showDetails = false;
  selectedPadre: User | null = null;
  hijosData: Nino[] = [];
  loadingHijos = false;

  constructor(private fb: FormBuilder, private api: ApiService, private auth: AuthService) {
    this.form = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      role: ['profesor', Validators.required],
      hijos: this.fb.array([])
    });
  }

  ngOnInit(): void {
    console.log('Componente inicializado');
    console.log('Usuario actual:', this.auth.getUser());
    console.log('Token:', this.auth.getToken());
    this.loadUsuarios();
    this.loadProfesores();
  }

  loadUsuarios(): void {
    console.log('Cargando usuarios...');
    this.loading = true;
    this.api.get<any>('usuarios').subscribe({
      next: data => { 
        console.log('Usuarios cargados desde API:', data);
        console.log('Tipo:', typeof data, 'Es Array:', Array.isArray(data));
        this.usuarios = Array.isArray(data) ? data : [];
        console.log('Total usuarios asignados:', this.usuarios.length);
        this.loading = false; 
      },
      error: (err) => { 
        console.error('Error cargando usuarios:', err);
        this.loading = false;
      }
    });
  }

  loadProfesores(): void {
    this.api.get<User[]>('usuarios').subscribe({
      next: data => this.profesores = data.filter(u => u.role === 'profesor'),
      error: () => {}
    });
  }

  get hijos(): FormArray { return this.form.get('hijos') as FormArray; }

  getHijosNames(user: User): string {
    if (!user.hijos || user.hijos.length === 0) return 'Sin hijos';
    return user.hijos.map(h => h.nombre + ' ' + h.apellido).join(', ');
  }

  addHijo(): void {
    this.hijos.push(this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      pin: ['', [Validators.required, Validators.pattern(/^\d{4}$/)]],
      profesor_id: [null, Validators.required]
    }));
  }

  removeHijo(index: number): void {
    this.hijos.removeAt(index);
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.form.reset();
      this.form.patchValue({ role: 'profesor' });
      while (this.hijos.length) this.hijos.removeAt(0);
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.submitting = true;

    const data = { ...this.form.value };
    if (data.role !== 'padre') delete data.hijos;

    this.api.post('register', data).subscribe({
      next: () => {
        this.toggleForm();
        this.loadUsuarios();
        this.submitting = false;
      },
      error: err => {
        alert('Error: ' + (err.error?.message || 'Error al crear usuario'));
        this.submitting = false;
      }
    });
  }

  suspender(id: number): void {
    this.api.patch(`usuarios/${id}/suspender`, {}).subscribe(() => this.loadUsuarios());
  }

  activar(id: number): void {
    this.api.patch(`usuarios/${id}/activar`, {}).subscribe(() => this.loadUsuarios());
  }

  eliminar(id: number): void {
    if (!confirm('¿Eliminar este usuario?')) return;
    this.api.delete(`usuarios/${id}`).subscribe(() => this.loadUsuarios());
  }

  verDetalles(padre: User): void {
    this.selectedPadre = padre;
    this.loadingHijos = true;
    this.showDetails = true;
    this.api.get<Nino[]>(`usuarios/${padre.id}/hijos`).subscribe({
      next: data => { this.hijosData = data; this.loadingHijos = false; },
      error: () => { this.loadingHijos = false; alert('Error al cargar hijos'); }
    });
  }

  cerrarDetalles(): void {
    this.showDetails = false;
    this.selectedPadre = null;
    this.hijosData = [];
  }
}
