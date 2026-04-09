import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Nino, Skin, Sticker } from '../../../core/models';

@Component({ selector: 'app-nino-tienda', standalone: true, imports: [CommonModule], templateUrl: './nino-tienda.component.html' })
export class NinoTiendaComponent implements OnInit {
  nino!: Nino;
  skins: Skin[] = [];
  stickers: Sticker[] = [];
  skinsCompradas: number[] = [];
  stickersComprados: number[] = [];
  loading = true;
  mensaje: { tipo: string; texto: string } | null = null;

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino()!;
    // Datos hardcodeados para tienda
    this.skins = [
      { id: 1, nombre: 'Ninja', descripcion: 'Skin de ninja', imagen: 'ninja.png', precio: 50, rareza: 'raro', categoria: 'avatar', activo: true },
      { id: 2, nombre: 'Pirata', descripcion: 'Skin de pirata', imagen: 'pirata.png', precio: 60, rareza: 'raro', categoria: 'avatar', activo: true },
      { id: 3, nombre: 'Superhéroe', descripcion: 'Skin de superhéroe', imagen: 'superheroe.png', precio: 70, rareza: 'legendario', categoria: 'avatar', activo: true }
    ];
    this.stickers = [
      { id: 1, nombre: 'Estrella', descripcion: 'Sticker de estrella', imagen: 'estrella.png', precio: 10, rareza: 'comun', categoria: 'decoracion', pdf_template: null, activo: true },
      { id: 2, nombre: 'Corazón', descripcion: 'Sticker de corazón', imagen: 'corazon.png', precio: 15, rareza: 'comun', categoria: 'decoracion', pdf_template: null, activo: true },
      { id: 3, nombre: 'Trofeo', descripcion: 'Sticker de trofeo', imagen: 'trofeo.png', precio: 20, rareza: 'raro', categoria: 'decoracion', pdf_template: null, activo: true }
    ];
    // Simular compras previas
    this.skinsCompradas = [1]; // Ejemplo
    this.stickersComprados = [2];
    this.loading = false;
  }

  tieneSkin(id: number): boolean { return this.skinsCompradas.includes(id); }
  tieneSticker(id: number): boolean { return this.stickersComprados.includes(id); }

  comprarSkin(skin: Skin): void {
    if (this.nino.monedas < skin.precio) {
      this.mostrarMensaje('danger', 'No tienes suficientes monedas');
      return;
    }
    this.skinsCompradas.push(skin.id);
    this.nino.monedas -= skin.precio;
    this.mostrarMensaje('success', `¡Compraste ${skin.nombre}!`);
    localStorage.setItem('nino', JSON.stringify(this.nino));
  }

  comprarSticker(sticker: Sticker): void {
    if (this.nino.monedas < sticker.precio) {
      this.mostrarMensaje('danger', 'No tienes suficientes monedas');
      return;
    }
    this.stickersComprados.push(sticker.id);
    this.nino.monedas -= sticker.precio;
    this.mostrarMensaje('success', `¡Compraste ${sticker.nombre}!`);
    localStorage.setItem('nino', JSON.stringify(this.nino));
  }

  descargarSticker(id: number): void {
    // Simular descarga
    this.mostrarMensaje('success', 'Sticker descargado');
  }

  private mostrarMensaje(tipo: string, texto: string): void {
    this.mensaje = { tipo, texto };
    setTimeout(() => this.mensaje = null, 3000);
  }
}
