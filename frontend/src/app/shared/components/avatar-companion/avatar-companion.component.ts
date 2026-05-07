import { Component, Input, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { AvatarStateService, AvatarExpression } from '../../../core/services/avatar-state.service';

export interface AvatarConfig {
  id: string;
  nombre: string;
  color: string;
  tipo: 'blob' | 'horn' | 'fluff' | 'ear';
}

export const AVATARES: AvatarConfig[] = [
  { id: 'nina1',  nombre: 'Gloop',  color: '#A855F7', tipo: 'blob' },
  { id: 'nina2',  nombre: 'Zorg',   color: '#22C55E', tipo: 'horn' },
  { id: 'nino1',  nombre: 'Fluff',  color: '#3B82F6', tipo: 'fluff' },
  { id: 'nino2',  nombre: 'Pip',    color: '#EAB308', tipo: 'ear' },
];

const MENSAJES: Record<AvatarExpression, string[]> = {
  feliz:       ['¡Tú puedes! ', '¡Vamos!  ', '¡Hola! '],
  alegre:      ['¡SÍII! ', '¡Eres el mejor! ⭐', '¡Increíble! 🌈'],
  sorprendido: ['¡Wow! ', '¡Qué bien! ', '¡Eso es! '],
  guino:       [' ¡Fácil!', '¡Lo sabías! ', '¡Genial! '],
  pensando:    ['Hmm... ', 'Piénsalo ', 'Ya casi... '],
  triste:      ['¡Inténtalo! ', '¡Casi! ', 'No te rindas '],
  enojado:     ['¡Concéntrate! ', '¡Tú puedes! ', '¡Ánimo! '],
};

@Component({
  selector: 'app-avatar-companion',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './avatar-companion.component.html',
  styleUrls: ['./avatar-companion.component.css']
})
export class AvatarCompanionComponent implements OnInit, OnDestroy {
  @Input() avatarId = 'nina1';
  @Input() displayName?: string;

  expresion: AvatarExpression = 'feliz';
  parpadeando    = false;
  mensajeVisible = false;
  mensajeActual  = '';

  private blinkTimer?: ReturnType<typeof setInterval>;
  private msgTimer?:   ReturnType<typeof setTimeout>;
  private expressionSubscription?: Subscription;
  private avatarState = inject(AvatarStateService);

  get avatar(): AvatarConfig {
    return AVATARES.find(a => a.id === this.avatarId) ?? AVATARES[0];
  }

  ngOnInit(): void {
    this.expressionSubscription = this.avatarState.expression$.subscribe(expr => {
      this.expresion = expr;
      this.mostrarMensaje(expr);
    });
    this.iniciarParpadeo();
  }

  ngOnDestroy(): void {
    this.expressionSubscription?.unsubscribe();
    clearInterval(this.blinkTimer);
    clearTimeout(this.msgTimer);
  }

  private iniciarParpadeo(): void {
    const tick = () => {
      this.parpadeando = true;
      setTimeout(() => (this.parpadeando = false), 160);
      this.blinkTimer = setTimeout(tick, 2800 + Math.random() * 2400);
    };
    this.blinkTimer = setTimeout(tick, 2000);
  }

  private mostrarMensaje(expr: AvatarExpression): void {
    const lista = MENSAJES[expr];
    this.mensajeActual  = lista[Math.floor(Math.random() * lista.length)];
    this.mensajeVisible = true;
    clearTimeout(this.msgTimer);
    this.msgTimer = setTimeout(() => (this.mensajeVisible = false), 2600);
  }

  /** Aclara un color hex en ~25% */
  lighten(hex: string): string {
    return this.adjustColor(hex, 40);
  }

  /** Oscurece un color hex en ~20% */
  darken(hex: string): string {
    return this.adjustColor(hex, -30);
  }

  private adjustColor(hex: string, amount: number): string {
    const h = hex.replace('#', '');
    const num = parseInt(h.length === 3
      ? h.split('').map(c => c + c).join('')
      : h, 16);
    const r = Math.min(255, Math.max(0, (num >> 16) + amount));
    const g = Math.min(255, Math.max(0, ((num >> 8) & 0xff) + amount));
    const b = Math.min(255, Math.max(0, (num & 0xff) + amount));
    return `#${[r, g, b].map(v => v.toString(16).padStart(2, '0')).join('')}`;
  }

  cos(deg: number): number { return Math.cos(deg * Math.PI / 180); }
  sin(deg: number): number { return Math.sin(deg * Math.PI / 180); }
}
