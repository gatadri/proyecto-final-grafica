import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Skin, Sticker } from '../../../core/models';

@Component({ selector: 'app-inventario-director', standalone: true, imports: [CommonModule], templateUrl: './inventario-director.component.html' })
export class InventarioDirectorComponent implements OnInit {
  skins: Skin[] = [];
  stickers: Sticker[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void { this.load(); }

  load(): void {
    this.api.get<{ skins: Skin[], stickers: Sticker[] }>('inventario').subscribe({
      next: data => { this.skins = data.skins; this.stickers = data.stickers; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }

  toggle(tipo: string, id: number): void {
    this.api.patch(`inventario/${tipo}/${id}/toggle`).subscribe(() => this.load());
  }
}
