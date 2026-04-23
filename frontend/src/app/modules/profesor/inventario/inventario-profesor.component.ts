import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { Skin, Sticker } from '../../../core/models';

@Component({ selector: 'app-inventario-profesor', standalone: true, imports: [CommonModule, ReactiveFormsModule], templateUrl: './inventario-profesor.component.html' })
export class InventarioProfesorComponent implements OnInit {
  skins: Skin[] = [];
  stickers: Sticker[] = [];
  loading = true;
  showForm = false;
  editItem: any = null;
  form: FormGroup;
  saving = false;
  error = '';

  constructor(private api: ApiService, private fb: FormBuilder) {
    this.form = this.fb.group({
      tipo:         ['skin', Validators.required],
      nombre:       ['', Validators.required],
      descripcion:  [''],
      imagen:       ['', Validators.required],
      precio:       [0, [Validators.required, Validators.min(0)]],
      rareza:       ['comun', Validators.required],
      categoria:    [''],
      pdf_template: ['']
    });
  }

  ngOnInit(): void { this.load(); }

  load(): void {
    this.api.get<{ skins: Skin[], stickers: Sticker[] }>('inventario').subscribe({
      next: data => { this.skins = data.skins; this.stickers = data.stickers; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  openCreate(): void {
    this.editItem = null;
    this.form.reset({ tipo: 'skin', precio: 0, rareza: 'comun' });
    this.showForm = true;
  }

  openEdit(tipo: string, item: any): void {
    this.editItem = { tipo, id: item.id };
    this.form.patchValue({ tipo, ...item });
    this.showForm = true;
  }

  save(): void {
    if (this.form.invalid) return;
    this.saving = true;
    this.error = '';
    const data = this.form.value;

    const req = this.editItem
      ? this.api.put(`inventario/${this.editItem.tipo}/${this.editItem.id}`, data)
      : this.api.post('inventario', data);

    req.subscribe({
      next: () => { this.showForm = false; this.saving = false; this.load(); },
      error: err => { this.error = err.error?.message ?? 'Error al guardar'; this.saving = false; }
    });
  }

  get isSticker(): boolean { return this.form.get('tipo')?.value === 'sticker'; }
}
