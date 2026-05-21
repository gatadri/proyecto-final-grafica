import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';

@Component({ selector: 'app-inventario-profesor', standalone: true, imports: [CommonModule, ReactiveFormsModule], templateUrl: './inventario-profesor.component.html' })
export class InventarioProfesorComponent implements OnInit {
  skins: any[] = [];
  stickers: any[] = [];
  loading = true;
  showForm = false;
  editItem: any = null;
  form: FormGroup;
  saving = false;
  error = '';
  selectedFile: File | null = null;
  imagePreview: string | null = null;

  constructor(private api: ApiService, private fb: FormBuilder) {
    this.form = this.fb.group({
      tipo:         ['skin', Validators.required],
      nombre:       ['', Validators.required],
      descripcion:  [''],
      precio:       [0, [Validators.required, Validators.min(0)]],
      rareza:       ['comun', Validators.required]
    });
  }

  ngOnInit(): void { this.load(); }

  load(): void {
    this.api.get<{ skins: any[], stickers: any[] }>('inventario/tienda').subscribe({
      next: data => { this.skins = data.skins; this.stickers = data.stickers; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  openCreate(): void {
    this.editItem = null;
    this.selectedFile = null;
    this.imagePreview = null;
    this.form.reset({ tipo: 'skin', precio: 0, rareza: 'comun' });
    this.showForm = true;
  }

  openEdit(tipo: string, item: any): void {
    this.editItem = { tipo, id: item.id };
    this.form.patchValue({ tipo, ...item });
    this.showForm = true;
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      // Validar que sea una imagen
      if (!file.type.startsWith('image/')) {
        this.error = 'Por favor selecciona un archivo de imagen (JPG, PNG, etc.)';
        return;
      }
      
      this.selectedFile = file;
      this.error = '';
      
      // Crear preview
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  save(): void {
    if (this.form.invalid) {
      this.error = 'Por favor completa todos los campos requeridos';
      return;
    }
    
    if (!this.editItem && !this.selectedFile) {
      this.error = 'Por favor selecciona una imagen';
      return;
    }
    
    this.saving = true;
    this.error = '';
    
    const formData = new FormData();
    formData.append('tipo', this.form.value.tipo);
    formData.append('nombre', this.form.value.nombre);
    formData.append('descripcion', this.form.value.descripcion || '');
    formData.append('precio', this.form.value.precio.toString());
    formData.append('rareza', this.form.value.rareza);
    
    if (this.selectedFile) {
      formData.append('imagen', this.selectedFile, this.selectedFile.name);
    }
    
    // Generar avatar_key automáticamente para skins
    if (this.form.value.tipo === 'skin') {
      const avatarKey = this.form.value.nombre.toLowerCase().replace(/\s+/g, '_');
      formData.append('avatar_key', avatarKey);
    }

    const req = this.editItem
      ? this.api.patch(`inventario/${this.editItem.tipo}/${this.editItem.id}`, formData)
      : this.api.post('inventario/tienda', formData);

    req.subscribe({
      next: () => { 
        this.showForm = false; 
        this.saving = false; 
        this.selectedFile = null;
        this.imagePreview = null;
        this.load(); 
      },
      error: err => { 
        this.error = err.error?.error ?? err.error?.message ?? 'Error al guardar'; 
        this.saving = false; 
      }
    });
  }

  get isSticker(): boolean { return this.form.get('tipo')?.value === 'sticker'; }
}
