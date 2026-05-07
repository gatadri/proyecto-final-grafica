import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

interface SkinItem {
  id: string;
  nombre: string;
  descripcion: string;
  imagen: string;       // ruta relativa desde /imagenes/avatares/
  avatarKey: string;    // valor que se guarda en nino.avatar
  precio: number;
  rareza: 'comun' | 'raro' | 'legendario';
}

interface StickerItem {
  id: number;
  nombre: string;
  descripcion: string;
  imagen: string;       // ruta relativa desde /imagenes/stickers/
  precio: number;
  rareza: 'comun' | 'raro' | 'legendario';
}

const STORAGE_KEY_SKINS    = 'tienda_skins_compradas';
const STORAGE_KEY_STICKERS = 'tienda_stickers_comprados';

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

  skins: SkinItem[] = [
    { id: 'nina',       nombre: 'Niña',       descripcion: 'Avatar de niña',       imagen: 'nina.png',       avatarKey: 'nina1',  precio: 0,  rareza: 'comun'     },
    { id: 'nino',       nombre: 'Niño',       descripcion: 'Avatar de niño',       imagen: 'nino.png',       avatarKey: 'nino1',  precio: 0,  rareza: 'comun'     },
    { id: 'astronauta', nombre: 'Astronauta', descripcion: 'Traje espacial (niña)', imagen: 'astronauta.png', avatarKey: 'nina2',  precio: 50, rareza: 'raro'      },
    { id: 'astronauto', nombre: 'Astronauto', descripcion: 'Traje espacial (niño)', imagen: 'astronauto.png', avatarKey: 'nino2',  precio: 60, rareza: 'legendario' },
  ];

  stickers: StickerItem[] = [
    { id: 1, nombre: 'Sticker Estrella',   descripcion: 'Sticker brillante de estrella',   imagen: 'sticker1.png', precio: 10, rareza: 'comun'      },
    { id: 2, nombre: 'Sticker Cohete',     descripcion: 'Sticker de cohete espacial',       imagen: 'sticker2.png', precio: 15, rareza: 'comun'      },
    { id: 3, nombre: 'Sticker Arcoíris',   descripcion: 'Sticker de arcoíris mágico',       imagen: 'sticker3.png', precio: 20, rareza: 'raro'       },
    { id: 4, nombre: 'Sticker Unicornio',  descripcion: 'Sticker de unicornio legendario',  imagen: 'sticker4.png', precio: 25, rareza: 'raro'       },
    { id: 5, nombre: 'Sticker Galaxia',    descripcion: 'Sticker de galaxia brillante',     imagen: 'sticker5.png', precio: 30, rareza: 'legendario'  },
  ];

  skinsCompradas:    string[] = [];
  stickersComprados: number[] = [];

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino();
    this.cargarCompras();
    this.loading = false;
  }

  // ── Monedas unificadas (puede venir de nino.monedas o nino.estadisticas.monedas) ──
  get monedas(): number {
    return this.nino?.monedas ?? this.nino?.estadisticas?.monedas ?? 0;
  }

  private setMonedas(valor: number): void {
    if (this.nino.monedas !== undefined) {
      this.nino.monedas = valor;
    } else if (this.nino?.estadisticas) {
      this.nino.estadisticas.monedas = valor;
    }
    localStorage.setItem('nino', JSON.stringify(this.nino));
  }

  // ── Persistencia de compras en localStorage por niño ──
  private keyFor(base: string): string {
    return `${base}_${this.nino?.id ?? 0}`;
  }

  private cargarCompras(): void {
    const s  = localStorage.getItem(this.keyFor(STORAGE_KEY_SKINS));
    const st = localStorage.getItem(this.keyFor(STORAGE_KEY_STICKERS));
    this.skinsCompradas    = s  ? JSON.parse(s)  : ['nina', 'nino']; // las gratuitas siempre disponibles
    this.stickersComprados = st ? JSON.parse(st) : [];
  }

  private guardarCompras(): void {
    localStorage.setItem(this.keyFor(STORAGE_KEY_SKINS),    JSON.stringify(this.skinsCompradas));
    localStorage.setItem(this.keyFor(STORAGE_KEY_STICKERS), JSON.stringify(this.stickersComprados));
  }

  tieneSkin(id: string):    boolean { return this.skinsCompradas.includes(id); }
  tieneSticker(id: number): boolean { return this.stickersComprados.includes(id); }

  // ── Compra de skin ──
  comprarSkin(skin: SkinItem): void {
    if (this.tieneSkin(skin.id)) return;
    if (this.monedas < skin.precio) {
      this.mostrarMensaje('danger', '¡No tienes suficientes monedas! 🪙');
      return;
    }
    this.setMonedas(this.monedas - skin.precio);
    this.skinsCompradas.push(skin.id);
    this.guardarCompras();
    this.mostrarMensaje('success', `¡Compraste la skin ${skin.nombre}! 🎉`);
  }

  // ── Equipar skin (cambia el avatar activo del niño) ──
  equiparSkin(skin: SkinItem): void {
    this.nino.avatar = skin.avatarKey;
    localStorage.setItem('nino', JSON.stringify(this.nino));
    this.mostrarMensaje('success', `¡Avatar cambiado a ${skin.nombre}! ✨`);
  }

  skinEquipada(skin: SkinItem): boolean {
    return this.nino?.avatar === skin.avatarKey;
  }

  // ── Compra de sticker ──
  comprarSticker(sticker: StickerItem): void {
    if (this.tieneSticker(sticker.id)) return;
    if (this.monedas < sticker.precio) {
      this.mostrarMensaje('danger', '¡No tienes suficientes monedas! 🪙');
      return;
    }
    this.setMonedas(this.monedas - sticker.precio);
    this.stickersComprados.push(sticker.id);
    this.guardarCompras();
    this.mostrarMensaje('success', `¡Compraste ${sticker.nombre}! 🎉`);
  }

  // ── Descarga de sticker en PDF listo para imprimir ──
  async descargarSticker(sticker: StickerItem): Promise<void> {
    this.generandoPdf = true;
    try {
      const { jsPDF } = await import('jspdf');

      // Cargar imagen como base64
      const imgBase64 = await this.cargarImagenBase64(`/imagenes/stickers/${sticker.imagen}`);

      // Hoja A4 en mm: 210 x 297
      const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

      const pageW = 210;
      const pageH = 297;

      // Fondo degradado simulado con rectángulos
      doc.setFillColor(245, 243, 255);
      doc.rect(0, 0, pageW, pageH, 'F');

      // Borde decorativo
      doc.setDrawColor(124, 58, 237);
      doc.setLineWidth(3);
      doc.roundedRect(8, 8, pageW - 16, pageH - 16, 6, 6, 'S');

      doc.setDrawColor(196, 181, 253);
      doc.setLineWidth(1);
      doc.roundedRect(12, 12, pageW - 24, pageH - 24, 4, 4, 'S');

      // Título
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(22);
      doc.setTextColor(109, 40, 217);
      doc.text('🌟 Mi Sticker Especial 🌟', pageW / 2, 32, { align: 'center' });

      // Nombre del sticker
      doc.setFontSize(16);
      doc.setTextColor(55, 48, 163);
      doc.text(sticker.nombre, pageW / 2, 44, { align: 'center' });

      // Imagen del sticker centrada — 4 copias en cuadrícula para imprimir
      const stickerSize = 70; // mm
      const gap = 10;
      const startX = (pageW - (stickerSize * 2 + gap)) / 2;
      const startY = 58;

      const posiciones = [
        { x: startX,                  y: startY },
        { x: startX + stickerSize + gap, y: startY },
        { x: startX,                  y: startY + stickerSize + gap },
        { x: startX + stickerSize + gap, y: startY + stickerSize + gap },
      ];

      for (const pos of posiciones) {
        // Sombra del sticker
        doc.setFillColor(200, 190, 240);
        doc.roundedRect(pos.x + 2, pos.y + 2, stickerSize, stickerSize, 8, 8, 'F');
        // Fondo blanco del sticker
        doc.setFillColor(255, 255, 255);
        doc.roundedRect(pos.x, pos.y, stickerSize, stickerSize, 8, 8, 'F');
        // Imagen
        doc.addImage(imgBase64, 'PNG', pos.x + 5, pos.y + 5, stickerSize - 10, stickerSize - 10);
        // Borde punteado (línea de corte)
        doc.setDrawColor(180, 160, 220);
        doc.setLineWidth(0.5);
        doc.setLineDashPattern([2, 2], 0);
        doc.roundedRect(pos.x - 2, pos.y - 2, stickerSize + 4, stickerSize + 4, 9, 9, 'S');
        doc.setLineDashPattern([], 0);
      }

      // Instrucción de corte
      doc.setFontSize(10);
      doc.setTextColor(120, 100, 180);
      doc.text('✂ Recorta por la línea punteada', pageW / 2, startY + stickerSize * 2 + gap + 16, { align: 'center' });

      // Descripción
      doc.setFontSize(11);
      doc.setTextColor(80, 70, 140);
      doc.text(sticker.descripcion, pageW / 2, startY + stickerSize * 2 + gap + 26, { align: 'center' });

      // Pie de página
      doc.setFontSize(9);
      doc.setTextColor(160, 140, 200);
      doc.text(`Generado para: ${this.nino?.nombre ?? 'Estudiante'} • EduApp`, pageW / 2, pageH - 16, { align: 'center' });

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
        canvas.width  = img.naturalWidth;
        canvas.height = img.naturalHeight;
        canvas.getContext('2d')!.drawImage(img, 0, 0);
        resolve(canvas.toDataURL('image/png'));
      };
      img.onerror = reject;
      img.src = url;
    });
  }

  private mostrarMensaje(tipo: string, texto: string): void {
    this.mensaje = { tipo, texto };
    setTimeout(() => (this.mensaje = null), 3500);
  }
}
