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
    this.api.get<any>(`nino/${this.nino.pin}/tienda`).subscribe({
      next: data => {
        this.skins    = data.skins_disponibles ?? [];
        this.stickers = data.stickers_disponibles ?? [];
        this.skinsCompradas    = data.skins_nino?.map((s: any) => s.id) ?? [];
        this.stickersComprados = data.stickers_nino?.map((s: any) => s.id) ?? [];
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  tieneSkin(id: number): boolean { return this.skinsCompradas.includes(id); }
  tieneSticker(id: number): boolean { return this.stickersComprados.includes(id); }

  comprarSkin(skin: Skin): void {
    this.api.post<any>(`nino/${this.nino.pin}/comprar-skin`, { skin_id: skin.id }).subscribe({
      next: res => {
        if (res.success) {
          this.skinsCompradas.push(skin.id);
          this.nino.monedas = res.monedas_restantes;
          this.mostrarMensaje('success', res.message);
          localStorage.setItem('nino', JSON.stringify(this.nino));
        } else {
          this.mostrarMensaje('danger', res.message);
        }
      }
    });
  }

  comprarSticker(sticker: Sticker): void {
    this.api.post<any>(`nino/${this.nino.pin}/comprar-sticker`, { sticker_id: sticker.id }).subscribe({
      next: res => {
        if (res.success) {
          this.stickersComprados.push(sticker.id);
          this.nino.monedas = res.monedas_restantes;
          this.mostrarMensaje('success', res.message);
          localStorage.setItem('nino', JSON.stringify(this.nino));
        } else {
          this.mostrarMensaje('danger', res.message);
        }
      }
    });
  }

  descargarSticker(id: number): void {
    window.open(`http://localhost:8000/nino/${this.nino.pin}/descargar-sticker/${id}`, '_blank');
  }

  private mostrarMensaje(tipo: string, texto: string): void {
    this.mensaje = { tipo, texto };
    setTimeout(() => this.mensaje = null, 3000);
  }
}
