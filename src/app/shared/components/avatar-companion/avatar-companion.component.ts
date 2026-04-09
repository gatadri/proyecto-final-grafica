import { Component, Input, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { AvatarStateService, AvatarExpression } from '../../../core/services/avatar-state.service';

export interface AvatarConfig {
  id: string;
  nombre: string;
  skin: string;
  hairColor: string;
  hairStyle: 'short' | 'long' | 'curly' | 'spiky';
  gender: 'nino' | 'nina';
  shirtColor: string;
}

export const AVATARES: AvatarConfig[] = [
  { id: 'nina1',  nombre: 'Luna',  skin: '#FDBCB4', hairColor: '#8B4513', hairStyle: 'long',  gender: 'nina', shirtColor: '#FF6B9D' },
  { id: 'nina2',  nombre: 'Sofia', skin: '#C68642', hairColor: '#1A0A00', hairStyle: 'curly', gender: 'nina', shirtColor: '#A855F7' },
  { id: 'nino1',  nombre: 'Mateo', skin: '#FDBCB4', hairColor: '#2C1810', hairStyle: 'spiky', gender: 'nino', shirtColor: '#3B82F6' },
  { id: 'nino2',  nombre: 'Diego', skin: '#C68642', hairColor: '#0A0A0A', hairStyle: 'short', gender: 'nino', shirtColor: '#10B981' },
];

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
  parpadeando = false;
  private blinkTimer: any;
  private expressionSubscription?: Subscription;
  private avatarState = inject(AvatarStateService);

  get avatar(): AvatarConfig {
    return AVATARES.find(a => a.id === this.avatarId) ?? AVATARES[0];
  }

  ngOnInit(): void {
    this.expressionSubscription = this.avatarState.expression$.subscribe(expr => {
      this.expresion = expr;
    });
    this.iniciarParpadeo();
  }

  ngOnDestroy(): void {
    this.expressionSubscription?.unsubscribe();
    clearInterval(this.blinkTimer);
  }

  private iniciarParpadeo(): void {
    this.blinkTimer = setInterval(() => {
      this.parpadeando = true;
      setTimeout(() => (this.parpadeando = false), 150);
    }, 2800 + Math.random() * 2200);
  }
}
