import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MockDataService } from '../../../core/services/mock-data.service';

@Component({ selector: 'app-inventario-director', standalone: true, imports: [CommonModule], templateUrl: './inventario-director.component.html' })
export class InventarioDirectorComponent implements OnInit {
  skins: any[]    = [];
  stickers: any[] = [];
  loading = true;
  tab: 'skins' | 'stickers' = 'skins';

  constructor(private mock: MockDataService) {}
  ngOnInit(): void { this.load(); }
  load(): void {
    const inv = this.mock.getInventario();
    this.skins    = inv.skins;
    this.stickers = inv.stickers;
    this.loading  = false;
  }
  toggle(tipo: string, id: number): void {
    this.mock.toggleInventario(tipo, id);
    this.load();
  }
}
