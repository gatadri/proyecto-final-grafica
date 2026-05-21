import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';
import { AudioService, AudioType } from '../../../core/services/audio.service';
import { Tarea } from '../../../core/models';
import { Subject, interval, takeUntil } from 'rxjs';

@Component({ selector: 'app-nino-dashboard', standalone: true, imports: [CommonModule, RouterModule], templateUrl: './nino-dashboard.component.html' })
export class NinoDashboardComponent implements OnInit, OnDestroy {
  nino: any = null;

  getAvatarUrl(avatar: string): string {
    if (!avatar) return '/imagenes/avatares/nino.png';
    if (avatar.startsWith('nina')) return '/imagenes/avatares/nina.png';
    return '/imagenes/avatares/nino.png';
  }

  get monedas(): number {
    return this.nino?.monedas ?? this.nino?.estadisticas?.monedas ?? 0;
  }
  tareas: Tarea[] = [];
  tareasCompletadasCount = 0;
  totalTareasAsignadas = 0;
  logrosRecientes: any[] = [];
  loading = true;
  private destroy$ = new Subject<void>();

  constructor(
    private auth: AuthService, 
    private api: ApiService,
    public audioService: AudioService
  ) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino();
    if (this.nino) {
      this.cargarTareas();
      interval(2000).pipe(takeUntil(this.destroy$)).subscribe(() => this.cargarTareas());
      
      // Reproducir audio general por defecto al entrar
      this.iniciarAudioGeneral();
    }
  }

  private iniciarAudioGeneral(): void {
    // Intentar reproducir inmediatamente
    setTimeout(() => {
      if (!this.audioService.getCurrentAudioType() || 
          this.audioService.getCurrentAudioType() === AudioType.GENERAL) {
        this.audioService.play(AudioType.GENERAL);
      }
    }, 100);

    // Si falla por políticas del navegador, intentar en el primer clic
    const intentarReproducir = () => {
      if (!this.audioService.isPlaying(AudioType.GENERAL) && 
          !this.audioService.getCurrentAudioType()) {
        this.audioService.play(AudioType.GENERAL);
      }
      // Remover el listener después del primer intento
      document.removeEventListener('click', intentarReproducir);
    };
    
    document.addEventListener('click', intentarReproducir, { once: true });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    // NO pausar el audio general al salir del dashboard
    // Se mantendrá sonando en otras secciones del niño
    // Solo se pausa si el usuario hace clic en el botón o hace logout
  }

  private cargarTareas(): void {
    this.api.get<Tarea[]>(`nino/tareas?nino_id=${this.nino.id}`).subscribe({
      next: tareas => {
        this.totalTareasAsignadas = tareas.length;
        this.api.get<any[]>(`nino/progreso?nino_id=${this.nino.id}`).subscribe({
          next: progreso => {
            this.tareasCompletadasCount = progreso.filter(p => p.completada).length;
            const completadas = progreso.filter(p => p.completada).map(p => p.tarea_id);
            this.tareas = tareas.filter(t => !completadas.includes(t.id));
            this.loading = false;
          },
          error: err => {
            console.error('Error cargando progreso', err);
            this.tareas = tareas;
            this.loading = false;
          }
        });
        this.cargarLogros();
      },
      error: err => {
        console.error('Error cargando tareas', err);
        this.loading = false;
      }
    });
  }

  private cargarLogros(): void {
    this.api.get<any[]>(`nino/logros?nino_id=${this.nino.id}`).subscribe({
      next: logros => {
        this.logrosRecientes = logros.slice(0, 3);
      },
      error: err => console.error('Error cargando logros', err)
    });
  }

  get totalTareas(): number {
    return this.totalTareasAsignadas;
  }

  logout(): void { 
    this.audioService.stopAll();
    this.auth.ninoLogout(); 
  }

  toggleMusic(): void {
    console.log('Toggle music clicked');
    console.log('Current state:', this.isMusicPlaying);
    this.audioService.toggle(AudioType.GENERAL);
    console.log('New state:', this.isMusicPlaying);
  }

  get isMusicPlaying(): boolean {
    return this.audioService.isPlaying(AudioType.GENERAL);
  }
}
