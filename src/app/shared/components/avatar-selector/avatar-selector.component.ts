import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AvatarCompanionComponent, AVATARES, AvatarConfig } from '../avatar-companion/avatar-companion.component';

@Component({
  selector: 'app-avatar-selector',
  standalone: true,
  imports: [CommonModule, AvatarCompanionComponent],
  templateUrl: './avatar-selector.component.html',
  styleUrls: ['./avatar-selector.component.css']
})
export class AvatarSelectorComponent implements OnInit {
  avatares = AVATARES;
  avatarActual = 'nina1';
  nombreNino = '';
  mostrarSelector = false;

  ngOnInit(): void {
    const nino = JSON.parse(localStorage.getItem('nino') ?? '{}');
    this.avatarActual = nino.avatar ?? 'nina1';
    this.nombreNino = nino.nombre ?? '';
  }

  seleccionar(id: string): void {
    this.avatarActual = id;
    const nino = JSON.parse(localStorage.getItem('nino') ?? '{}');
    nino.avatar = id;
    localStorage.setItem('nino', JSON.stringify(nino));
    this.mostrarSelector = false;
  }
}
