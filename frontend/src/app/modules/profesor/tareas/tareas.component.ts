import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { MockDataService } from '../../../core/services/mock-data.service';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';

interface Nino { id: number; nombre: string; apellido: string; grado: number; nivel: number; }

interface Nino { id: number; nombre: string; apellido: string; grado: number; nivel: number; }

@Component({
  selector: 'app-tareas',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './tareas.component.html'
})
export class TareasComponent implements OnInit {
  tareas: any[]       = [];
  estudiantes: Nino[] = [];
  loading   = true;
  showForm  = false;
  editando: any = null;
  saving    = false;
  error     = '';
  form: FormGroup;

  constructor(private mock: MockDataService, private auth: AuthService, private fb: FormBuilder, private api: ApiService) {
    this.form = this.fb.group({
      titulo:         ['', Validators.required],
      descripcion:    [''],
      tipo_ejercicio: ['multiple', Validators.required],
      ejercicios:     this.fb.array([]),
      nino_ids:       this.fb.array([])
    });
  }

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    this.api.get<any[]>('tareas').subscribe({
      next: tareas => this.tareas = tareas,
      error: err => { this.error = 'Error cargando tareas'; console.error(err); }
    });
    this.api.get<Nino[]>('profesor/estudiantes').subscribe({
      next: estudiantes => this.estudiantes = estudiantes,
      error: err => { this.error = 'Error cargando estudiantes'; console.error(err); }
    });
    this.loading = false;
  }

  get ejercicios(): FormArray { return this.form.get('ejercicios') as FormArray; }
  get nino_ids(): FormArray   { return this.form.get('nino_ids')   as FormArray; }

  agregarEjercicio(): void {
    this.ejercicios.push(this.fb.group({
      pregunta:           ['', Validators.required],
      opciones:           [''],
      respuesta_correcta: ['', Validators.required],
      explicacion:        [''],
    }));
  }

  eliminarEjercicio(i: number): void { this.ejercicios.removeAt(i); }

  toggleNino(id: number, checked: boolean): void {
    if (checked) { this.nino_ids.push(this.fb.control(id)); }
    else {
      const idx = this.nino_ids.controls.findIndex(c => c.value === id);
      if (idx !== -1) this.nino_ids.removeAt(idx);
    }
  }

  isNinoSelected(id: number): boolean { return this.nino_ids.controls.some(c => c.value === id); }

  openCreate(): void {
    this.editando = null;
    this.form.reset({ tipo_ejercicio: 'multiple' });
    this.ejercicios.clear();
    this.nino_ids.clear();
    this.agregarEjercicio();
    this.showForm = true;
    this.error = '';
  }

  openEdit(tarea: any): void {
    this.editando = tarea;
    this.ejercicios.clear();
    this.nino_ids.clear();
    this.form.patchValue({ titulo: tarea.titulo, descripcion: tarea.descripcion, tipo_ejercicio: tarea.tipo_ejercicio });
    tarea.ejercicios?.forEach((e: any) => {
      this.ejercicios.push(this.fb.group({
        pregunta: [e.pregunta], opciones: [e.opciones?.join(', ')],
        respuesta_correcta: [e.respuesta_correcta], explicacion: [e.explicacion]
      }));
    });
    tarea.nino_ids?.forEach((id: number) => this.nino_ids.push(this.fb.control(id)));
    this.showForm = true;
    this.error = '';
  }

  save(): void {
    if (this.form.invalid) return;
    this.saving = true;
    const data = {
      titulo:         this.form.value.titulo,
      descripcion:    this.form.value.descripcion,
      tipo_ejercicio: this.form.value.tipo_ejercicio,
      nino_ids:       this.nino_ids.value,
      ejercicios:     this.ejercicios.value.map((e: any) => ({
        ...e,
        opciones: e.opciones ? e.opciones.split(',').map((o: string) => o.trim()).filter((o: string) => o) : []
      }))
    };
    const obs = this.editando
      ? this.api.put(`tareas/${this.editando.id}`, data)
      : this.api.post('tareas', data);
    obs.subscribe({
      next: () => {
        this.showForm = false;
        this.saving = false;
        this.load();
      },
      error: err => {
        this.error = 'Error guardando tarea';
        this.saving = false;
        console.error(err);
      }
    });
  }

  eliminar(id: number): void {
    if (!confirm('¿Eliminar esta tarea?')) return;
    this.api.delete(`tareas/${id}`).subscribe({
      next: () => this.load(),
      error: err => { this.error = 'Error eliminando tarea'; console.error(err); }
    });
  }

  getNombresNinos(nino_ids: number[]): string {
    return (nino_ids || []).map(id => {
      const n = this.estudiantes.find(e => e.id === id);
      return n ? n.nombre : '';
    }).filter(Boolean).join(', ');
  }
}
