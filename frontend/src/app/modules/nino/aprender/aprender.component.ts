import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AvatarStateService } from '../../../core/services/avatar-state.service';
import { LeccionSumaComponent } from './lecciones/leccion-suma.component';
import { LeccionRestaComponent } from './lecciones/leccion-resta.component';
import { LeccionMultiplicacionComponent } from './lecciones/leccion-multiplicacion.component';
import { LeccionDivisionComponent } from './lecciones/leccion-division.component';
import { LeccionFraccionesComponent } from './lecciones/leccion-fracciones.component';
import { LeccionMcmComponent } from './lecciones/leccion-mcm.component';

interface Tema {
  id: string;
  titulo: string;
  icono: string;
  color: string;
  colorClaro: string;
  descripcion: string;
  emoji: string;
}

@Component({
  selector: 'app-aprender',
  standalone: true,
  imports: [
    CommonModule,
    LeccionSumaComponent,
    LeccionRestaComponent,
    LeccionMultiplicacionComponent,
    LeccionDivisionComponent,
    LeccionFraccionesComponent,
    LeccionMcmComponent
  ],
  templateUrl: './aprender.component.html',
  styleUrls: ['./aprender.component.css']
})
export class AprenderComponent implements OnInit {
  temas: Tema[] = [
    { id: 'suma',           titulo: 'Suma',           icono: '➕', emoji: '🍎', color: '#22c55e', colorClaro: '#dcfce7', descripcion: 'Juntamos cosas para saber cuántas hay en total' },
    { id: 'resta',          titulo: 'Resta',          icono: '➖', emoji: '🍬', color: '#f97316', colorClaro: '#ffedd5', descripcion: 'Quitamos cosas para saber cuántas quedan' },
    { id: 'multiplicacion', titulo: 'Multiplicación', icono: '✖️', emoji: '⭐', color: '#3b82f6', colorClaro: '#dbeafe', descripcion: 'Sumamos grupos iguales de forma rápida' },
    { id: 'division',       titulo: 'División',       icono: '➗', emoji: '🍕', color: '#a855f7', colorClaro: '#f3e8ff', descripcion: 'Repartimos cosas en partes iguales' },
    { id: 'fracciones',     titulo: 'Fracciones',     icono: '🔢', emoji: '🥧', color: '#ec4899', colorClaro: '#fce7f3', descripcion: 'Partes de un entero: ½, ¼, ¾...' },
    { id: 'mcm',            titulo: 'MCM',            icono: '🔁', emoji: '🎯', color: '#06b6d4', colorClaro: '#cffafe', descripcion: 'El número más pequeño que comparten dos números' }
  ];

  temaActivo: string | null = null;

  constructor(private avatarState: AvatarStateService) {}

  ngOnInit(): void {
    this.avatarState.resetExpression();
  }

  seleccionar(id: string): void {
    this.temaActivo = id;
    this.avatarState.setExpression('alegre');
    setTimeout(() => this.avatarState.resetExpression(), 1500);
  }

  volver(): void {
    this.temaActivo = null;
  }
}
