import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';
import jsPDF from 'jspdf';

interface Skin {
  id: number;
  nombre: string;
  descripcion: string;
  imagen: string;
  avatar_key: string;
  precio: number;
  rareza: 'comun' | 'raro' | 'legendario';
  comprada: boolean;
  equipada: boolean;
}

interface Sticker {
  id: number;
  nombre: string;
  descripcion: string;
  imagen: string;
  precio: number;
  rareza: 'comun' | 'raro' | 'legendario';
  comprado: boolean;
}

@Component({
  selector: 'app-nino-tienda',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './nino-tienda.component.html'
})
export class NinoTiendaComponent implements OnInit {
  nino: any;
  loading = true;
  mensaje: { tipo: string; texto: string } | null = null;
  generandoPdf = false;

  skins: Skin[] = [];
  stickers: Sticker[] = [];

  constructor(
    private auth: AuthService,
    private api: ApiService
  ) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino();
    this.cargarTienda();
  }

  cargarTienda(): void {
    this.loading = true;
    
    // Cargar skins
    this.api.get<Skin[]>(`tienda/skins?nino_id=${this.nino.id}`).subscribe({
      next: skins => {
        this.skins = skins;
        this.loading = false;
      },
      error: () => this.loading = false
    });

    // Cargar stickers
    this.api.get<Sticker[]>(`tienda/stickers?nino_id=${this.nino.id}`).subscribe({
      next: stickers => {
        this.stickers = stickers;
      },
      error: () => {}
    });
  }

  get monedas(): number {
    return this.nino?.monedas ?? this.nino?.estadisticas?.monedas ?? 0;
  }

  private actualizarMonedas(valor: number): void {
    if (this.nino.monedas !== undefined) {
      this.nino.monedas = valor;
    } else if (this.nino?.estadisticas) {
      this.nino.estadisticas.monedas = valor;
    }
    this.auth.saveNino(this.nino);
  }

  comprarSkin(skin: Skin): void {
    if (skin.comprada) return;
    if (this.monedas < skin.precio) {
      this.mostrarMensaje('danger', '¡No tienes suficientes monedas! 🪙');
      return;
    }

    this.api.post('tienda/skins/comprar', {
      nino_id: this.nino.id,
      skin_id: skin.id
    }).subscribe({
      next: (res: any) => {
        this.actualizarMonedas(res.monedas);
        skin.comprada = true;
        this.mostrarMensaje('success', `¡Compraste la skin ${skin.nombre}! 🎉`);
      },
      error: err => {
        this.mostrarMensaje('danger', err.error?.error || 'Error al comprar skin');
      }
    });
  }

  tieneSkin(skinId: number): boolean {
    const skin = this.skins.find(s => s.id === skinId);
    return skin ? skin.comprada : false;
  }

  skinEquipada(skin: Skin): boolean {
    return skin.equipada;
  }

  equiparSkin(skin: Skin): void {
    if (!skin.comprada) return;

    this.api.post('tienda/skins/equipar', {
      nino_id: this.nino.id,
      skin_id: skin.id
    }).subscribe({
      next: (res: any) => {
        this.nino.avatar = res.avatar;
        this.auth.saveNino(this.nino);
        
        // Actualizar estado de equipada
        this.skins.forEach(s => s.equipada = false);
        skin.equipada = true;
        
        this.mostrarMensaje('success', `¡Avatar cambiado a ${skin.nombre}! ✨`);
      },
      error: err => {
        this.mostrarMensaje('danger', err.error?.error || 'Error al equipar skin');
      }
    });
  }

  comprarSticker(sticker: Sticker): void {
    if (sticker.comprado) return;
    if (this.monedas < sticker.precio) {
      this.mostrarMensaje('danger', '¡No tienes suficientes monedas! 🪙');
      return;
    }

    this.api.post('tienda/stickers/comprar', {
      nino_id: this.nino.id,
      sticker_id: sticker.id
    }).subscribe({
      next: (res: any) => {
        this.actualizarMonedas(res.monedas);
        sticker.comprado = true;
        this.mostrarMensaje('success', `¡Compraste ${sticker.nombre}! 🎉`);
      },
      error: err => {
        this.mostrarMensaje('danger', err.error?.error || 'Error al comprar sticker');
      }
    });
  }

  tieneSticker(stickerId: number): boolean {
    const sticker = this.stickers.find(s => s.id === stickerId);
    return sticker ? sticker.comprado : false;
  }

  async descargarSticker(sticker: Sticker): Promise<void> {
    this.generandoPdf = true;
    try {
      const imgBase64 = await this.cargarImagenBase64(`/imagenes/stickers/${sticker.imagen}`);

      const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      const pageW = 210;
      const pageH = 297;

      doc.setFillColor(245, 243, 255);
      doc.rect(0, 0, pageW, pageH, 'F');

      doc.setDrawColor(124, 58, 237);
      doc.setLineWidth(3);
      doc.roundedRect(8, 8, pageW - 16, pageH - 16, 6, 6, 'S');

      doc.setDrawColor(196, 181, 253);
      doc.setLineWidth(1);
      doc.roundedRect(12, 12, pageW - 24, pageH - 24, 4, 4, 'S');

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(22);
      doc.setTextColor(109, 40, 217);
      doc.text('Mi Sticker Especial', pageW / 2, 32, { align: 'center' });

      doc.setFontSize(16);
      doc.setTextColor(55, 48, 163);
      doc.text(sticker.nombre, pageW / 2, 44, { align: 'center' });

      const stickerSize = 70;
      const gap = 10;
      const startX = (pageW - (stickerSize * 2 + gap)) / 2;
      const startY = 58;

      const posiciones = [
        { x: startX, y: startY },
        { x: startX + stickerSize + gap, y: startY },
        { x: startX, y: startY + stickerSize + gap },
        { x: startX + stickerSize + gap, y: startY + stickerSize + gap },
      ];

      for (const pos of posiciones) {
        doc.setFillColor(200, 190, 240);
        doc.roundedRect(pos.x + 2, pos.y + 2, stickerSize, stickerSize, 8, 8, 'F');
        doc.setFillColor(255, 255, 255);
        doc.roundedRect(pos.x, pos.y, stickerSize, stickerSize, 8, 8, 'F');
        doc.addImage(imgBase64, 'PNG', pos.x + 5, pos.y + 5, stickerSize - 10, stickerSize - 10);
        doc.setDrawColor(180, 160, 220);
        doc.setLineWidth(0.5);
        doc.setLineDashPattern([2, 2], 0);
        doc.roundedRect(pos.x - 2, pos.y - 2, stickerSize + 4, stickerSize + 4, 9, 9, 'S');
        doc.setLineDashPattern([], 0);
      }

      doc.setFontSize(10);
      doc.setTextColor(120, 100, 180);
      doc.text('Recorta por la linea punteada', pageW / 2, startY + stickerSize * 2 + gap + 16, { align: 'center' });

      doc.setFontSize(11);
      doc.setTextColor(80, 70, 140);
      doc.text(sticker.descripcion, pageW / 2, startY + stickerSize * 2 + gap + 26, { align: 'center' });

      doc.setFontSize(9);
      doc.setTextColor(160, 140, 200);
      doc.text(`Generado para: ${this.nino?.nombre ?? 'Estudiante'} - EduApp`, pageW / 2, pageH - 16, { align: 'center' });

      doc.save(`sticker-${sticker.id}-${sticker.nombre.toLowerCase().replace(/\s+/g, '-')}.pdf`);
      this.mostrarMensaje('success', '¡PDF descargado listo para imprimir! 🖨️');
    } catch (e) {
      console.error('Error generando PDF', e);
      this.mostrarMensaje('danger', 'Error al generar el PDF');
    } finally {
      this.generandoPdf = false;
    }
  }

  private cargarImagenBase64(url: string): Promise<string> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(img, 0, 0);
          resolve(canvas.toDataURL('image/png'));
        } else {
          reject(new Error('No se pudo obtener el contexto del canvas'));
        }
      };
      img.onerror = (error) => {
        console.error('Error cargando imagen:', url, error);
        reject(new Error(`No se pudo cargar la imagen: ${url}`));
      };
      // Intentar cargar la imagen
      img.src = url;
    });
  }

  private mostrarMensaje(tipo: string, texto: string): void {
    this.mensaje = { tipo, texto };
    setTimeout(() => (this.mensaje = null), 3500);
  }
}
